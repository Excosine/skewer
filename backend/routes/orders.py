"""Order routes — create, view, scan, close."""

import shutil
import tempfile
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from db import get_session
from db.queries import (
    PRICE_PER_SKEWER,
    create_order,
    get_order,
    update_order_count,
    close_order,
)
from routes._deps import current_user
from services.detection import detect_sticks
from pydantic import BaseModel

router = APIRouter(prefix="/api/orders", tags=["orders"])


class CreateBody(BaseModel):
    table_id: int


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
    return {
        "id": order.id,
        "order_no": order.order_no,
        "table_id": order.table_id,
        "zone_surcharge": float(order.zone_surcharge),
        "price_per_skewer": PRICE_PER_SKEWER,
        "total_count": order.total_count,
        "total_price": float(order.total_price),
        "status": order.status,
        "created_at": order.created_at.isoformat(),
    }


@router.post("/{order_id}/close")
def close(order_id: int, _user=Depends(current_user)):
    db = get_session()
    try:
        close_order(db, order_id)
    except ValueError as e:
        raise HTTPException(400, str(e))
    return {"status": "ok"}


# ── scan (YOLO detection) ─────────────────────

@router.post("/{order_id}/scan")
def scan_order(
    order_id: int,
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

        db = get_session()
        update_order_count(db, order_id, count)

        return {"detected_count": count, "confidence_avg": round(conf_avg, 4)}
    finally:
        Path(tmp_path).unlink(missing_ok=True)



