from src.schemas.bookings import BookingAdd
from datetime import date




async def test_add_bookings(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        user_id = user_id,
        room_id = room_id,
        date_from = date(year=2024, month=12, day=25),
        date_to = date(year=2025, month=1, day=5),
        price = 10000
    )
    await db.bookings.add(booking_data)
    await db.commit()