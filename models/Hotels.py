# Imports
from sqlalchemy import Column , String , Integer , Boolean , Enum , DateTime , CheckConstraint , Time ,Text , ForeignKey
from database import Base
from enums.HotelStatusEnum import HotelStatus
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Hotel(Base):
    __tablename__ = "hotels"
    id = Column(Integer , primary_key=True , index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String , nullable=False)
    description = Column(Text)
    city = Column(String)
    status = Column(Enum(HotelStatus) , nullable=False, default= HotelStatus.PENDING)
    star_rating = Column(Integer , nullable= False , default=3, server_default="3")
    check_in_time = Column(Time)
    check_out_time = Column(Time)
    address_id = Column(Integer , ForeignKey("addresses.id"),unique=True)
    createdAt = Column(DateTime(timezone=True) , server_default=func.now(), nullable=False)
    updatedAt = Column(DateTime(timezone=True),server_default=func.now(), onupdate=func.now(), nullable=False)

    owner = relationship("User", back_populates="hotels")
    address = relationship("Address", uselist=False )
    roomtypes = relationship("RoomType" , back_populates="hotel", cascade="all, delete-orphan")
    hotel_images = relationship("HotelImage", cascade="all, delete-orphan")
    bookings = relationship("Booking",back_populates="hotel",cascade="all, delete-orphan")
    hotel_reviews = relationship("Review",back_populates="hotel", cascade="all, delete-orphan" )

    __table_args__ = (
        CheckConstraint(
            "star_rating >= 1 AND star_rating <= 5",
            name="check_star_rating_range"
        ),
    )