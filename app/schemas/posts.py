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
        None,
        min_length=1,
        description="Текст поста",
        example="Это содержимое поста",
    )

    class Config:
        from_attributes = True


class PostCreate(PostBase):
    title: str = Field(
        ...,
        min_length=1,
        max_length=256,
        description="Заголовок поста",
        example="Мой первый пост",
    )
    text: str = Field(
        ...,
        min_length=1,
        description="Текст поста",
        example="Это содержимое поста",
    )


class PostUpdate(PostBase): ...


class PostOut(PostBase):
    id: int = Field(description="Уникальный идентификатор поста", example=1)
    date_of_creation: datetime = Field(
        description="Дата и время создания поста", example="08.06.2025 15:18"
    )

    title: str
    text: str

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime("%d.%m.%Y %H:%M"),
        }


class PostMenu(BaseModel):
    id: int
    title: str
