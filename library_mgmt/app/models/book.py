from sqlalchemy import String, Integer, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from library_mgmt.app.utils.db import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    author: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    isbn: Mapped[str | None] = mapped_column(String(20), unique=True)
    published_date: Mapped[Date | None]
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"))

    category: Mapped[Category | None] = relationship("Category")


