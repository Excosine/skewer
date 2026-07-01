"""Query helpers using SQLAlchemy ORM."""

from datetime import date, datetime
from sqlalchemy.orm import Session, joinedload

from .models import (
    Role, User,
    TableZone, Table,
    Category, SkewerType,
    Order, OrderItem,
)

PRICE_PER_SKEWER = 2.00  # 每根签子固定价格（元）

# ── tables ────────────────────────────────────

def list_tables_status(db: Session) -> list[dict]:
    tables = (
        db.query(Table)
        .join(TableZone, Table.zone_id == TableZone.id)
        .outerjoin(Order, (Order.table_id == Table.id) & (Order.status == 0))
        .options(
            joinedload(Table.zone),
            joinedload(Table.orders).joinedload(Order.waiter),
        )
        .order_by(TableZone.sort_order, Table.sort_order)
        .all()
    )
    result = []
    for t in tables:
        active = next((o for o in t.orders if o.status == 0), None)
        result.append({
            "table_id": t.id,
            "zone_name": t.zone.name,
            "zone_surcharge": float(t.zone.surcharge),
            "table_code": t.table_code,
            "capacity": t.capacity,
            "table_status": t.status,
            "order_id": active.id if active else None,
            "order_no": active.order_no if active else None,
            "total_count": active.total_count if active else None,
            "total_price": float(active.total_price) if active else None,
            "waiter_name": active.waiter.real_name if active and active.waiter else None,
            "order_created_at": active.created_at if active else None,
        })
    return result


# ── menu ──────────────────────────────────────

def list_menu(db: Session) -> list[dict]:
    items = (
        db.query(SkewerType)
        .join(Category)
        .filter(SkewerType.status == 1)
        .order_by(Category.id, SkewerType.sort_order)
        .all()
    )
    return [
        {
            "id": s.id,
            "skewer_name": s.name,
            "category_name": s.category.name,
            "unit_price": float(s.price),
            "sort_order": s.sort_order,
        }
        for s in items
    ]


def list_categories(db: Session) -> list[dict]:
    return [
        {"id": c.id, "name": c.name}
        for c in db.query(Category).order_by(Category.id).all()
    ]


def update_skewer_price(db: Session, skewer_id: int, price: float):
    item = db.query(SkewerType).get(skewer_id)
    if item is None:
        raise ValueError("skewer_type not found")
    item.price = price
    item.updated_at = datetime.utcnow()
    db.commit()


# ── orders ────────────────────────────────────

def create_order(db: Session, table_id: int, waiter_id: int) -> int:
    table = db.query(Table).options(joinedload(Table.zone)).filter(Table.id == table_id).first()
    if table is None:
        raise ValueError("table not found")

    surcharge = float(table.zone.surcharge)
    now = datetime.utcnow()
    order_no = f"{now:%Y%m%d%H%M%S}-{table_id}"

    order = Order(
        order_no=order_no,
        table_id=table_id,
        waiter_id=waiter_id,
        zone_surcharge=surcharge,
        created_at=now,
        updated_at=now,
    )
    table.status = 1
    db.add(order)
    db.commit()
    return order.id


def get_order(db: Session, order_id: int) -> Order | None:
    return db.query(Order).get(order_id)


def get_order_detail(db: Session, order_id: int) -> list[dict]:
    items = (
        db.query(OrderItem)
        .join(SkewerType)
        .filter(OrderItem.order_id == order_id)
        .all()
    )
    return [
        {
            "item_id": oi.id,
            "skewer_name": oi.skewer_type.name,
            "count": oi.count,
            "unit_price": float(oi.unit_price),
            "subtotal": float(oi.subtotal),
        }
        for oi in items
    ]


def add_order_item(db: Session, order_id: int, skewer_type_id: int) -> int:
    existing = (
        db.query(OrderItem)
        .filter(OrderItem.order_id == order_id, OrderItem.skewer_type_id == skewer_type_id)
        .first()
    )
    if existing:
        return existing.id

    st = db.query(SkewerType).get(skewer_type_id)
    if st is None:
        raise ValueError("skewer_type not found")

    item = OrderItem(
        order_id=order_id,
        skewer_type_id=skewer_type_id,
        count=0,
        unit_price=float(st.price),
        subtotal=0,
    )
    db.add(item)
    db.commit()
    return item.id


def update_order_item_count(db: Session, item_id: int, count: int):
    item = db.query(OrderItem).get(item_id)
    if item is None:
        raise ValueError("order_item not found")
    item.count = count
    item.subtotal = round(count * float(item.unit_price), 2)
    db.commit()


