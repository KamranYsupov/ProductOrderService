from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_mixins import Base


class Product(Base):
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[float]
    quantity: Mapped[int]
    
    items: Mapped[list['OrderItem']] = relationship(
        back_populates='product',
        lazy='selectin',
    )
    