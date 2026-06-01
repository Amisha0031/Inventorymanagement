from pydantic import BaseModel, EmailStr
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
