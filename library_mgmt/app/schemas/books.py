from datetime import date
from typing import Optional, List
from pydantic import BaseModel


class CategoryIn(BaseModel):
    name: str


class CategoryOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class BookIn(BaseModel):
    title: str
    author: str
    isbn: Optional[str] = None
    published_date: Optional[date] = None
    category_id: Optional[int] = None


class BookOut(BookIn):
    id: int
    category: Optional[CategoryOut] = None

    class Config:
        from_attributes = True


