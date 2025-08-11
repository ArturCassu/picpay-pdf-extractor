from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated

from app.repository import user_repository
from app.database import get_db
from app.dto.user_login_dto import UserLogin
from app.routes.middleware import get_current_user, create_access_token, User


router = APIRouter(tags=["Users"])

@router.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return {"username": current_user}

@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = user_repository.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        token = create_access_token(data={"sub": user.username})
        return {"access_token": token, "token_type": "bearer"}

@router.post("/register")
async def register_user(user: UserLogin, db: Session = Depends(get_db)):
  """
  Handle user registration.
  """
  db_user = user_repository.create_user(db, user.username, user.password)
  if not db_user:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
  return {"message": "User registered successfully"}