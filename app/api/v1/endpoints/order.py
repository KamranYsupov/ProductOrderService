from uuid import UUID
from typing import List, Dict, Any

from dependency_injector import providers
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Header, HTTPException
from starlette import status

from app.core.container import Container
from app.schemas.product import ProductSchema
from app.schemas.order import (
    OrderSchema,
    CreateOrderSchema,
    OrderStatusSchema,
)
from app.schemas.order_item import (
    OrderItemSchema,
    CreateOrderItemSchema
)
from app.utils.enums import OrderStatus
from app.services import OrderService
from app.db import Order


router = APIRouter(tags=['Order'], prefix='/orders')


@router.get(
    '/{order_id}',
    status_code=status.HTTP_200_OK,
    response_model=OrderSchema,
    response_model_exclude_none=True,
)
@inject
async def get_order(
    order_id: str,
    order_service: OrderService = Depends(
        Provide[Container.order_service]
    ),
) -> OrderSchema:
    order = await order_service.get(
        id=UUID(order_id),
        load_items_with_products=True
    )    
    order_schema = order.serialize()
    
    return order_schema


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=List[OrderSchema],
    response_model_exclude_none=True,
)
@inject
async def get_orders(
    limit: int = 10,
    skip: int = 0, 
    order_service: OrderService = Depends(
        Provide[Container.order_service]
    ),
) -> List[OrderSchema]:
    orders = await order_service.orders_list(
        limit=limit,
        skip=skip,
        load_items_with_products=True
    )    
    order_schemas = [order.serialize() for order in orders]
    
    return order_schemas


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=OrderSchema,
    response_model_exclude_none=True,
)
@inject
async def create_order(
    create_order_schema: CreateOrderSchema,
    order_service: OrderService = Depends(
        Provide[Container.order_service]
    ),
) -> OrderSchema:
    order = await order_service.create_order(obj_in=create_order_schema)
    
    items = await order_service.items_list(
        order_id=order.id,
        load_orders=False,
        load_products=True,
    )
    order_schema = order.serialize(items=items)

    return order_schema


@router.put(
    '/{order_id}/status',
    status_code=status.HTTP_200_OK,
)
@inject
async def update_order_status(
    order_id: str,
    status: OrderStatusSchema, 
    order_service: OrderService = Depends(
        Provide[Container.order_service]
    ),
) -> dict[str, str]:
    order = await order_service.update(
        obj_id=UUID(order_id),
        obj_in=status.model_dump(),
    )    
    
    return {'message': 'Статус успешно обновлен'}