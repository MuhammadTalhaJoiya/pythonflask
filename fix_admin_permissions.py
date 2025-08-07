#!/usr/bin/env python3
"""
Fix Admin Permissions Script

This script fixes the 403 Forbidden errors by ensuring the admin user has the correct 'admin' role.
It can be run directly to update the database and verify admin permissions.
"""

import os
import sys
import requests

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import app, db
from models.user import get_user_model

def fix_admin_role():
    """Ensure admin user has admin role"""
    
    with app.app_context():
        User = get_user_model(db)
        
        # Find or create admin user
        admin_email = "admin@example.com"
        admin_password = "adminpassword"
        
        # Check if admin user exists
        admin_user = User.query.filter_by(email=admin_email).first()
        
        if not admin_user:
            print("Creating admin user...")
            from werkzeug.security import generate_password_hash
            admin_user = User(
                name="Admin User",
                email=admin_email,
                password_hash=generate_password_hash(admin_password),
                role="admin",
                verified=True
            )
            db.session.add(admin_user)
            db.session.commit()
            print(f"✅ Admin user created with ID: {admin_user.id}")
        else:
            print(f"Found existing user: {admin_user.email} (ID: {admin_user.id})")
            
            # Ensure role is admin
            if admin_user.role != "admin":
                print("Updating user role to admin...")
                admin_user.role = "admin"
                admin_user.verified = True
                db.session.commit()
                print("✅ User role updated to admin")
            else:
                print("✅ User already has admin role")
        
        return admin_user.id

def test_admin_login():
    """Test admin login to get token"""
    
    login_data = {
        "email": "admin@example.com",
        "password": "adminpassword"
    }
    
    try:
        response = requests.post("http://127.0.0.1:5000/auth/login", json=login_data)
        if response.status_code == 200:
            token = response.json().get("access_token")
            print(f"✅ Admin login successful. Token: {token[:20]}...")
            return token
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return None

def test_admin_endpoints(token):
    """Test all admin endpoints with the token"""
    
    headers = {"Authorization": f"Bearer {token}"}
    base_url = "http://127.0.0.1:5000"
    
    endpoints = [
        ("GET", f"{base_url}/admin/users"),
        ("GET", f"{base_url}/admin/users/1"),
        ("GET", f"{base_url}/admin/orders"),
        ("GET", f"{base_url}/admin/products"),
        ("GET", f"{base_url}/admin/reports"),
        ("GET", f"{base_url}/admin/system/health"),
    ]
    
    print("\n🧪 Testing admin endpoints...")
    
    for method, url in endpoints:
        try:
            response = requests.request(method, url, headers=headers)
            if response.status_code == 200:
                print(f"✅ {method} {url.split('/')[-1]}: OK")
            elif response.status_code == 403:
                print(f"❌ {method} {url.split('/')[-1]}: 403 Forbidden")
            else:
                print(f"⚠️  {method} {url.split('/')[-1]}: {response.status_code}")
        except Exception as e:
            print(f"❌ {method} {url.split('/')[-1]}: Error - {e}")

def main():
    """Main function to fix admin permissions"""
    
    print("🔧 Fixing Admin Permissions")
    print("=" * 40)
    
    try:
        # Fix admin role
        admin_id = fix_admin_role()
        print(f"Admin user ID: {admin_id}")
        
        # Test login
        token = test_admin_login()
        
        if token:
            # Test endpoints
            test_admin_endpoints(token)
            
            print("\n✅ Admin permissions fixed successfully!")
            print("You can now use the admin token for testing:")
            print(f"Token: {token}")
            
            # Save token to file
            with open("admin_token.txt", "w") as f:
                f.write(token)
            print("Token saved to admin_token.txt")
        else:
            print("❌ Could not get admin token")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()