from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import RegisterTortoise

from app.schemas import PostCreate, PostOut, PostUpdate
from configs.tortoise_config import TORTOISE_ORM
from db.models import Posts


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Подключаемся к БД")
    async with RegisterTortoise(
        app=app,
        config=TORTOISE_ORM,
        generate_schemas=False,
    ):
        yield


app = FastAPI(title="Тестовое задание", lifespan=lifespan)
# app.include_router(posts_router, prefix="/api")


@app.get("/posts", response_model=List[PostOut])
async def get_all_posts():
    posts = await Posts.all()
    return posts


@app.post("/posts", response_model=PostOut, status_code=201)
async def create_post(post: PostCreate):
    post_obj = await Posts.create(**post.model_dump())
    return PostOut.model_validate(post_obj)


@app.patch("/posts/{post_id}", response_model=PostOut)
async def update_post(post_id: int, post_update: PostUpdate):
    post = await Posts.get_or_none(id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")

    post_data = post_update.model_dump(exclude_unset=True)
    for key, value in post_data.items():
        setattr(post, key, value)

    await post.save()
    return PostOut.model_validate(post)


@app.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    post = await Posts.get_or_none(id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    await post.delete()
    return {"message": f"Пост с id {post_id} удален."}
