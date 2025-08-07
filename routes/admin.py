from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime
from sqlalchemy import desc, asc

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.before_request
@jwt_required()
def admin_required():
    user_id = get_jwt_identity()
    jwt_claims = get_jwt()
    user_role = jwt_claims.get('role')
    
    if user_role != 'admin':
        # Fallback to database check if role not in JWT (for backward compatibility)
        User = current_app.config['User']
        user = User.query.get(user_id)
        if not user or user.role != 'admin':
            return jsonify({'error': 'Admin access required', 'code': 'ADMIN_REQUIRED'}), 403

@admin_bp.route('/users', methods=['GET'])
def get_users():
    User = current_app.config['User']
    users = User.query.all()
    return jsonify([{'id': u.id, 'name': u.name, 'email': u.email, 'role': u.role} for u in users])

@admin_bp.route('/orders', methods=['GET'])
def get_orders():
    Order = current_app.config['Order']
    
    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    
    # Filtering parameters
    status_filter = request.args.get('status')
    user_id = request.args.get('user_id', type=int)
    sort_by = request.args.get('sort_by', 'created_at')
    sort_order = request.args.get('sort_order', 'desc')
    
    # Base query
    query = Order.query
    
    # Apply filters
    if status_filter:
        query = query.filter(Order.status == status_filter)
    
    if user_id:
        query = query.filter(Order.user_id == user_id)
    
    # Apply sorting
    sort_column = getattr(Order, sort_by, Order.created_at)
    if sort_order.lower() == 'asc':
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))
    
    # Pagination
    total = query.count()
    orders = query.offset((page - 1) * per_page).limit(per_page).all()
    
    return jsonify({
        'orders': [{
            'id': o.id,
            'user_id': o.user_id,
            'product_id': o.product_id,
            'quantity': o.quantity,
            'status': o.status,
            'created_at': o.created_at.isoformat() if hasattr(o, 'created_at') else None,
            'total_price': o.total_price if hasattr(o, 'total_price') else None
        } for o in orders],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page
        }
    })

