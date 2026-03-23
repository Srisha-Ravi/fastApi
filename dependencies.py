from fastapi import Depends, HTTPException
from auth import decode_token
from security import oauth2_scheme
from database import SessionLocal


def get_current_user(token: str = Depends(oauth2_scheme)):

    payload = decode_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()