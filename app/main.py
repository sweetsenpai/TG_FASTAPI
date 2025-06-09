from contextlib import asynccontextmanager

from fastapi import FastAPI
from tortoise.contrib.fastapi import RegisterTortoise

from app.posts.posts_api import posts_router
from app.users.users_api import user_router
from configs.tortoise_config import TORTOISE_ORM


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with RegisterTortoise(
        app=app,
        config=TORTOISE_ORM,
        generate_schemas=False,
    ):
        yield


app = FastAPI(title="Тестовое задание", lifespan=lifespan)
app.include_router(posts_router, prefix="/api")
app.include_router(user_router)
