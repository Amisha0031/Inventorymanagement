from fastapi import APIRouter

router = APIRouter()

@router.get("/summary")
def get_dashboard_summary():
    return {
        "total_products": 0,
        "total_customers": 0,
        "total_orders": 0,
        "low_stock": 0,
        "revenue": 0,
        "recent_orders": [],
        "orders_per_day": [],
        "inventory_distribution": []
    }