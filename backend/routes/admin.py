"""Admin routes — menu, users, reports."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from db import get_session
from db.queries import (
    update_skewer_price,
    daily_skewer_sales,
    daily_table_sales,
    list_users,
    create_user,
    update_user,
)
from routes._deps import admin_only

router = APIRouter(prefix="/api/admin", tags=["admin"])


class UpdatePriceBody(BaseModel):
    price: float


class CreateUserBody(BaseModel):
    username: str
    password: str
    role_id: int          # 1=admin 2=waiter
    real_name: str = ""


class UpdateUserBody(BaseModel):
    real_name: str | None = None
    password: str | None = None


# ── menu ──────────────────────────────────────

@router.put("/skewers/{skewer_id}/price")
def update_price(skewer_id: int, body: UpdatePriceBody, _user=Depends(admin_only)):
    if body.price <= 0:
        raise HTTPException(400, "price must be > 0")
    db = get_session()
    try:
        update_skewer_price(db, skewer_id, body.price)
    except ValueError as e:
        raise HTTPException(404, str(e))
    return {"status": "ok"}


# ── users ─────────────────────────────────────

@router.get("/users")
def get_users(_user=Depends(admin_only)):
    return list_users(get_session())


@router.post("/users")
def add_user(body: CreateUserBody, _user=Depends(admin_only)):
    if body.role_id not in (1, 2):
        raise HTTPException(400, "role_id must be 1 (admin) or 2 (waiter)")
    if len(body.username) < 2:
        raise HTTPException(400, "username too short")
    if len(body.password) < 4:
        raise HTTPException(400, "password too short")

    db = get_session()
    try:
        uid = create_user(db, body.username, body.password, body.role_id, body.real_name)
    except ValueError as e:
        raise HTTPException(400, str(e))
    return {"id": uid, "username": body.username}


@router.put("/users/{user_id}")
def edit_user(user_id: int, body: UpdateUserBody, _user=Depends(admin_only)):
    if body.real_name is None and body.password is None:
        raise HTTPException(400, "nothing to update")

    db = get_session()
    try:
        update_user(db, user_id, body.real_name, body.password)
    except ValueError as e:
        raise HTTPException(404, str(e))
    return {"status": "ok"}


# ── reports ───────────────────────────────────

@router.get("/reports/skewers")
def skewer_sales(date: str | None = None, _user=Depends(admin_only)):
    db = get_session()
    return daily_skewer_sales(db, date)


@router.get("/reports/tables")
def table_sales(date: str | None = None, _user=Depends(admin_only)):
    db = get_session()
    return daily_table_sales(db, date)
