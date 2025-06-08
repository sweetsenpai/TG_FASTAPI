from typing import List

from fastapi import APIRouter, HTTPException

from app.schemas import PostCreate, PostOut, PostUpdate
from db.models import Posts

posts_router = APIRouter()


@posts_router.get("/posts", response_model=List[PostOut], tags=["Posts"])
async def get_all_posts():
    posts = await Posts.all()
    return posts


@posts_router.get("/posts/{post_id}", response_model=PostOut, tags=["Posts"])
async def get_one_posts(post_id: int):
    posts = await Posts.filter(id=post_id).first()
    if not posts:
        raise HTTPException(status_code=404, detail="Пост не найден")
    return posts


@posts_router.post("/posts", response_model=PostOut, status_code=201, tags=["Posts"])
async def create_post(post: PostCreate):
    post_obj = await Posts.create(**post.model_dump())
    return PostOut.model_validate(post_obj)


@posts_router.patch("/posts/{post_id}", response_model=PostOut, tags=["Posts"])
async def update_post(post_id: int, post_update: PostUpdate):
    post = await Posts.get_or_none(id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")

    post_data = post_update.model_dump(exclude_unset=True)
    for key, value in post_data.items():
        setattr(post, key, value)

    await post.save()
    return PostOut.model_validate(post)


@posts_router.delete("/posts/{post_id}", tags=["Posts"])
async def delete_post(post_id: int):
    post = await Posts.get_or_none(id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    await post.delete()
    return {"message": f"Пост с id {post_id} удален."}
