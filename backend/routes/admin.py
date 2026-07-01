"""Admin routes — menu, users, reports."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from db import get_session
from db.models import SkewerType
from db.queries import (
    update_skewer_price,
    daily_skewer_sales,
    daily_table_sales,
    list_users,
    create_user,
    update_user,
    toggle_user_status,
    record_log,
    list_logs,
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
        skewer = db.query(SkewerType).get(skewer_id)
        old_price = float(skewer.price) if skewer else 0
        update_skewer_price(db, skewer_id, body.price)
        record_log(db, int(_user["sub"]), "price_adjust",
                   target_type="skewer", target_id=skewer_id,
                   target_name=skewer.name if skewer else "",
                   detail=f"价格 {old_price} -> {body.price}")
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
        record_log(db, int(_user["sub"]), "user_create",
                   target_type="user", target_id=uid,
                   target_name=body.real_name or body.username,
                   detail=f"新增员工: {body.username}")
    except ValueError as e:
        raise HTTPException(400, str(e))
    return {"id": uid, "username": body.username}


@router.put("/users/{user_id}")
def edit_user(user_id: int, body: UpdateUserBody, _user=Depends(admin_only)):
    if body.real_name is None and body.password is None:
        raise HTTPException(400, "nothing to update")

    db = get_session()
    from db.models import User
    user = db.query(User).get(user_id)
    try:
        update_user(db, user_id, body.real_name, body.password)
        record_log(db, int(_user["sub"]), "user_update",
                   target_type="user", target_id=user_id,
                   target_name=body.real_name or (user.real_name if user else ""),
                   detail="修改员工信息" if body.real_name else "修改员工密码")
    except ValueError as e:
        raise HTTPException(404, str(e))
    return {"status": "ok"}


@router.put("/users/{user_id}/status")
def toggle_user(user_id: int, _user=Depends(admin_only)):
    try:
        result = toggle_user_status(get_session(), user_id)
        # 记录操作日志
        db = get_session()
        from db.models import User
        user = db.query(User).get(user_id)
        op_type = "user_enable" if result["status"] == 1 else "user_disable"
        record_log(db, int(_user["sub"]), op_type,
                   target_type="user", target_id=user_id,
                   target_name=user.real_name if user else "",
                   detail=f"{'启用' if result['status'] == 1 else '禁用'}员工账号")
    except ValueError as e:
        raise HTTPException(404, str(e))
    return result


# ── reports ───────────────────────────────────

@router.get("/reports/skewers")
def skewer_sales(date: str | None = None, _user=Depends(admin_only)):
    db = get_session()
    return daily_skewer_sales(db, date)


@router.get("/reports/tables")
def table_sales(date: str | None = None, _user=Depends(admin_only)):
    db = get_session()
    return daily_table_sales(db, date)


# ── logs ──────────────────────────────────────

@router.get("/logs")
def get_logs(
    date: str | None = None,
    operation_type: str | None = None,
    user_id: int | None = None,
    page: int = 1,
    page_size: int = 50,
    _user=Depends(admin_only),
):
    db = get_session()
    return list_logs(db, date_str=date, operation_type=operation_type,
                     user_id=user_id, page=page, page_size=page_size)
