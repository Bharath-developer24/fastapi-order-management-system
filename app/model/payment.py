from datetime import datetime

from app.database import Base
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey      

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    payment_method = Column(String, nullable=False)
    payment_status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    payment_at = Column(DateTime, default=None)




    