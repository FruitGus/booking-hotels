import pytest
from sqlalchemy.ext.asyncio import create_async_engine
from src.config import settings
from src.database import BaseOrm, engine_null_pull
from src.main import app
from src.models import *
from httpx import AsyncClient, ASGITransport



@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    assert settings.MODE == "TEST"




@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pull.begin() as conn:
        await conn.run_sync(BaseOrm.metadata.drop_all)
        await conn.run_sync(BaseOrm.metadata.create_all)



@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database):
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        await ac.post(
            "/auth/register",
            json={"email": "Fruit@mail.ru",
                  "password": "1234",
            }
        )


