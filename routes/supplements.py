from flask import Blueprint, request, jsonify, current_app, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from main import db
from datetime import datetime, date
import os
from werkzeug.utils import secure_filename

supplements_bp = Blueprint('supplements', __name__)

# Create a new supplement
@supplements_bp.route('/create', methods=['POST'])
@jwt_required()
def create_supplement():
    from flask import current_app
    current_user = int(get_jwt_identity())
    User = current_app.config.get('User')
    Supplement = current_app.config.get('Supplement')
    
    user = User.query.get(current_user)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    dosage = data.get('dosage')
    stock_level = data.get('stock_level', 0)
    low_stock_threshold = data.get('low_stock_threshold', 5)
    image_url = data.get('image_url')
    
    if not name:
        return jsonify({'error': 'Supplement name is required'}), 400
    
    supplement = Supplement(
        name=name,
        description=description,
        dosage=dosage,
        stock_level=stock_level,
        low_stock_threshold=low_stock_threshold,
        image_url=image_url,
        user_id=current_user
    )
    
    db.session.add(supplement)
    db.session.commit()
    
    return jsonify({
        'message': 'Supplement created successfully',
        'supplement_id': supplement.id,
        'name': supplement.name
    }), 201

# Get all supplements
@supplements_bp.route('/all', methods=['GET'])
@jwt_required()
def get_all_supplements():
    from flask import current_app
    current_user = int(get_jwt_identity())
    User = current_app.config.get('User')
    Supplement = current_app.config.get('Supplement')
    
    user = User.query.get(current_user)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    supplements = Supplement.query.filter_by(user_id=current_user).all()
    result = []
    for supplement in supplements:
        result.append({
            'id': supplement.id,
            'name': supplement.name,
            'description': supplement.description,
            'dosage': supplement.dosage,
            'stock_level': supplement.stock_level,
            'low_stock_threshold': supplement.low_stock_threshold,
            'image_url': supplement.image_url,
            'created_at': supplement.created_at.isoformat()
        })
    
    return jsonify(result), 200

# Update an existing supplement
@supplements_bp.route('/update/<int:supplement_id>', methods=['PUT'])
@jwt_required()
def update_supplement(supplement_id):
    from flask import current_app
    current_user = int(get_jwt_identity())
    User = current_app.config.get('User')
    Supplement = current_app.config.get('Supplement')
    
    user = User.query.get(current_user)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    supplement = Supplement.query.get(supplement_id)
    if not supplement:
        return jsonify({'error': 'Supplement not found'}), 404
        
    if supplement.user_id != current_user:
        return jsonify({'error': 'Unauthorized access to supplement'}), 403
    
    data = request.get_json()
    
    if 'name' in data:
        supplement.name = data['name']
    if 'description' in data:
        supplement.description = data['description']
    if 'dosage' in data:
        supplement.dosage = data['dosage']
    if 'stock_level' in data:
        supplement.stock_level = data['stock_level']
    if 'low_stock_threshold' in data:
        supplement.low_stock_threshold = data['low_stock_threshold']
    if 'image_url' in data:
        supplement.image_url = data['image_url']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Supplement updated successfully',
        'supplement_id': supplement.id,
        'name': supplement.name
    }), 200

# Delete a supplement
@supplements_bp.route('/delete/<int:supplement_id>', methods=['DELETE'])
@jwt_required()
def delete_supplement(supplement_id):
    from flask import current_app
    current_user = int(get_jwt_identity())
    User = current_app.config.get('User')
    Supplement = current_app.config.get('Supplement')
    
    user = User.query.get(current_user)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    supplement = Supplement.query.get(supplement_id)
    if not supplement:
        return jsonify({'error': 'Supplement not found'}), 404
        
    if supplement.user_id != current_user:
        return jsonify({'error': 'Unauthorized access to supplement'}), 403
    
    db.session.delete(supplement)
    db.session.commit()
    
    return jsonify({
        'message': 'Supplement deleted successfully'
    }), 200

