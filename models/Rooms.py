# Import
from sqlalchemy import Column , Integer , String , ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class Room(Base):
    __tablename__="rooms"
    id = Column(Integer , primary_key=True , index=True)
    room_type_id = Column(Integer , ForeignKey("room_types.id"))
    room_number = Column(String(100),nullable=False)
    floor = Column(Integer)

    room_type = relationship("RoomType",back_populates="rooms")