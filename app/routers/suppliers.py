from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Supplier
from app.schemas.schemas import SupplierBase, SupplierResponse
from app.routers.auth import get_current_user

router = APIRouter(
    prefix="/suppliers",
    tags=["Suppliers"],
    dependencies=[Depends(get_current_user)]
)

@router.get("/", response_model=List[SupplierResponse])
def get_suppliers(db: Session = Depends(get_db)):
    return db.query(Supplier).all()

@router.post("/", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED)
def create_supplier(supplier: SupplierBase, db: Session = Depends(get_db)):
    db_sup = Supplier(**supplier.dict())
    db.add(db_sup)
    db.commit()
    db.refresh(db_sup)
    return db_sup