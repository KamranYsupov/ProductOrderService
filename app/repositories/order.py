from typing import Type, Optional, List

from sqlalchemy import insert
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import Order, OrderItem
from .base import RepositoryBase, ModelType


class RepositoryOrder(RepositoryBase[Order]):
    """Репозиторий для работы с таблицей orders"""
    
    def __init__(
        self, 
        model: Type[ModelType], 
        session: AsyncSession
    ):
        self._session = session
        super().__init__(
            model=Order,
            session=session,
        )
        
    async def list(
        self,
        *args,
        limit: Optional[int] = None,
        skip: Optional[int] = None,
        load_items_with_products: bool = False,
        **kwargs
    ):
        options = self._get_query_options(load_items_with_products)
                
        return await super().list(
            *args, 
            limit=limit, 
            skip=skip,
            options=options,
            **kwargs,
        )
    
    async def get(
        self,
        load_items_with_products: bool = False,
        **kwargs
    ):
        options = self._get_query_options(load_items_with_products)
        
        return await super().get(options=options, **kwargs)
    
    @staticmethod
    def _get_query_options(
        load_items_with_products: bool = False
    ) -> List:
        query_options = []
        if load_items_with_products:
            query_options.append(
                selectinload(Order.items)
                .joinedload(OrderItem.product)
            )
            
        return query_options
        


class RepositoryOrderItem(RepositoryBase[OrderItem]):
    """Репозиторий для работы с таблицей order_items"""
    
    def __init__(
        self, 
        model: Type[ModelType], 
        session: AsyncSession
    ):
        self._session = session
        super().__init__(
            model=OrderItem,
            session=session,
        )
        
    async def list(
        self,
        *args,
        limit: Optional[int] = None,
        skip: Optional[int] = None,
        load_orders: bool = False,
        load_products: bool = False,
        **kwargs
    ):
        options = self._get_query_options(
            load_orders=load_orders,
            load_products=load_products,
        )
            
        return await super().list(
            *args, 
            limit=limit, 
            skip=skip,
            options=options,
            **kwargs,
        )
    
    async def bulk_create(
        self, 
        insert_data: dict,
        returning: bool = False,
    ):
        statement = insert(OrderItem)
        
        if returning:
            statement = statement.returning(OrderItem)
            
        result = await self._session.execute(
            statement, insert_data
        )
        await self._commit_or_rollback()

        if returning:
            return result.scalars().all()
        
    @staticmethod
    def _get_query_options(
        load_orders: bool = False,
        load_products: bool = False,
    ):
        query_options = []
        
        if load_orders:
            query_options.append(joinedload(OrderItem.order))
        if load_products:
            query_options.append(joinedload(OrderItem.product)) 
            
        return query_options
        

    