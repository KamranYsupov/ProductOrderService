from fastapi import APIRouter

from app.core.config import settings
from .endpoints.product import router as product_router
from .endpoints.order import router as order_router


api_router = APIRouter()

# REST
api_router.include_router(product_router)
api_router.include_router(order_router)
