from datetime import date

from sqlalchemy.ext.hybrid import hybrid_property

from src.database import BaseOrm
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey


class BookingsOrm(BaseOrm):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    date_from: Mapped[date]
    date_to: Mapped[date]
    price: Mapped[int]

    @hybrid_property
    def total_cost(self) -> int:
        return self.price * (self.date_to - self.date_from).days
