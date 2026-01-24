# Imports
from pydantic import BaseModel 
from typing import Optional
from enums.HotelStatusEnum import HotelStatus
from datetime import time
from fastapi import File , UploadFile

class HotelBase(BaseModel):
    name: str
    description: str
    city: str
    status: Optional[HotelStatus] = HotelStatus.PENDING
    star_rating: Optional[int] = 3
    check_in_time: time
    check_out_time: time
    state: str
    line_one: str
    line_two: str
    country: str
    pincode: str
    latitude: float
    longitude: float
    is_primary: bool = True

class HotelCreateRequest(HotelBase):
    pass

class HotelCreateResponse(BaseModel):
    id: int
    name: str
    description: str
    city: str
    status: HotelStatus 
    star_rating: int 
    check_in_time: time
    check_out_time: time
    state: str
    line_one: str
    line_two: str
    country: str
    pincode: str
    latitude: float
    longitude: float
    is_primary: bool
    image_url: str
    message: str
    class Config:
        from_attributes = True 

class HotelsResponse(BaseModel):
    id: int
    name: str
    description: str
    city: str
    status: HotelStatus 
    star_rating: int 
    check_in_time: time
    check_out_time: time
    address_id: int
    class Config:
        from_attributes = True 
