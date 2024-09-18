from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from .base_mixins import Base


class Product(Base):
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[float]
    quantity: Mapped[int]
    