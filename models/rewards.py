from datetime import datetime

def get_reward_model(db):
    class Reward(db.Model):
        __tablename__ = 'rewards'
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
        family_member_id = db.Column(db.Integer, db.ForeignKey('family_members.id'), nullable=True)
        points = db.Column(db.Integer, default=0)
        streak = db.Column(db.Integer, default=0)
        last_streak_date = db.Column(db.DateTime, nullable=True)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        
        user = db.relationship('User', backref='rewards')
        family_member = db.relationship('FamilyMember', backref='rewards')
    return Reward

def get_challenge_model(db):
    class Challenge(db.Model):
        __tablename__ = 'challenges'
        id = db.Column(db.Integer, primary_key=True)
        description = db.Column(db.Text, nullable=False)
        points = db.Column(db.Integer, nullable=False)
        is_active = db.Column(db.Boolean, default=True)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
    return Challenge

def get_referral_model(db):
    class Referral(db.Model):
        __tablename__ = 'referrals'
        id = db.Column(db.Integer, primary_key=True)
        referrer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
        referred_email = db.Column(db.String(120), nullable=False)
        status = db.Column(db.String(20), default='pending')
        bonus_points = db.Column(db.Integer, default=100)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        
        referrer = db.relationship('User', backref='referrals')
    return Referral

def get_reward_transaction_model(db):
    class RewardTransaction(db.Model):
        __tablename__ = 'reward_transactions'
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
        family_member_id = db.Column(db.Integer, db.ForeignKey('family_members.id'), nullable=True)
        points = db.Column(db.Integer, nullable=False)
        type = db.Column(db.String(50), nullable=False)
        description = db.Column(db.Text, nullable=True)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        
        user = db.relationship('User', backref='reward_transactions')
        family_member = db.relationship('FamilyMember', backref='reward_transactions')
    return RewardTransaction