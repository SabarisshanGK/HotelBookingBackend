# Imports
from sqlalchemy import Column , Integer , ForeignKey , Numeric , DateTime , String
from database import Base
from sqlalchemy.orm import relationship

# Definition
class Payment(Base):
    __tablename__="payments"
    id = Column(Integer , primary_key=True , index=True)
    booking_id = Column(Integer , ForeignKey("bookings.id"),nullable=False)
    amount = Column(Numeric(10,2),nullable=False)
    payment_method = Column(String(50))
    payment_status = Column(String(20))
    transaction_id = Column(String(255))
    paid_at = Column(DateTime(timezone=True))

    booking = relationship("Booking",back_populates="payments")