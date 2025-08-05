# D:\backendflask\project-root\routes/user.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from main import db  # Keep db for models

user_bp = Blueprint('user', __name__)

# Profile Endpoint
@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    from models.user import User
    current_user = int(get_jwt_identity())
    user = User.query.get(current_user)
    if user:
        return jsonify({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'verified': user.verified
        }), 200
    return jsonify({'error': 'User not found'}), 404

# Update Profile Endpoint
@user_bp.route('/profile/update', methods=['PUT'])
@jwt_required()
def update_profile():
    from models.user import User
    current_user = int(get_jwt_identity())
    user = User.query.get(current_user)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    db.session.commit()
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'verified': user.verified
    }), 200

# Invite Family Member Endpoint
@user_bp.route('/invite-family-member', methods=['POST'])
@jwt_required()
def invite_family_member():
    from models.family_member import FamilyMember
    from models.user import User
    current_user = int(get_jwt_identity())
    user = User.query.get(current_user)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    family_member = FamilyMember(user_id=current_user, name=data['name'], email=data['email'], status='pending')
    db.session.add(family_member)
    db.session.commit()
    return jsonify({
        'id': family_member.id,
        'user_id': family_member.user_id,
        'name': family_member.name,
        'email': family_member.email,
        'status': family_member.status
    }), 201

# Get Family Members Endpoint
@user_bp.route('/family-members', methods=['GET'])
@jwt_required()
def get_family_members():
    from models.family_member import FamilyMember
    from models.user import User
    current_user = int(get_jwt_identity())
    user = User.query.get(current_user)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    family_members = FamilyMember.query.filter_by(user_id=current_user).all()
    return jsonify([{
        'id': fm.id,
        'user_id': fm.user_id,
        'name': fm.name,
        'email': fm.email,
        'status': fm.status
    } for fm in family_members]), 200