from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
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
        # Try to add the image_url column to the supplements table
        db.session.execute(text('ALTER TABLE supplements ADD COLUMN image_url VARCHAR(255) NULL;'))
        db.session.commit()
        print('Column added successfully')
    except Exception as e:
        # If the column already exists, this will catch the error
        if 'Duplicate column name' in str(e):
            print('Column already exists')
        else:
            print(f'Error: {e}')