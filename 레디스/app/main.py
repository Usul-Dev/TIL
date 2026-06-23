from fastapi import FastAPI

from app.routes.basic_route import basic_v1_router
from app.routes.user_route import user_v1_router

app = FastAPI()
app.include_router(basic_v1_router)
app.include_router(user_v1_router)


@app.get("/api/ping/")
async def pong():
    return {"ping": "pong!"}
