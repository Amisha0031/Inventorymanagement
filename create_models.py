import os

models_dir = "backend/app/models"

user_model = """from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
"""

product_model = """from sqlalchemy import Column, Integer, String, Float
from app.db.base import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    sku = Column(String, unique=True, index=True, nullable=False)
    description = Column(String)
    category = Column(String, index=True)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=0, nullable=False)
"""

customer_model = """from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String)
    address = Column(String)
"""

order_model = """from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String, unique=True, index=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="Pending") # Pending, Processing, Completed, Cancelled
    total_amount = Column(Float, default=0.0)

    customer = relationship("Customer")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")
"""

inventory_log_model = """from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
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
"""

models_init = """from .user import User
from .product import Product
from .customer import Customer
from .order import Order, OrderItem
from .inventory_log import InventoryLog
"""

with open(os.path.join(models_dir, "user.py"), "w") as f: f.write(user_model)
with open(os.path.join(models_dir, "product.py"), "w") as f: f.write(product_model)
with open(os.path.join(models_dir, "customer.py"), "w") as f: f.write(customer_model)
with open(os.path.join(models_dir, "order.py"), "w") as f: f.write(order_model)
with open(os.path.join(models_dir, "inventory_log.py"), "w") as f: f.write(inventory_log_model)
with open(os.path.join(models_dir, "__init__.py"), "w") as f: f.write(models_init)

print("Models created.")
