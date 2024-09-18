import uuid
from typing import List, Optional, Union, Sequence

from fastapi import HTTPException
from starlette import status

from .mixins import CRUDServiceMixin
from app.repositories import (
    RepositoryProduct,
    RepositoryOrder,
    RepositoryOrderItem
)
from app.db import Order, OrderItem
from app.schemas.order import CreateOrderSchema


class OrderService(CRUDServiceMixin):
    def __init__(
        self, 
        repository_product: RepositoryProduct,
        repository_order: RepositoryOrder,
        repository_order_item: RepositoryOrder,
        unique_fields: Union[Sequence[str], None] = None,
    ):
        self._repository_order = repository_order
        self._repository_order_item = repository_order_item
        self._repository_product = repository_product

        super().__init__(
            repository=repository_order,
            unique_fields=unique_fields,
        )
        
        
    async def orders_list( 
        self,
        *args,
        limit: Optional[int] = None,
        skip: Optional[int] = None,
        load_items_with_products: bool = False,
        **kwargs
    ):
        return await self._repository_order.list(
            *args, 
            limit=limit, 
            skip=skip,
            load_items_with_products=load_items_with_products,
            **kwargs,
        )
        
    async def get_order(
        self,
        load_items_with_products: bool = False,
        **kwargs
    ):
        return await self._repository_order.get(
            load_items_with_products=load_items_with_products,
            **kwargs
        )
        
    async def create_order(self, obj_in: CreateOrderSchema) -> Order:
        order_data = dict(obj_in)
        order_data['id'] = uuid.uuid4()
        items_schemas = order_data.pop('items')
        
        products_ids = [uuid.UUID(item.product_id) for item in items_schemas]
        products = await self._repository_product.get_products_by_ids(
            ids=products_ids
        )
        if len(items_schemas) != len(products):
            raise HTTPException(
                detail='Неправильный ввод данных',
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        
        for index, item in enumerate(items_schemas):
            updated_quantity = (
                products[index].quantity - item.product_quantity
            )
            if updated_quantity < 0:
                raise HTTPException(
                    detail='Недостаточно товара на складе',
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
                
            products[index].quantity = updated_quantity
            item.order_id = order_data['id']
            
            if isinstance(item.product_id, str):
                item.product_id = uuid.UUID(item.product_id)
        
        order = await self._repository_order.create(order_data)
        await self._repository_order_item.bulk_create(items_schemas)
        
        return order
    
    async def items_list(
        self,
        *args,
        limit: Optional[int] = None,
        skip: Optional[int] = None,
        load_orders: bool = False,
        load_products: bool = False,
        **kwargs
    ) -> List[OrderItem]:
        return await self._repository_order_item.list(
            *args,
            limit=limit,
            skip=skip,
            load_orders=load_orders,
            load_products=load_products,
            **kwargs
        )
                
        
        
        
        
        
                