def delete_order_item(db: Session, item_id: int):
    item = db.query(OrderItem).get(item_id)
    if item:
        db.delete(item)
        db.commit()


def update_order_count(db: Session, order_id: int, count: int):
    order = db.query(Order).get(order_id)
    if order is None:
        raise ValueError("order not found")
    order.total_count = count
    order.updated_at = datetime.utcnow()
    db.commit()


def close_order(db: Session, order_id: int):
    order = db.query(Order).options(joinedload(Order.table)).filter(Order.id == order_id).first()
    if order is None:
        raise ValueError("order not found")

    total = round(order.total_count * PRICE_PER_SKEWER + float(order.zone_surcharge), 2)

    order.status = 1
    order.paid_at = datetime.utcnow()
    order.total_price = total
    order.updated_at = datetime.utcnow()
    order.table.status = 2
    db.commit()


# ── auth ──────────────────────────────────────

def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username, User.status == 1).first()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id, User.status == 1).first()


# ── user management ──────────────────────────

def list_users(db: Session) -> list[dict]:
    rows = (
        db.query(User, Role.name.label("role_name"))
        .join(Role, User.role_id == Role.id)
        .order_by(User.id)
        .all()
    )
    return [
        {
            "id": u.id,
            "username": u.username,
            "real_name": u.real_name,
            "role": role_name,
            "role_id": u.role_id,
            "status": u.status,
            "created_at": u.created_at.isoformat(),
        }
        for u, role_name in rows
    ]


def create_user(db: Session, username: str, password: str, role_id: int, real_name: str) -> int:
    existing = db.query(User).filter(User.username == username).first()
    if existing:
        raise ValueError("用户名已存在")

    import bcrypt
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = User(
        username=username,
        password_hash=pw_hash,
        role_id=role_id,
        real_name=real_name,
    )
    db.add(user)
    db.commit()
    return user.id


def update_user(db: Session, user_id: int, real_name: str | None, password: str | None):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise ValueError("用户不存在")

    if real_name is not None:
        user.real_name = real_name

    if password is not None and password.strip():
        import bcrypt
        user.password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    db.commit()


# ── admin reports ─────────────────────────────

def daily_skewer_sales(db: Session, date_str: str | None = None) -> list[dict]:
    if date_str is None:
        date_str = date.today().isoformat()

    from sqlalchemy import func, cast, Date
    rows = (
        db.query(
            cast(Order.paid_at, Date).label("sale_date"),
            SkewerType.name.label("skewer_name"),
            func.sum(OrderItem.count).label("total_count"),
            func.sum(OrderItem.subtotal).label("total_amount"),
        )
        .join(OrderItem, OrderItem.order_id == Order.id)
        .join(SkewerType, SkewerType.id == OrderItem.skewer_type_id)
        .filter(Order.status == 1)
        .filter(cast(Order.paid_at, Date) == date_str)
        .group_by(cast(Order.paid_at, Date), SkewerType.name)
        .order_by(func.sum(OrderItem.subtotal).desc())
        .all()
    )
    return [
        {
            "sale_date": str(r.sale_date),
            "skewer_name": r.skewer_name,
            "total_count": r.total_count,
            "total_amount": float(r.total_amount or 0),
        }
        for r in rows
    ]


def daily_table_sales(db: Session, date_str: str | None = None) -> list[dict]:
    if date_str is None:
        date_str = date.today().isoformat()

    from sqlalchemy import func, cast, Date
    rows = (
        db.query(
            cast(Order.paid_at, Date).label("sale_date"),
            TableZone.name.label("zone_name"),
            Table.table_code,
            func.count(Order.id).label("order_count"),
            func.sum(Order.total_count).label("total_skewers"),
            func.sum(Order.total_price).label("total_amount"),
        )
        .join(Table, Table.id == Order.table_id)
        .join(TableZone, TableZone.id == Table.zone_id)
        .filter(Order.status == 1)
        .filter(cast(Order.paid_at, Date) == date_str)
        .group_by(cast(Order.paid_at, Date), TableZone.name, Table.table_code)
        .order_by(func.sum(Order.total_price).desc())
        .all()
    )
    return [
        {
            "sale_date": str(r.sale_date),
            "zone_name": r.zone_name,
            "table_code": r.table_code,
            "order_count": r.order_count,
            "total_skewers": int(r.total_skewers or 0),
            "total_amount": float(r.total_amount or 0),
        }
        for r in rows
    ]
