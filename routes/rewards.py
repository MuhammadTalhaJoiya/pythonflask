from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from main import db
from datetime import datetime, date

rewards_bp = Blueprint('rewards', __name__)

@rewards_bp.route('/balance', methods=['GET'])
@jwt_required()
def get_balance():
    current_user = int(get_jwt_identity())
    Reward = current_app.config.get('Reward')
    reward = Reward.query.filter_by(user_id=current_user).first()
    if not reward:
        return jsonify({'balance': 0}), 200
    return jsonify({'balance': reward.points}), 200

@rewards_bp.route('/earn', methods=['POST'])
@jwt_required()
def earn_points():
    current_user = int(get_jwt_identity())
    Reward = current_app.config.get('Reward')
    RewardTransaction = current_app.config.get('RewardTransaction')
    data = request.get_json()
    points = data.get('points')
    description = data.get('description')
    if not points:
        return jsonify({'error': 'points required'}), 400
    reward = Reward.query.filter_by(user_id=current_user).first()
    if not reward:
        reward = Reward(user_id=current_user, points=points)
        db.session.add(reward)
    else:
        reward.points += points
    transaction = RewardTransaction(user_id=current_user, points=points, type='earn', description=description)
    db.session.add(transaction)
    db.session.commit()
    return jsonify({'message': 'Points earned', 'new_balance': reward.points}), 200

@rewards_bp.route('/spend', methods=['POST'])
@jwt_required()
def spend_points():
    current_user = int(get_jwt_identity())
    Reward = current_app.config.get('Reward')
    RewardTransaction = current_app.config.get('RewardTransaction')
    data = request.get_json()
    points = data.get('points')
    description = data.get('description')
    if not points:
        return jsonify({'error': 'points required'}), 400
    reward = Reward.query.filter_by(user_id=current_user).first()
    if not reward or reward.points < points:
        return jsonify({'error': 'Insufficient points'}), 400
    reward.points -= points
    transaction = RewardTransaction(user_id=current_user, points=-points, type='spend', description=description)
    db.session.add(transaction)
    db.session.commit()
    return jsonify({'message': 'Points spent', 'new_balance': reward.points}), 200

@rewards_bp.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    current_user = int(get_jwt_identity())
    RewardTransaction = current_app.config.get('RewardTransaction')
    transactions = RewardTransaction.query.filter_by(user_id=current_user).order_by(RewardTransaction.created_at.desc()).all()
    result = [{'id': t.id, 'points': t.points, 'type': t.type, 'description': t.description, 'date': t.created_at.isoformat()} for t in transactions]
    return jsonify(result), 200

@rewards_bp.route('/streaks/<int:member_id>', methods=['GET'])
@jwt_required()
def get_streaks(member_id):
    current_user = int(get_jwt_identity())
    FamilyMember = current_app.config.get('FamilyMember')
    Reward = current_app.config.get('Reward')
    if member_id != current_user:
        family_member = FamilyMember.query.get(member_id)
        if not family_member or family_member.user_id != current_user:
            return jsonify({'error': 'Unauthorized'}), 403
    reward = Reward.query.filter_by(user_id=member_id).first()
    if not reward:
        return jsonify({'streak': 0}), 200
    return jsonify({'streak': reward.streak}), 200

@rewards_bp.route('/challenges', methods=['GET'])
@jwt_required()
def get_challenges():
    Challenge = current_app.config.get('Challenge')
    challenges = Challenge.query.filter_by(is_active=True).all()
    result = [{'id': c.id, 'description': c.description, 'points': c.points} for c in challenges]
    return jsonify(result), 200

@rewards_bp.route('/claim-challenge', methods=['POST'])
@jwt_required()
def claim_challenge():
    current_user = int(get_jwt_identity())
    Challenge = current_app.config.get('Challenge')
    Reward = current_app.config.get('Reward')
    RewardTransaction = current_app.config.get('RewardTransaction')
    data = request.get_json()
    challenge_id = data.get('challenge_id')
    challenge = Challenge.query.get(challenge_id)
    if not challenge or not challenge.is_active:
        return jsonify({'error': 'Invalid challenge'}), 400
    reward = Reward.query.filter_by(user_id=current_user).first()
    if not reward:
        reward = Reward(user_id=current_user, points=challenge.points)
        db.session.add(reward)
    else:
        reward.points += challenge.points
    transaction = RewardTransaction(user_id=current_user, points=challenge.points, type='challenge', description=f'Claimed challenge {challenge.description}')
    db.session.add(transaction)
    challenge.is_active = False  # Assuming one-time claim
    db.session.commit()
    return jsonify({'message': 'Challenge claimed', 'new_balance': reward.points}), 200

@rewards_bp.route('/refer-friend', methods=['POST'])
@jwt_required()
def refer_friend():
    current_user = int(get_jwt_identity())
    Referral = current_app.config.get('Referral')
    Reward = current_app.config.get('Reward')
    RewardTransaction = current_app.config.get('RewardTransaction')
    data = request.get_json()
    referred_email = data.get('referred_email')
    if not referred_email:
        return jsonify({'error': 'referred_email required'}), 400
    referral = Referral(referrer_id=current_user, referred_email=referred_email)
    db.session.add(referral)
    # Assuming bonus on referral creation, adjust as needed
    reward = Reward.query.filter_by(user_id=current_user).first()
    bonus = referral.bonus_points
    if not reward:
        reward = Reward(user_id=current_user, points=bonus)
        db.session.add(reward)
    else:
        reward.points += bonus
    transaction = RewardTransaction(user_id=current_user, points=bonus, type='referral', description=f'Referred {referred_email}')
    db.session.add(transaction)
    db.session.commit()
    return jsonify({'message': 'Friend referred', 'new_balance': reward.points}), 200