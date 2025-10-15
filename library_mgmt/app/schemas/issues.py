from datetime import date
from pydantic import BaseModel


class IssueIn(BaseModel):
    user_id: int
    book_id: int
    issue_date: date
    due_date: date


class ReturnIn(BaseModel):
    return_date: date


