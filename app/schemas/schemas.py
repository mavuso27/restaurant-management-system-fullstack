from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List
from datetime import date, time
from decimal import Decimal


#Category
class CategoryBase(BaseModel):
    name: str

class CategoryResponse(CategoryBase):
    category_id: int
    class Config:
        from_attributes = True


#Igredient
class IngredientBase(BaseModel):
    name: str
    amount: Decimal
    unit: str

class IngredientResponse(IngredientBase):
    ing_no: int
    class Config:
        from_attributes = True


#Supplier
class SupplierBase(BaseModel):
    name: str
    phone: str
    address: str
    email: Optional[str] = None

class SupplierResponse(SupplierBase):
    supplier_id: int
    class Config:
        from_attributes = True


#Tables
class TableBase(BaseModel):
    capacity: int
    location: str
    status: str

class TableResponse(TableBase):
    table_id: int
    class Config:
        from_attributes = True


#Employee
class EmployeeBase(BaseModel):
    name: str
    role: str
    phone: str
    address: str
    salary: Decimal
    hire_date: date

class EmployeeResponse(EmployeeBase):
    employee_id: int
    class Config:
        from_attributes = True


#Customer
class CustomerBase(BaseModel):
    name: str
    phone: str
    address: str
    email: Optional[str] = None
    country: str

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    customer_id: int
    join_date: Optional[date] = None
    class Config:
        from_attributes = True


#Meal
class MealBase(BaseModel):
    name: str
    price: Decimal
    time: int
    category_id: int

    @field_validator("price")
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Price must be greater than 0")
        return v

    @field_validator("time")
    def time_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Time must be greater than 0")
        return v

class MealCreate(MealBase):
    pass

class MealResponse(MealBase):
    meal_id: int
    class Config:
        from_attributes = True


#Order
class OrderBase(BaseModel):
    date: date
    time: time
    tip: Optional[Decimal] = Decimal("0.00")
    customer_id: int
    employee_id: int
    table_id: int

    @field_validator("tip")
    def tip_must_be_positive(cls, v):
        if v is not None and v < 0:
            raise ValueError("Tip cannot be negative")
        return v

class OrderCreate(OrderBase):
    pass

class OrderResponse(OrderBase):
    order_id: int
    class Config:
        from_attributes = True


#Order item
class OrderItemBase(BaseModel):
    quantity: int
    order_id: int
    meal_id: int

    @field_validator("quantity")
    def quantity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Quantity must be greater than 0")
        return v

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemResponse(OrderItemBase):
    order_item_id: int
    class Config:
        from_attributes = True


#Payment
class PaymentBase(BaseModel):
    payment_date: date
    method: str
    amount: Decimal
    order_id: int

    @field_validator("amount")
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Amount must be greater than 0")
        return v

class PaymentCreate(PaymentBase):
    pass

class PaymentResponse(PaymentBase):
    payment_id: int
    class Config:
        from_attributes = True


#Reservation 
class ReservationBase(BaseModel):
    date: date
    time: time
    status: str
    customer_id: int
    table_id: int

class ReservationCreate(ReservationBase):
    pass

class ReservationResponse(ReservationBase):
    reservation_id: int
    class Config:
        from_attributes = True


#Rate
class RateBase(BaseModel):
    rating: int
    comment: Optional[str] = None
    customer_id: int
    meal_id: int

    @field_validator("rating")
    def rating_must_be_valid(cls, v):
        if v < 1 or v > 5:
            raise ValueError("Rating must be between 1 and 5")
        return v

class RateCreate(RateBase):
    pass

class RateResponse(RateBase):
    rate_id: int
    class Config:
        from_attributes = True


#Auth
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    github_id: Optional[str] = None