# Log supplement intake
@supplements_bp.route('/log-intake', methods=['POST'])
@jwt_required()
def log_supplement_intake():
    from flask import current_app
    current_user = int(get_jwt_identity())
    User = current_app.config.get('User')
    Supplement = current_app.config.get('Supplement')
    SupplementIntake = current_app.config.get('SupplementIntake')
    FamilyMember = current_app.config.get('FamilyMember')
    
    user = User.query.get(current_user)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    supplement_id = data.get('supplement_id')
    family_member_id = data.get('family_member_id')
    dosage_taken = data.get('dosage_taken')
    notes = data.get('notes')
    
    supplement = Supplement.query.get(supplement_id)
    if not supplement:
        return jsonify({'error': 'Supplement not found'}), 404
    
    if supplement.user_id != current_user:
        return jsonify({'error': 'Unauthorized access to supplement'}), 403
    
    # Verify family member if provided
    if family_member_id:
        family_member = FamilyMember.query.get(family_member_id)
        if not family_member or family_member.user_id != current_user:
            return jsonify({'error': 'Family member not found or not associated with user'}), 404
    
    # Create intake record
    intake = SupplementIntake(
        supplement_id=supplement_id,
        user_id=current_user,
        family_member_id=family_member_id,
        dosage_taken=dosage_taken,
        notes=notes
    )
    
    # Update stock level
    if supplement.stock_level > 0:
        supplement.stock_level -= 1
    
    db.session.add(intake)
    db.session.commit()
    
    return jsonify({
        'message': 'Supplement intake logged successfully',
        'intake_id': intake.id,
        'taken_at': intake.taken_at.isoformat()
    }), 201

# Get today's intake for a member
@supplements_bp.route('/today-intake/<int:member_id>', methods=['GET'])
@jwt_required()
def get_today_intake(member_id):
    from flask import current_app
    current_user = int(get_jwt_identity())
    User = current_app.config.get('User')
    SupplementIntake = current_app.config.get('SupplementIntake')
    Supplement = current_app.config.get('Supplement')
    FamilyMember = current_app.config.get('FamilyMember')
    
    user = User.query.get(current_user)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Check if member_id is valid (either current user or a family member)
    if member_id != current_user:
        family_member = FamilyMember.query.get(member_id)
        if not family_member or family_member.user_id != current_user:
            return jsonify({'error': 'Unauthorized access to member data'}), 403
    
    # Get today's date
    today = date.today()
    
    # Query intakes for today
    if member_id == current_user:
        intakes = SupplementIntake.query.filter(
            SupplementIntake.user_id == current_user,
            SupplementIntake.family_member_id.is_(None),
            db.func.date(SupplementIntake.taken_at) == today
        ).all()
    else:
        intakes = SupplementIntake.query.filter(
            SupplementIntake.family_member_id == member_id,
            db.func.date(SupplementIntake.taken_at) == today
        ).all()
    
    result = []
    for intake in intakes:
        supplement = Supplement.query.get(intake.supplement_id)
        result.append({
            'id': intake.id,
            'supplement_id': intake.supplement_id,
            'supplement_name': supplement.name if supplement else 'Unknown',
            'dosage_taken': intake.dosage_taken,
            'taken_at': intake.taken_at.isoformat(),
            'notes': intake.notes,
            'photo_confirmation': intake.photo_confirmation
        })
    
    return jsonify(result), 200

# Upload supplement image
@supplements_bp.route('/upload-image/<int:supplement_id>', methods=['POST'])
@jwt_required()
def upload_supplement_image(supplement_id):
    from flask import current_app
    current_user = int(get_jwt_identity())
    User = current_app.config.get('User')
    Supplement = current_app.config.get('Supplement')
    
    user = User.query.get(current_user)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    supplement = Supplement.query.get(supplement_id)
    if not supplement:
        return jsonify({'error': 'Supplement not found'}), 404
    
    if supplement.user_id != current_user:
        return jsonify({'error': 'Unauthorized access to supplement'}), 403
    
    # Check if the request has the file part
    if 'image' not in request.files:
        return jsonify({'error': 'No image part in the request'}), 400
    
    image = request.files['image']
    if image.filename == '':
        return jsonify({'error': 'No image selected for uploading'}), 400
    
    # Create uploads directory if it doesn't exist
    uploads_dir = os.path.join(current_app.root_path, 'uploads', 'supplements')
    os.makedirs(uploads_dir, exist_ok=True)
    
    # Save the file
    filename = secure_filename(f"supplement_{supplement_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg")
    image_path = os.path.join(uploads_dir, filename)
    image.save(image_path)
    
    # Update the supplement record with the image URL
    # Store the relative path to the file
    relative_path = f'/uploads/supplements/{filename}'
    supplement.image_url = relative_path
    db.session.commit()
    
    return jsonify({
        'message': 'Supplement image uploaded successfully',
        'image_url': relative_path
    }), 201

