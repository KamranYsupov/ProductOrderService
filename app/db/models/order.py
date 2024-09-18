from uuid import UUID

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_mixins import Base, TimestampedMixin
from .product import Product
from app.schemas.order import OrderSchema
from app.schemas.product import ProductSchema
from app.schemas.order_item import OrderItemSchema
from app.utils.enums import OrderStatus


class Order(Base, TimestampedMixin):
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus),
        nullable=False
    ) 
    
    items: Mapped[list['OrderItem']] = relationship(
        back_populates='order',
        lazy='selectin',
    )
    
    def serialize(
        self,
        model_dump: bool = False,
        items: list['OrderItem'] | None = None,
    ) -> dict | OrderSchema:
        """_summary_

        Args:
            model_dump (bool, optional): _description_. Defaults to False.
            items (list[OrderItem] | None, optional): 
                Передается если в запросе не был выполнен join 
                на Order.items.
                ОБЯЗАТЕЛЬНО доставать Order.items вместе с OrderItem.product
                
                Пример запроса в app.repositories.order.py,
                класс RepositoryOrder, метод get: load_items_with_products=True
                 
            Defaults to None.

        Returns:
            dict | OrderSchema
        """
        if not items:
            items = self.items
            
        items_schemas = [
            OrderItemSchema(
                id=item.id,
                product=item.product.serialize(
                    schema_class=ProductSchema,
                    model_dump=False
                ),
                product_quantity=item.product_quantity
            ) for item in items
        ]
        
        order_schema = OrderSchema(
            id=self.id,
            status=self.status,
            items=items_schemas
        )
        
        if model_dump:
            return order_schema.model_dump()
        
        return order_schema
    

class OrderItem(Base):
    __tablename__ = 'order_items'
    
    order_id: Mapped[UUID]  = mapped_column(
        ForeignKey('orders.id', ondelete='CASCADE'),
    )
    product_id: Mapped[UUID]  = mapped_column(
        ForeignKey('products.id', ondelete='CASCADE'),
    )
    product_quantity: Mapped[int]
    
    order: Mapped[Order] = relationship(
        back_populates='items',
        lazy='joined',
    )
    product: Mapped[Product]  = relationship(
        back_populates='items',
        lazy='joined',
    )