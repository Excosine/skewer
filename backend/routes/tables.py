"""Table routes — list tables, table status."""

from fastapi import APIRouter, Depends, HTTPException

from db import get_session
from db.queries import list_tables_status, reset_table_status
from routes._deps import current_user

router = APIRouter(prefix="/api/tables", tags=["tables"])


@router.get("")
def get_tables(_user=Depends(current_user)):
    db = get_session()
    return list_tables_status(db)


@router.put("/{table_code}/reset")
def reset_table(table_code: str, _user=Depends(current_user)):
    """强制结账后，将清洁中桌子重置为空闲"""
    db = get_session()
    try:
        reset_table_status(db, table_code)
    except ValueError as e:
        raise HTTPException(400, str(e))
    return {"status": "ok"}
