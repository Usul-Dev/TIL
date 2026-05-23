from fastapi import APIRouter, FastAPI

from app.routes.basic_route import basic_v1_router
from app.routes.user_route import user_v1_router

router = APIRouter()


@router.get("/api/ping/")
async def pong():
    return {"ping": "pong!"}


app = FastAPI()
app.include_router(basic_v1_router)
app.include_router(user_v1_router)
app.include_router(router)
