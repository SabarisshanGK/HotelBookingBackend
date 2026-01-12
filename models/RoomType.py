# Imports
from sqlalchemy import Column , Text , String , Integer , ForeignKey , Numeric
from database import Base
from sqlalchemy.orm import relationship

class RoomType(Base):
    __tablename__="room_types"
    id =Column(Integer , primary_key=True , index=True)
    hotel_id = Column(Integer , ForeignKey("hotels.id"))
    name = Column(String(100) , nullable=False)
    capacity = Column(Integer , nullable=False , default=1, server_default="1")
    base_price = Column(Numeric(10,2), nullable=False , default=100.00 , server_default="100.00")
    description = Column(Text)

    hotel = relationship("Hotel",back_populates="roomtypes")
    rooms = relationship("Room",back_populates="room_type",cascade="all, delete-orphan" )
    room_availabilities = relationship("RoomAvailability",back_populates="",cascade="all, delete-orphan")
    booking_room = relationship("BookingRoom",back_populates="room_type",cascade="all, delete-orphan")
    room_amenity = relationship("RoomAmenity",back_populates="room_type",cascade="all, delete-orphan")