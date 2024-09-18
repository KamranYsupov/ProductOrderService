import pytest
from httpx import AsyncClient
from uuid import uuid4
from app.main import app 
from app.schemas.order import (
    OrderSchema,
    CreateOrderSchema,
)
from app.schemas.order_item import (
    OrderItemSchema,
    CreateOrderItemSchema
)
from app.utils.enums import OrderStatus


async def test_get_order(
    async_client: AsyncClient,
    created_order: dict,
):
    order_id = created_order['id']
    
    response = await async_client.get(f'/orders/{order_id}')
    assert response.status_code == 200
    

async def test_get_orders(
    async_client: AsyncClient,
):
    response = await async_client.get('/orders/')
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_create_order(async_client, order_data):
    response = await async_client.post(
        '/orders/',
        json=order_data
    )
    created_order = response.json()
    
    assert response.status_code == 201


async def test_update_order_status(
    async_client: AsyncClient,
    created_order: dict,
):
    order_id = created_order['id'] 
    response = await async_client.put(
        f'/orders/{order_id}/status',
        json={'status': OrderStatus.SENT.value},
    )
    
    assert response.status_code == 200
    assert response.json()['message'] == 'Статус успешно обновлен'
