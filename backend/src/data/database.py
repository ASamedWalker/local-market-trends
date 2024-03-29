from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./market_trends.db"
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a sessionmaker instance configured for AsyncSession
AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


async def create_db_and_tables():
    async with engine.begin() as conn:
        try:
            await conn.run_sync(SQLModel.metadata.drop_all)
            await conn.run_sync(SQLModel.metadata.create_all)
        except Exception as e:
            print(f"An error occurred when creating the tables: {e}")


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
