from dotenv import load_dotenv
import os
from models import db, Category, Product  # Import db and models
from rc_cardapio import app  # Import app to access app context

# Load environment variables
load_dotenv()

# Sample data to insert into the database
categories_data = [
    {"category_name": "Bebidas"},
    {"category_name": "Cafés"},
    {"category_name": "Doces"},
]

products_data = [
    {"name": "capuccino", "price": 5.99, "category_name": "Cafés"},
    {"name": "Coca cola", "price": 12.99, "category_name": "Bebidas"},
    {"name": "Cheesecake", "price": 6.99, "category_name": "Doces"},
]

# Function to initialize the database
def initialize_database():
    with app.app_context():  # Ensures we're in the app context to use db
        # Create tables if they don't exist
        db.create_all()

        # Insert data into Category table
        for cat_data in categories_data:
            category = Category.query.filter_by(category_name=cat_data["category_name"]).first()
            if not category:
                category = Category(category_name=cat_data["category_name"])
                db.session.add(category)
        
        # Commit the categories first so we have category IDs
        db.session.commit()

        # Insert data into Product table
        for prod_data in products_data:
            category = Category.query.filter_by(category_name=prod_data["category_name"]).first()
            if category:
                product = Product(
                    name=prod_data["name"],
                    price=prod_data["price"],
                    category_id=category.id
                )
                db.session.add(product)

        # Commit all changes to the database
        db.session.commit()
        print("Database initialized with sample data.")

# Run the initialization function
if __name__ == "__main__":
    initialize_database()
