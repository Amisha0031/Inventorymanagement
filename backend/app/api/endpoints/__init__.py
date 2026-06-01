from fastapi import APIRouter

from .auth import router as auth_router
from .dashboard import router as dashboard_router
from .products import router as products_router
from .customers import router as customers_router
from .orders import router as orders_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(products_router, prefix="/products", tags=["products"])
api_router.include_router(customers_router, prefix="/customers", tags=["customers"])
api_router.include_router(orders_router, prefix="/orders", tags=["orders"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["dashboard"])