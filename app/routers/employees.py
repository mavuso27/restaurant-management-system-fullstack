from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Employee
from app.schemas.schemas import EmployeeBase, EmployeeResponse
from app.routers.auth import get_current_user
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/employees", tags=["Employees"])

def require_admin(current_user):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to perform this action"
        )

@router.get("/", response_model=List[EmployeeResponse])
@limiter.limit("10/minute")
def get_employees(request: Request, db: Session = Depends(get_db)):
    return db.query(Employee).all()

@router.get("/{employee_id}", response_model=EmployeeResponse)
@limiter.limit("10/minute")
def get_employee(request: Request, employee_id: int, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

@router.post("/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def create_employee(
    request: Request,
    employee: EmployeeBase,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)
    db_emp = Employee(**employee.dict())
    db.add(db_emp)
    db.commit()
    db.refresh(db_emp)
    return db_emp

@router.delete("/{employee_id}")
@limiter.limit("5/minute")
def delete_employee(
    request: Request,
    employee_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)
    emp = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(emp)
    db.commit()
    return {"message": f"Employee {employee_id} deleted successfully"}