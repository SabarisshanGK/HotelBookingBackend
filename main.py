# Imports 
import models
from fastapi import FastAPI 
from database import engine , Base
from routes.v1 import auth_routes , hotel_admin_routes , hotel_owner_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title= "Hotel Booking Website Backend",
    description= "An Restful API for booking hotel",
    version= "0.0.1"
)

app.include_router(router= auth_routes.router , prefix="/api/v1" , tags=["Authentication"] )
app.include_router(router= hotel_owner_routes.router , prefix="/api/v1" , tags=["Hotel Owner"] )
app.include_router(router= hotel_admin_routes.router , prefix="/api/v1" , tags=["Hotel Admin"] )