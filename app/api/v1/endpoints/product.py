from uuid import UUID
from typing import List, Dict, Any

from dependency_injector import providers
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Header, HTTPException
from starlette import status

from app.core.container import Container
from app.schemas.product import (
    UpdateProductSchema,
    CreateProductSchema, 
    ProductSchema
)
from app.services import ProductService
from app.db import Product

router = APIRouter(tags=['Product'], prefix='/products')


@router.get(
    '/{product_id}',
    status_code=status.HTTP_200_OK,
    response_model=ProductSchema,
)
@inject
async def get_product(
    product_id: UUID,
    product_service: ProductService = Depends(
        Provide[Container.product_service]
    ),
) -> ProductSchema:
    product = await product_service.get(id=product_id)
    product_schema = product.serialize(
        schema_class=ProductSchema,
        model_dump=False,
    )
    return product_schema


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=List[ProductSchema],
)
@inject
async def get_products(
    limit: int = 10,
    skip: int = 0, 
    product_service: ProductService = Depends(
        Provide[Container.product_service]
    ),
) -> List[ProductSchema]:

    products = await product_service.list(limit=limit, skip=skip)
    products_schemas = [
        product.serialize(
            schema_class=ProductSchema,
            model_dump=False,
        )
        for product in products
    ]
   
    return products_schemas


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=ProductSchema,
)
@inject
async def create_product(
    create_product_schema: CreateProductSchema,
    product_service: ProductService = Depends(
        Provide[Container.product_service]
    ),
) -> ProductSchema:
    product = await product_service.create(obj_in=create_product_schema)
    product_schema = product.serialize(
        schema_class=ProductSchema,
        model_dump=False,
    )
    
    return product_schema


@router.put(
    '/{product_id}',
    status_code=status.HTTP_200_OK,
    response_model=ProductSchema,
)
@inject
async def update_product(
    product_id: str,
    update_product_schema: UpdateProductSchema,
    product_service: ProductService = Depends(
        Provide[Container.product_service]
    ),
) -> ProductSchema:
    product = await product_service.update(
        obj_id=UUID(product_id),
        obj_in=update_product_schema,
    )
    product_schema = product.serialize(
        schema_class=ProductSchema,
        model_dump=False,
    )
    return product_schema


@router.delete(
    '/{product_id}',
    status_code=status.HTTP_200_OK,
)
@inject
async def delete_product(
    product_id: str,
    product_service: ProductService = Depends(
        Provide[Container.product_service]
    ),
) -> str:
    await product_service.delete(id=UUID(product_id))
    return "Товар успешно удален"