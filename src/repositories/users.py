from sqlalchemy import Select

from src.repositories.base import BaseRepository
from src.models.users import UsersOrm
from src.schemas.users import User


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User

    async def get_by_email(self, email: str):
        result = await self.session.execute(
            Select(UsersOrm).where(UsersOrm.email == email)
        )
        return result.scalar()