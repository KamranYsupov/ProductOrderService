from uuid import uuid4

import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app 
from app.core.config import settings
    
    
async def test_create_product(
    async_client: AsyncClient,
    product_data: dict,
):
    response = await async_client.post(
        '/products/', 
        json=product_data
    )
    assert response.status_code == 201
    created_product = response.json()
    assert created_product['name'] == product_data['name']
    assert created_product['description'] == product_data['description']
    assert created_product['price'] == product_data['price']


async def test_get_product(
    async_client: AsyncClient, 
    created_product: dict,
):
    product_id = created_product['id']
    response = await async_client.get(
        f'/products/{product_id}'
    )
    assert response.status_code == 200
    assert response.json() == created_product


async def test_update_product(
    async_client: AsyncClient, 
    created_product: dict,
):
    product_id = created_product['id']
    updated_data = {
        'name': 'Updated Product',
        'description': 'An updated product for testing',
        'price': 150.0,
        'quantity': 10,
    }
    
    response = await async_client.put(
        f'/products/{product_id}',
        json=updated_data
    )
    assert response.status_code == 200
    assert response.json()['name'] == updated_data['name']


async def test_delete_product(
    async_client: AsyncClient, 
    created_product: dict,
):
    product_id = created_product['id']
    response = await async_client.delete(
        f'/products/{product_id}'
    )
    assert response.status_code == 200
    
    response = await async_client.get(
        f'/products/{product_id}'
    )
    assert response.status_code == 404


async def test_get_non_existent_product(async_client: AsyncClient):
    non_existent_id = uuid4() 
    response = await async_client.get(
        f'/products/{non_existent_id}'
    )
    assert response.status_code == 404
