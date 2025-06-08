from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class PostBase(BaseModel):
    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=256,
        description="Заголовок поста",
        example="Мой первый пост",
    )
    text: Optional[str] = Field(
        None, min_length=1, description="Текст поста", example="Это содержимое поста"
    )

    class Config:
        from_attributes = True


class PostCreate(PostBase):
    # В PostCreate поля title и text обязательны, поэтому переопределяем без Optional и без default None
    title: str = Field(
        ...,
        min_length=1,
        max_length=256,
        description="Заголовок поста",
        example="Мой первый пост",
    )
    text: str = Field(
        ..., min_length=1, description="Текст поста", example="Это содержимое поста"
    )


class PostUpdate(PostBase): ...


class PostOut(PostBase):
    id: int = Field(description="Уникальный идентификатор поста", example=1)
    date_of_creation: datetime = Field(
        description="Дата и время создания поста", example="2025-06-08T12:00:00"
    )

    # В PostOut поля title и text уже не Optional, так как при отдаче они обязательны
    title: str
    text: str
