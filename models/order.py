from datetime import datetime

def get_order_model(db):
    class Order(db.Model):
        __tablename__ = 'orders'
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
        product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
        quantity = db.Column(db.Integer, nullable=False)
        total_price = db.Column(db.Float, nullable=False)
        status = db.Column(db.String(50), default='pending')
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    return Order

Order = None