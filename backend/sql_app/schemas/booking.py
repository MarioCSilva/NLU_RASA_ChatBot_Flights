from pydantic import BaseModel
from datetime import datetime

class BookingBase(BaseModel):
    user:int
    flight_icao: str 
    flight_number:str
    price: float = None
    # useful to identify each flight since same the same flight ICAO
    # is used for multiple flights
    departure_time: datetime
    
class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    id: int
    timestamp: datetime
    class Config:
        orm_mode = True
