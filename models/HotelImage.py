# Imports
from sqlalchemy import Column , Integer , Text , ForeignKey , Boolean , text
from database import Base

class HotelImage(Base):
    __tablename__="hotel_images"
    id = Column(Integer , primary_key=True , index=True)
    hotel_id = Column(Integer , ForeignKey("hotels.id"))
    image_url = Column(Text , nullable=False)
    is_primary = Column(Boolean , nullable=False , default=False , server_default=text("false"))
    