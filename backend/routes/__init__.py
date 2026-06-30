from .auth import router as auth_router
from .tables import router as tables_router
from .orders import router as orders_router
from .menu import router as menu_router
from .admin import router as admin_router

__all__ = ["auth_router", "tables_router", "orders_router", "menu_router", "admin_router"]
