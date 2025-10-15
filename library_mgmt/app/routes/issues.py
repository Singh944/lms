from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from library_mgmt.app.models import Issue, User, Book
from library_mgmt.app.schemas.issues import IssueIn, ReturnIn
from library_mgmt.app.utils.db import get_db
from library_mgmt.app.auth.jwt import get_current_user, require_superadmin


router = APIRouter(prefix="/issues", tags=["issues"])


@router.post("/", response_model=dict)
def create_issue(payload: IssueIn, _: User = Depends(require_superadmin), db: Session = Depends(get_db)):
    if not db.query(User).get(payload.user_id):
        raise HTTPException(status_code=404, detail="User not found")
    if not db.query(Book).get(payload.book_id):
        raise HTTPException(status_code=404, detail="Book not found")
    issue = Issue(**payload.model_dump())
    db.add(issue)
    db.commit()
    return {"ok": True, "id": issue.id}


@router.post("/{issue_id}/return", response_model=dict)
def return_book(issue_id: int, payload: ReturnIn, _: User = Depends(require_superadmin), db: Session = Depends(get_db)):
    issue = db.query(Issue).get(issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    issue.return_date = payload.return_date
    db.commit()
    return {"ok": True}


@router.get("/me", response_model=List[dict])
def my_issues(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    issues = db.query(Issue).filter(Issue.user_id == current_user.id).all()
    return [
        {
            "id": i.id,
            "book_id": i.book_id,
            "issue_date": i.issue_date,
            "due_date": i.due_date,
            "return_date": i.return_date,
        }
        for i in issues
    ]


