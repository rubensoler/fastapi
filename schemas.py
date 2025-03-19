from pydantic import BaseModel

class ProductSchema(BaseModel):
    id: int
    name: str
    price: float
    image_url: str

    class Config:
        from_attributes = True

class CreateProductSchema(BaseModel):
    name: str
    price: float
    image_url: str

class UpdateProductSchema(BaseModel):
    name: str
    price: float
    image_url: str
