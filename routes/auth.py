# D:\backendflask\project-root\routes/auth.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from marshmallow import Schema, fields, ValidationError
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)  # Define blueprint at the top

# Validation Schemas
class UserSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=lambda n: len(n) >= 6)

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=lambda n: len(n) >= 6)

user_schema = UserSchema()
login_schema = LoginSchema()

# Signup Endpoint
@auth_bp.route('/signup', methods=['POST'])
def signup():
    from main import db
    from models.user import User
    try:
        data = user_schema.load(request.json)
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400

        user = User(name=data['name'], email=data['email'])
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()

        return jsonify({
            'message': 'User registered successfully',
            'user': {'id': user.id, 'name': user.name, 'email': user.email}
        }), 201

    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Login Endpoint
@auth_bp.route('/login', methods=['POST'])
def login():
    from main import db
    from models.user import User
    try:
        data = login_schema.load(request.json)
        
        user = User.query.filter_by(email=data['email']).first()
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401

        additional_claims = {"email": user.email}
        access_token = create_access_token(identity=str(user.id), additional_claims=additional_claims)
        refresh_token = create_refresh_token(identity=str(user.id), additional_claims=additional_claims)
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {'id': user.id, 'name': user.name, 'email': user.email}
        }), 200

    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Logout Endpoint
@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    from main import app
    jti = get_jwt()['jti']
    app.blocklist.add(jti)
    return jsonify({'message': 'Successfully logged out'}), 200

# Refresh Token Endpoint
@auth_bp.route('/refresh-token', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    from main import app
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify({'access_token': new_access_token}), 200

# Verify Email Endpoint (Mock)
@auth_bp.route('/verify-email', methods=['POST'])
@jwt_required()
def verify_email():
    from main import db, app
    from models.user import User
    current_user = int(get_jwt_identity())
    user = User.query.get(current_user)
    if user:
        user.verified = True
        db.session.commit()
        return jsonify({'message': 'Email verified successfully'}), 200
    return jsonify({'error': 'User not found'}), 404

# Forgot Password Endpoint (Mock)
@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')
    return jsonify({'message': f'Password reset link sent to {email}'}), 200

# Reset Password Endpoint
@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    from main import db
    from models.user import User
    data = request.get_json()
    email = data.get('email')
    new_password = data.get('password')
    user = User.query.filter_by(email=email).first()
    if user and new_password:
        user.set_password(new_password)
        db.session.commit()
        return jsonify({'message': 'Password reset successfully'}), 200
    return jsonify({'error': 'Invalid email or password'}), 400