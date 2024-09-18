from uuid import UUID
from typing import List, Optional, TYPE_CHECKING

from pydantic import BaseModel
      
from .product import ProductSchema
from app.utils.enums import OrderStatus


from .order_item import OrderItemSchema, CreateOrderItemSchema
    
    
class OrderBaseSchema(BaseModel):
    status: OrderStatus = OrderStatus.IN_PROGRESS
    

class OrderSchema(OrderBaseSchema):
    id: UUID
    items: Optional[List[OrderItemSchema]] = None
    
    
class CreateOrderSchema(OrderBaseSchema):
    items: List[CreateOrderItemSchema] 
    
     

    

    
