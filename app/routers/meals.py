from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.models import Meal, Category
from app.schemas.schemas import MealCreate, MealResponse
from app.routers.auth import get_current_user
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/meals", tags=["Meals"])



def require_admin(current_user):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to perform this action"
        )



@router.get("/", response_model=List[MealResponse])
def get_all_meals(db: Session = Depends(get_db)):
    return db.query(Meal).all()


@router.get("/category/{category_id}", response_model=List[MealResponse])
def get_meals_by_category(category_id: int, db: Session = Depends(get_db)):
    meals = db.query(Meal).filter(Meal.category_id == category_id).all()
    if not meals:
        raise HTTPException(status_code=404, detail="No meals found for this category")
    return meals


@router.get("/{meal_id}", response_model=MealResponse)
def get_meal(meal_id: int, db: Session = Depends(get_db)):
    meal = db.query(Meal).filter(Meal.meal_id == meal_id).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    return meal




@router.post("/", response_model=MealResponse)
@limiter.limit("5/minute")
def create_meal(
    request: Request,
    meal: MealCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    
    require_admin(current_user)

    category = db.query(Category).filter(
        Category.category_id == meal.category_id
    ).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    existing = db.query(Meal).filter(Meal.name == meal.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Meal already exists")

    
    new_meal = Meal(
        name=meal.name,
        price=meal.price,
        time=meal.time,
        category_id=meal.category_id
    )
    db.add(new_meal)
    db.commit()
    db.refresh(new_meal)
    return new_meal


@router.delete("/{meal_id}")
@limiter.limit("5/minute")
def delete_meal(
    request: Request,  
    meal_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    
    require_admin(current_user)

    meal = db.query(Meal).filter(Meal.meal_id == meal_id).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")

    db.delete(meal)
    db.commit()
    return {"message": f"Meal {meal_id} deleted successfully"}