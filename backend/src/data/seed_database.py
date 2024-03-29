# data/seed_database.py
from sqlmodel import SQLModel
from data.database import engine, create_db_and_tables, AsyncSessionLocal
from data.seed_data import grocery_items_seed_data, market_seed_data
from models.all_models import GroceryItem, Market, PriceRecord, SpecialOffer

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
        for market in market_seed_data:
            new_market = Market(**market)
            session.add(new_market)
            await session.commit()
            await session.refresh(new_market)
            inserted_market_ids[new_market.name] = new_market.id

    return inserted_grocery_item_ids, inserted_market_ids

async def seed_price_records_and_special_offers(inserted_grocery_item_ids, inserted_market_ids):
    async with AsyncSessionLocal() as session:
        # Example for seeding a PriceRecord
        for name, grocery_item_id in inserted_grocery_item_ids.items():
            for market_name, market_id in inserted_market_ids.items():
                price_record = PriceRecord(
                    grocery_item_id=grocery_item_id,
                    market_id=market_id,
                    price=0.99,  # Example price
                    date_recorded=datetime.utcnow(),
                    is_promotional=False,
                    promotional_details=None
                )
                session.add(price_record)

        # Similar seed for SpecialOffer
        for name, grocery_item_id in inserted_grocery_item_ids.items():
            for market_name, market_id in inserted_market_ids.items():
                special_offer = SpecialOffer(
                    grocery_item_id=grocery_item_id,
                    description="Special offer on {}".format(name),
                    valid_from=datetime.utcnow(),
                    valid_to=datetime.utcnow() + timedelta(days=7),
                    image_url="/static/images/special_offer.jpg"
                )
                session.add(special_offer)

        await session.commit()


async def main():
    # Create DB and tables, if they don't exist
    await create_db_and_tables()
    grocery_item_ids, market_ids = await seed_grocery_items_and_markets()
    await seed_price_records_and_special_offers(grocery_item_ids, market_ids)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
