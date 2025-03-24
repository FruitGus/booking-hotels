from pydantic import ConfigDict, BaseModel
from datetime import date



class BookingAddRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date



class BookingAdd(BaseModel):
    user_id: int
    room_id: int
    date_from: date
    date_to: date
    price: int



class Booking(BookingAdd):

    id: int

    model_config = ConfigDict(from_attributes=True)