from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Rate
from app.schemas.schemas import RateCreate, RateResponse
from app.routers.auth import get_current_user
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/rates", tags=["Rates"])

def require_admin(current_user):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to perform this action"
        )

@router.get("/", response_model=List[RateResponse])
@limiter.limit("10/minute")
def get_rates(request: Request, db: Session = Depends(get_db)):
    return db.query(Rate).all()

@router.get("/{rate_id}", response_model=RateResponse)
@limiter.limit("10/minute")
def get_rate(request: Request, rate_id: int, db: Session = Depends(get_db)):
    rate = db.query(Rate).filter(Rate.rate_id == rate_id).first()
    if not rate:
        raise HTTPException(status_code=404, detail="Rate not found")
    return rate

@router.post("/", response_model=RateResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def create_rate(
    request: Request,
    rate: RateCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)
    db_rate = Rate(**rate.dict())
    db.add(db_rate)
    db.commit()
    db.refresh(db_rate)
    return db_rate

@router.delete("/{rate_id}")
@limiter.limit("5/minute")
def delete_rate(
    request: Request,
    rate_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)
    rate = db.query(Rate).filter(Rate.rate_id == rate_id).first()
    if not rate:
        raise HTTPException(status_code=404, detail="Rate not found")
    db.delete(rate)
    db.commit()
    return {"message": f"Rate {rate_id} deleted successfully"}