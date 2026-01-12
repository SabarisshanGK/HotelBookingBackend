# Imports
from sqlalchemy import Column , Integer , String , ForeignKey , Date , Enum , Numeric , DateTime
from database import Base
from enums.BookingStatusEnum import BookingStatus
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

# Definition
class Booking(Base):
    __tablename__="bookings"
    id = Column(Integer , primary_key=True , index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    hotel_id = Column(Integer , ForeignKey("hotels.id"))
    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)
    status = Column(Enum(BookingStatus) , nullable=False, default=BookingStatus.PENDING)
    total_amount = Column(Numeric(10,2),nullable=False)
    createdAt = Column(DateTime(timezone=True) , server_default=func.now(), nullable=False)

    user = relationship("User",back_populates="bookings")
    hotel = relationship("Hotel",back_populates="bookings")
    booking_rooms = relationship("BookingRoom",back_populates="booking",cascade="all, delete-orphan")
    payments = relationship("Payment",back_populates="booking")