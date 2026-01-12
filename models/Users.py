# Imports
from sqlalchemy import Column , String , Integer , Boolean  , Enum , DateTime 
from database import Base
from enums.UserRoleEnum import UserRole
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer , primary_key = True , index=True)
    name = Column(String , nullable= False)
    email = Column(String , nullable= False , unique=True , index=True)
    password = Column(String , nullable=False)
    profilePic = Column(String)
    phone = Column(String,nullable=False)
    country = Column(String, nullable=False)
    role = Column(Enum(UserRole) , nullable=False, default=UserRole.CUSTOMER)
    is_verified = Column(Boolean , nullable= False , default=False)
    otp_hash = Column(String, nullable=True)
    otp_expiry = Column(DateTime(timezone=True), nullable=True)
    createdAt = Column(DateTime(timezone=True) , server_default=func.now(), nullable=False)
    updatedAt = Column(DateTime(timezone=True),server_default=func.now(), onupdate=func.now(), nullable=False)

    hotels = relationship("Hotel", back_populates="owner" ,  cascade="all, delete-orphan")
    bookings = relationship("Booking" , back_populates="user" , cascade="all, delete-orphan")
    reviews = relationship("Review" , back_populates="user")