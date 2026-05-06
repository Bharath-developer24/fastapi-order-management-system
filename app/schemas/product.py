from pydantic import BaseModel, Field

class ProductCreate(BaseModel):
    name: str = Field(..., example="Laptop")
    description: str = Field(..., example="A high-performance laptop for gaming and work.")
    price: float = Field(..., example=999.99)
    stock: int = Field(..., examples=[10, 20, 30])

class ProductRead(BaseModel):
    id: int
    name: str
    description: str
    price: float

    class Config:
        orm_mode = True