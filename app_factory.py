from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flasgger import Swagger
from models import db
from sqlalchemy.orm import scoped_session, sessionmaker

# Import the controllers (blueprints)
from controllers.product_controller import product_bp
from controllers.category_controller import category_bp
from controllers.order_controller import order_bp

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    if not app.config['SQLALCHEMY_DATABASE_URI']:
        raise ValueError("DATABASE_URI is not set in the environment variables")
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_POOL_SIZE'] = 10
    app.config['SQLALCHEMY_POOL_TIMEOUT'] = 30
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 1800
    app.config['SQLALCHEMY_MAX_OVERFLOW'] = 5

    swagger = Swagger(app)
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    # Initialize database
    db.init_app(app)
    Migrate(app, db)  # Initialize Flask-Migrate

    # Set up a scoped session within the app context
    with app.app_context():
        session_factory = sessionmaker(bind=db.engine)
        Session = scoped_session(session_factory)
        app.Session = Session  # Attach session to app for global access

    # Register blueprints for the controllers
    app.register_blueprint(product_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(order_bp)

    # Clean up sessions after each request
    @app.teardown_appcontext
    def remove_session(exception=None):
        app.Session.remove()

    return app
