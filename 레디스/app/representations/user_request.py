from pydantic import BaseModel


class UserProfileUpdateRequest(BaseModel):
    name: str
    age: int
