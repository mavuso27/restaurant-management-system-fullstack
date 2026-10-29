from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Tables
from app.schemas.schemas import TableBase, TableResponse
from app.routers.auth import get_current_user
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/tables", tags=["Tables"])

def require_admin(current_user):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to perform this action"
        )

@router.get("/", response_model=List[TableResponse])
@limiter.limit("10/minute")
def get_tables(request: Request, db: Session = Depends(get_db)):
    return db.query(Tables).all()

@router.get("/{table_id}", response_model=TableResponse)
@limiter.limit("10/minute")
def get_table(request: Request, table_id: int, db: Session = Depends(get_db)):
    table = db.query(Tables).filter(Tables.table_id == table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    return table

@router.post("/", response_model=TableResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def create_table(
    request: Request,
    table: TableBase,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)
    db_table = Tables(**table.dict())
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table

@router.delete("/{table_id}")
@limiter.limit("5/minute")
def delete_table(
    request: Request,
    table_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)
    table = db.query(Tables).filter(Tables.table_id == table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    db.delete(table)
    db.commit()
    return {"message": f"Table {table_id} deleted successfully"}