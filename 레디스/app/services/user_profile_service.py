from redis.exceptions import RedisError

from app.repositories.user_profile_repository import UserProfileRepository
from app.representations.user_response import UserProfileResponse
from app.services.user_profile_cache import UserProfileCache


class UserProfileService:
    """Coordinate cache-aside reads for user profile lookups."""

    def __init__(
        self,
        repository: UserProfileRepository,
        cache: UserProfileCache,
    ) -> None:
        self.repository = repository
        self.cache = cache

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
            cached_profile = None

        if cached_profile is not None:
            return cached_profile

        profile = self.repository.find_by_id(user_id)
        if profile is None:
            return None

        try:
            await self.cache.set(user_id, profile)
        except RedisError:
            pass

        return profile
