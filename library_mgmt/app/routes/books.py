from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from library_mgmt.app.models import Book, Category, User
from library_mgmt.app.schemas.books import BookIn, BookOut, CategoryIn, CategoryOut
from library_mgmt.app.utils.db import get_db
from library_mgmt.app.auth.jwt import get_current_user, require_superadmin


router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=List[BookOut])
def list_books(
    q: Optional[str] = Query(None, description="Search by title or author"),
    category_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Book)
    if q:
        query = query.filter((Book.title.ilike(f"%{q}%")) | (Book.author.ilike(f"%{q}%")))
    if category_id:
        query = query.filter(Book.category_id == category_id)
    return query.all()


@router.post("/", response_model=BookOut)
def create_book(payload: BookIn, _: User = Depends(require_superadmin), db: Session = Depends(get_db)):
    book = Book(**payload.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@router.put("/{book_id}", response_model=BookOut)
def update_book(book_id: int, payload: BookIn, _: User = Depends(require_superadmin), db: Session = Depends(get_db)):
    book = db.query(Book).get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    for k, v in payload.model_dump().items():
        setattr(book, k, v)
    db.commit()
    db.refresh(book)
    return book


@router.delete("/{book_id}")
def delete_book(book_id: int, _: User = Depends(require_superadmin), db: Session = Depends(get_db)):
    book = db.query(Book).get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"ok": True}


@router.get("/categories", response_model=List[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()


@router.post("/categories", response_model=CategoryOut)
def create_category(payload: CategoryIn, _: User = Depends(require_superadmin), db: Session = Depends(get_db)):
    if db.query(Category).filter(Category.name == payload.name).first():
        raise HTTPException(status_code=400, detail="Category already exists")
    category = Category(**payload.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


