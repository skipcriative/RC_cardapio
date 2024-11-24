from dotenv import load_dotenv
import os
from models import db, Category, Product, Order, OrderItem  # Import db and models
from rc_cardapio import app  # Import app to access app context

# Load environment variables
load_dotenv()

# Sample data to insert into the database
categories_data = [
    {"category_name": "Bebidas"},
    {"category_name": "Cafés"},
    {"category_name": "Doces"},
    {"category_name": "Salgados"},
]

products_data = [
    # Bebidas
    {"name": "Coca Cola", "price": 12.99, "category_name": "Bebidas", "description": "Lorem ipsum dolor sit amet"},
    {"name": "Pepsi", "price": 11.99, "category_name": "Bebidas", "description": "Lorem ipsum dolor sit amet"},
    {"name": "Suco de Laranja", "price": 8.99, "category_name": "Bebidas", "description": "Lorem ipsum dolor sit amet"},
    {"name": "Suco de Uva", "price": 8.99, "category_name": "Bebidas", "description": "Lorem ipsum dolor sit amet"},
    {"name": "Água Mineral", "price": 4.99, "category_name": "Bebidas", "description": "Lorem ipsum dolor sit amet"},
    {"name": "Água com Gás", "price": 5.49, "category_name": "Bebidas", "description": "Lorem ipsum dolor sit amet"},
    {"name": "Chá Gelado", "price": 6.99, "category_name": "Bebidas", "description": "Lorem ipsum dolor sit amet"},
    {"name": "Energético", "price": 15.99, "category_name": "Bebidas", "description": "Lorem ipsum dolor sit amet"},

    # Cafés
    {"name": "Cappuccino", "price": 5.99, "category_name": "Cafés", "description": "Lorem ipsum dolor sit amet"},
    {"name": "Expresso", "price": 3.99, "category_name": "Cafés", "description": "Lorem ipsum dolor sit amet"},
    {"name": "Latte", "price": 6.99, "category_name": "Cafés", "description": "Lorem ipsum dolor sit amet"},
    {"name": "Macchiato", "price": 7.49, "category_name": "Cafés", "description": "Lorem ipsum dolor sit amet"},
    {"name": "Mocha", "price": 8.49, "category_name": "Cafés", "description": "Lorem ipsum dolor sit amet"},
    {"name": "Café Gelado", "price": 5.99, "category_name": "Cafés", "description": "Lorem ipsum dolor sit amet"},
    {"name": "Café com Leite", "price": 4.49, "category_name": "Cafés", "description": "Lorem ipsum dolor sit amet"},
    {"name": "Americano", "price": 4.99, "category_name": "Cafés", "description": "Lorem ipsum dolor sit amet"},

    # Doces
    {"name": "Cheesecake", "price": 6.99, "category_name": "Doces", "description": "Lorem ipsum dolor sit amet"},
    {"name": "Bolo de Chocolate", "price": 7.99, "category_name": "Doces", "description": "Lorem ipsum dolor sit amet"},
    {"name": "Brownie", "price": 5.99, "category_name": "Doces", "description": "Lorem ipsum dolor sit amet"},
    {"name": "Mousse de Maracujá", "price": 6.49, "category_name": "Doces", "description": "Lorem ipsum dolor sit amet"},
    {"name": "Pudim", "price": 4.99, "category_name": "Doces", "description": "Lorem ipsum dolor sit amet"},
    {"name": "Torta de Maçã", "price": 5.99, "category_name": "Doces", "description": "Lorem ipsum dolor sit amet"},
    {"name": "Gelatina", "price": 3.49, "category_name": "Doces", "description": "Lorem ipsum dolor sit amet"},
    {"name": "Tiramisu", "price": 8.99, "category_name": "Doces", "description": "Lorem ipsum dolor sit amet"},

    # Salgados
    {"name": "Coxinha", "price": 4.99, "category_name": "Salgados", "description": "Lorem ipsum dolor sit amet"},
    {"name": "Pastel", "price": 6.49, "category_name": "Salgados", "description": "Lorem ipsum dolor sit amet"},
    {"name": "Pão de Queijo", "price": 2.99, "category_name": "Salgados", "description": "Lorem ipsum dolor sit amet"},
    {"name": "Empada", "price": 5.49, "category_name": "Salgados", "description": "Lorem ipsum dolor sit amet"},
    {"name": "Esfiha", "price": 3.99, "category_name": "Salgados", "description": "Lorem ipsum dolor sit amet"},
    {"name": "Quibe", "price": 3.99, "category_name": "Salgados", "description": "Lorem ipsum dolor sit amet"},
    {"name": "Sanduíche Natural", "price": 7.49, "category_name": "Salgados", "description": "Lorem ipsum dolor sit amet"},
    {"name": "Torta Salgada", "price": 6.99, "category_name": "Salgados", "description": "Lorem ipsum dolor sit amet"}
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
                    description=prod_data["description"],  # Include description
                    category_id=category.id
                )
                db.session.add(product)

        # Commit all changes to the database
        db.session.commit()
        print("Database initialized with sample data.")

# Run the initialization function
if __name__ == "__main__":
    initialize_database()
