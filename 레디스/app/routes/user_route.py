from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter

from app.dependencies import get_user_profile_service
from app.representations.user_request import UserProfileUpdateRequest
from app.representations.user_response import UserProfileResponse
from app.services.user_profile_service import UserProfileService

user_v1_router = APIRouter(prefix="/api/v1")


@user_v1_router.get(
    "/users/{user_id}/profile",
    response_model=UserProfileResponse,
)
async def get_user_profile(
    user_id: int,
    service: Annotated[
        UserProfileService,
        Depends(get_user_profile_service),
    ],
) -> UserProfileResponse:
    try:
        profile = await service.get_user_profile(user_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=500,
            detail="Invalid user profile data",
        ) from exc

    if profile is None:
        raise HTTPException(status_code=404, detail="User profile not found")

    return profile


@user_v1_router.put(
    "/users/{user_id}/profile",
    response_model=UserProfileResponse,
)
async def update_user_profile(
    user_id: int,
    request: UserProfileUpdateRequest,
    service: Annotated[
        UserProfileService,
        Depends(get_user_profile_service),
    ],
) -> UserProfileResponse:
    profile = UserProfileResponse(name=request.name, age=request.age)
    return await service.update_user_profile(user_id, profile)
