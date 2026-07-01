"""Database engine + session — SQLAlchemy, DB-agnostic."""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool

from .models import Base

_engine = None
_Session = None
_db_url: str | None = None


def _build_url(db_path: str | None = None) -> str:
    """Construct DB URL. Dev defaults to SQLite, prod via DB_URL env."""
    if url := os.environ.get("DB_URL"):
        return url
    if db_path is None:
        db_path = str(Path(__file__).resolve().parent.parent / "runtime" / "data.db")
    return f"sqlite:///{db_path}"


def init_db(db_path: str | None = None) -> None:
    global _engine, _Session, _db_url

    _db_url = _build_url(db_path)
    # _engine = create_engine(_db_url, echo=False, poolclass=NullPool)
    _engine = create_engine(_db_url, echo=False)

    if _db_url.startswith("sqlite"):
        @event.listens_for(_engine, "connect")
        def _sqlite_pragma(dbapi_conn, _record):
            dbapi_conn.execute("PRAGMA foreign_keys = ON")
            dbapi_conn.execute("PRAGMA journal_mode = WAL")

    Base.metadata.create_all(_engine)
    _Session = sessionmaker(bind=_engine)

    # seed default data if tables are empty
    from .models import (
        Role, User, TableZone, Table, Category, SkewerType,
    )
    with _Session() as s:
        if s.query(Role).count() == 0:
            import bcrypt
            s.add_all([
                Role(name="admin"),
                Role(name="waiter"),
            ])
            s.add_all([
                User(username="admin",    password_hash=bcrypt.hashpw(b"123456", bcrypt.gensalt()).decode(), role_id=1, real_name="张经理"),
                User(username="waiter01", password_hash=bcrypt.hashpw(b"123456", bcrypt.gensalt()).decode(), role_id=2, real_name="小李"),
            ])
            s.add_all([
                TableZone(name="大厅", surcharge=0.00,  sort_order=1),
                TableZone(name="包间", surcharge=10.00, sort_order=2),
                TableZone(name="露台", surcharge=5.00,  sort_order=3),
            ])
            s.flush()
            s.add_all([
                Table(zone_id=1, table_code="A01", capacity=4, sort_order=1),
                Table(zone_id=1, table_code="A02", capacity=4, sort_order=2),
                Table(zone_id=1, table_code="A03", capacity=6, sort_order=3),
                Table(zone_id=2, table_code="B01", capacity=8, sort_order=4),
                Table(zone_id=2, table_code="B02", capacity=8, sort_order=5),
                Table(zone_id=3, table_code="C01", capacity=4, sort_order=6),
                Table(zone_id=3, table_code="C02", capacity=4, sort_order=7),
            ])
            s.add_all([
                Category(name="肉类"),
                Category(name="蔬菜"),
                Category(name="海鲜"),
                Category(name="豆制品"),
                Category(name="主食"),
            ])
            s.flush()
            s.add_all([
                # 肉类
                SkewerType(category_id=1, name="牛肉串",   price=3.00, sort_order=1),
                SkewerType(category_id=1, name="羊肉串",   price=3.50, sort_order=2),
                SkewerType(category_id=1, name="五花肉串", price=2.50, sort_order=3),
                SkewerType(category_id=1, name="鸡翅",     price=4.00, sort_order=4),
                SkewerType(category_id=1, name="鸡胗",     price=2.00, sort_order=5),
                SkewerType(category_id=1, name="掌中宝",   price=3.50, sort_order=6),
                SkewerType(category_id=1, name="烤肠",     price=2.00, sort_order=7),
                # 蔬菜
                SkewerType(category_id=2, name="韭菜",     price=1.00, sort_order=1),
                SkewerType(category_id=2, name="金针菇",   price=1.50, sort_order=2),
                SkewerType(category_id=2, name="土豆片",   price=1.00, sort_order=3),
                SkewerType(category_id=2, name="茄子",     price=1.50, sort_order=4),
                SkewerType(category_id=2, name="玉米",     price=2.00, sort_order=5),
                SkewerType(category_id=2, name="青椒",     price=1.00, sort_order=6),
                # 海鲜
                SkewerType(category_id=3, name="鱿鱼串",   price=4.00, sort_order=1),
                SkewerType(category_id=3, name="虾",       price=5.00, sort_order=2),
                SkewerType(category_id=3, name="生蚝",     price=6.00, sort_order=3),
                # 豆制品
                SkewerType(category_id=4, name="豆腐皮",   price=1.50, sort_order=1),
                SkewerType(category_id=4, name="面筋",     price=1.50, sort_order=2),
                # 主食
                SkewerType(category_id=5, name="馒头片",   price=1.00, sort_order=1),
                SkewerType(category_id=5, name="年糕",     price=2.00, sort_order=2),
            ])
            s.commit()

            # ── 历史订单数据（近30天） ──
            from .models import Order, OrderItem
            import random

            skewers = s.query(SkewerType).all()  # 全部签子类型
            tables_all = s.query(Table).all()     # 全部桌子

            history_days = 30
            for day_offset in range(1, history_days + 1):
                # 每天 1~3 笔订单
                daily_orders_count = random.randint(1, 3)
                used_tables = set()

                for _ in range(daily_orders_count):
                    # 随机选桌子（避开重复）
                    available = [t for t in tables_all if t.id not in used_tables]
                    if not available:
                        break
                    tbl = random.choice(available)
                    used_tables.add(tbl.id)

                    # 随机 2~4 种签子
                    item_count = random.randint(2, 4)
                    chosen = random.sample(skewers, item_count)

                    total_count = 0
                    items_total = 0.0
                    items_data = []
                    for sk in chosen:
                        cnt = random.randint(5, 30)
                        subtotal = round(cnt * float(sk.price), 2)
                        total_count += cnt
                        items_total += subtotal
                        items_data.append((sk.id, cnt, subtotal))

                    zone_fee = float(random.choice([0, 0, 0, 5, 10, 10]))
                    total_price = round(items_total + zone_fee, 2)

                    paid_date = (datetime.utcnow() - timedelta(days=day_offset)).replace(
                        hour=random.randint(10, 22), minute=random.randint(0, 59), second=0
                    )
                    waiter_id = random.choice([1, 2])

                    order = Order(
                        order_no=f"{paid_date:%Y%m%d}{paid_date:%H%M%S}-{tbl.id}",
                        table_id=tbl.id,
                        waiter_id=waiter_id,
                        zone_surcharge=zone_fee,
                        total_count=total_count,
                        total_price=total_price,
                        status=1,  # 已结账
                        paid_at=paid_date,
                        created_at=paid_date,
                        updated_at=paid_date,
                    )
                    s.add(order)
                    s.flush()

                    for sid, cnt, subtotal in items_data:
                        s.add(OrderItem(
                            order_id=order.id,
                            skewer_type_id=sid,
                            count=cnt,
                            unit_price=float(s.query(SkewerType).get(sid).price),
                            subtotal=subtotal,
                        ))

            s.commit()

            # ── 测试订单数据 ──

            orders_data = [
                # (table_id, waiter_id, zone_surcharge, [(skewer_type_id, count), ...])
                (1, 2, 0.00, [(1, 15), (2, 10), (8, 5)]),           # A01: 牛肉15+羊肉10+韭菜5
                (3, 2, 0.00, [(1, 20), (14, 10), (9, 8)]),           # A03: 牛肉20+鱿鱼10+金针菇8
                (4, 2, 10.00, [(1, 30), (2, 20), (14, 15), (8, 10)]),# B01: 牛肉30+羊肉20+鱿鱼15+韭菜10
                (6, 2, 5.00, [(1, 18), (2, 12), (14, 8)]),           # C01: 牛肉18+羊肉12+鱿鱼8
            ]

            for table_id, waiter_id, zone_fee, items in orders_data:
                # 计算 total
                total_count = sum(c for _, c in items)
                items_total = sum(c * (float(s.query(SkewerType).get(sid).price)) for sid, c in items)
                total_price = items_total + zone_fee

                order = Order(
                    order_no=f"20260701-{random.randint(100,999)}",
                    table_id=table_id,
                    waiter_id=waiter_id,
                    zone_surcharge=zone_fee,
                    total_count=total_count,
                    total_price=total_price,
                    status=0,
                )
                s.add(order)
                s.flush()

                for sid, cnt in items:
                    sk = s.query(SkewerType).get(sid)
                    s.add(OrderItem(
                        order_id=order.id,
                        skewer_type_id=sid,
                        count=cnt,
                        unit_price=sk.price,
                        subtotal=float(sk.price) * cnt,
                    ))

                # 设置桌子为占用
                s.query(Table).filter(Table.id == table_id).update({"status": 1})

            s.commit()


def get_session() -> Session:
    global _Session
    if _Session is None:
        init_db()
    return _Session()


def close_db() -> None:
    global _engine
    if _engine:
        _engine.dispose()
        _engine = None
