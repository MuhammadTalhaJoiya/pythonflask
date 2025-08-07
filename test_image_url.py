from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)

# Construct SQLALCHEMY_DATABASE_URI from environment variables
db_user = os.getenv('DB_USER', 'root')
db_password = os.getenv('DB_PASSWORD', 'Hacker!@#123123')
db_host = os.getenv('DB_HOST', '127.0.0.1')
db_name = os.getenv('DB_NAME', 'mobile_app_backend')

# URL encode the password to handle special characters
from urllib.parse import quote

# Handle host and port correctly
if ':' in db_host:
    host_parts = db_host.split(':')
    db_host = host_parts[0]
    db_port = host_parts[1]
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{quote(db_password)}@{db_host}:{db_port}/{db_name}'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{quote(db_password)}@{db_host}/{db_name}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define a simple Supplement model for testing
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

with app.app_context():
    try:
        # Try to create a test supplement with an image_url
        test_supplement = Supplement(
            name="Test Supplement",
            description="Test Description",
            dosage="1 tablet",
            stock_level=10,
            low_stock_threshold=2,
            image_url="https://example.com/test.jpg",
            user_id=1  # Make sure this user exists in your database
        )
        db.session.add(test_supplement)
        db.session.commit()
        print(f"Test supplement created with image_url: {test_supplement.image_url}")
        
        # Clean up - delete the test supplement
        db.session.delete(test_supplement)
        db.session.commit()
        print("Test supplement deleted")
    except Exception as e:
        print(f"Error: {e}")