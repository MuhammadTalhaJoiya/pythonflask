# D:\backendflask\project-root\main.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from urllib.parse import quote
from models.user import get_user_model
from models.family_member import get_family_member_model

load_dotenv()  # Load .env file

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    
    # Construct SQLALCHEMY_DATABASE_URI from environment variables
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', 'Hacker!@#123123')
    db_host = os.getenv('DB_HOST', '127.0.0.1')
    db_name = os.getenv('DB_NAME', 'mobile_app_backend')
    # URL encode the password to handle special characters like #
    encoded_password = quote(db_password)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{encoded_password}@{db_host}/{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secure-secret-key')
    app.config['JWT_BLOCKLIST_ENABLED'] = True
    app.config['JWT_BLOCKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Import and register blueprints after app initialization
    from routes.auth import auth_bp
    from routes.user import user_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')

    # Set up models
    global User, FamilyMember
    User = get_user_model(db)
    FamilyMember = get_family_member_model(db)
    with app.app_context():
        db.create_all()

    # JWT blocklist callback
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_data):
        jti = jwt_data['jti']
        return jti in app.blocklist

    # Initialize blocklist as a set
    app.blocklist = set()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)