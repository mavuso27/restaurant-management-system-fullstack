from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Payment
from app.schemas.schemas import PaymentCreate, PaymentResponse
from app.routers.auth import get_current_user
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/payments", tags=["Payments"])

def require_admin(current_user):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to perform this action"
        )

@router.get("/", response_model=List[PaymentResponse])
@limiter.limit("10/minute")
def get_payments(request: Request, db: Session = Depends(get_db)):
    return db.query(Payment).all()

@router.get("/{payment_id}", response_model=PaymentResponse)
@limiter.limit("10/minute")
def get_payment(request: Request, payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def create_payment(
    request: Request,
    payment: PaymentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)
    db_payment = Payment(**payment.dict())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

@router.delete("/{payment_id}")
@limiter.limit("5/minute")
def delete_payment(
    request: Request,
    payment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)
    payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    db.delete(payment)
    db.commit()
    return {"message": f"Payment {payment_id} deleted successfully"}