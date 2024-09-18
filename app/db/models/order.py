from uuid import UUID

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base_mixins import Base, TimestampedMixin
from app.utils.enums import OrderStatus


class Order(Base, TimestampedMixin):
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus),
        nullable=False
    ) 
    

class OrderItem(Base):
    __tablename__ = 'order_items'
    
    order_id: Mapped[UUID]  = mapped_column(
        ForeignKey('orders.id', ondelete='CASCADE'),
        unique=True,
    )
    product_id: Mapped[UUID]  = mapped_column(
        ForeignKey('products.id', ondelete='CASCADE'),
    )
    product_quantity: Mapped[int]