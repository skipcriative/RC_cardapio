from flask import Blueprint, request, jsonify, current_app as app
from models import Order
from flasgger import swag_from

# Define a blueprint for order routes
order_bp = Blueprint('order_bp', __name__)

# Create a new order
@order_bp.route('/orders', methods=['POST'])
@swag_from({
    'tags': ['Orders'],
    'description': 'Create a new order',
    'parameters': [
        {'name': 'body', 'in': 'body', 'required': True, 'schema': {'table': 'int', 'products': 'list', 'total': 'float', 'status': 'str'}}
    ],
    'responses': {
        '201': {'description': 'Order created successfully'},
        '400': {'description': 'Invalid input'}
    }
})
def create_order():
    data = request.get_json()
    table = data.get('table')
    products = data.get('products')  # Expected as a list
    total = data.get('total')
    status = data.get('status', 'open')  # Default to 'open'

    session = app.Session()
    try:
        new_order = Order(table=table, products=str(products), total=total, status=status)
        session.add(new_order)
        session.commit()
        return jsonify({"message": "Order created", "id": new_order.id}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

# Get all orders
@order_bp.route('/orders', methods=['GET'])
@swag_from({
    'tags': ['Orders'],
    'description': 'Retrieve all orders',
    'responses': {
        '200': {'description': 'List of orders'}
    }
})
def get_orders():
    session = app.Session()
    try:
        orders = session.query(Order).all()
        result = [
            {
                "id": o.id,
                "table": o.table,
                "products": eval(o.products),  # Convert back to list
                "total": o.total,
                "status": o.status
            }
            for o in orders
        ]
        return jsonify(result), 200
    finally:
        session.close()

# Get order by ID
@order_bp.route('/orders/<int:id>', methods=['GET'])
@swag_from({
    'tags': ['Orders'],
    'description': 'Retrieve an order by ID',
    'parameters': [
        {'name': 'id', 'in': 'path', 'type': 'integer', 'required': True}
    ],
    'responses': {
        '200': {'description': 'Order data'},
        '404': {'description': 'Order not found'}
    }
})
def get_order(id):
    session = app.Session()
    try:
        order = session.query(Order).get(id)
        if order:
            result = {
                "id": order.id,
                "table": order.table,
                "products": eval(order.products),  # Convert back to list
                "total": order.total,
                "status": order.status
            }
            return jsonify(result), 200
        return jsonify({"message": "Order not found"}), 404
    finally:
        session.close()

# Update an order
@order_bp.route('/orders/<int:id>', methods=['PUT'])
@swag_from({
    'tags': ['Orders'],
    'description': 'Update an order by ID',
    'parameters': [
        {'name': 'id', 'in': 'path', 'type': 'integer', 'required': True},
        {'name': 'body', 'in': 'body', 'required': True, 'schema': {'table': 'int', 'products': 'list', 'total': 'float', 'status': 'str'}}
    ],
    'responses': {
        '200': {'description': 'Order updated successfully'},
        '404': {'description': 'Order not found'}
    }
})
def update_order(id):
    data = request.get_json()
    session = app.Session()
    try:
        order = session.query(Order).get(id)
        if not order:
            return jsonify({"message": "Order not found"}), 404

        order.table = data.get('table', order.table)
        order.products = str(data.get('products', eval(order.products)))  # Convert list to string
        order.total = data.get('total', order.total)
        order.status = data.get('status', order.status)
        session.commit()
        return jsonify({"message": "Order updated"}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

# Delete an order
@order_bp.route('/orders/<int:id>', methods=['DELETE'])
@swag_from({
    'tags': ['Orders'],
    'description': 'Delete an order by ID',
    'parameters': [
        {'name': 'id', 'in': 'path', 'type': 'integer', 'required': True}
    ],
    'responses': {
        '204': {'description': 'Order deleted successfully'},
        '404': {'description': 'Order not found'}
    }
})
def delete_order(id):
    session = app.Session()
    try:
        order = session.query(Order).get(id)
        if not order:
            return jsonify({"message": "Order not found"}), 404

        session.delete(order)
        session.commit()
        return jsonify({"message": "Order deleted"}), 204
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()
