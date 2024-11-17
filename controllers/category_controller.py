from flask import Blueprint, request, jsonify
from models import db, Category
from flasgger import swag_from

# Define a blueprint for category routes
category_bp = Blueprint('category_bp', __name__)

# Create new category
@category_bp.route('/categories', methods=['POST'])
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

    new_category = Category(category_name=category_name)
    db.session.add(new_category)
    db.session.commit()

    return jsonify({"message": "Category created", "id": new_category.id}), 201

# Get all categories
@category_bp.route('/categories', methods=['GET'])
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

# Get category by ID
@category_bp.route('/categories/<int:id>', methods=['GET'])
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

# Update category
@category_bp.route('/categories/<int:id>', methods=['PUT'])
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

    category.category_name = data.get('category_name', category.category_name)
    db.session.commit()
    return jsonify({"message": "Category updated"}), 200

# Delete category
@category_bp.route('/categories/<int:id>', methods=['DELETE'])
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
