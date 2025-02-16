from fastapi import APIRouter, Query, Body
from datetime import date

from src.api.dependencies import UserIdDep, DBDep, PaginationDep
from src.schemas.bookings import BookingAdd, BookingAddRequest, Booking

router = APIRouter(prefix="/bookings", tags=["Бронирования"])



@router.get("", summary="Получение всех бронирований")
async def get_booking(
        pagination: PaginationDep,
        db: DBDep,

):
    per_page = pagination.per_page or 5
    return await db.bookings.get_all(
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )


@router.get("/bookings/{user_id}", summary="Получение своих бронирований")
async def get_booking(
        user_id: int,
        db: DBDep,
):

    return await db.bookings.get_all(
        user_id = user_id
    )




@router.post("", summary="Создание бронирования")
async def add_booking(
        user_id: UserIdDep,
        db: DBDep,
        booking_data: BookingAddRequest = Body(openapi_examples={
    "1": {"summary": "Комната", "value": {
        "title": "Отель Сочи 5 звезд у моря",
        "location": "ул. Морячки, 3",
    }},
})
):

    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price: int = room.price

    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump(),
    )

    booking = await db.bookings.add(_booking_data)
    await db.commit()

    return {"status": "OK", "data": booking}