from app.db.session import SessionLocal
from app.models.user import User
from app.models.product import Product
from app.models.customer import Customer
from app.core.security import get_password_hash
import os

def seed():
    db = SessionLocal()
    # Create default user
    if not db.query(User).filter(User.email == "admin@example.com").first():
        admin = User(
            email="admin@example.com",
            hashed_password=get_password_hash("password")
        )
        db.add(admin)
    
    # Create sample products
    if not db.query(Product).first():
        products = [
            Product(name="Laptop Pro", sku="LP-001", category="Electronics", price=1299.99, quantity_in_stock=50),
            Product(name="Wireless Mouse", sku="WM-002", category="Accessories", price=49.99, quantity_in_stock=200),
            Product(name="Mechanical Keyboard", sku="MK-003", category="Accessories", price=149.99, quantity_in_stock=5),
            Product(name="4K Monitor", sku="MN-004", category="Electronics", price=399.99, quantity_in_stock=30),
            Product(name="USB-C Hub", sku="UH-005", category="Accessories", price=29.99, quantity_in_stock=0)
        ]
        db.add_all(products)

    # Create sample customers
    if not db.query(Customer).first():
        customers = [
            Customer(full_name="John Doe", email="john@example.com", phone_number="555-0101", address="123 Main St"),
            Customer(full_name="Jane Smith", email="jane@example.com", phone_number="555-0102", address="456 Oak Ave")
        ]
        db.add_all(customers)

    db.commit()
    print("Database seeded successfully.")

if __name__ == "__main__":
    seed()
