from app.repositories.user import UserRepository
from app.models.user import User
from app.schemas.auth import SignUp
from app.core.security import hash_password
from app.schemas.exception import AppException

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def get_user_by_id(self, user_id: int):
        return self.repo.get_user_by_id(user_id)

    def get_user_by_email(self, email: str):
        return self.repo.get_user_by_email(email)
    
    def register_user(self, user: SignUp):
        if(user.password != user.password_confirm):
            raise AppException(status_code=400, detail="Passwords do not match")
        
        if(self.get_user_by_email(user.email)):
            raise AppException(status_code=409, detail=f"User with email {user.email} already exists")
        
        new_user = User(
            name = user.name,
            email = user.email,
            password = hash_password(user.password),
            is_active = True
        )

        return self.repo.register_user(new_user)
    
    def update_user(self, user_id: int, user_update):
        user_db = self.get_user_by_id(user_id)

        for key, value in user_update.dict(exclude_none=True).items():
            if key == "password" and value:
                value = hash_password(value)

            setattr(user_db, key, value)

        return self.repo.update_user(user_db)

    def delete_user(self, user_id: int):
        user_delete = self.get_user_by_id(user_id)
        return self.repo.delete_user(user_delete)