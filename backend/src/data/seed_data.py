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

]


market_seed_data = [
    {"name": "Downtown Farmers' Market", "location_description": "Central square", "latitude": 40.712776, "longitude": -74.005974},
    {"name": "Uptown Grocers", "location_description": "Near the north end park", "latitude": 40.785091, "longitude": -73.968285},
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

price_records_seed_data = [
    {
        "grocery_item_id": "Apples",
        "market_id": "Downtown Farmers' Market",
        "price": 1.99,
        "date_recorded": datetime.utcnow(),
        "is_promotional": False,
        # Generate a random promotional detail
        "promotional_details": "Buy one get one free!",
    },
    # Add more price records here and generate random promotional details
    {
        "grocery_item_id": "Apples",
        "market_id": "Uptown Grocers",
        "price": 2.49,
        "date_recorded": datetime.utcnow(),
        "is_promotional": False,
        "promotional_details": "10% off on all fruits!",
    },
    {
        "grocery_item_id": "Bananas",
        "market_id": "Downtown Farmers' Market",
        "price": 0.99,
        "date_recorded": datetime.utcnow(),
        "is_promotional": False,
        "promotional_details": "20% off on all fruits!",
    },
    {
        "grocery_item_id": "Bananas",
        "market_id": "Uptown Grocers",
        "price": 1.29,
        "date_recorded": datetime.utcnow(),
        "is_promotional": False,
        "promotional_details": "15% off on all fruits!",
    },
    {
        "grocery_item_id": "Carrots",
        "market_id": "Downtown Farmers' Market",
        "price": 0.79,
        "date_recorded": datetime.utcnow(),
        "is_promotional": False,
        "promotional_details": "25% off on all vegetables!",
    },
    {
        "grocery_item_id": "Carrots",
        "market_id": "Uptown Grocers",
        "price": 0.99,
        "date_recorded": datetime.utcnow(),
        "is_promotional": False,
        "promotional_details": "20% off on all vegetables!",
    },
    {
        "grocery_item_id": "Tomatoes",
        "market_id": "Downtown Farmers' Market",
        "price": 1.29,
        "date_recorded": datetime.utcnow(),
        "is_promotional": False,
        "promotional_details": "15% off on all vegetables!",
    },
    {
        "grocery_item_id": "Tomatoes",
        "market_id": "Uptown Grocers",
        "price": 1.49,
        "date_recorded": datetime.utcnow(),
        "is_promotional": False,
        "promotional_details": "10% off on all vegetables!",
    },
    {
        "grocery_item_id": "Whole Wheat Bread",
        "market_id": "Downtown Farmers' Market",
        "price": 2.99,
        "date_recorded": datetime.utcnow(),
        "is_promotional": False,
        "promotional_details": "Buy one get one free!",
    },
    {
        "grocery_item_id": "Whole Wheat Bread",
        "market_id": "Uptown Grocers",
        "price": 3.49,
        "date_recorded": datetime.utcnow(),
        "is_promotional": False,
        "promotional_details": "10% off on all bakery items!",
    },
    {
        "grocery_item_id": "Orange Juice",
        "market_id": "Downtown Farmers' Market",
        "price": 3.99,
        "date_recorded": datetime.utcnow(),
        "is_promotional": False,
        "promotional_details": "20% off on all beverages!",
    },
    {
        "grocery_item_id": "Orange Juice",
        "market_id": "Uptown Grocers",
        "price": 4.49,
        "date_recorded": datetime.utcnow(),
        "is_promotional": False,
        "promotional_details": "15% off on all beverages!",
    },
    {
        "grocery_item_id": "Eggs",
        "market_id": "Downtown Farmers' Market",
        "price": 2.49,
        "date_recorded": datetime.utcnow(),
        "is_promotional": False,
        "promotional_details": "10% off on all dairy & eggs!",
    },
    {
        "grocery_item_id": "Eggs",
        "market_id": "Uptown Grocers",
        "price": 2.99,
        "date_recorded": datetime.utcnow(),
        "is_promotional": False,
        "promotional_details": "5% off on all dairy & eggs!",
    },
    {
        "grocery_item_id": "Milk",
        "market_id": "Downtown Farmers' Market",
        "price": 3.49,
        "date_recorded": datetime.utcnow(),
        "is_promotional": False,
        "promotional_details": "15% off on all dairy & eggs!",
    },
    {
        "grocery_item_id": "Milk",
        "market_id": "Uptown Grocers",
        "price": 3.99,
        "date_recorded": datetime.utcnow(),
        "is_promotional": False,
        "promotional_details": "10% off on all dairy & eggs!",
    },
    {
        "grocery_item_id": "Cheddar Cheese",
        "market_id": "Downtown Farmers' Market",
        "price": 4.99,
        "date_recorded": datetime.utcnow(),
        "is_promotional": False,
        "promotional_details": "10% off on all dairy & eggs!",
    },
    {
        "grocery_item_id": "Almonds",
        "market_id": "Downtown Farmers' Market",
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