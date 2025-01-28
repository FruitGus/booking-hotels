from src.database import BaseOrm
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class UsersOrm(BaseOrm):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key = True)
    email: Mapped[str] = mapped_column(String(200), unique=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(100))
    hashed_password: Mapped[str] = mapped_column(String(200))