from tarfile import TruncatedHeaderError

import pytest
from sqlalchemy.ext.asyncio import create_async_engine

from src.config import settings
from src.database import BaseOrm, engine_null_pull
from src.models import *


@pytest.fixture(scope="session", autouse=True)
async def async_main():
    assert settings.MODE == "TEST"

    async with engine_null_pull.begin() as conn:
        await conn.run_sync(BaseOrm.metadata.drop_all)
        await conn.run_sync(BaseOrm.metadata.create_all)

