from uuid import UUID
from typing import List, Optional, TYPE_CHECKING

from pydantic import BaseModel
      
from .product import ProductSchema
from app.utils.enums import OrderStatus


from .order_item import OrderItemSchema, CreateOrderItemSchema
    
    
class OrderStatusSchema(BaseModel):
    status: OrderStatus = OrderStatus.IN_PROGRESS
    

class OrderSchema(OrderStatusSchema):
    id: UUID
    items: Optional[List[OrderItemSchema]] = None
    
    
class CreateOrderSchema(OrderStatusSchema):
    items: List[CreateOrderItemSchema] 
    
    

     

    

    
