from flask import Blueprint, request, jsonify
from models import db, Product, Category
from flasgger import swag_from

# Define a blueprint for product routes
product_bp = Blueprint('product_bp', __name__)

# Create new product
@product_bp.route('/products', methods=['POST'])
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

# Get all products
@product_bp.route('/products', methods=['GET'])
@swag_from({
    'tags': ['Products'],
    'description': 'Retrieve all products',
    'responses': {
        '200': {'description': 'List of products'}
    }
})
def get_products():
    products = Product.query.all()
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

# Get product by ID
@product_bp.route('/products/<int:id>', methods=['GET'])
@swag_from({
    'tags': ['Products'],
    'description': 'Retrieve a product by ID',
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

# Update product
@product_bp.route('/products/<int:id>', methods=['PUT'])
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

    if not product:
        return jsonify({"message": "Product not found"}), 404

    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.category_id = data.get('category_id', product.category_id)
    db.session.commit()
    return jsonify({"message": "Product updated"}), 200

# Delete product
@product_bp.route('/products/<int:id>', methods=['DELETE'])
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

    if not product:
        return jsonify({"message": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"}), 204
