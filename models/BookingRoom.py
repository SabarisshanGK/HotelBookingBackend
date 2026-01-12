# Imports
from sqlalchemy import Column , Integer , ForeignKey , Numeric
from database import Base
from sqlalchemy.orm import relationship

# Definition
class BookingRoom(Base):
    __tablename__="booking_rooms"
    id = Column(Integer , primary_key=True, index=True)
    booking_id = Column(Integer , ForeignKey("bookings.id"))
    room_type_id = Column(Integer , ForeignKey("room_types.id",ondelete="CASCADE"))
    quantity = Column(Integer , nullable=False, default=1)
    price_per_night = Column(Numeric(10,2) , nullable=False)

    room_type = relationship("RoomType",back_populates="booking_room")
    booking = relationship("Booking",back_populates="booking_rooms")