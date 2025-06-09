from contextlib import asynccontextmanager

from fastapi import FastAPI
from tortoise.contrib.fastapi import RegisterTortoise

from app.auth.auth_api import auth_router
from app.logger_config import setup_logger
from app.posts.posts_api import posts_router
from configs.tortoise_config import TORTOISE_ORM

logger = setup_logger(__name__)


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
app.include_router(auth_router)
