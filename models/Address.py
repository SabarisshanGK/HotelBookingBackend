# Imports
from sqlalchemy import Column , String , Integer , Numeric
from database import Base

class Address(Base):
    __tablename__="addresses"
    id = Column(Integer , primary_key=True , index=True)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    line_one = Column(String, nullable=False)
    line_two = Column(String , nullable=False)
    country = Column(String, nullable=False)
    pincode = Column(String, nullable=False)
    latitude = Column(Numeric(10,7) , nullable=False)
    longitude = Column(Numeric(10,7) , nullable=False)