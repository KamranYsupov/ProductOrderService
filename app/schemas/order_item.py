from uuid import UUID
from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel
      
from .product import ProductSchema


if TYPE_CHECKING:
    from .order import OrderSchema
    
    
class OrderItemBaseSchema(BaseModel):
    product_quantity: int
    
   
class OrderItemSchema(OrderItemBaseSchema):
    id: UUID
    order: Optional['OrderSchema'] = None
    product: ProductSchema
    
     
class CreateOrderItemSchema(OrderItemBaseSchema):
    order_id: Optional[UUID] = None
    product_id: UUID | str
    