from uuid import uuid4

import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app 
from app.core.config import settings
from app.db import db_manager, Base
from app.schemas.product import CreateProductSchema
from app.schemas.order import (
    OrderSchema,
    CreateOrderSchema,
)
from app.schemas.order_item import (
    OrderItemSchema,
    CreateOrderItemSchema
)
from app.utils.enums import OrderStatus



@pytest.fixture(scope='session', autouse=True)
async def setup_db():
    async with db_manager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    yield
    
    async with db_manager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        

@pytest.fixture(scope='function')
def fastapi_app():
    return app


@pytest.fixture(scope='function')
async def async_client(fastapi_app):
    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app),
        base_url=f'{settings.base_url}{settings.api_v1_prefix}',
    ) as ac:
        yield ac
        
   
@pytest.fixture(scope='function')
async def product_data():
    product_data = {
        'name': 'Test Product',
        'description': 'A product for testing',
        'price': 100.0,
        'quantity': 100,
    }
    product = CreateProductSchema(**product_data)
    return product.model_dump()

     
@pytest.fixture(scope='function')
async def created_product(async_client, product_data):
    response = await async_client.post('/products/', json=product_data)
    return response.json()
   

@pytest.fixture(scope='function')
async def order_data(created_product):
    items_data = [
        {
            'product_id': created_product['id'],
            'product_quantity': 10,
        }    
    ]
    order_data = {
        'items': items_data,
    }
    order = CreateOrderSchema(**order_data)
    
    order_data = order.model_dump()
    order_data['status'] = order.status.value # OrderStatus.IN_PROGRESS.value
    
    return order_data

     
@pytest.fixture(scope='function')
async def created_order(async_client, order_data):    
    response = await async_client.post('/orders/', json=order_data)
    return response.json()



