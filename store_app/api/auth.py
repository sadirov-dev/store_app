from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from store_app.database.db import get_db
from store_app.database.schemas import TokenResponse, UserLogin, UserRegister, UserResponse
from store_app.api.dependencies import get_current_user
from store_app.services.auth_service import authenticate_user, create_access_token, register_user


router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    return register_user(db, user_data)


@router.post("/login", response_model=TokenResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_data.email, user_data.password)
    token = create_access_token(user)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def me(current_user=Depends(get_current_user)):
    return current_user
