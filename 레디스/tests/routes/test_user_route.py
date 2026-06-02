import asyncio
from random import Random

import pytest
from fastapi import HTTPException
from redis.exceptions import ConnectionError as RedisConnectionError

from app.repositories.user_profile_repository import UserProfileRepository
from app.representations.user_request import UserProfileUpdateRequest
from app.representations.user_response import UserProfileResponse
from app.routes.user_route import get_user_profile, update_user_profile
from app.services.user_profile_cache import UserProfileCache
from app.services.user_profile_service import UserProfileService
from app.storages.redis import redis_storage


def _service() -> UserProfileService:
    return UserProfileService(
        repository=UserProfileRepository(),
        cache=UserProfileCache(),
    )


class _UnavailableUserProfileCache(UserProfileCache):
    async def get(self, user_id: int) -> UserProfileResponse | None:
        raise RedisConnectionError("redis unavailable")

    async def set(self, user_id: int, profile: UserProfileResponse) -> None:
        raise RedisConnectionError("redis unavailable")

    async def delete(self, user_id: int) -> None:
        raise RedisConnectionError("redis unavailable")

    async def acquire_refresh_lock(self, user_id: int, token: str) -> bool:
        raise RedisConnectionError("redis unavailable")

    async def release_refresh_lock(self, user_id: int, token: str) -> None:
        raise RedisConnectionError("redis unavailable")


class _CountingUserProfileRepository(UserProfileRepository):
    def __init__(self, profile: UserProfileResponse) -> None:
        self.profile = profile
        self.find_count = 0

    def find_by_id(self, user_id: int) -> UserProfileResponse | None:
        self.find_count += 1
        return self.profile


class _CoordinatedInitialMissUserProfileCache(UserProfileCache):
    def __init__(self, initial_miss_count: int) -> None:
        super().__init__()
        self.initial_miss_count = initial_miss_count
        self.initial_get_count = 0
        self.initial_misses_seen = asyncio.Event()

    async def get(self, user_id: int) -> UserProfileResponse | None:
        if self.initial_get_count < self.initial_miss_count:
            self.initial_get_count += 1
            if self.initial_get_count == self.initial_miss_count:
                self.initial_misses_seen.set()

            await self.initial_misses_seen.wait()
            return None

        return await super().get(user_id)


class _BlockingCacheSetUserProfileCache(UserProfileCache):
    def __init__(self, blocked_profile_name: str) -> None:
        super().__init__()
        self.blocked_profile_name = blocked_profile_name
        self.has_blocked = False
        # 조회 요청이 오래된 profile을 Redis에 쓰기 직전에 도착했음을 알린다.
        self.set_started = asyncio.Event()
        # 테스트가 허용할 때까지 오래된 profile의 cache set을 멈춰 둔다.
        self.allow_set = asyncio.Event()

    async def set(self, user_id: int, profile: UserProfileResponse) -> None:
        if profile.name == self.blocked_profile_name and not self.has_blocked:
            self.has_blocked = True
            self.set_started.set()
            await self.allow_set.wait()

        await super().set(user_id, profile)


@pytest.mark.asyncio
async def test_get_user_profile_cache_miss_sets_redis() -> None:
    repository = UserProfileRepository()
    user_id = 1
    repository.save(
        user_id,
        UserProfileResponse(name="mina", age=29),
    )

    profile = await get_user_profile(user_id, service=_service())

    conn = redis_storage.get_connection()
    cached_profile = await conn.get(f"cache:user:{user_id}:profile")
    assert profile.model_dump() == {"name": "mina", "age": 29}
    assert cached_profile is not None


@pytest.mark.asyncio
async def test_user_profile_cache_sets_ttl_within_jitter_range() -> None:
    user_id = 1
    # A seeded Random makes the jitter sequence reproducible for the test.
    cache = UserProfileCache(random_source=Random(1))
    await cache.set(
        user_id,
        UserProfileResponse(name="cached-mina", age=30),
    )

    conn = redis_storage.get_connection()
    ttl_seconds = await conn.ttl(cache.key(user_id))
    # Redis TTL returns remaining seconds, so assert the policy range.
    assert 60 <= ttl_seconds <= 70


