from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.logger_config import setup_logger
from app.posts.crud import (
    create_post,
    delete_post,
    get_all_posts,
    get_post,
    get_posts_menu,
    update_post,
)
from app.schemas.posts import PostCreate, PostMenu, PostOut, PostUpdate
from app.security.jwt_auth import get_current_user

logger = setup_logger(__name__)

posts_router = APIRouter()


@posts_router.get("/posts", response_model=List[PostOut], tags=["Posts"])
async def list_posts():
    return await get_all_posts()


@posts_router.get("/posts/menu", response_model=List[PostMenu], tags=["Posts"])
async def menu_posts():
    return await get_posts_menu()


@posts_router.get("/posts/{post_id}", response_model=PostOut, tags=["Posts"])
async def get_one_post(post_id: int):
    post = await get_post(post_id)
    if not post:
        logger.warning("Попытка получения не существующего поста с id %s}", post_id)
        raise HTTPException(status_code=404, detail="Пост не найден")
    return post


@posts_router.post("/posts", response_model=PostOut, status_code=201, tags=["Posts"])
async def create(post: PostCreate):
    post_obj = await create_post(post)
    logger.info("Создан новый пост")
    return PostOut.model_validate(post_obj)


@posts_router.patch("/posts/{post_id}", response_model=PostOut, tags=["Posts"])
async def patch(
    post_id: int,
    post_update: PostUpdate,
    current_user: dict = Depends(get_current_user),
):
    post = await get_post(post_id)
    if not post:
        raise HTTPException(404, detail="Пост не найден")
    updated = await update_post(post, post_update)
    return PostOut.model_validate(updated)


@posts_router.delete("/posts/{post_id}", tags=["Posts"])
async def delete(post_id: int, current_user: dict = Depends(get_current_user)):
    post = await get_post(post_id)
    if not post:
        logger.warning("Попытка удаления не существующего поста с id %s}", post_id)
        raise HTTPException(404, detail="Пост не найден")
    await delete_post(post)
    return {"message": f"Пост с id {post_id} удален."}
