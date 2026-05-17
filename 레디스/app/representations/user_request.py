from pydantic import BaseModel


class GetUserProfile(BaseModel):
    user_id: int
