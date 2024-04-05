# data/seed_data.py
from datetime import datetime, timedelta
from uuid import UUID, uuid4
grocery_items_seed_data = [
    {
        "name": "Apples",
        "description": "Crisp and juicy apples, perfect for snacking.",
        "category": "Fruits",
        "image_url": "/static/images/fruits/apples.jpg",
    },
    {
        "name": "Bananas",
        "description": "Rich in potassium and ideal for breakfast.",
        "category": "Fruits",
        "image_url": "/static/images/fruits/bananas.jpg",
    },
    {
        "name": "Carrots",
        "description": "Fresh and crunchy carrots, great for salads.",
        "category": "Vegetables",
        "image_url": "/static/images/fruits/carrots.jpg",
    },
    {
        "name": "Tomatoes",
        "description": "Juicy tomatoes, a versatile kitchen staple.",
        "category": "Vegetables",
        "image_url": "/static/images/fruits/tomatoes.jpg",
    },
    {
        "name": "Whole Wheat Bread",
        "description": "Nutritious whole wheat bread, freshly baked.",
        "category": "Bakery",
        "image_url": "/static/images/fruits/whole_wheat_bread.jpg",
    },
    {
        "name": "Orange Juice",
        "description": "Refreshing orange juice, squeezed from fresh oranges.",
        "category": "Beverages",
        "image_url": "/static/images/fruits/orange_juice.jpg",
    },
    {
        "name": "Eggs",
        "description": "Farm-fresh eggs, a breakfast essential.",
        "category": "Dairy & Eggs",
        "image_url": "/static/images/fruits/eggs.jpg",
    },
    {
        "name": "Milk",
        "description": "Creamy and rich milk, sourced from local farms.",
        "category": "Dairy & Eggs",
        "image_url": "/static/images/fruits/milk.jpg",
    },
    {
        "name": "Cheddar Cheese",
        "description": "Sharp and flavorful cheddar, aged to perfection.",
        "category": "Dairy & Eggs",
        "image_url": "/static/images/fruits/cheddar_cheese.jpg",
    },
    {
        "name": "Almonds",
        "description": "Crunchy almonds, a healthy snacking option.",
        "category": "Nuts & Seeds",
        "image_url": "/static/images/fruits/almonds.jpg",
    },
    # Add more grocery items here
    {
        "name": "Cashews",
        "description": "Roasted cashews, a delicious and healthy snack.",
        "category": "Nuts & Seeds",
        "image_url": "/static/images/fruits/almonds.jpg",
    },
    {
        "name": "Peanuts",
        "description": "Salted peanuts, a classic snack for all occasions.",
        "category": "Nuts & Seeds",
        "image_url": "/static/images/fruits/milk.jpg",
    },
    {
        "name": "Pistachios",
        "description": "Roasted pistachios, a flavorful and nutritious snack.",
        "category": "Nuts & Seeds",
        "image_url": "/static/images/fruits/eggs.jpg",
    },
    {
        "name": "Walnuts",
        "description": "Crunchy walnuts, rich in omega-3 fatty acids.",
        "category": "Nuts & Seeds",
        "image_url": "/static/images/fruits/milk.jpg",
    },
    {
        "name": "Sunflower Seeds",
        "description": "Roasted sunflower seeds, a healthy and tasty snack.",
        "category": "Nuts & Seeds",
        "image_url": "/static/images/fruits/eggs.jpg",
    },
    {
        "name": "Pumpkin Seeds",
        "description": "Toasted pumpkin seeds, a nutritious and crunchy snack.",
        "category": "Nuts & Seeds",
        "image_url": "/static/images/fruits/milk.jpg",
    },
]