# Upload photo confirmation
@supplements_bp.route('/photo-confirmation', methods=['POST'])
@jwt_required()
def upload_photo_confirmation():
    from flask import current_app
    current_user = int(get_jwt_identity())
    User = current_app.config.get('User')
    SupplementIntake = current_app.config.get('SupplementIntake')
    
    user = User.query.get(current_user)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    intake_id = request.form.get('intake_id')
    if not intake_id:
        return jsonify({'error': 'Intake ID is required'}), 400
    
    intake = SupplementIntake.query.get(intake_id)
    if not intake:
        return jsonify({'error': 'Intake record not found'}), 404
    
    if intake.user_id != current_user:
        return jsonify({'error': 'Unauthorized access to intake record'}), 403
    
    # Check if the request has the file part
    if 'photo' not in request.files:
        return jsonify({'error': 'No photo part in the request'}), 400
    
    photo = request.files['photo']
    if photo.filename == '':
        return jsonify({'error': 'No photo selected for uploading'}), 400
    
    # Create uploads directory if it doesn't exist
    uploads_dir = os.path.join(current_app.root_path, 'uploads', 'supplements')
    os.makedirs(uploads_dir, exist_ok=True)
    
    # Save the file
    filename = secure_filename(f"{current_user}_{intake_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg")
    photo_path = os.path.join(uploads_dir, filename)
    photo.save(photo_path)
    
    # Update the intake record
    intake.photo_confirmation = filename
    db.session.commit()
    
    return jsonify({
        'message': 'Photo confirmation uploaded successfully',
        'photo_path': filename
    }), 201

# Set reminder settings
@supplements_bp.route('/reminder-settings', methods=['POST'])
@jwt_required()
def set_reminder_settings():
    from flask import current_app
    current_user = int(get_jwt_identity())
    User = current_app.config.get('User')
    Supplement = current_app.config.get('Supplement')
    Reminder = current_app.config.get('Reminder')
    FamilyMember = current_app.config.get('FamilyMember')
    
    user = User.query.get(current_user)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    supplement_id = data.get('supplement_id')
    family_member_id = data.get('family_member_id')
    time = data.get('time')  # Format: 'HH:MM'
    days = data.get('days')  # Format: 'Mon,Tue,Wed'
    
    if not supplement_id or not time or not days:
        return jsonify({'error': 'Missing required fields'}), 400
    
    supplement = Supplement.query.get(supplement_id)
    if not supplement:
        return jsonify({'error': 'Supplement not found'}), 404
    
    if supplement.user_id != current_user:
        return jsonify({'error': 'Unauthorized access to supplement'}), 403
    
    # Verify family member if provided
    if family_member_id:
        family_member = FamilyMember.query.get(family_member_id)
        if not family_member or family_member.user_id != current_user:
            return jsonify({'error': 'Family member not found or not associated with user'}), 404
    
    # Parse time string to Time object
    try:
        time_obj = datetime.strptime(time, '%H:%M').time()
    except ValueError:
        return jsonify({'error': 'Invalid time format. Use HH:MM'}), 400
    
    # Create or update reminder
    reminder = Reminder.query.filter_by(
        supplement_id=supplement_id,
        user_id=current_user,
        family_member_id=family_member_id
    ).first()
    
    if reminder:
        reminder.time = time_obj
        reminder.days = days
        reminder.active = True
    else:
        reminder = Reminder(
            supplement_id=supplement_id,
            user_id=current_user,
            family_member_id=family_member_id,
            time=time_obj,
            days=days
        )
        db.session.add(reminder)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Reminder settings saved successfully',
        'reminder_id': reminder.id
    }), 201