@pytest.mark.asyncio
async def test_user_profile_cache_jitter_spreads_ttl_values() -> None:
    cache = UserProfileCache(random_source=Random(1))
    conn = redis_storage.get_connection()

    for user_id in range(1, 4):
        await cache.set(
            user_id,
            UserProfileResponse(name=f"cached-mina-{user_id}", age=30),
        )

    ttl_values = [await conn.ttl(cache.key(user_id)) for user_id in range(1, 4)]

    assert len(set(ttl_values)) > 1


@pytest.mark.asyncio
async def test_release_refresh_lock_keeps_lock_when_owner_token_differs() -> None:
    cache = UserProfileCache()
    conn = redis_storage.get_connection()
    user_id = 1

    acquired = await cache.acquire_refresh_lock(user_id, "owner-token")
    await cache.release_refresh_lock(user_id, "other-token")

    assert acquired is True
    assert await conn.get(cache.lock_key(user_id)) == "owner-token"

    await cache.release_refresh_lock(user_id, "owner-token")

    assert await conn.get(cache.lock_key(user_id)) is None


@pytest.mark.asyncio
async def test_get_user_profile_cache_hit_returns_redis_value() -> None:
    user_id = 1
    cache = UserProfileCache()
    await cache.set(
        user_id,
        UserProfileResponse(name="cached-mina", age=30),
    )

    profile = await get_user_profile(user_id, service=_service())

    assert profile.model_dump() == {"name": "cached-mina", "age": 30}


@pytest.mark.asyncio
async def test_update_user_profile_deletes_stale_cache_before_next_read() -> None:
    repository = UserProfileRepository()
    cache = UserProfileCache()
    service = UserProfileService(repository=repository, cache=cache)
    user_id = 1

    repository.save(user_id, UserProfileResponse(name="origin-mina", age=29))
    await cache.set(user_id, UserProfileResponse(name="stale-mina", age=28))

    updated_profile = await update_user_profile(
        user_id,
        UserProfileUpdateRequest(name="updated-mina", age=31),
        service=service,
    )

    conn = redis_storage.get_connection()
    assert updated_profile.model_dump() == {"name": "updated-mina", "age": 31}
    assert await conn.get(cache.key(user_id)) is None

    profile = await get_user_profile(user_id, service=service)

    assert profile.model_dump() == {"name": "updated-mina", "age": 31}
    assert await conn.get(cache.key(user_id)) is not None


@pytest.mark.asyncio
async def test_update_user_profile_keeps_origin_write_when_redis_unavailable() -> None:
    repository = UserProfileRepository()
    user_id = 1

    updated_profile = await update_user_profile(
        user_id,
        UserProfileUpdateRequest(name="updated-mina", age=31),
        service=UserProfileService(
            repository=repository,
            cache=_UnavailableUserProfileCache(),
        ),
    )

    stored_profile = repository.find_by_id(user_id)
    assert updated_profile.model_dump() == {"name": "updated-mina", "age": 31}
    assert stored_profile is not None
    assert stored_profile.model_dump() == {"name": "updated-mina", "age": 31}


