from sqlalchemy.orm import Session
import models, schemas

def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def get_students(db: Session):
    return db.query(models.Student).all()

def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

def update_student(db: Session, student_id: int, student: schemas.StudentCreate):
    db_student = get_student(db, student_id)
    if db_student:
        for key, value in student.model_dump().items():
            setattr(db_student, key, value)
        db.commit()
        db.refresh(db_student)
    return db_student

# def delete_student(db: Session, student_id: int):
#     db_student = get_student(db, student_id)
#     if db_student:
#         db_student.status = "Inactive"
#         db.commit()
#         db.refresh(db_student)
#     return db_student 

def soft_delete_student(db: Session, student_id: int):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()

    if student:
        student.status = "Inactive"
        db.commit()
        db.refresh(student)

    return student

from sqlalchemy.orm import Session
import models

def get_user_with_role(db: Session, username: str):
    return (
        db.query(models.User, models.Role)
        .join(models.Role, models.User.role_id == models.Role.id)
        .filter(models.User.username == username)
        .first()
    )