# Get supplement stats for a member
@supplements_bp.route('/stats/<int:member_id>', methods=['GET'])
@jwt_required()
def get_supplement_stats(member_id):
    from flask import current_app
    current_user = int(get_jwt_identity())
    User = current_app.config.get('User')
    SupplementIntake = current_app.config.get('SupplementIntake')
    Supplement = current_app.config.get('Supplement')
    FamilyMember = current_app.config.get('FamilyMember')
    
    user = User.query.get(current_user)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Check if member_id is valid (either current user or a family member)
    if member_id != current_user:
        family_member = FamilyMember.query.get(member_id)
        if not family_member or family_member.user_id != current_user:
            return jsonify({'error': 'Unauthorized access to member data'}), 403
    
    # Get all supplements for the user
    supplements = Supplement.query.filter_by(user_id=current_user).all()
    
    # Calculate stats for each supplement
    stats = []
    for supplement in supplements:
        # Query intakes for this supplement and member
        if member_id == current_user:
            intakes = SupplementIntake.query.filter(
                SupplementIntake.supplement_id == supplement.id,
                SupplementIntake.user_id == current_user,
                SupplementIntake.family_member_id.is_(None)
            ).all()
        else:
            intakes = SupplementIntake.query.filter(
                SupplementIntake.supplement_id == supplement.id,
                SupplementIntake.family_member_id == member_id
            ).all()
        
        # Calculate adherence rate (last 30 days)
        thirty_days_ago = datetime.now() - db.func.interval(30, 'day')
        recent_intakes = [i for i in intakes if i.taken_at >= thirty_days_ago]
        adherence_rate = len(recent_intakes) / 30 * 100 if recent_intakes else 0
        
        stats.append({
            'supplement_id': supplement.id,
            'supplement_name': supplement.name,
            'total_intakes': len(intakes),
            'adherence_rate': round(adherence_rate, 2),
            'last_taken': intakes[-1].taken_at.isoformat() if intakes else None
        })
    
    return jsonify(stats), 200

# Get low stock alerts
@supplements_bp.route('/low-stock-alerts', methods=['GET'])
@jwt_required()
def get_low_stock_alerts():
    from flask import current_app
    current_user = int(get_jwt_identity())
    User = current_app.config.get('User')
    Supplement = current_app.config.get('Supplement')
    
    user = User.query.get(current_user)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Find supplements with stock below threshold
    low_stock_supplements = Supplement.query.filter(
        Supplement.user_id == current_user,
        Supplement.stock_level <= Supplement.low_stock_threshold
    ).all()
    
    alerts = []
    for supplement in low_stock_supplements:
        alerts.append({
            'supplement_id': supplement.id,
            'supplement_name': supplement.name,
            'current_stock': supplement.stock_level,
            'threshold': supplement.low_stock_threshold
        })
    
    return jsonify(alerts), 200

# Get supplement intake history for a member
@supplements_bp.route('/history/<int:member_id>', methods=['GET'])
@jwt_required()
def get_supplement_history(member_id):
    from flask import current_app
    current_user = int(get_jwt_identity())
    User = current_app.config.get('User')
    SupplementIntake = current_app.config.get('SupplementIntake')
    Supplement = current_app.config.get('Supplement')
    FamilyMember = current_app.config.get('FamilyMember')
    
    user = User.query.get(current_user)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Check if member_id is valid (either current user or a family member)
    if member_id != current_user:
        family_member = FamilyMember.query.get(member_id)
        if not family_member or family_member.user_id != current_user:
            return jsonify({'error': 'Unauthorized access to member data'}), 403
    
    # Get query parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    supplement_id = request.args.get('supplement_id')
    
    # Build query
    query = SupplementIntake.query
    
    if member_id == current_user:
        query = query.filter(
            SupplementIntake.user_id == current_user,
            SupplementIntake.family_member_id.is_(None)
        )
    else:
        query = query.filter(SupplementIntake.family_member_id == member_id)
    
    if supplement_id:
        query = query.filter(SupplementIntake.supplement_id == supplement_id)
    
    if start_date:
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            query = query.filter(db.func.date(SupplementIntake.taken_at) >= start_date_obj)
        except ValueError:
            return jsonify({'error': 'Invalid start_date format. Use YYYY-MM-DD'}), 400
    
    if end_date:
        try:
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            query = query.filter(db.func.date(SupplementIntake.taken_at) <= end_date_obj)
        except ValueError:
            return jsonify({'error': 'Invalid end_date format. Use YYYY-MM-DD'}), 400
    
    # Order by taken_at descending
    intakes = query.order_by(SupplementIntake.taken_at.desc()).all()
    
    result = []
    for intake in intakes:
        supplement = Supplement.query.get(intake.supplement_id)
        result.append({
            'id': intake.id,
            'supplement_id': intake.supplement_id,
            'supplement_name': supplement.name if supplement else 'Unknown',
            'dosage_taken': intake.dosage_taken,
            'taken_at': intake.taken_at.isoformat(),
            'notes': intake.notes,
            'photo_confirmation': intake.photo_confirmation
        })
    
    return jsonify(result), 200