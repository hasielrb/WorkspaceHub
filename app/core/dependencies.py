from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core.security import oauth2, jwt_decode
from app.services.user import UserService
from app.repositories.user import UserRepository
from app.schemas.user import UserBase
from app.schemas.exception import AppException

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency to get UserRepository and UserService
def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

def get_user_service(repo: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repo)

# Dependency to get current user
def get_current_user(token: str = Depends(oauth2), service: UserService = Depends(get_user_service)) -> UserBase:
    jwt_data = jwt_decode(token)
    user_id = jwt_data.get("sub")

    if not user_id:
        raise AppException(status_code=401, detail="Could not validate credentials")
    
    user = service.get_user_by_id(int(user_id))
    
    if not user:
        raise AppException(status_code=401, detail="Could not validate credentials")
    
    return user
