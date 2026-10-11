from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.models import Customer
from app.schemas.schemas import CustomerCreate, CustomerResponse
from app.routers.auth import get_current_user
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/customers", tags=["Customers"])


# ─── HELPER: Admin check ────────────────────────────────
def require_admin(current_user):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to perform this action"
        )


# ─── 1. STATIC CONSUMER ENDPOINTS (Must go first!) ──────

@router.get("/me", response_model=CustomerResponse)
@limiter.limit("20/minute")
def get_my_profile(
    request: Request, 
    current_user=Depends(get_current_user)
):
    
    return current_user




@router.get("/{customer_id}", response_model=CustomerResponse)
@limiter.limit("10/minute")
def get_customer(
    request: Request, 
    customer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    
    if not current_user.is_admin and current_user.customer_id != customer_id:
        raise HTTPException(
            status_code=403,
            detail="You can only view your own profile"
        )
        
    customer = db.query(Customer).filter(
        Customer.customer_id == customer_id
    ).first()
    
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer




@router.get("/", response_model=List[CustomerResponse])
@limiter.limit("5/minute") 
def get_all_customers(
    request: Request, 
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    
    require_admin(current_user)
    return db.query(Customer).all()


@router.delete("/{customer_id}")
@limiter.limit("5/minute")
def delete_customer(
    request: Request, 
    customer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    
    require_admin(current_user)
    
    customer = db.query(Customer).filter(
        Customer.customer_id == customer_id
    ).first()
    
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
        
    db.delete(customer)
    db.commit()
    return {"message": f"Customer {customer_id} deleted successfully"}