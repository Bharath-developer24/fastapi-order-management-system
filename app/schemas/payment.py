from pydantic import BaseModel, Field


class PaymentCreate(BaseModel):
    amount: float = Field(..., example=99.99)
    order_id: int = Field(..., example=1)   
    payment_method: str = Field(..., example="credit_card/UPI/cash_on_delivery")
    payment_status: str = Field(default="pending")



class PaymentRead(BaseModel):
    id: int
    order_id: int
    amount: float
    payment_method: str
    payment_status: str

    class Config:
        orm_mode = True
    