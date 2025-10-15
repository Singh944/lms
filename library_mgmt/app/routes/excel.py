from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import pandas as pd
from io import BytesIO

from library_mgmt.app.auth.jwt import require_superadmin
from library_mgmt.app.utils.db import get_db
from library_mgmt.app.services.excel import import_books_from_dataframe, export_books_dataframe
from library_mgmt.app.models import User


router = APIRouter(prefix="/excel", tags=["excel"])


@router.post("/import/books")
async def import_books(file: UploadFile = File(...), _: User = Depends(require_superadmin), db: Session = Depends(get_db)):
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Only Excel files are supported")
    content = await file.read()
    df = pd.read_excel(BytesIO(content))
    count = import_books_from_dataframe(df, db)
    return {"imported": count}


@router.get("/export/books")
def export_books(_: User = Depends(require_superadmin), db: Session = Depends(get_db)):
    df = export_books_dataframe(db)
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": 'attachment; filename="books.xlsx"'},
    )


