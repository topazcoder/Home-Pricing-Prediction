"""
Sample data for testing the home pricing system
"""

SUBJECT_HOME = {
    "address": "123 Main Street, Austin, TX 78701",
    "latitude": 30.2672,
    "longitude": -97.7431,
    "square_footage": 2400,
    "bedrooms": 4,
    "bathrooms": 3,
    "year_built": 2010,
    "pool": True,
    "garage": True,
    "lot_size": 8000,
    "property_type": "Single Family"
}

PHOTOS = [
    "photo1.jpg",
    "photo2.jpg",
    "photo3.jpg"
]

VIDEO_TRANSCRIPT = """
Welcome to 123 Main Street. This beautiful home features 4 bedrooms and 3 bathrooms.
The kitchen has been recently updated with new granite countertops and stainless steel appliances.
The flooring throughout is in excellent condition with hardwood in the living areas.
The master bedroom is spacious with an ensuite bathroom that has been fully renovated.
Moving to the exterior, the home has a great backyard with a pool that's in good working condition.
The roof was replaced about 5 years ago and is in solid shape.
Some minor cosmetic updates would be recommended for the guest bathrooms.
The landscaping is well-maintained and the driveway is in good condition.
Overall, this is a well-maintained home in a desirable neighborhood.
"""

COMPARABLE_SALES = [
    {
        "address": "125 Main Street, Austin, TX 78701",
        "latitude": 30.2680,
        "longitude": -97.7425,
        "square_footage": 2350,
        "bedrooms": 4,
        "bathrooms": 3,
        "year_built": 2008,
        "pool": True,
        "garage": True,
        "sale_price": 675000,
        "days_since_sale": 45,
        "sale_date": "2025-08-24"
    },
    {
        "address": "456 Oak Avenue, Austin, TX 78701",
        "latitude": 30.2665,
        "longitude": -97.7440,
        "square_footage": 2500,
        "bedrooms": 4,
        "bathrooms": 3.5,
        "year_built": 2012,
        "pool": False,
        "garage": True,
        "sale_price": 695000,
        "days_since_sale": 30,
        "sale_date": "2025-09-08"
    },
    {
        "address": "789 Elm Street, Austin, TX 78701",
        "latitude": 30.2670,
        "longitude": -97.7450,
        "square_footage": 2300,
        "bedrooms": 3,
        "bathrooms": 2.5,
        "year_built": 2009,
        "pool": True,
        "garage": True,
        "sale_price": 650000,
        "days_since_sale": 60,
        "sale_date": "2025-08-09"
    },
    {
        "address": "321 Pine Road, Austin, TX 78701",
        "latitude": 30.2685,
        "longitude": -97.7420,
        "square_footage": 2450,
        "bedrooms": 4,
        "bathrooms": 3,
        "year_built": 2011,
        "pool": True,
        "garage": True,
        "sale_price": 685000,
        "days_since_sale": 75,
        "sale_date": "2025-07-25"
    },
    {
        "address": "555 Maple Drive, Austin, TX 78701",
        "latitude": 30.2660,
        "longitude": -97.7435,
        "square_footage": 2550,
        "bedrooms": 4,
        "bathrooms": 3.5,
        "year_built": 2013,
        "pool": False,
        "garage": True,
        "sale_price": 710000,
        "days_since_sale": 20,
        "sale_date": "2025-09-18"
    },
    {
        "address": "888 Cedar Lane, Austin, TX 78701",
        "latitude": 30.2675,
        "longitude": -97.7445,
        "square_footage": 2200,
        "bedrooms": 3,
        "bathrooms": 2,
        "year_built": 2007,
        "pool": False,
        "garage": True,
        "sale_price": 620000,
        "days_since_sale": 90,
        "sale_date": "2025-07-10"
    },
    {
        "address": "222 Birch Court, Austin, TX 78701",
        "latitude": 30.2668,
        "longitude": -97.7428,
        "square_footage": 2420,
        "bedrooms": 4,
        "bathrooms": 3,
        "year_built": 2010,
        "pool": True,
        "garage": True,
        "sale_price": 680000,
        "days_since_sale": 50,
        "sale_date": "2025-08-19"
    }
]
