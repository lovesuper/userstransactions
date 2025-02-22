import asyncio

import pytest
from fastapi.testclient import TestClient

from app.database import engine
from app.domain.mixins import Base
from app.main import app


@pytest.fixture(scope="module")
def client():
    async def init_db():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(init_db())
    with TestClient(app) as c:
        yield c
