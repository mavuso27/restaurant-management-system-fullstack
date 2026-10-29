from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Table
from app.schemas import TableBase, TableResponse

router = APIRouter()

@router.get("/", response_model=List[TableResponse])
def get_tables(db: Session = Depends(get_db)):
    return db.query(Table).all()

@router.post("/", response_model=TableResponse, status_code=status.HTTP_201_CREATED)
def create_table(table: TableBase, db: Session = Depends(get_db)):
    db_table = Table(**table.dict())
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table