from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import List
from decimal import Decimal
from datetime import datetime, timezone
from app.database import get_db
from app.models import Order, OrderItem, Meal, Category, Employee
from app.schemas.schemas import (
    OrderItemCreate, OrderItemResponse,
    OrderPlaceRequest, OrderDetail, OrderLine, TipUpdate,
)
from app.routers.auth import get_current_user
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/orders", tags=["Orders"])


def require_admin(current_user):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to perform this action"
        )


def build_order_detail(order, db: Session) -> OrderDetail:
    rows = (
        db.query(OrderItem, Meal, Category)
        .join(Meal, OrderItem.meal_id == Meal.meal_id)
        .join(Category, Meal.category_id == Category.category_id)
        .filter(OrderItem.order_id == order.order_id)
        .all()
    )

    lines = []
    subtotal = Decimal("0.00")
    for item, meal, category in rows:
        price = Decimal(str(meal.price))
        line_total = price * item.quantity
        subtotal += line_total
        lines.append(OrderLine(
            order_item_id=item.order_item_id,
            meal_id=meal.meal_id,
            meal_name=meal.name,
            category=category.name,
            unit_price=price,
            quantity=item.quantity,
            line_total=line_total,
        ))

    tip = Decimal(str(order.tip or 0))
    return OrderDetail(
        order_id=order.order_id,
        date=order.date,
        time=order.time,
        customer_id=order.customer_id,
        table_id=order.table_id,
        items=lines,
        subtotal=subtotal,
        tip=tip,
        total=subtotal + tip,
    )


@router.get("/", response_model=List[OrderDetail])
@limiter.limit("10/minute")
def get_all_orders(
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    query = db.query(Order)
    if not current_user.is_admin:
        query = query.filter(Order.customer_id == current_user.customer_id)
    orders = query.order_by(Order.order_id.desc()).all()
    return [build_order_detail(o, db) for o in orders]


@router.get("/{order_id}", response_model=OrderDetail)
@limiter.limit("10/minute")
def get_order(
    request: Request,
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if not current_user.is_admin and order.customer_id != current_user.customer_id:
        raise HTTPException(
            status_code=403,
            detail="You can only view your own orders"
        )

    return build_order_detail(order, db)


@router.post("/", response_model=OrderDetail, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
def create_order(
    request: Request,
    order: OrderPlaceRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    waiter = (
        db.query(Employee)
        .filter(Employee.role.in_(["Waiter", "Waitress"]))
        .order_by(func.random())
        .first()
    )
    if not waiter:
        raise HTTPException(status_code=503, detail="No waiter available right now")

    now = datetime.now(timezone.utc)
    new_order = Order(
        date=now.date(),
        time=now.time().replace(microsecond=0),
        tip=order.tip,
        customer_id=current_user.customer_id,
        employee_id=waiter.employee_id,
        table_id=order.table_id,
    )

    try:
        db.add(new_order)
        db.flush()
        for item in order.items:
            db.add(OrderItem(
                quantity=item.quantity,
                order_id=new_order.order_id,
                meal_id=item.meal_id,
            ))
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid table_id or meal_id")

    db.refresh(new_order)
    return build_order_detail(new_order, db)


@router.patch("/{order_id}/tip", response_model=OrderDetail)
@limiter.limit("10/minute")
def update_tip(
    request: Request,
    order_id: int,
    body: TipUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.customer_id != current_user.customer_id:
        raise HTTPException(
            status_code=403,
            detail="You can only tip on your own orders"
        )

    order.tip = body.tip
    db.commit()
    db.refresh(order)
    return build_order_detail(order, db)


@router.post("/items", response_model=OrderItemResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
def add_order_item(
    request: Request,
    item: OrderItemCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    order = db.query(Order).filter(Order.order_id == item.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if not current_user.is_admin and order.customer_id != current_user.customer_id:
        raise HTTPException(
            status_code=403,
            detail="You can only modify your own orders"
        )

    new_item = OrderItem(
        quantity=item.quantity,
        order_id=item.order_id,
        meal_id=item.meal_id
    )
    try:
        db.add(new_item)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid meal_id")

    db.refresh(new_item)
    return new_item


@router.delete("/{order_id}")
@limiter.limit("5/minute")
def delete_order(
    request: Request,
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)

    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(order)
    db.commit()
    return {"message": f"Order {order_id} deleted successfully"}