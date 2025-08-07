from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, inspect
import os
from dotenv import load_dotenv

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

with app.app_context():
    try:
        # Get the inspector
        inspector = inspect(db.engine)
        
        # Get columns for the supplements table
        columns = inspector.get_columns('supplements')
        
        # Check if image_url column exists
        image_url_exists = any(column['name'] == 'image_url' for column in columns)
        
        if image_url_exists:
            print("image_url column exists in the supplements table")
            # Show all columns
            print("\nAll columns in supplements table:")
            for column in columns:
                print(f"- {column['name']}: {column['type']}")
        else:
            print("image_url column does NOT exist in the supplements table")
    except Exception as e:
        print(f"Error: {e}")