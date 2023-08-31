from typing import Any
from sqlalchemy.orm import Session
from sql_app.schemas.booking import Booking, BookingCreate
from  sql_app import models 
from flightbooking.AviationStackHandler import aviationStackHandler
from typing import Any
from sql_app.crud import crud_user

def get_bookingByFlightNumber(db: Session, flight_icao: str):
    return db.query(models.Booking).filter(models.Booking.flight_icao == flight_icao).first()

def get_bookingsByUserId(db: Session, userId: int):
     return db.query(models.Booking).filter(models.Booking.user_id == userId).all()

def  create_booking(db: Session, booking_data: BookingCreate):
    user = crud_user.get_userById(db,booking_data.user)
    db_booking = models.Booking(
        flight_icao=booking_data.flight_icao,
        price=booking_data.price,
        flight_date=booking_data.departure_time,
        user=user,
        flight_number=booking_data.flight_number
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return Booking(
        id=db_booking.booking_id,
        user=db_booking.user_id,
        price=db_booking.price,
        flight_number=db_booking.flight_number,
        departure_time=db_booking.flight_date,
        flight_icao=db_booking.flight_icao,
        timestamp=db_booking.timestamp
    )
    