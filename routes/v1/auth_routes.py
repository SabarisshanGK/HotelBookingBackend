# Imports
from fastapi import Depends , APIRouter , BackgroundTasks
from database import get_db
from utils.jwt_util import create_jwt_access_token
from services.AuthService import AuthService
from schemas.AuthSchema import AuthLoginRequest, AuthUserRegisterRequest , RegisterUserResponse , UserResponse , LoginResponse , VerifyEmail
from sqlalchemy.orm import Session


router = APIRouter(prefix="/auth")

# Register User to our website 
# Method: POST
@router.post('/register', response_model=RegisterUserResponse)
def register_user(create_user: AuthUserRegisterRequest , backgroundtasks: BackgroundTasks , db: Session = Depends(get_db)):
    user = AuthService.register_user(payload=create_user , backgroundtasks= backgroundtasks, db= db)
    return {**user.__dict__ , "message": "User registered successfully. An verification email is sent please verify your account"}
 

#  Verify Email
# Method: POST
@router.post("/verify-email")
def verify_email_address( verifyRequest : VerifyEmail , db: Session = Depends(get_db)):
    message = AuthService.verify_email(payload=verifyRequest , db=db)
    return { "message": message}
    
    