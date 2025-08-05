# D:\backendflask\project-root\models\family_member.py
from datetime import datetime

def get_family_member_model(db):
    class FamilyMember(db.Model):
        __tablename__ = 'family_members'
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
        name = db.Column(db.String(100), nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        status = db.Column(db.String(20), default='pending')  # e.g., 'pending', 'accepted'
        created_at = db.Column(db.DateTime, default=datetime.utcnow)

    return FamilyMember

# This will be set by main.py or another initialization point
FamilyMember = None