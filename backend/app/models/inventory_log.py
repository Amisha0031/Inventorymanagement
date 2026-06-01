from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class InventoryLog(Base):
    __tablename__ = "inventory_logs"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    change_amount = Column(Integer, nullable=False) # positive for add, negative for remove
    reason = Column(String) # e.g., "Order #123", "Manual adjustment"
    created_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product")
