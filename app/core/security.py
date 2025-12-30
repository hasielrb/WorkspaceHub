from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from datetime import datetime, timedelta
import jwt
from app.schemas.auth import SignIn
from app.schemas.exception import AppException
from app.core.config import settings

oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/signin")
pwd_hasher = PasswordHash.recommended()

#  [ AUTH ]

def authenticate_user(user: SignIn, service):
    user_db = service.get_user_by_email(user.email)

    if not user_db:
        raise AppException(status_code=401, detail="Invalid credentials")
    if not user_db.is_active:
        raise AppException(status_code=403, detail="Inactive user")
    if not verify_password_hash(user.password, str(user_db.password)):
        raise AppException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(user_db.id)

    return access_token

#  [ JWT ]

def jwt_encode(access_token: dict) -> str:
    return jwt.encode(access_token, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def jwt_decode(token: str) -> dict:
    try:
        jwt_data = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise AppException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise AppException(status_code=401, detail="Invalid token")
    
    return jwt_data

#  [ ACCESS TOKEN ]

def create_access_token(user_id: int) -> str:
    exp = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXP_MIN)
    access_token = {"sub": str(user_id), "exp": exp}
    return jwt_encode(access_token)

#  [ PASSWORD HASHER ]

def hash_password(plain_password: str) -> str:
    return pwd_hasher.hash(plain_password)

def verify_password_hash(plain_password: str, password_hash: str) -> bool:
    return pwd_hasher.verify(plain_password, password_hash)
