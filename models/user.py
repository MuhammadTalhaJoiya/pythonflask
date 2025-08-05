# D:\backendflask\project-root\models\user.py
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

def get_user_model(db):
    class User(db.Model):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        password_hash = db.Column(db.String(255), nullable=False)  # Increased from 128 to 255
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        verified = db.Column(db.Boolean, default=False)

        def set_password(self, password):
            self.password_hash = generate_password_hash(password)

        def check_password(self, password):
            return check_password_hash(self.password_hash, password)
    return User

# This will be set by main.py or another initialization point
User = None