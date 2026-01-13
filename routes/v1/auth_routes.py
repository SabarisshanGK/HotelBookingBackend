# Imports
from fastapi import Depends , APIRouter , BackgroundTasks
from database import get_db
from utils.jwt_util import create_jwt_access_token  , verify_token
from services.AuthService import AuthService
from schemas.AuthSchema import AuthLoginRequest, AuthUserRegisterRequest , RegisterUserResponse , UserResponse , LoginResponse , VerifyEmail , ResendOTP , ForgotPasswordRequest
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

# Resend otp 
# Method: POST
@router.post("/resend-otp")
def resend_email_verification_otp( resendOTPRequest: ResendOTP , backgroundTasks: BackgroundTasks , db: Session = Depends(get_db) ):
    message = AuthService.resend_verify_email(payload=resendOTPRequest , backgroundTasks=backgroundTasks , db=db)
    return {"message": message}

# Login User
# Method: POST
@router.post('/login' , response_model= LoginResponse)
def login_user( loginRequest: AuthLoginRequest , db: Session = Depends(get_db)):
    return AuthService.login(payload=loginRequest, db=db)
    
# Forgot Password
# Method: PATCH
@router.patch('/reset-password')
def reset_password(resetPassword: ForgotPasswordRequest, db: Session = Depends(get_db)):
    message = AuthService.forgot_password(payload=resetPassword , db=db)
    return {"message": message}

# Get current user
# Method: GET
@router.get("/me", response_model=UserResponse)
def get_details_of_me(user = Depends(verify_token) , db: Session = Depends(get_db)):
    return AuthService.get_me(user=user , db=db)