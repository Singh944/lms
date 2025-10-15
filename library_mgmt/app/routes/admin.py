from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from library_mgmt.app.auth.jwt import require_superadmin
from library_mgmt.app.models import User, Book, Issue
from library_mgmt.app.utils.db import get_db


router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/stats", response_model=dict)
def stats(_: User = Depends(require_superadmin), db: Session = Depends(get_db)):
    return {
        "users": db.query(User).count(),
        "books": db.query(Book).count(),
        "issues": db.query(Issue).count(),
    }