# lets update the seed data for markets
market_seed_data = [
    {
        "name": "whole foods market",
        "location_description": "123 Main Street, Anytown, USA",
        "image_url": "/static/images/markets/whole_foods_market.jpg",
        "operating_hours": "Mon-Sat: 8am-8pm, Sun: 10am-6pm",
        "rating": 4.5,
    },
    {
        "name": "morrisons market",
        "location_description": "456 Elm Street, manhattan, USA",
        "image_url": "/static/images/markets/morrisons_market.jpg",
        "operating_hours": "Mon-Sat: 7am-9pm, Sun: 9am-5pm",
        "rating": 4.0,
    },
    {
        "name": "m local market",
        "location_description": "789 Oak Street, harlem, USA",
        "image_url": "/static/images/markets/m_local_market.jpg",
        "operating_hours": "Mon-Sat: 9am-9pm, Sun: 10am-7pm",
        "rating": 4.2,
    },
    {
        "name": "minuto market",
        "location_description": "101 Market Street, sprint, USA",
        "image_url": "/static/images/markets/minuto_market.jpg",
        "operating_hours": "Sat: 8am-12pm, Sun: 10am-2pm",
        "rating": 4.8,
    },
    {
        "name": "fresh and easy market",
        "location_description": "202 Grocery Avenue, Ashtown, USA",
        "image_url": "/static/images/markets/fresh_easy_market.jpg",
        "operating_hours": "Mon-Sat: 9am-8pm, Sun: 10am-6pm",
        "rating": 4.6,
    },
    {
        "name": "wholeworths market",
        "location_description": "303 Farm Road, Greenfield, USA",
        "image_url": "/static/images/markets/farmers_market.jpg",
        "operating_hours": "Sat: 8am-12pm, Sun: 10am-2pm",
        "rating": 4.9,
    }
]

reviews_seed_data = [
    {
        "grocery_item_id": "Apples",
        "rating": 5,
        "comment": "Delicious apples, very fresh and crisp from this store!",
        "created_at": datetime.utcnow(),
    },
    # Generate 5 more reviews here
     {
        "grocery_item_id": "Apples",
        "rating": 4,
        "comment": "Good apples, but a bit expensive.",
        "created_at": datetime.utcnow(),
    },
    {
        "grocery_item_id": "Bananas",
        "rating": 4.5,
        "comment": "Great bananas, very ripe and sweet!",
        "created_at": datetime.utcnow(),
    },
    {
        "grocery_item_id": "Bananas",
        "rating": 4,
        "comment": "Good bananas, but a bit overripe.",
        "created_at": datetime.utcnow(),
    },
    {
        "grocery_item_id": "Carrots",
        "rating": 5,
        "comment": "Fresh carrots, great for salads!",
        "created_at": datetime.utcnow(),
    },
    {
        "grocery_item_id": "Carrots",
        "rating": 3.5,
        "comment": "Good carrots, but a bit expensive.",
        "created_at": datetime.utcnow(),
    },
    {
        "grocery_item_id": "Tomatoes",
        "rating": 4.5,
        "comment": "Juicy tomatoes, perfect for sandwiches!",
        "created_at": datetime.utcnow(),
    },
    {
        "grocery_item_id": "Tomatoes",
        "rating": 4,
        "comment": "Good tomatoes, but a bit pricey.",
        "created_at": datetime.utcnow(),
    }
]

