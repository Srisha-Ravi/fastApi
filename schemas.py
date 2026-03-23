from pydantic import BaseModel, EmailStr, Field
from datetime import date

class StudentBase(BaseModel):
    name: str = Field(..., min_length=3)
    email: EmailStr
    department: str
    year: int = Field(..., ge=1, le=4)
    date_of_birth: date
    phone_no: str = Field(..., min_length=10, max_length=15)
    address: str
    city: str
    gender: str = Field(..., pattern="^(Male|Female|Other)$")

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int
    status: str

    class Config:
        from_attributes = True   # (for SQLAlchemy ORM)