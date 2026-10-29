from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Ingredient
from app.schemas.schemas import IngredientBase, IngredientResponse
from app.routers.auth import get_current_user
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/ingredients", tags=["Ingredients"])

def require_admin(current_user):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to perform this action"
        )

@router.get("/", response_model=List[IngredientResponse])
@limiter.limit("10/minute")
def get_ingredients(request: Request, db: Session = Depends(get_db)):
    return db.query(Ingredient).all()

@router.get("/{ingredient_id}", response_model=IngredientResponse)
@limiter.limit("10/minute")
def get_ingredient(request: Request, ingredient_id: int, db: Session = Depends(get_db)):
    item = db.query(Ingredient).filter(Ingredient.ingredient_id == ingredient_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return item

@router.post("/", response_model=IngredientResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def create_ingredient(
    request: Request,
    item: IngredientBase,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)
    db_item = Ingredient(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{ingredient_id}")
@limiter.limit("5/minute")
def delete_ingredient(
    request: Request,
    ingredient_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)
    item = db.query(Ingredient).filter(Ingredient.ingredient_id == ingredient_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    db.delete(item)
    db.commit()
    return {"message": f"Ingredient {ingredient_id} deleted successfully"}