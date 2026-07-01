"""Table routes — list tables, table status."""

from fastapi import APIRouter, Depends

from db import get_session
from db.queries import list_tables_status
from routes._deps import current_user

router = APIRouter(prefix="/api/tables", tags=["tables"])


@router.get("")
def get_tables(_user=Depends(current_user)):
    db = get_session()
    return list_tables_status(db)
