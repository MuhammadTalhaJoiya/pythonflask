from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from main import db
from datetime import datetime

subscription_bp = Blueprint('subscription', __name__)

@subscription_bp.route('/tiers', methods=['GET'])
@jwt_required()
def get_tiers():
    # Hardcoded tiers for now
    tiers = ['basic', 'premium', 'family']
    return jsonify({'tiers': tiers}), 200

@subscription_bp.route('/start', methods=['POST'])
@jwt_required()
def start_subscription():
    current_user = int(get_jwt_identity())
    User = current_app.config.get('User')
    FamilyMember = current_app.config.get('FamilyMember')
    Subscription = current_app.config.get('Subscription')
    data = request.get_json()
    family_id = data.get('family_id')
    tier = data.get('tier')
    if not family_id or not tier:
        return jsonify({'error': 'family_id and tier are required'}), 400
    family_member = FamilyMember.query.get(family_id)
    if not family_member or family_member.user_id != current_user:
        return jsonify({'error': 'Unauthorized'}), 403
    subscription = Subscription(family_id=family_id, tier=tier)
    db.session.add(subscription)
    db.session.commit()
    return jsonify({'message': 'Subscription started', 'subscription_id': subscription.id}), 201

@subscription_bp.route('/pause', methods=['POST'])
@jwt_required()
def pause_subscription():
    current_user = int(get_jwt_identity())
    User = current_app.config.get('User')
    Subscription = current_app.config.get('Subscription')
    data = request.get_json()
    subscription_id = data.get('subscription_id')
    if not subscription_id:
        return jsonify({'error': 'subscription_id required'}), 400
    subscription = Subscription.query.get(subscription_id)
    if not subscription or subscription.family_member.user_id != current_user:
        return jsonify({'error': 'Unauthorized'}), 403
    subscription.status = 'paused'
    subscription.pause_date = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Subscription paused'}), 200

@subscription_bp.route('/resume', methods=['POST'])
@jwt_required()
def resume_subscription():
    current_user = int(get_jwt_identity())
    User = current_app.config.get('User')
    Subscription = current_app.config.get('Subscription')
    data = request.get_json()
    subscription_id = data.get('subscription_id')
    if not subscription_id:
        return jsonify({'error': 'subscription_id required'}), 400
    subscription = Subscription.query.get(subscription_id)
    if not subscription or subscription.family_member.user_id != current_user:
        return jsonify({'error': 'Unauthorized'}), 403
    subscription.status = 'active'
    subscription.resume_date = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Subscription resumed'}), 200

@subscription_bp.route('/modify', methods=['POST'])
@jwt_required()
def modify_subscription():
    current_user = int(get_jwt_identity())
    User = current_app.config.get('User')
    Subscription = current_app.config.get('Subscription')
    data = request.get_json()
    subscription_id = data.get('subscription_id')
    new_tier = data.get('new_tier')
    if not subscription_id or not new_tier:
        return jsonify({'error': 'subscription_id and new_tier required'}), 400
    subscription = Subscription.query.get(subscription_id)
    if not subscription or subscription.family_member.user_id != current_user:
        return jsonify({'error': 'Unauthorized'}), 403
    subscription.tier = new_tier
    db.session.commit()
    return jsonify({'message': 'Subscription modified'}), 200

@subscription_bp.route('/add-product', methods=['POST'])
@jwt_required()
def add_product():
    current_user = int(get_jwt_identity())
    User = current_app.config.get('User')
    Subscription = current_app.config.get('Subscription')
    SubscriptionProduct = current_app.config.get('SubscriptionProduct')
    Supplement = current_app.config.get('Supplement')
    data = request.get_json()
    subscription_id = data.get('subscription_id')
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    if not subscription_id or not product_id:
        return jsonify({'error': 'subscription_id and product_id required'}), 400
    subscription = Subscription.query.get(subscription_id)
    if not subscription or subscription.family_member.user_id != current_user:
        return jsonify({'error': 'Unauthorized'}), 403
    product = Supplement.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    sub_product = SubscriptionProduct(subscription_id=subscription_id, product_id=product_id, quantity=quantity)
    db.session.add(sub_product)
    db.session.commit()
    return jsonify({'message': 'Product added', 'product_id': sub_product.id}), 201

@subscription_bp.route('/status/<int:family_id>', methods=['GET'])
@jwt_required()
def get_status(family_id):
    current_user = int(get_jwt_identity())
    User = current_app.config.get('User')
    FamilyMember = current_app.config.get('FamilyMember')
    Subscription = current_app.config.get('Subscription')
    family_member = FamilyMember.query.get(family_id)
    if not family_member or family_member.user_id != current_user:
        return jsonify({'error': 'Unauthorized'}), 403
    subscriptions = Subscription.query.filter_by(family_id=family_id).all()
    result = [{'id': s.id, 'tier': s.tier, 'status': s.status, 'start_date': s.start_date.isoformat()} for s in subscriptions]
    return jsonify(result), 200

@subscription_bp.route('/history/<int:family_id>', methods=['GET'])
@jwt_required()
def get_history(family_id):
    current_user = int(get_jwt_identity())
    User = current_app.config.get('User')
    FamilyMember = current_app.config.get('FamilyMember')
    Subscription = current_app.config.get('Subscription')
    family_member = FamilyMember.query.get(family_id)
    if not family_member or family_member.user_id != current_user:
        return jsonify({'error': 'Unauthorized'}), 403
    subscriptions = Subscription.query.filter_by(family_id=family_id).order_by(Subscription.created_at.desc()).all()
    result = [{'id': s.id, 'tier': s.tier, 'status': s.status, 'start_date': s.start_date.isoformat(), 'pause_date': s.pause_date.isoformat() if s.pause_date else None, 'resume_date': s.resume_date.isoformat() if s.resume_date else None} for s in subscriptions]
    return jsonify(result), 200