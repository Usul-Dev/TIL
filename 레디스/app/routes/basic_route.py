from fastapi.routing import APIRouter
from pydantic import BaseModel

from app.storages.redis import redis_storage

basic_v1_router = APIRouter(prefix="/api/v1")


@basic_v1_router.get("/")
async def get_basic_route():
    return {"hello": "world"}


class FruitCreate(BaseModel):
    fruit_name: str


@basic_v1_router.post("/")
async def add_fruit(payload: FruitCreate):
    fruit_name = payload.fruit_name
    key = f"fruit:{fruit_name}"
    conn = redis_storage.get_connection()
    await conn.set(key, fruit_name)
    result = await conn.get(key)

    return {"success_fruit_name": result}
