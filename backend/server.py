"""Skewer counting backend — FastAPI entry point."""

import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db import init_db, close_db
from routes import (
    auth_router,
    tables_router,
    orders_router,
    menu_router,
    admin_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_path = os.environ.get("DB_PATH", str(Path(__file__).parent / "runtime" / "data.db"))
    init_db(db_path)
    yield
    close_db()


app = FastAPI(
    title="Skewer Counter",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(tables_router)
app.include_router(orders_router)
app.include_router(menu_router)
app.include_router(admin_router)


@app.get("/")
def root():
    return {"service": "skewer-counter", "version": "0.1.0"}


def main():
    import uvicorn
    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)


if __name__ == "__main__":
    main()
