from pydantic import BaseModel
from typing import Optional


class BookBaseSchema(BaseModel):
    title: str
    description: Optional[str] = None


class BookCreateSchema(BookBaseSchema):
    author_id: int


class BookResponseSchema(BookBaseSchema):
    id: int
    author_id: Optional[int]

    class Config:
        orm_mode = True
