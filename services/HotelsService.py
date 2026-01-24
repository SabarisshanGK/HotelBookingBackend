# Imports
from sqlalchemy.orm import Session
from schemas.HotelsSchema import HotelCreateRequest , HotelCreateResponse
from models.Users import User
from fastapi import HTTPException , status , BackgroundTasks
from enums.UserRoleEnum import UserRole
from models.Address import Address
from enums.HotelStatusEnum import HotelStatus
from models.Hotels import Hotel
from utils.emails import send_email
import cloudinary.uploader
from models.HotelImage import HotelImage

class HotelService:

    @staticmethod
    async def create_hotel(user: User, payload: HotelCreateRequest , image , db:Session) -> HotelCreateResponse:
        if not user:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        if user.role not in [UserRole.ADMIN , UserRole.OWNER]:
            raise HTTPException(
                status_code= status.HTTP_405_METHOD_NOT_ALLOWED,
                detail= "Only admin and hotel owner can create hotel"
            )
        
        new_address = Address(
            city = payload.city,
            state = payload.state,
            line_one = payload.line_one,
            line_two = payload.line_two,
            country = payload.country,
            pincode = payload.pincode,
            latitude = payload.latitude,
            longitude= payload.longitude
        )
        
        db.add(new_address)
        db.commit()

        db.refresh(new_address)

        new_hotel = Hotel(
            address_id = new_address.id,
            owner_id = user.id,
            name = payload.name,
            description = payload.description,
            status = HotelStatus.APPROVED if user.role == UserRole.ADMIN else HotelStatus.PENDING,
            city = payload.city,
            check_in_time= payload.check_in_time,
            check_out_time = payload.check_out_time
        )

        db.add(new_hotel)
        db.commit()

        db.refresh(new_hotel)

        image_content = await image.read()

        cloudinary_result = cloudinary.uploader.upload(
            image_content,
            folder= "hotel_images"
        )

        hotel_image_url = cloudinary_result["secure_url"]

        new_hotel_image = HotelImage(
            hotel_id = new_hotel.id,
            image_url = hotel_image_url,
            is_primary = payload.is_primary
        )

        db.add(new_hotel_image)
        db.commit()
        db.refresh(new_hotel_image)

        result= {
            "id": new_hotel.id,
            "name": new_hotel.name,
            "description": new_hotel.description,
            "city": new_hotel.city,
            "status": new_hotel.status,
            "star_rating": new_hotel.star_rating,
            "check_in_time": new_hotel.check_in_time,
            "check_out_time": new_hotel.check_out_time,
            "state": new_address.state,
            "line_one": new_address.line_one,
            "line_two": new_address.line_two,
            "country": new_address.country,
            "pincode": new_address.pincode,
            "latitude": new_address.latitude,
            "longitude": new_address.longitude,
            "is_primary": new_hotel_image.is_primary,
            "image_url": new_hotel_image.image_url,
            "message": "Hotel successfully created" if user.role == UserRole.ADMIN else "Hotel created successfully and waiting to be approved by admin"
        }

        return result

    @staticmethod
    def get_hotels(status: HotelStatus, user: User , db: Session):
        if not user:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail= "User not found"
            )
        if user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code= status.HTTP_405_METHOD_NOT_ALLOWED,
                detail= "Only admin can get hotels"
            )
        hotels = db.query(Hotel)
        if status  is not None:
            hotels = hotels.filter(Hotel.status == status)
        return hotels.all()
        


    @staticmethod
    def approve_hotel(id: int, user: User , db: Session) -> str:
        if not user:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail= "User not found"
            )