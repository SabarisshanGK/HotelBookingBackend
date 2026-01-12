# Imports
from sqlalchemy import Column , Integer , ForeignKey  , Text , CheckConstraint , DateTime
from database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

# Definition
class Review(Base):
    __tablename__="reviews"
    id = Column(Integer , primary_key=True , index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    hotel_id = Column(Integer , ForeignKey("hotels.id"))
    rating = Column(Integer, nullable=False , default=3, server_default="3")
    comment = Column(Text)
    createdAt = Column(DateTime(timezone=True) , server_default=func.now(), nullable=False)

    user = relationship("User",back_populates="reviews")
    hotel = relationship("Hotel",back_populates="hotel_reviews")

    __table_args__ = (
        CheckConstraint(
            "star_rating >= 1 AND star_rating <= 5",
            name="check_star_rating_range"
        ),
    )