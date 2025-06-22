# Auth/routes.py
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from uuid import uuid4
from models import User
from Auth.schemas import RegisterUser, LoginUser
from Auth.auth_utils import hash_password, verify_password, create_access_token
from Database.db_session import get_db

auth_router = APIRouter()

@auth_router.post("/register")
def register(user_data: RegisterUser, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter_by(email=user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(user_data.password)
    user = User(id=str(uuid4()), email=user_data.email, password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "Registered successfully"}


@auth_router.post("/login")
def login(user_data: LoginUser, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=user_data.email).first()
    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.id})
    return {"access_token": token, "token_type": "bearer"}
