from fastapi import APIRouter, Depends
from app.schemas.auth import SignUp, SignIn, TokenResponse
from app.schemas.user import UserBase
from app.services.user import UserService
from app.core.security import authenticate_user
from app.core.dependencies import get_user_service

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=UserBase)
def signup(user: SignUp, service: UserService = Depends(get_user_service)):
    return service.register_user(user)

@router.post("/signin", response_model=TokenResponse)
def signin(user: SignIn, service: UserService = Depends(get_user_service)):
    token = authenticate_user(user, service)
    return {"access_token": token, "token_type": "bearer"}