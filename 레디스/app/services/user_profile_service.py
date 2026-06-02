import asyncio
from uuid import uuid4

from redis.exceptions import RedisError

from app.repositories.user_profile_repository import UserProfileRepository
from app.representations.user_response import UserProfileResponse
from app.services.user_profile_cache import UserProfileCache


class UserProfileService:
    """Coordinate cache-aside reads and write-time invalidation."""

    def __init__(
        self,
        repository: UserProfileRepository,
        cache: UserProfileCache,
        stampede_protection_enabled: bool = True,
        lock_retry_attempts: int = 5,
        lock_retry_delay_seconds: float = 0.05,
        write_lock_retry_attempts: int = 100,
    ) -> None:
        self.repository = repository
        self.cache = cache
        self.stampede_protection_enabled = stampede_protection_enabled
        self.lock_retry_attempts = lock_retry_attempts
        self.lock_retry_delay_seconds = lock_retry_delay_seconds
        self.write_lock_retry_attempts = write_lock_retry_attempts

    async def get_user_profile(
        self,
        user_id: int,
    ) -> UserProfileResponse | None:
        """Read a user profile using the cache-aside pattern.

        Args:
            user_id: User identifier.

        Returns:
            User profile when found in Redis or SQLite, otherwise None.
        """
        try:
            cached_profile = await self.cache.get(user_id)
        except RedisError:
            return await self._read_origin_and_cache(user_id)

        if cached_profile is not None:
            return cached_profile

        if self.stampede_protection_enabled:
            return await self._get_user_profile_with_refresh_lock(user_id)

        return await self._read_origin_and_cache(user_id)

    async def update_user_profile(
        self,
        user_id: int,
        profile: UserProfileResponse,
    ) -> UserProfileResponse:
        """Save the origin profile and invalidate the cached copy.

        The source-of-truth write is performed first. Redis is a performance
        layer, so cache delete failures are not allowed to roll back a
        successful SQLite update.
        """
        token = uuid4().hex
        try:
            acquired = await self._acquire_refresh_lock_with_retry(
                user_id,
                token,
                self.write_lock_retry_attempts,
            )
        except RedisError:
            return await self._save_origin_and_invalidate_cache(user_id, profile)

        if not acquired:
            return await self._save_origin_and_invalidate_cache(user_id, profile)

        try:
            return await self._save_origin_and_invalidate_cache(user_id, profile)
        finally:
            try:
                await self.cache.release_refresh_lock(user_id, token)
            except RedisError:
                pass

    async def _get_user_profile_with_refresh_lock(
        self,
        user_id: int,
    ) -> UserProfileResponse | None:
        token = uuid4().hex
        try:
            acquired = await self.cache.acquire_refresh_lock(user_id, token)
        except RedisError:
            return await self._read_origin_and_cache(user_id)

        if not acquired:
            return await self._wait_for_refreshed_cache(user_id)

        try:
            try:
                cached_profile = await self.cache.get(user_id)
            except RedisError:
                cached_profile = None

            if cached_profile is not None:
                return cached_profile

            return await self._read_origin_and_cache(user_id)
        finally:
            try:
                await self.cache.release_refresh_lock(user_id, token)
            except RedisError:
                pass

    async def _wait_for_refreshed_cache(
        self,
        user_id: int,
    ) -> UserProfileResponse | None:
        for _ in range(self.lock_retry_attempts):
            await asyncio.sleep(self.lock_retry_delay_seconds)
            try:
                cached_profile = await self.cache.get(user_id)
            except RedisError:
                return await self._read_origin_and_cache(user_id)

            if cached_profile is not None:
                return cached_profile

        return await self._read_origin_and_cache(user_id)

    async def _acquire_refresh_lock_with_retry(
        self,
        user_id: int,
        token: str,
        retry_attempts: int,
    ) -> bool:
        for attempt in range(retry_attempts + 1):
            acquired = await self.cache.acquire_refresh_lock(user_id, token)
            if acquired:
                return True

            if attempt == retry_attempts:
                return False

            await asyncio.sleep(self.lock_retry_delay_seconds)

        return False

    async def _save_origin_and_invalidate_cache(
        self,
        user_id: int,
        profile: UserProfileResponse,
    ) -> UserProfileResponse:
        self.repository.save(user_id, profile)

        try:
            await self.cache.delete(user_id)
        except RedisError:
            pass

        return profile

    async def _read_origin_and_cache(
        self,
        user_id: int,
    ) -> UserProfileResponse | None:
        profile = self.repository.find_by_id(user_id)
        if profile is None:
            return None

        try:
            await self.cache.set(user_id, profile)
        except RedisError:
            pass

        return profile
