from io import BytesIO
import pandas as pd
from sqlalchemy.orm import Session
from typing import List

from library_mgmt.app.models import Book, Category, User


def import_books_from_dataframe(df: pd.DataFrame, db: Session) -> int:
    required_cols = {"title", "author"}
    if not required_cols.issubset(set(df.columns.str.lower())):
        raise ValueError("Missing required columns: title, author")

    count = 0
    for _, row in df.iterrows():
        book = Book(
            title=str(row.get("title")),
            author=str(row.get("author")),
            isbn=str(row.get("isbn")) if pd.notna(row.get("isbn")) else None,
        )
        db.add(book)
        count += 1
    db.commit()
    return count


def export_books_dataframe(db: Session) -> pd.DataFrame:
    books: List[Book] = db.query(Book).all()
    data = [
        {
            "id": b.id,
            "title": b.title,
            "author": b.author,
            "isbn": b.isbn,
            "category_id": b.category_id,
        }
        for b in books
    ]
    return pd.DataFrame(data)


