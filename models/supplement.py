from datetime import datetime

def get_supplement_model(db):
    class Supplement(db.Model):
        __tablename__ = 'supplements'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        description = db.Column(db.Text, nullable=True)
        dosage = db.Column(db.String(50), nullable=True)
        stock_level = db.Column(db.Integer, default=0)
        low_stock_threshold = db.Column(db.Integer, default=5)
        image_url = db.Column(db.String(255), nullable=True)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
        
    return Supplement

# This will be set by main.py or another initialization point
Supplement = None

def get_supplement_intake_model(db):
    class SupplementIntake(db.Model):
        __tablename__ = 'supplement_intakes'
        id = db.Column(db.Integer, primary_key=True)
        supplement_id = db.Column(db.Integer, db.ForeignKey('supplements.id'), nullable=False)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
        family_member_id = db.Column(db.Integer, db.ForeignKey('family_members.id'), nullable=True)
        taken_at = db.Column(db.DateTime, default=datetime.utcnow)
        dosage_taken = db.Column(db.String(50), nullable=True)
        notes = db.Column(db.Text, nullable=True)
        photo_confirmation = db.Column(db.String(255), nullable=True)  # Path to photo
        
    return SupplementIntake

# This will be set by main.py or another initialization point
SupplementIntake = None

def get_reminder_model(db):
    class Reminder(db.Model):
        __tablename__ = 'reminders'
        id = db.Column(db.Integer, primary_key=True)
        supplement_id = db.Column(db.Integer, db.ForeignKey('supplements.id'), nullable=False)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
        family_member_id = db.Column(db.Integer, db.ForeignKey('family_members.id'), nullable=True)
        time = db.Column(db.Time, nullable=False)
        days = db.Column(db.String(50), nullable=False)  # e.g., 'Mon,Tue,Wed'
        active = db.Column(db.Boolean, default=True)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        
    return Reminder

# This will be set by main.py or another initialization point
Reminder = None