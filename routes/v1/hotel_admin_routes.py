# Imports
from fastapi import APIRouter , Depends , HTTPException , status , UploadFile , File , Form
from database import get_db
from utils.jwt_util import verify_token
from services.HotelsService import HotelService
from schemas.HotelsSchema import HotelCreateRequest , HotelCreateResponse
from sqlalchemy.orm import Session
from dependencies.get_current_user import get_current_user_from_jwt
from datetime import time


router = APIRouter(prefix="/admin/hotel")

# Create Hotel
# Method: POST
@router.post('/create-hotel', response_model=HotelCreateResponse , description="An endpoint to create hotel Admin route")
async def create_admin_hotel(
     name: str = Form(...),
    description: str = Form(...),
    city: str = Form(...),
    check_in_time: time = Form(...),
    check_out_time: time = Form(...),
    state: str = Form(...),
    line_one: str = Form(...),
    line_two: str = Form(...),
    country: str = Form(...),
    pincode: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    star_rating: int = Form(3),
    is_primary: bool = Form(True),
    image: UploadFile = File(...),
    user=Depends(verify_token),
    db: Session = Depends(get_db),
):
    current_user = get_current_user_from_jwt(user=user,db=db)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    hotel_payload = HotelCreateRequest(
        name=name,
        description=description,
        city=city,
        check_in_time=check_in_time,
        check_out_time=check_out_time,
        state=state,
        line_one=line_one,
        line_two=line_two,
        country=country,
        pincode=pincode,
        latitude=latitude,
        longitude=longitude,
        star_rating=star_rating,
        is_primary=is_primary,
    )
    return await HotelService.create_hotel(user=current_user, payload=hotel_payload , image=image , db=db )