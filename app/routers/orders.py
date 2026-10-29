from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone
from app.database import get_db
from app.models import Order, OrderItem
from app.schemas.schemas import OrderCreate, OrderResponse, OrderItemCreate, OrderItemResponse
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


@router.get("/", response_model=List[OrderResponse])
@limiter.limit("10/minute")
def get_all_orders(
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Secure Authorization Boundaries: Admins scan everything, clients get their own historical records only
    if current_user.is_admin:
        return db.query(Order).all()
    return db.query(Order).filter(
        Order.customer_id == current_user.customer_id
    ).all()


@router.get("/{order_id}", response_model=OrderResponse)
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
    return order


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
def create_order(
    request: Request,
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    
    now = datetime.now(timezone.utc)
    
    new_order = Order(
        date=now.date(),
        time=now.time(),
        tip=order.tip,
        customer_id=current_user.customer_id,  
        employee_id=order.employee_id,
        table_id=order.table_id
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


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
    db.add(new_item)
    db.commit()
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