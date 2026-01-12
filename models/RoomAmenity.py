# Imports
from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

# Definition
class RoomAmenity(Base):
    __tablename__="room_amenities"
    id = Column(Integer , primary_key=True, index=True)
    room_type_id = Column(Integer , ForeignKey("room_types.id"))
    amenity_id = Column(Integer, ForeignKey("amenities.id"))

    room_type = relationship("RoomType",back_populates="room_amenity")