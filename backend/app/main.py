import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.endpoints import products, customers, orders, auth
from app.db.base import Base
from app.db.session import engine
from app.models.user import User

Base.metadata.create_all(bind=engine)
app = FastAPI(title=settings.PROJECT_NAME)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["auth"])
app.include_router(products.router, prefix=settings.API_V1_STR, tags=["products"])
app.include_router(customers.router, prefix=settings.API_V1_STR, tags=["customers"])
app.include_router(orders.router, prefix=settings.API_V1_STR, tags=["orders"])
