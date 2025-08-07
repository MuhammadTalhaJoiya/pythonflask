from datetime import datetime
import enum

def get_subscription_model(db):
    class Subscription(db.Model):
        __tablename__ = 'subscriptions'
        id = db.Column(db.Integer, primary_key=True)
        family_id = db.Column(db.Integer, db.ForeignKey('family_members.id'), nullable=False)
        tier = db.Column(db.String(50), nullable=False)
        status = db.Column(db.String(20), default='active')
        start_date = db.Column(db.DateTime, default=datetime.utcnow)
        pause_date = db.Column(db.DateTime, nullable=True)
        resume_date = db.Column(db.DateTime, nullable=True)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        
        family_member = db.relationship('FamilyMember', backref='subscriptions')
    return Subscription

def get_subscription_product_model(db):
    class SubscriptionProduct(db.Model):
        __tablename__ = 'subscription_products'
        id = db.Column(db.Integer, primary_key=True)
        subscription_id = db.Column(db.Integer, db.ForeignKey('subscriptions.id'), nullable=False)
        product_id = db.Column(db.Integer, db.ForeignKey('supplements.id'), nullable=False)  # Assuming product is supplement
        quantity = db.Column(db.Integer, default=1)
        added_at = db.Column(db.DateTime, default=datetime.utcnow)
        
        subscription = db.relationship('Subscription', backref='products')
        product = db.relationship('Supplement', backref='subscription_products')
    return SubscriptionProduct