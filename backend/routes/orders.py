"""Order routes — create, view, add items, scan, close."""

import base64
import shutil
import tempfile
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel

from db import get_session
from db.models import OrderItem
from db.queries import (
    create_order,
    get_order,
    get_order_detail,
    add_order_item,
    update_order_item_count,
    delete_order_item,
    close_order,
    record_log,
)
from routes._deps import current_user
from services.detection import detect_sticks, draw_detection

router = APIRouter(prefix="/api/orders", tags=["orders"])


class CreateBody(BaseModel):
    table_id: int


class AddItemBody(BaseModel):
    skewer_type_id: int


class UpdateItemBody(BaseModel):
    count: int


# ── order CRUD ────────────────────────────────

@router.post("")
def create(body: CreateBody, user=Depends(current_user)):
    db = get_session()
    try:
        oid = create_order(db, body.table_id, int(user["sub"]))
    except ValueError as e:
        raise HTTPException(400, str(e))
    order = get_order(db, oid)
    return {
        "id": order.id,
        "order_no": order.order_no,
        "table_id": order.table_id,
        "zone_surcharge": float(order.zone_surcharge),
        "status": order.status,
        "created_at": order.created_at.isoformat(),
    }


@router.get("/{order_id}")
def get_one(order_id: int, _user=Depends(current_user)):
    db = get_session()
    order = get_order(db, order_id)
    if order is None:
        raise HTTPException(404, "order not found")
    items = get_order_detail(db, order_id)
    return {
        "id": order.id,
        "order_no": order.order_no,
        "table_id": order.table_id,
        "zone_surcharge": float(order.zone_surcharge),
        "total_count": order.total_count,
        "total_price": float(order.total_price),
        "status": order.status,
        "created_at": order.created_at.isoformat(),
        "items": items,
    }


@router.post("/{order_id}/close")
def close(order_id: int, _user=Depends(current_user)):
    db = get_session()
    try:
        order = get_order(db, order_id)
        close_order(db, order_id)
        record_log(db, int(_user["sub"]), "order_close",
                   target_type="order", target_id=order_id,
                   target_name=f"桌号 {order.table.table_code}" if order and order.table else "",
                   detail=f"强制结账: 总额 ¥{float(order.total_price) if order else 0}")
    except ValueError as e:
        raise HTTPException(400, str(e))
    return {"status": "ok"}


# ── items CRUD ────────────────────────────────

@router.post("/{order_id}/items")
def add_item(order_id: int, body: AddItemBody, _user=Depends(current_user)):
    db = get_session()
    try:
        item_id = add_order_item(db, order_id, body.skewer_type_id)
    except ValueError as e:
        raise HTTPException(400, str(e))
    item = db.query(OrderItem).filter(OrderItem.id == item_id).first()
    return {"id": item_id, "count": item.count if item else 0}


@router.put("/{order_id}/items/{item_id}")
def update_item(order_id: int, item_id: int, body: UpdateItemBody, _user=Depends(current_user)):
    db = get_session()
    try:
        update_order_item_count(db, item_id, body.count)
    except ValueError as e:
        raise HTTPException(404, str(e))
    return {"status": "ok"}


@router.delete("/{order_id}/items/{item_id}")
def remove_item(order_id: int, item_id: int, _user=Depends(current_user)):
    db = get_session()
    delete_order_item(db, item_id)
    return {"status": "ok"}


# ── scan (YOLO detection) ─────────────────────

@router.post("/{order_id}/items/{item_id}/scan")
def scan_item(
    order_id: int,
    item_id: int,
    image: UploadFile = File(...),
    _user=Depends(current_user),
):
    suffix = Path(image.filename).suffix or ".jpg"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(image.file, tmp)
        tmp_path = tmp.name

    try:
        circles = detect_sticks(tmp_path)
        count = len(circles)
        conf_avg = sum(c["score"] for c in circles) / count if count else 0.0

        # Generate annotated image
        if circles:
            annotated_bytes = draw_detection(tmp_path, circles)
            annotated_b64 = base64.b64encode(annotated_bytes).decode()
        else:
            annotated_b64 = None

        db = get_session()
        update_order_item_count(db, item_id, count)

        return {
            "detected_count": count,
            "confidence_avg": round(conf_avg, 4),
            "annotated_image": annotated_b64,
        }
    finally:
        Path(tmp_path).unlink(missing_ok=True)
