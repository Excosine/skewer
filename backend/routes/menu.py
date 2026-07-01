"""Menu routes — categories and skewer types."""

from fastapi import APIRouter, Depends

from db import get_session
from db.queries import list_menu, list_categories
from routes._deps import current_user

router = APIRouter(prefix="/api/menu", tags=["menu"])


@router.get("/categories")
def get_categories(_user=Depends(current_user)):
    return list_categories(get_session())


@router.get("/skewers")
def get_skewers(_user=Depends(current_user)):
    return list_menu(get_session())
