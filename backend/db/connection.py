"""Database engine + session — SQLAlchemy, DB-agnostic."""

import os
import sys
from pathlib import Path
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session

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
