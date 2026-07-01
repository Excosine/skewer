"""Table routes — list tables, table detail, update status."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from db import get_session
from db.queries import (
    list_tables_status,
    get_table_detail,
    update_table_status,
)
from routes._deps import current_user

router = APIRouter(prefix="/api/tables", tags=["tables"])


class UpdateTableBody(BaseModel):
    status: int


@router.get("")
def get_tables(_user=Depends(current_user)):
    db = get_session()
    return list_tables_status(db)


@router.get("/{table_id}")
def get_one(table_id: int, _user=Depends(current_user)):
    db = get_session()
    data = get_table_detail(db, table_id)
    if data is None:
        raise HTTPException(404, "桌子不存在")
    return data


@router.put("/{table_id}")
def update_table(table_id: int, body: UpdateTableBody, _user=Depends(current_user)):
    if body.status != 0:
        raise HTTPException(400, "status 仅允许 0")
    db = get_session()
    try:
        update_table_status(db, table_id, body.status)
    except ValueError as e:
        raise HTTPException(400, str(e))
    return {"status": "ok"}
