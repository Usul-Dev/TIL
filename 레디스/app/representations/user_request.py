from pydantic import BaseModel


class GetUserProfile(BaseModel):
    user_id: int


class UserProfileUpdateRequest(BaseModel):
    name: str
    age: int
