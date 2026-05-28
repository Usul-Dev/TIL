import os
from collections.abc import AsyncGenerator, Generator
from pathlib import Path

import pytest
import pytest_asyncio
import redis.asyncio as redis
from testcontainers.core.container import DockerContainer
from testcontainers.core.wait_strategies import ExecWaitStrategy

from app.storages.redis import redis_storage


@pytest.fixture(autouse=True)
def sqlite_test_path(tmp_path: Path) -> Generator[None, None, None]:
    previous = os.environ.get("SQLITE_PATH")
    os.environ["SQLITE_PATH"] = str(tmp_path / "test.sqlite3")
    try:
        yield
    finally:
        if previous is None:
            os.environ.pop("SQLITE_PATH", None)
        else:
            os.environ["SQLITE_PATH"] = previous


@pytest.fixture(scope="session")
def redis_container() -> Generator[DockerContainer, None, None]:
    previous_ryuk = os.environ.get("TESTCONTAINERS_RYUK_DISABLED")
    os.environ.setdefault("TESTCONTAINERS_RYUK_DISABLED", "true")
    try:
        with (
            DockerContainer("redis:7.4-alpine")
            .with_exposed_ports(6379)
            .waiting_for(ExecWaitStrategy(["redis-cli", "ping"]))
        ) as container:
            host = container.get_container_host_ip()
            port = container.get_exposed_port(6379)
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
    finally:
        if previous_ryuk is None:
            os.environ.pop("TESTCONTAINERS_RYUK_DISABLED", None)
        else:
            os.environ["TESTCONTAINERS_RYUK_DISABLED"] = previous_ryuk


@pytest_asyncio.fixture(autouse=True)
async def redis_cleanup(
    redis_container: DockerContainer,
    sqlite_test_path: None,
) -> AsyncGenerator[None, None]:
    client = redis.Redis.from_url(
        os.environ["REDIS_URL"],
        decode_responses=True,
    )
    await redis_storage.close()
    await client.flushdb()
    try:
        yield
    finally:
        await client.flushdb()
        await redis_storage.close()
        await client.aclose()
