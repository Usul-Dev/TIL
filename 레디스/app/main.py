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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        use_colors=True,
        reload=False,
    )
