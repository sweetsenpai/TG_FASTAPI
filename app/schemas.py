from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PostOut(BaseModel):
    id: int
    title: str
    text: str
    date_of_creation: datetime

    class Config:
        from_attributes = True


class PostCreate(BaseModel):
    title: str
    text: str

    class Config:
        from_attributes = True


class PostUpdate(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None

    class Config:
        from_attributes = True
