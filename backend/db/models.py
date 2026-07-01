"""SQLAlchemy ORM models — database-agnostic (SQLite dev / PostgreSQL prod)."""

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, SmallInteger, Numeric, DateTime, text,
    ForeignKey, UniqueConstraint, Index,
)
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Role(Base):
    __tablename__ = "roles"

    id   = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False, unique=True)

    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"

    id            = Column(Integer, primary_key=True, autoincrement=True)
    username      = Column(String(64), nullable=False, unique=True)
    password_hash = Column(String(256), nullable=False)
    role_id       = Column(Integer, ForeignKey("roles.id"), nullable=False)
    real_name     = Column(String(64), nullable=False, default="", server_default=text("''"))
    status        = Column(SmallInteger, nullable=False, default=1, server_default=text("1"))
    created_at    = Column(DateTime, default=datetime.utcnow)

    role   = relationship("Role", back_populates="users")
    orders = relationship("Order", back_populates="waiter")


class TableZone(Base):
    __tablename__ = "table_zones"

    id         = Column(Integer, primary_key=True, autoincrement=True)
    name       = Column(String(64), nullable=False, unique=True)
    surcharge  = Column(Numeric(10, 2), nullable=False, default=0, server_default=text("0"))
    sort_order = Column(Integer, nullable=False, default=0, server_default=text("0"))

    tables = relationship("Table", back_populates="zone")


class Table(Base):
    __tablename__ = "tables"

    id         = Column(Integer, primary_key=True, autoincrement=True)
    zone_id    = Column(Integer, ForeignKey("table_zones.id"), nullable=False)
    table_code = Column(String(16), nullable=False, unique=True)
    capacity   = Column(Integer, nullable=False, default=4, server_default=text("4"))
    status     = Column(SmallInteger, nullable=False, default=0, server_default=text("0"))
    sort_order = Column(Integer, nullable=False, default=0, server_default=text("0"))

    zone   = relationship("TableZone", back_populates="tables")
    orders = relationship("Order", back_populates="table")


class Category(Base):
    __tablename__ = "categories"

    id   = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False, unique=True)

    skewer_types = relationship("SkewerType", back_populates="category")


class SkewerType(Base):
    __tablename__ = "skewer_types"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    name        = Column(String(64), nullable=False, unique=True)
    price       = Column(Numeric(10, 2), nullable=False)
    status      = Column(SmallInteger, nullable=False, default=1, server_default=text("1"))
    sort_order  = Column(Integer, nullable=False, default=0, server_default=text("0"))
    created_at  = Column(DateTime, default=datetime.utcnow, server_default=text("CURRENT_TIMESTAMP"))
    updated_at  = Column(DateTime, default=datetime.utcnow, server_default=text("CURRENT_TIMESTAMP"))

    category    = relationship("Category", back_populates="skewer_types")
    order_items = relationship("OrderItem", back_populates="skewer_type")


class Order(Base):
    __tablename__ = "orders"

    id              = Column(Integer, primary_key=True, autoincrement=True)
    order_no        = Column(String(32), nullable=False, unique=True)
    table_id        = Column(Integer, ForeignKey("tables.id"), nullable=False)
    waiter_id       = Column(Integer, ForeignKey("users.id"), nullable=False)
    zone_surcharge  = Column(Numeric(10, 2), nullable=False, default=0, server_default=text("0"))
    total_count     = Column(Integer, nullable=False, default=0, server_default=text("0"))
    total_price     = Column(Numeric(10, 2), nullable=False, default=0, server_default=text("0"))
    status          = Column(SmallInteger, nullable=False, default=0, server_default=text("0"))
    paid_at         = Column(DateTime, nullable=True)
    created_at      = Column(DateTime, default=datetime.utcnow, server_default=text("CURRENT_TIMESTAMP"))
    updated_at      = Column(DateTime, default=datetime.utcnow, server_default=text("CURRENT_TIMESTAMP"))

    table = relationship("Table", back_populates="orders")
    waiter = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan", passive_deletes=True)

    __table_args__ = (
        Index("idx_orders_table", "table_id", "status"),
        Index("idx_orders_waiter", "waiter_id", "created_at"),
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id              = Column(Integer, primary_key=True, autoincrement=True)
    order_id        = Column(Integer, ForeignKey("orders.id"), nullable=False)
    skewer_type_id  = Column(Integer, ForeignKey("skewer_types.id"), nullable=False)
    count           = Column(Integer, nullable=False)
    unit_price      = Column(Numeric(10, 2), nullable=False)
    subtotal        = Column(Numeric(10, 2), nullable=False)
    created_at      = Column(DateTime, default=datetime.utcnow, server_default=text("CURRENT_TIMESTAMP"))

    order       = relationship("Order", back_populates="items", passive_deletes=True)
    skewer_type = relationship("SkewerType", back_populates="order_items")

    __table_args__ = (
        UniqueConstraint("order_id", "skewer_type_id"),
    )
