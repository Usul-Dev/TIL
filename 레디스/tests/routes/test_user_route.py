import json

import pytest
from fastapi import HTTPException

from app.routes.user_route import get_user_profile
from app.storages.redis import redis_storage


@pytest.mark.asyncio
async def test_get_user_profile() -> None:
    conn = redis_storage.get_connection()
    user_id = 1
    await conn.set(
        f"user:{user_id}",
        json.dumps({"name": "mina", "age": 29}),
    )

    profile = await get_user_profile(user_id)
    assert profile is not None
    assert profile.model_dump() == {"name": "mina", "age": 29}


@pytest.mark.asyncio
async def test_get_user_profile_missing() -> None:
    with pytest.raises(HTTPException) as exc:
        await get_user_profile(999)
    assert exc.value.status_code == 404
