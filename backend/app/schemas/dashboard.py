from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class RecentOrder(BaseModel):
    id: int
    order_number: str
    total_amount: float
    order_date: datetime
    status: str

    class Config:
        orm_mode = True

class OrdersPerDay(BaseModel):
    date: str  # ISO formatted date
    count: int

class InventoryCategory(BaseModel):
    category: Optional[str]
    count: int

class DashboardSummary(BaseModel):
    total_products: int
    total_customers: int
    total_orders: int
    low_stock: int
    revenue: float
    recent_orders: List[RecentOrder]
    orders_per_day: List[OrdersPerDay]
    inventory_distribution: List[InventoryCategory]
