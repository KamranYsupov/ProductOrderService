from app.db import Order, OrderItem
from .base import RepositoryBase


class RepositoryOrder(RepositoryBase[Order]):
    """Репозиторий для работы с таблицей orders"""


class RepositoryOrderItem(RepositoryBase[OrderItem]):
    """Репозиторий для работы с таблицей order_items"""
    