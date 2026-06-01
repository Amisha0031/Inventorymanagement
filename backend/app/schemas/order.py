from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from .customer import Customer
from .product import ProductOut as Product

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    
class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    order_id: int
    unit_price: float
    product: Product | None = None
    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    customer_id: int

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderUpdate(BaseModel):
    status: str # Pending, Processing, Completed, Cancelled

class Order(OrderBase):
    id: int
    order_number: str
    order_date: datetime
    status: str
    total_amount: float
    items: List[OrderItem]
    customer: Customer | None = None
    class Config:
        from_attributes = True
