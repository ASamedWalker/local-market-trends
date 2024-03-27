# data/seed_database.py
from sqlmodel import SQLModel
from .database import create_db_and_tables, engine, AsyncSessionLocal
from .seed_data import grocery_items_seed_data  # Adjust import paths as necessary
from models.grocery_item import GroceryItem  # Adjust import paths as necessary

async def seed_grocery_items():
    async with AsyncSessionLocal() as session:
        for item_data in grocery_items_seed_data:
            item = GroceryItem(**item_data)
            session.add(item)
        await session.commit()

async def main():
    # Create DB and tables, if they don't exist
    await create_db_and_tables()
    # Seed the data
    await seed_grocery_items()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
