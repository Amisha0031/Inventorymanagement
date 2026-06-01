import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import Base, engine, SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    # add test user
    if not db.query(User).filter(User.email == "test@example.com").first():
        user = User(email="test@example.com", hashed_password=get_password_hash("testpass"))
        db.add(user)
        db.commit()
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to IOMS API"}

def test_login():
    response = client.post(
        "/api/auth/login",
        data={"username": "test@example.com", "password": "testpass"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_create_product():
    response = client.post(
        "/api/products/",
        json={"name": "Test Product", "sku": "TST-001", "price": 10.0, "quantity": 100}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Product"
    assert response.json()["sku"] == "TST-001"
