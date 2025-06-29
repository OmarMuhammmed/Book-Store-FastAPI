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
        from_attributes = True

class BookUpdateSchema(BookBaseSchema):
    title: Optional[str]
