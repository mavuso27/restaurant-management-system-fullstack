from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Rate
from app.schemas.schemas import RateCreate, RateResponse

router = APIRouter()

@router.get("/", response_model=List[RateResponse])
def get_rates(db: Session = Depends(get_db)):
    return db.query(Rate).all()

@router.post("/", response_model=RateResponse, status_code=status.HTTP_201_CREATED)
def create_rate(rate: RateCreate, db: Session = Depends(get_db)):
    db_rate = Rate(**rate.dict())
    db.add(db_rate)
    db.commit()
    db.refresh(db_rate)
    return db_rate