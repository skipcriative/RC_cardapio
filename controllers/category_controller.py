from flask import Blueprint, request, jsonify, current_app as app
from models import Category
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

    session = app.Session()
    try:
        new_category = Category(category_name=category_name)
        session.add(new_category)
        session.commit()
        return jsonify({"message": "Category created", "id": new_category.id}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

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
    session = app.Session()
    try:
        categories = session.query(Category).all()
        result = [{"id": c.id, "category_name": c.category_name} for c in categories]
        return jsonify(result), 200
    finally:
        session.close()

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
    session = app.Session()
    try:
        category = session.query(Category).get(id)
        if category:
            result = {"id": category.id, "category_name": category.category_name}
            return jsonify(result), 200
        return jsonify({"error": "Category not found"}), 404
    finally:
        session.close()

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
    session = app.Session()
    try:
        category = session.query(Category).get(id)
        if not category:
            return jsonify({"error": "Category not found"}), 404

        category.category_name = data.get('category_name', category.category_name)
        session.commit()
        return jsonify({"message": "Category updated"}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

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
    session = app.Session()
    try:
        category = session.query(Category).get(id)
        if not category:
            return jsonify({"error": "Category not found"}), 404

        session.delete(category)
        session.commit()
        return jsonify({"message": "Category deleted"}), 204
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()
