from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Tables
from app.schemas.schemas import TableBase, TableResponse
from app.routers.auth import get_current_user

router = APIRouter(
    prefix="/tables",
    tags=["Tables"],
    dependencies=[Depends(get_current_user)]
)

@router.get("/", response_model=List[TableResponse])
def get_tables(db: Session = Depends(get_db)):
    return db.query(Tables).all()

@router.post("/", response_model=TableResponse, status_code=status.HTTP_201_CREATED)
def create_table(table: TableBase, db: Session = Depends(get_db)):
    db_table = Tables(**table.dict())
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table