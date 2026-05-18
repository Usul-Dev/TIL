import os
from collections.abc import Generator

import pytest
import pytest_asyncio
from testcontainers.redis import AsyncRedisContainer

from app.storages.redis import redis_storage


@pytest.fixture(scope="session")
def redis_container() -> Generator[AsyncRedisContainer, None, None]:
    with AsyncRedisContainer(image="redis:7.4-alpine") as container:
        host = container.get_container_host_ip()
        port = container.get_exposed_port(container.port)
        url = f"redis://{host}:{port}/0"
        previous = os.environ.get("REDIS_URL")
        os.environ["REDIS_URL"] = url
        try:
            yield container
        finally:
            if previous is None:
                os.environ.pop("REDIS_URL", None)
            else:
                os.environ["REDIS_URL"] = previous


@pytest_asyncio.fixture(autouse=True)
async def redis_cleanup(redis_container):
    client = await redis_container.get_async_client()
    await redis_storage.close()
    await client.flushdb()
    try:
        yield
    finally:
        await client.flushdb()
        await redis_storage.close()
        await client.aclose()
