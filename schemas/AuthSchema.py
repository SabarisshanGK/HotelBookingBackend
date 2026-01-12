# Imports
from pydantic import BaseModel ,EmailStr
from typing import Optional
from datetime import datetime
from enums.UserRoleEnum import UserRole

class AuthBase(BaseModel):
    name: str
    email: EmailStr
    password: str
    profilePic: Optional[str] = None
    phone: str 
    country: str
    role: Optional[UserRole] = UserRole.CUSTOMER
    is_verified: Optional[bool] = False
    otp_hash: Optional[str] = None
    otp_expiry: Optional[datetime] = None

class AuthUserRegisterRequest(AuthBase):
    pass

class VerifyEmail(BaseModel):
    email: EmailStr
    otp: str

class ResendOTP(BaseModel):
    email: EmailStr

class AuthLoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    profilePic: str
    phone: str
    country: str
    role: UserRole
    is_verified: bool
    createdAt: datetime
    updatedAt: datetime
    class Config:
        from_attributes = True 

class RegisterUserResponse(BaseModel):
    id: int
    name: str
    email: str
    profilePic: str
    phone: str
    country: str
    role: UserRole
    is_verified: bool
    createdAt: datetime
    updatedAt: datetime
    message: str
    class Config:
        from_attributes = True 