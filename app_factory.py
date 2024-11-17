from flask import Flask
from dotenv import load_dotenv
import os
from flasgger import Swagger
from models import db

# Import the controllers here
from controllers.product_controller import product_bp
from controllers.category_controller import category_bp

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    swagger = Swagger(app)
    
    # Initialize database
    db.init_app(app)

    # Register blueprints for the controllers
    app.register_blueprint(product_bp)
    app.register_blueprint(category_bp)

    return app
