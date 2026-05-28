import json

from pydantic import ValidationError

from app.representations.user_response import UserProfileResponse
from app.storages.redis import redis_storage


class UserProfileCache:
    """Store user profiles in Redis for cache-aside reads."""

    def __init__(self, ttl_seconds: int = 60) -> None:
        self.ttl_seconds = ttl_seconds

    def key(self, user_id: int) -> str:
        """Build the Redis cache key for a user profile.

        Args:
            user_id: User identifier.

        Returns:
            Redis key for the cached user profile.
        """
        return f"cache:user:{user_id}:profile"

    async def get(self, user_id: int) -> UserProfileResponse | None:
        """Read a user profile from Redis.

        Args:
            user_id: User identifier.

        Returns:
            Cached profile when the key exists, otherwise None.

        Raises:
            ValueError: If the cached JSON cannot be decoded or validated.
        """
        conn = redis_storage.get_connection()
        raw_profile = await conn.get(self.key(user_id))
        if raw_profile is None:
            return None

        try:
            data = json.loads(raw_profile)
            return UserProfileResponse(**data)
        except (json.JSONDecodeError, ValidationError) as exc:
            raise ValueError("Invalid cached user profile data") from exc

    async def set(self, user_id: int, profile: UserProfileResponse) -> None:
        """Store a user profile in Redis with a fixed TTL.

        Args:
            user_id: User identifier.
            profile: User profile to cache.

        Returns:
            None.
        """
        conn = redis_storage.get_connection()
        await conn.setex(
            self.key(user_id),
            self.ttl_seconds,
            profile.model_dump_json(),
        )
