# Imports
from schemas.AuthSchema import AuthUserRegisterRequest , VerifyEmail
from sqlalchemy.orm import Session
from models.Users import User
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException , status , BackgroundTasks
from utils.bcrypt_util import generate_otp , verify_otp , hash_otp , bcrypt_context
from datetime import timedelta , datetime , timezone
from dependencies.register_verify_email import build_verify_otp_email
from utils.emails import send_email

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