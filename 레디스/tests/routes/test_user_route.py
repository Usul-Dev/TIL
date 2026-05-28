import pytest
from fastapi import HTTPException
from redis.exceptions import ConnectionError as RedisConnectionError

from app.repositories.user_profile_repository import UserProfileRepository
from app.representations.user_response import UserProfileResponse
from app.routes.user_route import get_user_profile
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
