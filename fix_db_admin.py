#!/usr/bin/env python3
"""
Fix Admin Permissions in Database
"""

from main import create_app
from models.user import get_user_model
from werkzeug.security import generate_password_hash

def fix_admin_permissions():
    app = create_app()
    with app.app_context():
        from main import db
        User = get_user_model(db)
        
        # Check current users
        users = User.query.all()
        print('Current users:')
        for user in users:
            print(f'  ID: {user.id}, Email: {user.email}, Role: {user.role}')
        
        # Update admin user
        admin_user = User.query.filter_by(email='admin@example.com').first()
        if admin_user:
            admin_user.role = 'admin'
            admin_user.verified = True
            db.session.commit()
            print(f'✅ Updated {admin_user.email} to admin role')
        else:
            # Create admin user
            admin_user = User(name='Admin User', email='admin@example.com')
            admin_user.set_password('adminpassword')
            admin_user.role = 'admin'
            admin_user.verified = True
            db.session.add(admin_user)
            db.session.commit()
            print('✅ Created admin user with admin role')
            
        # Verify
        updated_user = User.query.filter_by(email='admin@example.com').first()
        print(f'✅ Final role: {updated_user.role}')

if __name__ == "__main__":
    fix_admin_permissions()