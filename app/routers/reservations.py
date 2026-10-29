from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Reservation
from app.schemas.schemas import ReservationCreate, ReservationResponse
from app.routers.auth import get_current_user
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/reservations", tags=["Reservations"])

def require_admin(current_user):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to perform this action"
        )

@router.get("/", response_model=List[ReservationResponse])
@limiter.limit("10/minute")
def get_reservations(request: Request, db: Session = Depends(get_db)):
    return db.query(Reservation).all()

@router.get("/{reservation_id}", response_model=ReservationResponse)
@limiter.limit("10/minute")
def get_reservation(request: Request, reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(Reservation).filter(Reservation.reservation_id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation

@router.post("/", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def create_reservation(
    request: Request,
    reservation: ReservationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)
    db_res = Reservation(**reservation.dict())
    db.add(db_res)
    db.commit()
    db.refresh(db_res)
    return db_res

@router.delete("/{reservation_id}")
@limiter.limit("5/minute")
def delete_reservation(
    request: Request,
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)
    reservation = db.query(Reservation).filter(Reservation.reservation_id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    db.delete(reservation)
    db.commit()
    return {"message": f"Reservation {reservation_id} deleted successfully"}