from sqlalchemy import Column, Integer, String, Numeric, Date, Time, ForeignKey, TIMESTAMP, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Category(Base):
    __tablename__ = "category"

    category_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)

    meals = relationship("Meal", back_populates="category")


class Ingredient(Base):
    __tablename__ = "ingredient"

    ing_no = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    amount = Column(Numeric(10, 2), nullable=False)
    unit = Column(String(20), nullable=False)

    meal_ingredients = relationship("MealIngre", back_populates="ingredient")
    supplier_ingredients = relationship("SupplierIngredient", back_populates="ingredient")


class Supplier(Base):
    __tablename__ = "supplier"

    supplier_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False, unique=True)
    address = Column(String(200), nullable=False)
    email = Column(String(100), unique=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    supplier_ingredients = relationship("SupplierIngredient", back_populates="supplier")


class SupplierIngredient(Base):
    __tablename__ = "supplier_ingredient"

    supplier_id = Column(Integer, ForeignKey("supplier.supplier_id"), primary_key=True)
    ing_no = Column(Integer, ForeignKey("ingredient.ing_no"), primary_key=True)

    supplier = relationship("Supplier", back_populates="supplier_ingredients")
    ingredient = relationship("Ingredient", back_populates="supplier_ingredients")


class Tables(Base):
    __tablename__ = "tables"

    table_id = Column(Integer, primary_key=True, index=True)
    capacity = Column(Integer, nullable=False)
    location = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False, default="Available")

    orders = relationship("Order", back_populates="table")
    reservations = relationship("Reservation", back_populates="table")


class Employee(Base):
    __tablename__ = "employee"

    employee_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    role = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=False, unique=True)
    address = Column(String(200), nullable=False)
    salary = Column(Numeric(10, 2), nullable=False)
    hire_date = Column(Date, nullable=False)

    orders = relationship("Order", back_populates="employee")


class Customer(Base):
    __tablename__ = "customer"

    customer_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False, unique=True)
    address = Column(String(200), nullable=False)
    email = Column(String(100), unique=True)
    country = Column(String(100), nullable=False, default="Unknown")
    join_date = Column(Date, server_default=func.now())
    github_id = Column(String(100), unique=True, nullable=True)
    access_token = Column(String(500), nullable=True)

    orders = relationship("Order", back_populates="customer")
    reservations = relationship("Reservation", back_populates="customer")
    ratings = relationship("Rate", back_populates="customer")


class Meal(Base):
    __tablename__ = "meal"

    meal_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    price = Column(Numeric(10, 2), nullable=False)
    time = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey("category.category_id"), nullable=False)

    category = relationship("Category", back_populates="meals")
    meal_ingredients = relationship("MealIngre", back_populates="meal")
    order_items = relationship("OrderItem", back_populates="meal")
    ratings = relationship("Rate", back_populates="meal")


class MealIngre(Base):
    __tablename__ = "meal_ingre"

    meal_id = Column(Integer, ForeignKey("meal.meal_id"), primary_key=True)
    ing_no = Column(Integer, ForeignKey("ingredient.ing_no"), primary_key=True)

    meal = relationship("Meal", back_populates="meal_ingredients")
    ingredient = relationship("Ingredient", back_populates="meal_ingredients")


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, server_default=func.now())
    time = Column(Time, nullable=False)
    tip = Column(Numeric(10, 2), default=0.00)
    customer_id = Column(Integer, ForeignKey("customer.customer_id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employee.employee_id"), nullable=False)
    table_id = Column(Integer, ForeignKey("tables.table_id"), nullable=False)

    customer = relationship("Customer", back_populates="orders")
    employee = relationship("Employee", back_populates="orders")
    table = relationship("Tables", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")
    payment = relationship("Payment", back_populates="order", uselist=False)


class OrderItem(Base):
    __tablename__ = "order_item"

    order_item_id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, nullable=False)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False)
    meal_id = Column(Integer, ForeignKey("meal.meal_id"), nullable=False)

    order = relationship("Order", back_populates="order_items")
    meal = relationship("Meal", back_populates="order_items")


class Payment(Base):
    __tablename__ = "payment"

    payment_id = Column(Integer, primary_key=True, index=True)
    payment_date = Column(Date, nullable=False, server_default=func.now())
    method = Column(String(50), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False, unique=True)

    order = relationship("Order", back_populates="payment")


class Reservation(Base):
    __tablename__ = "reservation"

    reservation_id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    status = Column(String(20), nullable=False, default="Pending")
    customer_id = Column(Integer, ForeignKey("customer.customer_id"), nullable=False)
    table_id = Column(Integer, ForeignKey("tables.table_id"), nullable=False)

    customer = relationship("Customer", back_populates="reservations")
    table = relationship("Tables", back_populates="reservations")


class Rate(Base):
    __tablename__ = "rate"

    rate_id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    customer_id = Column(Integer, ForeignKey("customer.customer_id"), nullable=False)
    meal_id = Column(Integer, ForeignKey("meal.meal_id"), nullable=False)

    customer = relationship("Customer", back_populates="ratings")
    meal = relationship("Meal", back_populates="ratings")