# lets update the seed data for price records to reflect the new markets
price_records_seed_data = [
    {
        "grocery_item_id": "Apples",
        "market_id": "whole foods market",
        "price": 1.99,
        "date_recorded": datetime.utcnow(),
        "is_promotional": False,
        # Generate a random promotional detail
        "promotional_details": "Buy one get one free!",
    },
    # Add more price records here and generate random promotional details
    {
        "grocery_item_id": "Apples",
        "market_id": "morrisons market",
        "price": 2.49,
        "date_recorded": datetime.utcnow(),
        "is_promotional": False,
        "promotional_details": "10% off on all fruits!",
    },
    {
        "grocery_item_id": "Bananas",
        "market_id": "whole foods market",
        "price": 0.99,
        "date_recorded": datetime.utcnow(),
        "is_promotional": False,
        "promotional_details": "20% off on all fruits!",
    },
    {
        "grocery_item_id": "Bananas",
        "market_id": "minuto market",
        "price": 1.29,
        "date_recorded": datetime.utcnow(),
        "is_promotional": False,
        "promotional_details": "15% off on all fruits!",
    },
    {
        "grocery_item_id": "Carrots",
        "market_id": "whole foods market",
        "price": 0.79,
        "date_recorded": datetime.utcnow(),
        "is_promotional": False,
        "promotional_details": "25% off on all vegetables!",
    },
    {
        "grocery_item_id": "Carrots",
        "market_id": "morrisons market",
        "price": 0.99,
        "date_recorded": datetime.utcnow(),
        "is_promotional": False,
        "promotional_details": "20% off on all vegetables!",
    },
    {
        "grocery_item_id": "Tomatoes",
        "market_id": "wholeworths market",
        "price": 1.29,
        "date_recorded": datetime.utcnow(),
        "is_promotional": False,
        "promotional_details": "15% off on all vegetables!",
    },
    {
        "grocery_item_id": "Tomatoes",
        "market_id": "fresh and easy market",
        "price": 1.49,
        "date_recorded": datetime.utcnow(),
        "is_promotional": False,
        "promotional_details": "10% off on all vegetables!",
    },
    {
        "grocery_item_id": "Whole Wheat Bread",
        "market_id": "m local market",
        "price": 2.99,
        "date_recorded": datetime.utcnow(),
        "is_promotional": False,
        "promotional_details": "Buy one get one free!",
    },
    {
        "grocery_item_id": "Whole Wheat Bread",
        "market_id": "minuto market",
        "price": 3.49,
        "date_recorded": datetime.utcnow(),
        "is_promotional": False,
        "promotional_details": "10% off on all bakery items!",
    },
    {
        "grocery_item_id": "Orange Juice",
        "market_id": "whole foods market",
        "price": 3.99,
        "date_recorded": datetime.utcnow(),
        "is_promotional": False,
        "promotional_details": "20% off on all beverages!",
    },
    {
        "grocery_item_id": "Orange Juice",
        "market_id": "morrisons market",
        "price": 4.49,
        "date_recorded": datetime.utcnow(),
        "is_promotional": False,
        "promotional_details": "15% off on all beverages!",
    },
    {
        "grocery_item_id": "Eggs",
        "market_id": "m local market",
        "price": 2.49,
        "date_recorded": datetime.utcnow(),
        "is_promotional": False,
        "promotional_details": "10% off on all dairy & eggs!",
    },
    {
        "grocery_item_id": "Eggs",
        "market_id": "wholeworths market",
        "price": 2.99,
        "date_recorded": datetime.utcnow(),
        "is_promotional": False,
        "promotional_details": "5% off on all dairy & eggs!",
    },
    {
        "grocery_item_id": "Milk",
        "market_id": "whole foods market",
        "price": 3.49,
        "date_recorded": datetime.utcnow(),
        "is_promotional": False,
        "promotional_details": "15% off on all dairy & eggs!",
    },
    {
        "grocery_item_id": "Milk",
        "market_id": "morrisons market",
        "price": 3.99,
        "date_recorded": datetime.utcnow(),
        "is_promotional": False,
        "promotional_details": "10% off on all dairy & eggs!",
    },
    {
        "grocery_item_id": "Cheddar Cheese",
        "market_id": "fresh and easy market",
        "price": 4.99,
        "date_recorded": datetime.utcnow(),
        "is_promotional": False,
        "promotional_details": "10% off on all dairy & eggs!",
    },
    {
        "grocery_item_id": "Almonds",
        "market_id": "minuto market",
        "price": 5.99,
        "date_recorded": datetime.utcnow(),
        "is_promotional": False,
        "promotional_details": "Buy one get one free!",
    }
]

