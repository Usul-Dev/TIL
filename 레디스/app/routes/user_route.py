import json

from fastapi import HTTPException
from fastapi.routing import APIRoute, APIRouter

from app.representations.user_response import UserProfileResponse
from app.storages.redis import redis_storage

user_v1_router = APIRouter(
    route_class=APIRoute,
    prefix="/api/v1",
)


@user_v1_router.get(
    "/users/{user_id}/profile",
    response_model=UserProfileResponse,
)
async def get_user_profile(user_id: int):
    conn = redis_storage.get_connection()
    key = f"user:{user_id}"
    raw_profile = await conn.get(key)
    if raw_profile is None:
        raise HTTPException(status_code=404, detail="User profile not found")
    try:
        data = json.loads(raw_profile)
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=500, detail="Invalid user profile data"
        ) from exc
    return UserProfileResponse(**data)
