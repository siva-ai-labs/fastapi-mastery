
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Employee
from schemas import EmployeeCreate, EmployeeResponse

app = FastAPI(
    title="SIVA AI LABS - Employee Management API",
    version="1.0.0"
)

# Creates the table if it doesn't exist.
Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "UP"}


# CREATE
@app.post(
    "/employees",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED
)
def create_employee(
    data: EmployeeCreate,
    db: Session = Depends(get_db)
):
    employee = Employee(**data.model_dump())

    db.add(employee)
    db.commit()
    db.refresh(employee)

    return employee


# READ ALL
@app.get(
    "/employees",
    response_model=list[EmployeeResponse]
)
def get_employees(db: Session = Depends(get_db)):
    return db.scalars(
        select(Employee).order_by(Employee.id)
    ).all()


# READ BY ID
@app.get(
    "/employees/{employee_id}",
    response_model=EmployeeResponse
)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = db.get(Employee, employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee


# UPDATE
@app.put(
    "/employees/{employee_id}",
    response_model=EmployeeResponse
)
def update_employee(
    employee_id: int,
    data: EmployeeCreate,
    db: Session = Depends(get_db)
):
    employee = db.get(Employee, employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    employee.name = data.name
    employee.department = data.department
    employee.salary = data.salary

    db.commit()
    db.refresh(employee)

    return employee


# DELETE
@app.delete(
    "/employees/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = db.get(Employee, employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    db.delete(employee)
    db.commit()
    return None
