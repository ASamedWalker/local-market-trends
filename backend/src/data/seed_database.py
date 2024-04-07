# data/seed_database.py
from sqlmodel import SQLModel
from data.database import engine, create_db_and_tables, AsyncSessionLocal
from data.seed_data import (
    grocery_items_seed_data,
    market_seed_data,
    price_records_seed_data,
    special_offers_seed_data,
    reviews_seed_data,
    special_offer_grocery_item_link_seed_data
)
from models.all_models import GroceryItem, Market, PriceRecord, SpecialOffer, Review, SpecialOfferGroceryItemLink
from sqlalchemy import select
from datetime import datetime, timedelta

async def seed_grocery_items_and_markets():
    # Dictionary to store inserted grocery item IDs with a key to relate them back to
    inserted_grocery_item_ids = {}
    # Similar for markets
    inserted_market_ids = {}

    async with AsyncSessionLocal() as session:
        # Seed GroceryItem
        for item in grocery_items_seed_data:
            new_item = GroceryItem(**item)
            session.add(new_item)
            await session.commit()
            await session.refresh(new_item)
            inserted_grocery_item_ids[new_item.name] = new_item.id

        # Seed Market
        # Seed Market
        for market in market_seed_data:
            new_market = Market(**market)
            session.add(new_market)
            try:
                await session.commit()
                await session.refresh(new_market)
                inserted_market_ids[new_market.name] = new_market.id
            except Exception as e:
                print(f"An error occurred when inserting market {new_market.name}: {e}")
                continue  # Skip this market and continue with the next one
    return inserted_grocery_item_ids, inserted_market_ids

async def seed_reviews(inserted_grocery_item_ids):
    async with AsyncSessionLocal() as session:
        # Seed Reviews
        for review_data in reviews_seed_data:
            # Replace grocery item names with the corresponding IDs
            review_data["grocery_item_id"] = inserted_grocery_item_ids[review_data["grocery_item_id"]]
            new_review = Review(**review_data)
            session.add(new_review)
            await session.commit()

async def seed_price_records_and_special_offers(inserted_grocery_item_ids, inserted_market_ids):
    async with AsyncSessionLocal() as session:
        # Seed PriceRecord
        for record in price_records_seed_data:
            # Replace grocery item and market names with IDs
            record["grocery_item_id"] = inserted_grocery_item_ids[record["grocery_item_id"]]
            record["market_id"] = inserted_market_ids[record["market_id"]]
            new_record = PriceRecord(**record)
            session.add(new_record)
            await session.commit()

        # Seed SpecialOffer
        for offer in special_offers_seed_data:
            # Replace grocery item name with ID
            offer["grocery_item_id"] = inserted_grocery_item_ids[offer["grocery_item_id"]]

            # Convert date strings to datetime objects
            offer["valid_from"] = datetime.fromisoformat(offer["valid_from"].replace("Z", ""))
            offer["valid_to"] = datetime.fromisoformat(offer["valid_to"].replace("Z", ""))

            new_offer = SpecialOffer(**offer)
            session.add(new_offer)
            await session.commit()

async def seed_special_offer_grocery_item_links(inserted_grocery_item_ids, inserted_market_ids):
    async with AsyncSessionLocal() as session:
        for link_data in special_offer_grocery_item_link_seed_data:
            # Assuming `special_offer_name` and `grocery_item_name` are fields that can be used
            # to look up the respective IDs for `SpecialOffer` and `GroceryItem`
            special_offer_id = await session.execute(
                select(SpecialOffer.id).where(SpecialOffer.description == link_data["special_offer_name"])
            )
            special_offer_id = special_offer_id.scalars().first()

            grocery_item_id = await session.execute(
                select(GroceryItem.id).where(GroceryItem.name == link_data["grocery_item_name"])
            )
            grocery_item_id = grocery_item_id.scalars().first()

            if special_offer_id and grocery_item_id:
                link = SpecialOfferGroceryItemLink(
                    special_offer_id=special_offer_id,
                    grocery_item_id=grocery_item_id
                )
                session.add(link)
            await session.commit()


async def seed_database():
    inserted_grocery_item_ids, inserted_market_ids = await seed_grocery_items_and_markets()
    await seed_price_records_and_special_offers(inserted_grocery_item_ids, inserted_market_ids)
    await seed_reviews(inserted_grocery_item_ids)
    print("Seeding special offer grocery item links...")
    await seed_special_offer_grocery_item_links(inserted_grocery_item_ids, inserted_market_ids)

async def main():
    # Create DB and tables, if they don't exist
    try:
        print("Creating database tables...")
        await create_db_and_tables()
        print("Database tables created successfully.")
    except Exception as e:
        print(f"An error occurred when creating the tables: {e}")
        return  # Exit if table creation fails

    # Seed the database
    try:
        print("Seeding the database...")
        await seed_database()
        print("Database seeded successfully.")
    except Exception as e:
        print(f"An error occurred when seeding the database: {e}")
        return



if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

