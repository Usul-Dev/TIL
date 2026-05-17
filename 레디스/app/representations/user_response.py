from pydantic import BaseModel


class UserProfileResponse(BaseModel):
    name: str
    age: int
