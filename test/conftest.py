# test/conftest.py
import os
import pytest
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env.test")
load_dotenv(dotenv_path=dotenv_path)
print(dotenv_path)

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
print(TEST_DATABASE_URL)


@pytest.fixture(scope="module")
async def async_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=True)
    SQLModel.metadata.create_all(engine.sync_engine)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="module")
async def async_session(async_engine):
    async_session_factory = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session_factory() as session:
        yield session
