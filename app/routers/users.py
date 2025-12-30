from fastapi import APIRouter, Depends
from app.schemas.user import UserBase, UserUpdate
from app.services.user import UserService
from app.core.dependencies import get_user_service, get_current_user

router = APIRouter(prefix="/users", tags=["User"])

@router.get("/me", response_model=UserBase)
def get_user(current_user: UserBase = Depends(get_current_user), service: UserService = Depends(get_user_service)):
    return service.get_user_by_id(current_user.id)

@router.put("/me", response_model=UserBase)
def update_user(user_update: UserUpdate, current_user: UserBase = Depends(get_current_user), service : UserService = Depends(get_user_service)):
    return service.update_user(current_user.id, user_update)

@router.delete("/me")
def delete_user(current_user: UserBase = Depends(get_current_user), service: UserService = Depends(get_user_service)):
    return service.delete_user(current_user.id)