from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Ingredient
from app.schemas.schemas import IngredientBase, IngredientResponse
from app.routers.auth import get_current_user

router = APIRouter(
    prefix="/ingredients",
    tags=["Ingredients"],
    dependencies=[Depends(get_current_user)]
)

@router.get("/", response_model=List[IngredientResponse])
def get_ingredients(db: Session = Depends(get_db)):
    return db.query(Ingredient).all()

@router.post("/", response_model=IngredientResponse, status_code=status.HTTP_201_CREATED)
def create_ingredient(item: IngredientBase, db: Session = Depends(get_db)):
    db_item = Ingredient(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item