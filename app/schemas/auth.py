from pydantic import BaseModel, EmailStr

class SignUp(BaseModel):
    name: str
    email: EmailStr
    password: str
    password_confirm: str

class SignIn(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str