@pytest.mark.asyncio
async def test_update_user_profile_waits_for_in_flight_cache_fill() -> None:
    repository = UserProfileRepository()
    cache = _BlockingCacheSetUserProfileCache(blocked_profile_name="origin-mina")
    service = UserProfileService(
        repository=repository,
        cache=cache,
        lock_retry_delay_seconds=0.01,
    )
    user_id = 1

    repository.save(user_id, UserProfileResponse(name="origin-mina", age=29))

    # 1. 조회 요청이 cache miss 후 SQLite에서 기존 값을 읽고 cache set까지 진입한다.
    #    helper cache는 이 시점에서 Redis 쓰기를 잠시 멈춰 race 상황을 만든다.
    read_task = asyncio.create_task(get_user_profile(user_id, service=service))
    await cache.set_started.wait()

    # 2. 기존 값을 Redis에 쓰기 전에 PUT 요청을 시작한다.
    #    올바른 구현이라면 PUT은 refresh lock을 기다려야 한다.
    update_task = asyncio.create_task(
        update_user_profile(
            user_id,
            UserProfileUpdateRequest(name="updated-mina", age=31),
            service=service,
        )
    )
    await asyncio.sleep(0.05)

    # 3. PUT이 먼저 끝나면 위험하다.
    #    이후 read_task가 오래된 값을 Redis에 저장해 stale cache가 남을 수 있다.
    if update_task.done():
        cache.allow_set.set()
        await asyncio.gather(read_task, update_task, return_exceptions=True)
        pytest.fail("update completed before the in-flight cache fill finished")

    # 4. 멈춰 있던 조회 요청을 마무리한다.
    #    그 뒤 PUT이 lock을 얻어 SQLite 저장과 cache delete를 수행해야 한다.
    cache.allow_set.set()
    read_profile, updated_profile = await asyncio.gather(read_task, update_task)

    conn = redis_storage.get_connection()
    assert read_profile.model_dump() == {"name": "origin-mina", "age": 29}
    assert updated_profile.model_dump() == {"name": "updated-mina", "age": 31}
    # 5. PUT이 조회 요청보다 나중에 cache delete를 수행했으므로
    #    최종 Redis cache에는 오래된 값이 남아 있지 않아야 한다.
    assert await conn.get(cache.key(user_id)) is None

    # 6. 다음 조회는 cache miss 후 SQLite의 최신 값을 읽고 Redis를 다시 채운다.
    fresh_profile = await get_user_profile(user_id, service=service)

    assert fresh_profile.model_dump() == {"name": "updated-mina", "age": 31}
    assert await conn.get(cache.key(user_id)) is not None


@pytest.mark.asyncio
async def test_concurrent_cache_miss_duplicates_origin_reads_without_lock() -> None:
    repository = _CountingUserProfileRepository(
        UserProfileResponse(name="origin-mina", age=29),
    )
    service = UserProfileService(
        repository=repository,
        cache=_CoordinatedInitialMissUserProfileCache(initial_miss_count=5),
        stampede_protection_enabled=False,
    )

    profiles = await asyncio.gather(
        *[get_user_profile(1, service=service) for _ in range(5)],
    )

    assert [profile.model_dump() for profile in profiles] == [
        {"name": "origin-mina", "age": 29},
    ] * 5
    assert repository.find_count == 5


@pytest.mark.asyncio
async def test_concurrent_cache_miss_uses_redis_lock_to_reduce_origin_reads() -> None:
    repository = _CountingUserProfileRepository(
        UserProfileResponse(name="origin-mina", age=29),
    )
    service = UserProfileService(
        repository=repository,
        cache=_CoordinatedInitialMissUserProfileCache(initial_miss_count=5),
    )

    profiles = await asyncio.gather(
        *[get_user_profile(1, service=service) for _ in range(5)],
    )

    assert [profile.model_dump() for profile in profiles] == [
        {"name": "origin-mina", "age": 29},
    ] * 5
    assert repository.find_count == 1


@pytest.mark.asyncio
async def test_get_user_profile_invalid_cache_payload() -> None:
    conn = redis_storage.get_connection()
    user_id = 1
    await conn.set(f"cache:user:{user_id}:profile", "[]")

    with pytest.raises(HTTPException) as exc:
        await get_user_profile(user_id, service=_service())

    assert exc.value.status_code == 500
    assert exc.value.detail == "Invalid user profile data"


@pytest.mark.asyncio
async def test_get_user_profile_uses_sqlite_when_redis_unavailable() -> None:
    repository = UserProfileRepository()
    user_id = 1
    repository.save(
        user_id,
        UserProfileResponse(name="origin-mina", age=29),
    )

    profile = await get_user_profile(
        user_id,
        service=UserProfileService(
            repository=repository,
            cache=_UnavailableUserProfileCache(),
        ),
    )

    assert profile.model_dump() == {"name": "origin-mina", "age": 29}


@pytest.mark.asyncio
async def test_get_user_profile_missing() -> None:
    with pytest.raises(HTTPException) as exc:
        await get_user_profile(999, service=_service())
    assert exc.value.status_code == 404
