from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from library_mgmt.app.auth.jwt import require_superadmin
from library_mgmt.app.services.email import send_due_reminder_emails
from library_mgmt.app.utils.db import get_db


router = APIRouter(prefix="/emails", tags=["emails"])


@router.post("/reminders")
def trigger_due_reminders(_: str = Depends(require_superadmin), db: Session = Depends(get_db)):
    # Placeholder: derive recipient list from due loans
    recipients = ["user1@example.com", "user2@example.com"]
    count = send_due_reminder_emails(recipients)
    return {"queued": count}


