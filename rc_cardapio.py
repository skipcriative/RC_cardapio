from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from flasgger import Swagger, swag_from
from models import db, Product, Category  # Import db here without circular import

# Load environment variables
load_dotenv()

# Flask app setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
swagger = Swagger(app)

# Initialize db with app
db.init_app(app)

# Initialize tables when the app context starts
with app.app_context():
    db.create_all()

@app.route('/test')
def home():
    return "Welcome to the Restaurant Menu API!"

#Endpoints for products

# Create new product
@app.route('/products', methods=['POST'])
@swag_from({
    'tags': ['Products'],
    'description': 'Create a new product',
    'parameters': [
        {'name': 'body', 'in': 'body', 'required': True, 'schema': {'name': 'str', 'price': 'float', 'category_id': 'int'}}
    ],
    'responses': {
        '201': {'description': 'Product created successfully'},
        '400': {'description': 'Invalid input'}
    }
})
def create_product():
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    category_id = data.get('category_id')

    new_product = Product(name=name, price=price, category_id=category_id)
    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "Product created", "id": new_product.id}), 201

# Get all products with pagination
@app.route('/products', methods=['GET'])
@swag_from({
    'tags': ['Products'],
    'description': 'Get paginated list of products',
    'parameters': [
        {'name': 'page', 'in': 'query', 'type': 'integer', 'default': 1},
        {'name': 'limit', 'in': 'query', 'type': 'integer', 'default': 10}
    ],
    'responses': {
        '200': {'description': 'List of products'}
    }
})
def get_products():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    products = Product.query.paginate(page, limit, False).items
    result = [
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "category": {"id": p.category.id, "category_name": p.category.category_name}
        }
        for p in products
    ]
    return jsonify(result), 200

# Get a single product by ID
@app.route('/products/<int:id>', methods=['GET'])
@swag_from({
    'tags': ['Products'],
    'description': 'Get a single product by ID',
    'parameters': [
        {'name': 'id', 'in': 'path', 'type': 'integer', 'required': True}
    ],
    'responses': {
        '200': {'description': 'Product data'},
        '404': {'description': 'Product not found'}
    }
})
def get_product(id):
    product = Product.query.get(id)
    if product:
        result = {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "category": {
                "id": product.category.id,
                "category_name": product.category.category_name
            }
        }
        return jsonify(result), 200
    return jsonify({"message": "Product not found"}), 404

# Update a product
@app.route('/products/<int:id>', methods=['PUT'])
@swag_from({
    'tags': ['Products'],
    'description': 'Update a product by ID',
    'parameters': [
        {'name': 'id', 'in': 'path', 'type': 'integer', 'required': True},
        {'name': 'body', 'in': 'body', 'required': True, 'schema': {'name': 'str', 'price': 'float', 'category_id': 'int'}}
    ],
    'responses': {
        '200': {'description': 'Product updated successfully'},
        '404': {'description': 'Product not found'}
    }
})
def update_product(id):
    data = request.get_json()
    product = Product.query.get(id)

    if product:
        product.name = data.get('name', product.name)
        product.price = data.get('price', product.price)
        product.category_id = data.get('category_id', product.category_id)
        db.session.commit()
        return jsonify({"message": "Product updated"}), 200
    return jsonify({"message": "Product not found"}), 404

# Delete a product
@app.route('/products/<int:id>', methods=['DELETE'])
@swag_from({
    'tags': ['Products'],
    'description': 'Delete a product by ID',
    'parameters': [
        {'name': 'id', 'in': 'path', 'type': 'integer', 'required': True}
    ],
    'responses': {
        '204': {'description': 'Product deleted successfully'},
        '404': {'description': 'Product not found'}
    }
})
def delete_product(id):
    product = Product.query.get(id)

    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted"}), 204
    return jsonify({"message": "Product not found"}), 404


#Endpoints for category

# Endpoint to create a new category
@app.route('/categories', methods=['POST'])
@swag_from({
    'tags': ['Categories'],
    'description': 'Create a new category',
    'parameters': [
        {'name': 'body', 'in': 'body', 'required': True, 'schema': {'category_name': 'str'}}
    ],
    'responses': {
        '201': {'description': 'Category created successfully'},
        '400': {'description': 'Invalid input'}
    }
})
def create_category():
    data = request.get_json()
    category_name = data.get('category_name')

    if not category_name:
        return jsonify({"error": "Category name is required"}), 400

    new_category = Category(category_name=category_name)
    db.session.add(new_category)
    db.session.commit()

    return jsonify({"message": "Category created", "id": new_category.id}), 201

# Endpoint to get all categories
@app.route('/categories', methods=['GET'])
@swag_from({
    'tags': ['Categories'],
    'description': 'Retrieve all categories',
    'responses': {
        '200': {'description': 'List of categories'}
    }
})
def get_categories():
    categories = Category.query.all()
    result = [{"id": c.id, "category_name": c.category_name} for c in categories]
    return jsonify(result), 200

# Endpoint to get a category by ID
@app.route('/categories/<int:id>', methods=['GET'])
@swag_from({
    'tags': ['Categories'],
    'description': 'Retrieve a category by ID',
    'parameters': [
        {'name': 'id', 'in': 'path', 'type': 'integer', 'required': True}
    ],
    'responses': {
        '200': {'description': 'Category data'},
        '404': {'description': 'Category not found'}
    }
})
def get_category(id):
    category = Category.query.get(id)
    if category:
        result = {"id": category.id, "category_name": category.category_name}
        return jsonify(result), 200
    return jsonify({"error": "Category not found"}), 404

# Endpoint to update a category by ID
@app.route('/categories/<int:id>', methods=['PUT'])
@swag_from({
    'tags': ['Categories'],
    'description': 'Update a category by ID',
    'parameters': [
        {'name': 'id', 'in': 'path', 'type': 'integer', 'required': True},
        {'name': 'body', 'in': 'body', 'required': True, 'schema': {'category_name': 'str'}}
    ],
    'responses': {
        '200': {'description': 'Category updated successfully'},
        '404': {'description': 'Category not found'}
    }
})
def update_category(id):
    data = request.get_json()
    category = Category.query.get(id)

    if not category:
        return jsonify({"error": "Category not found"}), 404

    category_name = data.get('category_name')
    if not category_name:
        return jsonify({"error": "Category name is required"}), 400

    category.category_name = category_name
    db.session.commit()
    return jsonify({"message": "Category updated"}), 200

# Endpoint to delete a category by ID
@app.route('/categories/<int:id>', methods=['DELETE'])
@swag_from({
    'tags': ['Categories'],
    'description': 'Delete a category by ID',
    'parameters': [
        {'name': 'id', 'in': 'path', 'type': 'integer', 'required': True}
    ],
    'responses': {
        '204': {'description': 'Category deleted successfully'},
        '404': {'description': 'Category not found'}
    }
})
def delete_category(id):
    category = Category.query.get(id)

    if not category:
        return jsonify({"error": "Category not found"}), 404

    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category deleted"}), 204

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
