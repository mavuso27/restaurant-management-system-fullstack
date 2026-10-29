from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Supplier
from app.schemas.schemas import SupplierBase, SupplierResponse
from app.routers.auth import get_current_user
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/suppliers", tags=["Suppliers"])

def require_admin(current_user):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to perform this action"
        )

@router.get("/", response_model=List[SupplierResponse])
@limiter.limit("10/minute")
def get_suppliers(request: Request, db: Session = Depends(get_db)):
    return db.query(Supplier).all()

@router.get("/{supplier_id}", response_model=SupplierResponse)
@limiter.limit("10/minute")
def get_supplier(request: Request, supplier_id: int, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier

@router.post("/", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def create_supplier(
    request: Request,
    supplier: SupplierBase,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)
    db_sup = Supplier(**supplier.dict())
    db.add(db_sup)
    db.commit()
    db.refresh(db_sup)
    return db_sup

@router.delete("/{supplier_id}")
@limiter.limit("5/minute")
def delete_supplier(
    request: Request,
    supplier_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)
    supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    db.delete(supplier)
    db.commit()
    return {"message": f"Supplier {supplier_id} deleted successfully"}