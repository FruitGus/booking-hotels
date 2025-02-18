from datetime import date

from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import Room
from src.database import engine

from sqlalchemy import select, func




class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(
            self,
            hotel_id,
            date_from: date,
            date_to: date,

    ):

        """
    with rooms_count as (
        select room_id, count(*) as rooms_booked from bookings
        where date_from <= '2025-02-28' and date_to >= '2025-02-10'
        group by room_id
    ),
    rooms_left_table as (
        select rooms.id as room_id, quantity - coalesce(rooms_booked, 0) as rooms_left
        from rooms
        left join rooms_count on rooms.id = rooms_count.room_id
    )
    select * from rooms_left_table
    where rooms_left > 0 and room_id in (select id from rooms where hotel_id = 4);

        """

        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)


        return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))