from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid
from app.db.session import get_db
from app.schemas import order as schemas
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.customer import Customer
from app.models.inventory_log import InventoryLog

router = APIRouter()

@router.get("/", response_model=List[schemas.Order])
def get_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Order).offset(skip).limit(limit).all()

@router.post("/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == order.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
    new_order = Order(
        order_number=order_number,
        customer_id=order.customer_id,
        status="Pending",
        total_amount=0.0
    )
    db.add(new_order)
    db.flush() # flush to get new_order.id

    total_amount = 0.0
    for item in order.items:
        product = db.query(Product).with_for_update().filter(Product.id == item.product_id).first()
        if not product:
            db.rollback()
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        if product.quantity < item.quantity:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Insufficient stock for {product.name}")
        
        # Reduce stock
        product.quantity -= item.quantity
        
        # Log inventory
        inv_log = InventoryLog(
            product_id=product.id,
            change_amount=-item.quantity,
            reason=f"Order {order_number}"
        )
        db.add(inv_log)
        
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=product.price
        )
        db.add(order_item)
        total_amount += item.quantity * product.price

    new_order.total_amount = total_amount
    db.commit()
    db.refresh(new_order)
    return new_order

@router.put("/{order_id}", response_model=schemas.Order)
def update_order(order_id: int, order_update: schemas.OrderUpdate, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # If order is cancelled, we might want to restore inventory, but keeping it simple for now
    db_order.status = order_update.status
    db.commit()
    db.refresh(db_order)
    return db_order
