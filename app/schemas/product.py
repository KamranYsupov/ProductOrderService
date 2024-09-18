from uuid import UUID

from pydantic import BaseModel, Field
      
      
class ProductBaseSchema(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=500)
    price: float = Field(gt=0.0)
    quantity: int = Field(ge=0)
    

class ProductSchema(ProductBaseSchema):
    id: UUID


class CreateProductSchema(ProductBaseSchema):
    pass

class UpdateProductSchema(ProductBaseSchema):
    pass