special_offers_seed_data = [
    {
        "grocery_item_id": "Apples",
        "description": "20% off on all fruits!",
        "valid_from": "2022-01-01T00:00:00Z",
        "valid_to": "2022-01-31T23:59:59Z",
        "image_url": "/static/images/discounts/twenty-percent-off.jpg",
    },
    # Add more special offers here
    {
        "grocery_item_id": "Bananas",
        "description": "15% off on all fruits!",
        "valid_from": "2022-01-01T00:00:00Z",
        "valid_to": "2022-01-31T23:59:59Z",
        "image_url": "/static/images/discounts/fifteen-percent-off.jpg",
    },
    {
        "grocery_item_id": "Carrots",
        "description": "25% off on all vegetables!",
        "valid_from": "2022-01-01T00:00:00Z",
        "valid_to": "2022-01-31T23:59:59Z",
        "image_url": "/static/images/discounts/twenty-five-percent.jpg",
    },
    {
        "grocery_item_id": "Tomatoes",
        "description": "15% off on all vegetables!",
        "valid_from": "2022-01-01T00:00:00Z",
        "valid_to": "2022-01-31T23:59:59Z",
        "image_url": "/static/images/discounts/fifteen-percent-off.jpg",
    },
    {
        "grocery_item_id": "Whole Wheat Bread",
        "description": "Buy one get one free!",
        "valid_from": "2022-01-01T00:00:00Z",
        "valid_to": "2022-01-31T23:59:59Z",
        "image_url": "/static/images/discounts/ten-percent-off.jpg",
    },
    {
        "grocery_item_id": "Orange Juice",
        "description": "20% off on all beverages!",
        "valid_from": "2022-01-01T00:00:00Z",
        "valid_to": "2022-01-31T23:59:59Z",
        "image_url": "/static/images/discounts/twenty-percent-off.jpg",
    },
    {
        "grocery_item_id": "Eggs",
        "description": "10% off on all dairy & eggs!",
        "valid_from": "2022-01-01T00:00:00Z",
        "valid_to": "2022-01-31T23:59:59Z",
        "image_url": "/static/images/discounts/ten-percent-off.jpg",
    },
    {
        "grocery_item_id": "Milk",
        "description": "15% off on all dairy & eggs!",
        "valid_from": "2022-01-01T00:00:00Z",
        "valid_to": "2022-01-31T23:59:59Z",
        "image_url": "/static/images/discounts/fifteen-percent-off.jpg",
    },
    {
        "grocery_item_id": "Cheddar Cheese",
        "description": "10% off on all dairy & eggs!",
        "valid_from": "2022-01-01T00:00:00Z",
        "valid_to": "2022-01-31T23:59:59Z",
        "image_url": "/static/images/discounts/ten-percent-off.jpg",
    },
    # Add more special offers here
    {
        "grocery_item_id": "Almonds",
        "description": "Buy one get one free!",
        "valid_from": "2022-01-01T00:00:00Z",
        "valid_to": "2022-01-31T23:59:59Z",
        "image_url": "/static/images/discounts/buy-1-get-1-free.jpg",
    },
    {
        "grocery_item_id": "Almonds",
        "description": "15% off on all nuts & seeds!",
        "valid_from": "2022-01-01T00:00:00Z",
        "valid_to": "2022-01-31T23:59:59Z",
        "image_url": "/static/images/discounts/fifteen-percent-off.png",
    },
    {
        "grocery_item_id": "Almonds",
        "description": "25% off on all nuts & seeds!",
        "valid_from": "2022-01-01T00:00:00Z",
        "valid_to": "2022-01-31T23:59:59Z",
        "image_url": "/static/images/discounts/twenty-five-percent.jpg",
    },
    {
        "grocery_item_id": "Almonds",
        "description": "10% off on all nuts & seeds!",
        "valid_from": "2022-01-01T00:00:00Z",
        "valid_to": "2022-01-31T23:59:59Z",
        "image_url": "/static/images/discounts/ten-percent-off.jpg",
    },

]