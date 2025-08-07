# D:\backendflask\project-root\main.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from models.user import get_user_model
from models.family_member import get_family_member_model
from models.supplement import get_supplement_model, get_supplement_intake_model, get_reminder_model
from models.subscription import get_subscription_model, get_subscription_product_model
from models.rewards import get_reward_model, get_challenge_model, get_referral_model, get_reward_transaction_model
from models.product import get_product_model
from models.order import get_order_model

load_dotenv()  # Load .env file

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

# Initialize models at module level
User = None
FamilyMember = None
Supplement = None
SupplementIntake = None
Reminder = None
Subscription = None
SubscriptionProduct = None
Reward = None
Challenge = None
Referral = None
RewardTransaction = None
Product = None
Order = None

def create_app():
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
    from routes.supplements import supplements_bp
    from routes.compliance import compliance_bp
    from routes.subscription import subscription_bp
    from routes.rewards import rewards_bp
    from routes.admin import admin_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(supplements_bp, url_prefix='/supplements')
    app.register_blueprint(compliance_bp, url_prefix='/compliance')
    app.register_blueprint(subscription_bp, url_prefix='/subscription')
    app.register_blueprint(rewards_bp, url_prefix='/rewards')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Set up models
    global User, FamilyMember, Supplement, SupplementIntake, Reminder, Subscription, SubscriptionProduct, Reward, Challenge, Referral, RewardTransaction, Product, Order
    User = get_user_model(db)
    FamilyMember = get_family_member_model(db)
    Supplement = get_supplement_model(db)
    SupplementIntake = get_supplement_intake_model(db)
    Reminder = get_reminder_model(db)
    Subscription = get_subscription_model(db)
    SubscriptionProduct = get_subscription_product_model(db)
    Reward = get_reward_model(db)
    Challenge = get_challenge_model(db)
    Referral = get_referral_model(db)
    RewardTransaction = get_reward_transaction_model(db)
    Product = get_product_model(db)
    Order = get_order_model(db)
    # Store models in app.config for access from routes
    app.config['User'] = User
    app.config['FamilyMember'] = FamilyMember
    app.config['Supplement'] = Supplement
    app.config['SupplementIntake'] = SupplementIntake
    app.config['Reminder'] = Reminder
    app.config['Subscription'] = Subscription
    app.config['SubscriptionProduct'] = SubscriptionProduct
    app.config['Reward'] = Reward
    app.config['Challenge'] = Challenge
    app.config['Referral'] = Referral
    app.config['RewardTransaction'] = RewardTransaction
    app.config['Product'] = Product
    app.config['Order'] = Order
    with app.app_context():
        db.create_all()
        # Seed sample challenges if none exist
        if Challenge.query.count() == 0:
            sample_challenges = [
                Challenge(description="Complete daily intake for a week", points=100),
                Challenge(description="Refer a friend", points=50),
                Challenge(description="Maintain streak for 30 days", points=200)
            ]
            db.session.add_all(sample_challenges)
            db.session.commit()
        # Seed admin user if none exists
        if User.query.filter_by(role='admin').count() == 0:
            admin_user = User(name='Admin User', email='admin@example.com')
            admin_user.set_password('adminpassword')
            admin_user.role = 'admin'
            admin_user.verified = True
            db.session.add(admin_user)
            db.session.commit()

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