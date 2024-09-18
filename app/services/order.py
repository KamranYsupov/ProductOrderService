from .mixins import CRUDServiceMixin
from app.repositories import (
     RespositoryOrder,
     RespositoryOrderItem
)


class OrderService:
    def __init__(
        self, 
        repository_order: RespositoryOrder,
        repository_order_item: RespositoryOrder,
    ):
        self._repository_order = repository_order
        self._repository_order_item = repository_order_item
