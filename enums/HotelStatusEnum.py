# Imports
from enum import Enum

class HotelStatus(str,Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
