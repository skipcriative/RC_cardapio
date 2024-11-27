from flask import Blueprint, request, jsonify, current_app as app
from models import Product
from flasgger import swag_from
from s3_handler import S3Handler #import s3Handler class

# Define a blueprint for product routes
product_bp = Blueprint('product_bp', __name__)

# Create new product with optional image
@product_bp.route('/products', methods=['POST'])
@swag_from({
    'tags': ['Products'],
    'description': 'Create a new product',
    'parameters': [
        {'name': 'body', 'in': 'body', 'required': True, 'schema': {'name': 'str', 'price': 'float', 'description': 'str', 'category_id': 'int'}},
        {'name': 'file', 'in': 'formData', 'type': 'file', 'required': False}
    ],
    'responses': {
        '201': {'description': 'Product created successfully'},
        '400': {'description': 'Invalid input'}
    }
})
def create_product():
    data = request.form
    name = data.get('name')
    price = data.get('price')
    description = data.get('description')  # Optional field
    category_id = data.get('category_id')
    file = request.files.get('file')  # Optional image file

    session = app.Session()
    try:
        image_link = None
        if file:
            # Use S3Handler to upload the file and get the public URL
            s3_handler = S3Handler()
            image_link = s3_handler.upload_file(file)

        # Create the new product
        new_product = Product(name=name, price=price, description=description, image_link=image_link, category_id=category_id)
        session.add(new_product)
        session.commit()
        return jsonify({"message": "Product created", "id": new_product.id, "image_link": new_product.image_link}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

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
    session = app.Session()
    try:
        products = session.query(Product).all()
        result = [
            {
                "id": p.id,
                "name": p.name,
                "price": p.price,
                "description": p.description,
                "image_link": p.image_link,  # Include image link
                "category": {"id": p.category.id, "category_name": p.category.category_name}
            }
            for p in products
        ]
        return jsonify(result), 200
    finally:
        session.close()

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
    session = app.Session()
    try:
        product = session.query(Product).get(id)
        if product:
            result = {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "description": product.description,
                "image_link": product.image_link,  # Include image link
                "category": {
                    "id": product.category.id,
                    "category_name": product.category.category_name
                }
            }
            return jsonify(result), 200
        return jsonify({"message": "Product not found"}), 404
    finally:
        session.close()

# Update product with optional image update
@product_bp.route('/products/<int:id>', methods=['PUT'])
@swag_from({
    'tags': ['Products'],
    'description': 'Update a product by ID',
    'parameters': [
        {'name': 'id', 'in': 'path', 'type': 'integer', 'required': True},
        {'name': 'body', 'in': 'body', 'required': True, 'schema': {'name': 'str', 'price': 'float', 'description': 'str', 'category_id': 'int'}},
        {'name': 'file', 'in': 'formData', 'type': 'file', 'required': False}
    ],
    'responses': {
        '200': {'description': 'Product updated successfully'},
        '404': {'description': 'Product not found'}
    }
})
def update_product(id):
    data = request.form
    session = app.Session()
    try:
        product = session.query(Product).get(id)
        if not product:
            return jsonify({"message": "Product not found"}), 404

        product.name = data.get('name', product.name)
        product.price = data.get('price', product.price)
        product.description = data.get('description', product.description)  # Update description
        product.category_id = data.get('category_id', product.category_id)

        # Handle file upload for image update
        file = request.files.get('file')
        if file:
            s3_handler = S3Handler()
            image_link = s3_handler.upload_file(file)
            product.image_link = image_link

        session.commit()
        return jsonify({"message": "Product updated", "image_link": product.image_link}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


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
    session = app.Session()
    try:
        product = session.query(Product).get(id)
        if not product:
            return jsonify({"message": "Product not found"}), 404

        session.delete(product)
        session.commit()
        return jsonify({"message": "Product deleted"}), 204
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()
