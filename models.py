from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy without attaching to the app
db = SQLAlchemy()

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(50), nullable=False)

    # Relationship to Product
    products = db.relationship('Product', backref='category', lazy=True)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)  # Optional description field
    image_link = db.Column(db.String(255), nullable=True)  # Link to the S3 image
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    # Relationship to OrderItem (if applicable)
    order_items = db.relationship('OrderItem', backref='product', lazy=True)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    table = db.Column(db.String(20), nullable=False)
    products = db.Column(db.Text, nullable=False)  # Store as JSON-like string
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(10), nullable=False, default='open')

class OrderItem(db.Model):  # Optional model for detailed product relationships in orders
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    # Relationship to Order
    order = db.relationship('Order', backref='items', lazy=True)
