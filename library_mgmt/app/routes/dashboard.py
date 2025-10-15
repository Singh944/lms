from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from library_mgmt.app.auth.jwt import get_current_user, require_superadmin
from library_mgmt.app.models import Issue, User
from library_mgmt.app.utils.db import get_db


templates = Jinja2Templates(directory="library_mgmt/app/templates")
router = APIRouter(tags=["dashboard"])


@router.get("/")
def home(request: Request):
    return templates.TemplateResponse("base.html", {"request": request, "title": "LMS"})


@router.get("/dashboard")
def user_dashboard(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    borrowed_count = db.query(Issue).filter(Issue.user_id == current_user.id, Issue.return_date.is_(None)).count()
    return templates.TemplateResponse(
        "base.html",
        {"request": request, "title": "User Dashboard", "borrowed_count": borrowed_count},
    )


@router.get("/admin/dashboard")
def admin_dashboard(request: Request, _: User = Depends(require_superadmin), db: Session = Depends(get_db)):
    issued = db.query(Issue).count()
    users = db.query(User).count()
    return templates.TemplateResponse(
        "base.html",
        {"request": request, "title": "Admin Dashboard", "issued": issued, "users": users},
    )


