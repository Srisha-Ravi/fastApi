from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from fastapi.security import OAuth2PasswordRequestForm
from auth import create_access_token, verify_password
from dependencies import get_current_user,require_role

import models, schemas, crud
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS (for React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create Student
@app.post("/students")
def create_student(
    student: schemas.StudentCreate,
    db: Session = Depends(get_db),
    user = Depends(require_role("admin"))
):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    return crud.create_student(db, student)

# Get All Students
@app.get("/students")
def read_students(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return crud.get_students(db)

# Update Student
@app.put("/students/{student_id}")
def update_student(
    student_id: int,
    student: schemas.StudentCreate,
    db: Session = Depends(get_db),
    user = Depends(require_role("admin"))
):
    return crud.update_student(db, student_id, student)

#softDelete
@app.patch("/students/{student_id}")
def soft_delete(
    student_id: int,
    db: Session = Depends(get_db),
    user = Depends(require_role("admin"))  # ✅ clean
):
    return crud.soft_delete_student(db, student_id)


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    result = crud.get_user_with_role(db, form_data.username)
    if not result:
        raise HTTPException(status_code=401, detail="Invalid username")
    
    user, role = result

    if not verify_password(form_data.password, user.password):  # ✅ bcrypt verify
        raise HTTPException(status_code=401, detail="Invalid password")

    token = create_access_token({"sub": user.username, "role": role.name, "user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}
