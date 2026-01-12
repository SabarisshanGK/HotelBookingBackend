# Imports
from sqlalchemy import Column , Integer , String , ForeignKey , Date , Numeric , UniqueConstraint
from database import Base
from sqlalchemy.orm import relationship

# Definition
class RoomAvailability(Base):
    __tablename__="room_availability"
    __table_args__ = (
        UniqueConstraint("room_type_id", "date", name="uq_room_type_date"),
    )
    id = Column(Integer , primary_key= True, index=True)
    room_type_id = Column(Integer , ForeignKey("room_types.id",ondelete="CASCADE"))
    date = Column(Date,nullable=False)
    price_override = Column(Numeric(10,2))
    available_rooms = Column(Integer, nullable=False, default=1, server_default="1")

    room_type = relationship("RoomType",back_populates="room_availabilities")