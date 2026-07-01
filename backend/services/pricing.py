"""Pricing logic for orders."""

from sqlalchemy.orm import Session
from db.models import Order, OrderItem


def calculate_order_totals(db: Session, order_id: int) -> dict:
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise ValueError("order not found")

    total_count = sum(i.count for i in order.items)
    items_total = sum(float(i.subtotal) for i in order.items)
    total_price = round(items_total + float(order.zone_surcharge), 2)

    return {
        "total_count": total_count,
        "items_total": items_total,
        "zone_surcharge": float(order.zone_surcharge),
        "total_price": total_price,
    }
