from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from library_mgmt.config import get_settings
from library_mgmt.app.auth.jwt import create_access_token
from library_mgmt.app.models import User
from library_mgmt.app.utils.db import get_db


router = APIRouter(prefix="/oauth", tags=["oauth"])
settings = get_settings()


@router.get("/google/login")
def google_login_url():
    if not settings.GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=501, detail="Google OAuth not configured")
    return {"message": "Google OAuth scaffold - configure client ID/secret"}


@router.get("/google/callback")
def google_callback(code: str | None = None, db: Session = Depends(get_db)):
    if not settings.GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=501, detail="Google OAuth not configured")
    # Placeholder: Normally exchange code -> tokens, fetch profile
    # Mock user creation for scaffold
    email = "scaffold-user@example.com"
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(email=email, full_name="Google User", is_active=True, provider="google")
        db.add(user)
        db.commit()
        db.refresh(user)
    token = create_access_token(subject=user.email)
    return {"access_token": token, "token_type": "bearer"}


