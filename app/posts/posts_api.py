from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path

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


@posts_router.get(
    "/posts",
    response_model=List[PostOut],
    tags=["Posts"],
    summary="Все посты",
    description="Получение всех постов со полным набором полей.",
)
async def list_posts():
    return await get_all_posts()


@posts_router.get(
    "/posts/menu",
    response_model=List[PostMenu],
    tags=["Posts"],
    summary="Меню для телеграм бота",
    description="Получения всех постов списком для формирования телеграм бота. Из полей присутствуют только `id` и `title`.",
)
async def menu_posts():
    return await get_posts_menu()


@posts_router.get(
    "/posts/{post_id}",
    response_model=PostOut,
    tags=["Posts"],
    summary="Получение одного поста",
    description="Получение детальной информации о посте по его `id`.",
    responses={
        404: {"description": "Пост не найден"},
    },
)
async def get_one_post(
    post_id: int = Path(
        ..., title="ID поста", description="Уникальный идентификатор поста", example=1
    )
):
    post = await get_post(post_id)
    if not post:
        logger.warning("Попытка получения не существующего поста с id %s", post_id)
        raise HTTPException(status_code=404, detail="Пост не найден")
    return post


@posts_router.post(
    "/posts",
    response_model=PostOut,
    status_code=201,
    tags=["Posts"],
    summary="Создание поста",
    description="Создание поста на основе полей `text` и `title`.",
    responses={401: {"description": "Ошибка авторизации"}},
)
async def create(post: PostCreate, current_user: dict = Depends(get_current_user)):
    post_obj = await create_post(post)
    logger.info("Создан новый пост")
    return PostOut.model_validate(post_obj)


@posts_router.patch(
    "/posts/{post_id}",
    response_model=PostOut,
    tags=["Posts"],
    summary="Частичное обновление поста",
    description="Частичное обновление полей поста(`title`, `text`)",
    responses={
        404: {"description": "Пост не найден"},
        401: {"description": "Ошибка авторизации"},
    },
)
async def patch(
    post_update: PostUpdate,
    post_id: int = Path(
        ..., title="ID поста", description="Уникальный идентификатор поста", example=1
    ),
    current_user: dict = Depends(get_current_user),
):
    post = await get_post(post_id)
    if not post:
        raise HTTPException(404, detail="Пост не найден")
    updated = await update_post(post, post_update)
    return PostOut.model_validate(updated)


@posts_router.delete(
    "/posts/{post_id}",
    tags=["Posts"],
    summary="Удаление поста",
    description="Удаление поста по его `id`",
    responses={
        404: {"description": "Пост не найден"},
        401: {"description": "Ошибка авторизации"},
    },
)
async def delete(
    post_id: int = Path(
        ..., title="ID поста", description="Уникальный идентификатор поста", example=1
    ),
    current_user: dict = Depends(get_current_user),
):
    post = await get_post(post_id)
    if not post:
        logger.warning("Попытка удаления не существующего поста с id %s", post_id)
        raise HTTPException(404, detail="Пост не найден")
    await delete_post(post)
    return {"message": f"Пост с id {post_id} удален."}
