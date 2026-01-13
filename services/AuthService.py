# Imports
from schemas.AuthSchema import AuthUserRegisterRequest , VerifyEmail , ResendOTP , LoginResponse , AuthLoginRequest , ForgotPasswordRequest , UserResponse
from sqlalchemy.orm import Session
from models.Users import User
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException , status , BackgroundTasks
from utils.bcrypt_util import generate_otp , verify_otp , hash_otp , bcrypt_context
from datetime import timedelta , datetime , timezone
from dependencies.register_verify_email import build_verify_otp_email
from utils.emails import send_email
from dependencies.login_dependency import authenticate_user
from utils.jwt_util import create_jwt_access_token

class AuthService:

    @staticmethod
    def register_user(payload: AuthUserRegisterRequest , backgroundtasks: BackgroundTasks ,db: Session) -> User:
        # Checking whether this user alraedy exists or not
        existing_user = db.query(User).filter(User.email == payload.email).first()
        if existing_user:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail="User already exists with same email"
            )
        
        # Generating otp for email verification
        otp = generate_otp()

        new_user = User(
            name = payload.name,
            email = payload.email,
            profilePic = payload.profilePic,
            phone = payload.phone,
            country = payload.country,
            role = payload.role,
            is_verified = False,
            otp_hash = hash_otp(otp=otp),
            otp_expiry = datetime.now(timezone.utc) + timedelta(minutes=10),
            password = bcrypt_context.hash(payload.password)
        )

        db.add(new_user)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
        
        db.refresh(new_user)

        email_body = build_verify_otp_email(otp= otp,name=new_user.name)

        backgroundtasks.add_task(
            send_email,
            to_email = new_user.email,
            subject = "Please Verify your account✌🏻",
            body= email_body
        )

        return new_user
    
    @staticmethod
    def verify_email(payload: VerifyEmail , db: Session) ->str:
        user = db.query(User).filter(User.email == payload.email).first()
        if not user:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail= "User not found"
            )
        
        # Check whether user is already verified or not
        if user.is_verified:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail="Email already verified"
            )
        
        # check whether otp is expired
        if not user.otp_expiry or user.otp_expiry < datetime.now(timezone.utc):
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail= "OTP expired"
            )
        
        # verify whether otp is right or wrong
        if not verify_otp(plain_otp=payload.otp , hashed_otp=user.otp_hash):
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail="Invalid OTP"
            )
        
        # Now change user to veified
        user.is_verified = True
        user.otp_expiry = None
        user.otp_hash = None

        db.commit()

        return "Email verified successfully!"
    
    @staticmethod
    def resend_verify_email(payload: ResendOTP , backgroundTasks: BackgroundTasks , db: Session) -> str:
        user = db.query(User).filter(User.email == payload.email).first()
        if not user:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND , 
                detail= "User not found"
            )
        
        # Check whether user is already verified email
        if user.is_verified:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail= "Email already verified"
            )
        
        otp = generate_otp()

        user.otp_hash = hash_otp(otp=otp)
        user.otp_expiry = datetime.now(timezone.utc) + timedelta(minutes=10)

        db.commit()
        email_body = build_verify_otp_email(otp= otp,name=user.name)
        backgroundTasks.add_task(
            send_email,
            to_email = user.email,
            subject = "Please Verify your account✌🏻",
            body= email_body
        )

        return "Resend OTP to you email successfully"
    
    @staticmethod
    def login(payload: AuthLoginRequest , db: Session) -> LoginResponse:
        user = authenticate_user(email=payload.email , password=payload.password , db=db)
        if not user:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail= "Invalid credentials / Email not verified"
            )
        token = create_jwt_access_token(user_email=user.email, user_role= user.role, expiry_delta=timedelta(minutes=30))

        return {"token": token , "token_type": "bearer"}
    
    @staticmethod
    def forgot_password(payload: ForgotPasswordRequest , db: Session) -> str:
        user = db.query(User).filter(User.email == payload.email).first()
        if not user:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail= "User not found"
            )
        
        if  payload.new_password != payload.confirm_new_password:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail= "Confirm password and new password are not same. Please enter same password to continue"
            )
        
        user.password = bcrypt_context.hash(payload.new_password)

        db.commit()

        return "Password reset successfully"
    
    @staticmethod
    def get_me(user, db : Session) -> UserResponse:
        current_user = db.query(User).filter(User.email == user["user_email"]).first()
        if not current_user:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail= "User not found"
            )
        return current_user

