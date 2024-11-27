from flask import Blueprint, request, jsonify, current_app as app
from models import Order, OrderItem, Product
from flasgger import swag_from

# Define a blueprint for order routes
order_bp = Blueprint('order_bp', __name__)

# Create a new order
@order_bp.route('/orders', methods=['POST'])
@swag_from({
    'tags': ['Orders'],
    'description': 'Create a new order',
    'parameters': [
        {'name': 'body', 'in': 'body', 'required': True, 'schema': {'table_number': 'int', 'products': 'list'}}
    ],
    'responses': {
        '201': {'description': 'Order created successfully'},
        '400': {'description': 'Invalid input'}
    }
})
def create_order():
    data = request.get_json()
    table_number = data.get('table_number')
    products = data.get('products')  # List of {id, quantity}

    if not table_number or not products:
        return jsonify({"error": "Table number and products are required"}), 400

    session = app.Session()
    print(f"Session initialized: {session}")

    try:
        # Calculate total
        total = 0
        order_items = []
        for item in products:
            product = session.query(Product).get(item['id'])
            if not product:
                return jsonify({"error": f"Product with ID {item['product_id']} not found"}), 400
            quantity = item.get('quantity', 1)
            total += product.price * quantity
            order_items.append(OrderItem(product_id=product.id, quantity=quantity))

        
        # Create the order
        new_order = Order(table_number=table_number, total=total, status='open')
        session.add(new_order)
        session.commit()

        print(new_order)

        # Add order items
        for order_item in order_items:
            order_item.order_id = new_order.id
            session.add(order_item)
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
                "table_number": o.table_number,
                "total": o.total,
                "status": o.status,
                "products": [
                    {
                        "product_id": item.product_id,
                        "name": item.product.name,
                        "quantity": item.quantity,
                        "price": item.product.price
                    }
                    for item in o.items
                ]
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
                "table_number": order.table_number,
                "total": order.total,
                "status": order.status,
                "products": [
                    {
                        "product_id": item.product_id,
                        "name": item.product.name,
                        "quantity": item.quantity,
                        "price": item.product.price
                    }
                    for item in order.items
                ]
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
        {'name': 'body', 'in': 'body', 'required': True, 'schema': {'table_number': 'int', 'products': 'list'}}
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

        # Update order fields
        order.table_number = data.get('table_number', order.table_number)
        order.status = data.get('status', order.status)

        # Update products (optional)
        if 'products' in data:
            # Remove existing items
            session.query(OrderItem).filter_by(order_id=order.id).delete()

            # Add new items
            products = data['products']
            total = 0
            for item in products:
                product = session.query(Product).get(item['product_id'])
                if not product:
                    return jsonify({"error": f"Product with ID {item['product_id']} not found"}), 400
                quantity = item.get('quantity', 1)
                total += product.price * quantity
                order_item = OrderItem(order_id=order.id, product_id=product.id, quantity=quantity)
                session.add(order_item)

            order.total = total
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
