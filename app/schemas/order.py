from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.schemas.product import ProductRead

class OrderCreate(BaseModel):
    item: str = Field(..., example="Laptop")
    quantity : int = Field(..., example=1)
    status: Optional[str] = Field(...,example="pending/shipped/delivered")
    product_id: int = Field(..., example=1)

class OrderRead(BaseModel):
    id: int
    item: str
    quantity: int
    status: str
    user_id: int
    product : ProductRead

    class Config:
        orm_mode = True

