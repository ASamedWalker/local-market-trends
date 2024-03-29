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
]

special_offers_seed_data = [
    {
        "grocery_item_id": "Apples",
        "description": "20% off on all fruits!",
        "valid_from": "2022-01-01T00:00:00Z",
        "valid_to": "2022-01-31T23:59:59Z",
        "image_url": "/static/images/discounts/.jpg",
    },
]