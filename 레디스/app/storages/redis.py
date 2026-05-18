import os

import redis.asyncio as redis


class _RedisStorage:
    _instance: "_RedisStorage | None" = None

    def __new__(cls) -> "_RedisStorage":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if hasattr(self, "_initialized") and self._initialized:
            return
        self._client: redis.Redis | None = None
        self._initialized = True

    def _redis_url(self) -> str:
        return os.getenv("REDIS_URL", "redis://localhost:6379/0")

    def get_connection(self) -> redis.Redis:
        if self._client is None:
            self._client = redis.Redis.from_url(
                self._redis_url(),
                decode_responses=True,
            )
        return self._client

    async def close(self) -> None:
        if self._client is None:
            return
        await self._client.aclose()
        self._client = None


redis_storage = _RedisStorage()