@admin_bp.route('/product/update', methods=['POST'])
def update_product():
    Product = current_app.config['Product']
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided', 'code': 'NO_DATA'}), 400
    
    product_id = data.get('id')
    if not product_id:
        return jsonify({'error': 'Product ID is required', 'code': 'MISSING_ID'}), 400
    
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found', 'code': 'PRODUCT_NOT_FOUND'}), 404
    
    # Validate and update fields
    updated_fields = []
    
    if 'name' in data:
        if not isinstance(data['name'], str) or not data['name'].strip():
            return jsonify({'error': 'Name must be a non-empty string', 'code': 'INVALID_NAME'}), 400
        product.name = data['name'].strip()
        updated_fields.append('name')
    
    if 'description' in data:
        if not isinstance(data['description'], str):
            return jsonify({'error': 'Description must be a string', 'code': 'INVALID_DESCRIPTION'}), 400
        product.description = data['description']
        updated_fields.append('description')
    
    if 'price' in data:
        try:
            price = float(data['price'])
            if price < 0:
                return jsonify({'error': 'Price must be non-negative', 'code': 'INVALID_PRICE'}), 400
            product.price = price
            updated_fields.append('price')
        except (ValueError, TypeError):
            return jsonify({'error': 'Price must be a valid number', 'code': 'INVALID_PRICE'}), 400
    
    if 'stock' in data:
        try:
            stock = int(data['stock'])
            if stock < 0:
                return jsonify({'error': 'Stock must be non-negative', 'code': 'INVALID_STOCK'}), 400
            product.stock = stock
            updated_fields.append('stock')
        except (ValueError, TypeError):
            return jsonify({'error': 'Stock must be a valid integer', 'code': 'INVALID_STOCK'}), 400
    
    if not updated_fields:
        return jsonify({'error': 'No valid fields to update', 'code': 'NO_UPDATES'}), 400
    
    try:
        from main import db
        db.session.commit()
        return jsonify({
            'message': 'Product updated successfully',
            'product_id': product.id,
            'updated_fields': updated_fields,
            'product': {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'stock': product.stock
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update product', 'code': 'UPDATE_FAILED', 'details': str(e)}), 500

@admin_bp.route('/reports', methods=['GET'])
def get_reports():
    User = current_app.config['User']
    Order = current_app.config['Order']
    Product = current_app.config['Product']
    
    # Basic counts
    total_users = User.query.count()
    total_orders = Order.query.count()
    total_products = Product.query.count()
    
    # User role distribution
    admin_users = User.query.filter_by(role='admin').count()
    regular_users = User.query.filter_by(role='user').count()
    
    # Order status distribution
    if hasattr(Order, 'status'):
        pending_orders = Order.query.filter_by(status='pending').count()
        completed_orders = Order.query.filter_by(status='completed').count()
        cancelled_orders = Order.query.filter_by(status='cancelled').count()
    else:
        pending_orders = completed_orders = cancelled_orders = 0
    
    # Recent activity (last 7 days)
    from datetime import datetime, timedelta
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    
    # Users created in last 7 days
    if hasattr(User, 'created_at'):
        recent_users = User.query.filter(User.created_at >= seven_days_ago).count()
    else:
        recent_users = 0
    
    # Orders created in last 7 days
    if hasattr(Order, 'created_at'):
        recent_orders = Order.query.filter(Order.created_at >= seven_days_ago).count()
    else:
        recent_orders = 0
    
    return jsonify({
        'overview': {
            'total_users': total_users,
            'total_orders': total_orders,
            'total_products': total_products
        },
        'user_distribution': {
            'admin_users': admin_users,
            'regular_users': regular_users
        },
        'order_distribution': {
            'pending': pending_orders,
            'completed': completed_orders,
            'cancelled': cancelled_orders
        },
        'recent_activity': {
            'users_last_7_days': recent_users,
            'orders_last_7_days': recent_orders
        }
    })

@admin_bp.route('/notifications/broadcast', methods=['POST'])
def broadcast_notification():
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided', 'code': 'NO_DATA'}), 400
    
    message = data.get('message')
    if not message or not isinstance(message, str) or not message.strip():
        return jsonify({'error': 'Message is required and must be a non-empty string', 'code': 'INVALID_MESSAGE'}), 400
    
    # Additional options
    target_audience = data.get('target_audience', 'all')  # 'all', 'admins', 'users'
    priority = data.get('priority', 'normal')  # 'low', 'normal', 'high', 'urgent'
    
    try:
        # In a real application, this would integrate with:
        # - Push notification service
        # - Email service
        # - SMS service
        # - WebSocket for real-time notifications
        
        # For now, we'll simulate the broadcast
        User = current_app.config['User']
        
        if target_audience == 'admins':
            target_count = User.query.filter_by(role='admin').count()
        elif target_audience == 'users':
            target_count = User.query.filter_by(role='user').count()
        else:
            target_count = User.query.count()
        
        return jsonify({
            'message': 'Broadcast notification sent successfully',
            'details': {
                'message': message.strip(),
                'target_audience': target_audience,
                'priority': priority,
                'recipients_count': target_count,
                'sent_at': datetime.utcnow().isoformat()
            }
        })
    except Exception as e:
        return jsonify({'error': 'Failed to send broadcast', 'code': 'BROADCAST_FAILED', 'details': str(e)}), 500

@admin_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    """Get detailed information about a specific user"""
    User = current_app.config['User']
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found', 'code': 'USER_NOT_FOUND'}), 404
    
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'role': user.role,
        'created_at': user.created_at.isoformat(),
        'verified': user.verified
    })

@admin_bp.route('/users/<int:user_id>/role', methods=['PUT'])
def update_user_role(user_id):
    """Update a user's role"""
    User = current_app.config['User']
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found', 'code': 'USER_NOT_FOUND'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided', 'code': 'NO_DATA'}), 400
    
    new_role = data.get('role')
    if not new_role or new_role not in ['user', 'admin']:
        return jsonify({'error': 'Role must be either "user" or "admin"', 'code': 'INVALID_ROLE'}), 400
    
    try:
        user.role = new_role
        from main import db
        db.session.commit()
        
        return jsonify({
            'message': 'User role updated successfully',
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'role': user.role
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update user role', 'code': 'UPDATE_FAILED', 'details': str(e)}), 500

@admin_bp.route('/products', methods=['GET'])
def get_products():
    """Get all products with pagination and filtering"""
    Product = current_app.config['Product']
    
    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    
    # Filtering parameters
    search = request.args.get('search')
    sort_by = request.args.get('sort_by', 'created_at')
    sort_order = request.args.get('sort_order', 'desc')
    
    # Base query
    query = Product.query
    
    # Apply search filter
    if search:
        search_term = f'%{search}%'
        query = query.filter(
            Product.name.ilike(search_term) | 
            Product.description.ilike(search_term)
        )
    
    # Apply sorting
    sort_column = getattr(Product, sort_by, Product.created_at)
    if sort_order.lower() == 'asc':
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))
    
    # Pagination
    total = query.count()
    products = query.offset((page - 1) * per_page).limit(per_page).all()
    
    return jsonify({
        'products': [{
            'id': p.id,
            'name': p.name,
            'description': p.description,
            'price': p.price,
            'stock': p.stock,
            'created_at': p.created_at.isoformat() if hasattr(p, 'created_at') else None
        } for p in products],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page
        }
    })

@admin_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product"""
    Product = current_app.config['Product']
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({'error': 'Product not found', 'code': 'PRODUCT_NOT_FOUND'}), 404
    
    try:
        from main import db
        db.session.delete(product)
        db.session.commit()
        
        return jsonify({
            'message': 'Product deleted successfully',
            'product_id': product_id
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete product', 'code': 'DELETE_FAILED', 'details': str(e)}), 500

@admin_bp.route('/system/health', methods=['GET'])
def system_health():
    """Get system health status"""
    try:
        User = current_app.config['User']
        Order = current_app.config['Order']
        Product = current_app.config['Product']
        
        # Check database connectivity
        db_status = "healthy"
        try:
            User.query.count()
        except Exception as e:
            db_status = f"unhealthy: {str(e)}"
        
        return jsonify({
            'status': 'ok' if db_status == "healthy" else 'error',
            'database': db_status,
            'timestamp': datetime.utcnow().isoformat(),
            'models': {
                'users': User.query.count(),
                'orders': Order.query.count(),
                'products': Product.query.count()
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'database': f'unhealthy: {str(e)}',
            'timestamp': datetime.utcnow().isoformat()
        }), 500