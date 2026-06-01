import os

schemas_dir = "backend/app/schemas"
api_dir = "backend/app/api/endpoints"
services_dir = "backend/app/services"
main_file = "backend/app/main.py"

# Schemas
schemas_init = """from .token import Token, TokenData
from .user import UserCreate, User, UserLogin
from .product import ProductBase, ProductCreate, ProductUpdate, Product
from .customer import CustomerBase, CustomerCreate, CustomerUpdate, Customer
from .order import OrderBase, OrderCreate, OrderUpdate, Order, OrderItemBase, OrderItemCreate, OrderItem
"""
token_schema = """from pydantic import BaseModel
class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    email: str | None = None
"""
user_schema = """from pydantic import BaseModel, EmailStr
class UserBase(BaseModel):
    email: EmailStr
class UserCreate(UserBase):
    password: str
class UserLogin(UserBase):
    password: str
class User(UserBase):
    id: int
    is_active: bool
    class Config:
        from_attributes = True
"""
product_schema = """from pydantic import BaseModel, Field
class ProductBase(BaseModel):
    name: str
    sku: str
    description: str | None = None
    category: str | None = None
    price: float = Field(ge=0)
    quantity: int = Field(ge=0)
class ProductCreate(ProductBase):
    pass
class ProductUpdate(BaseModel):
    name: str | None = None
    sku: str | None = None
    description: str | None = None
    category: str | None = None
    price: float | None = Field(default=None, ge=0)
    quantity: int | None = Field(default=None, ge=0)
class Product(ProductBase):
    id: int
    class Config:
        from_attributes = True
"""
customer_schema = """from pydantic import BaseModel, EmailStr
class CustomerBase(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: str | None = None
    address: str | None = None
class CustomerCreate(CustomerBase):
    pass
class CustomerUpdate(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None
    address: str | None = None
class Customer(CustomerBase):
    id: int
    class Config:
        from_attributes = True
"""
order_schema = """from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from .customer import Customer
from .product import Product

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
"""

os.makedirs(schemas_dir, exist_ok=True)
with open(os.path.join(schemas_dir, "__init__.py"), "w") as f: f.write(schemas_init)
with open(os.path.join(schemas_dir, "token.py"), "w") as f: f.write(token_schema)
with open(os.path.join(schemas_dir, "user.py"), "w") as f: f.write(user_schema)
with open(os.path.join(schemas_dir, "product.py"), "w") as f: f.write(product_schema)
with open(os.path.join(schemas_dir, "customer.py"), "w") as f: f.write(customer_schema)
with open(os.path.join(schemas_dir, "order.py"), "w") as f: f.write(order_schema)

# Main app file
main_content = """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import auth, products, customers, orders
from app.db.base import Base
from app.db.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inventory & Order Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(products.router, prefix="/api/products", tags=["products"])
app.include_router(customers.router, prefix="/api/customers", tags=["customers"])
app.include_router(orders.router, prefix="/api/orders", tags=["orders"])

@app.get("/")
def read_root():
    return {"message": "Welcome to IOMS API"}
"""
with open(main_file, "w") as f: f.write(main_content)

print("Schemas and main file created.")
