from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from library_mgmt.app.models import User
from library_mgmt.app.schemas.auth import UserOut, UserCreate
from library_mgmt.app.utils.db import get_db
from library_mgmt.app.utils.security import get_password_hash
from library_mgmt.app.auth.jwt import require_superadmin


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[UserOut])
def list_users(_: User = Depends(require_superadmin), db: Session = Depends(get_db)):
    return db.query(User).all()


@router.post("/", response_model=UserOut)
def create_user(payload: UserCreate, _: User = Depends(require_superadmin), db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    user = User(
        email=payload.email,
        full_name=payload.full_name,
        hashed_password=get_password_hash(payload.password),
        is_superadmin=payload.is_superadmin,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}")
def delete_user(user_id: int, _: User = Depends(require_superadmin), db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"ok": True}


