#!/usr/bin/env python3
"""
Admin API Setup and Testing Script

This script helps you:
1. Ensure admin user exists with proper role
2. Test all updated admin APIs
3. Provide setup verification
"""

import requests
import json
import sys
import os

# Configuration
BASE_URL = 'http://127.0.0.1:5000'
ADMIN_EMAIL = 'admin@example.com'
ADMIN_PASSWORD = 'adminpassword'

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def print_colored(text, color):
    """Print colored text"""
    print(f"{color}{text}{Colors.RESET}")

def check_server_connection():
    """Check if the Flask server is running"""
    try:
        response = requests.get(f'{BASE_URL}/health', timeout=5)
        return response.status_code == 200
    except:
        return False

def create_admin_user():
    """Create admin user if it doesn't exist"""
    print_colored("🔧 Setting up admin user...", Colors.BLUE)
    
    # First, try to login
    login_data = {
        'email': ADMIN_EMAIL,
        'password': ADMIN_PASSWORD
    }
    
    try:
        response = requests.post(f'{BASE_URL}/auth/login', json=login_data)
        if response.status_code == 200:
            print_colored("✅ Admin user already exists and login successful", Colors.GREEN)
            return response.json()['access_token']
    except Exception as e:
        print_colored(f"❌ Error connecting to server: {e}", Colors.RED)
        return None
    
    # If login failed, try to create admin user
    print_colored("📝 Creating admin user...", Colors.YELLOW)
    signup_data = {
        'email': ADMIN_EMAIL,
        'password': ADMIN_PASSWORD,
        'name': 'Admin User'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/auth/signup', json=signup_data)
        if response.status_code == 201:
            print_colored("✅ Admin user created successfully", Colors.GREEN)
            
            # Now login to get token
            login_response = requests.post(f'{BASE_URL}/auth/login', json=login_data)
            if login_response.status_code == 200:
                return login_response.json()['access_token']
        else:
            print_colored(f"❌ Failed to create admin user: {response.text}", Colors.RED)
    except Exception as e:
        print_colored(f"❌ Error creating admin user: {e}", Colors.RED)
    
    return None

def verify_admin_role(token):
    """Verify the admin user has admin role"""
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        # Get current user info
        response = requests.get(f'{BASE_URL}/auth/me', headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            if user_data.get('role') == 'admin':
                print_colored("✅ Admin user has correct role", Colors.GREEN)
                return True
            else:
                print_colored("⚠️  Admin user doesn't have admin role, updating...", Colors.YELLOW)
                return update_user_role(token, user_data['id'])
    except Exception as e:
        print_colored(f"❌ Error verifying admin role: {e}", Colors.RED)
    
    return False

def update_user_role(token, user_id):
    """Update user role to admin"""
    headers = {'Authorization': f'Bearer {token}'}
    data = {'role': 'admin'}
    
    try:
        response = requests.put(f'{BASE_URL}/admin/users/{user_id}/role', headers=headers, json=data)
        if response.status_code == 200:
            print_colored("✅ User role updated to admin", Colors.GREEN)
            return True
        else:
            print_colored(f"❌ Failed to update user role: {response.text}", Colors.RED)
    except Exception as e:
        print_colored(f"❌ Error updating user role: {e}", Colors.RED)
    
    return False

def run_quick_tests(token):
    """Run quick tests on all endpoints"""
    print_colored("\n🧪 Running quick API tests...", Colors.BLUE)
    
    headers = {'Authorization': f'Bearer {token}'}
    tests = [
        {
            'name': 'Get Users',
            'method': 'GET',
            'url': f'{BASE_URL}/admin/users?page=1&per_page=5'
        },
        {
            'name': 'Get Orders',
            'method': 'GET',
            'url': f'{BASE_URL}/admin/orders?page=1&per_page=5'
        },
        {
            'name': 'Get Products',
            'method': 'GET',
            'url': f'{BASE_URL}/admin/products?page=1&per_page=5'
        },
        {
            'name': 'Get Reports',
            'method': 'GET',
            'url': f'{BASE_URL}/admin/reports'
        },
        {
            'name': 'System Health',
            'method': 'GET',
            'url': f'{BASE_URL}/admin/system/health'
        }
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            response = requests.request(test['method'], test['url'], headers=headers)
            if response.status_code == 200:
                print_colored(f"✅ {test['name']}: OK", Colors.GREEN)
                passed += 1
            else:
                print_colored(f"❌ {test['name']}: {response.status_code} - {response.text}", Colors.RED)
                failed += 1
        except Exception as e:
            print_colored(f"❌ {test['name']}: Error - {e}", Colors.RED)
            failed += 1
    
    print_colored(f"\n📊 Test Results: {passed} passed, {failed} failed", Colors.BLUE)
    return failed == 0

def display_usage_guide():
    """Display usage guide"""
    print_colored("\n📖 Usage Guide:", Colors.BLUE)
    print("1. Run comprehensive tests: python test_updated_admin_apis.py")
    print("2. Test individual endpoints using curl commands from admin_api_updated_guide.md")
    print("3. Use Postman with the provided collection structure")
    print("4. Import the collection into your API testing tool")
    
    print_colored("\n🔑 Your Admin Token:", Colors.YELLOW)
    print("Save this token for testing individual endpoints")
    
    print_colored("\n📋 Quick curl commands:", Colors.CYAN)
    print("Get users: curl -X GET 'http://127.0.0.1:5000/admin/users?page=1&per_page=10' -H 'Authorization: Bearer <token>'")
    print("Get reports: curl -X GET 'http://127.0.0.1:5000/admin/reports' -H 'Authorization: Bearer <token>'")
    print("Broadcast notification: curl -X POST 'http://127.0.0.1:5000/admin/notifications/broadcast' -H 'Authorization: Bearer <token>' -H 'Content-Type: application/json' -d '{\"message\": \"Test message\", \"target_audience\": \"all\"}'")

def main():
    """Main setup and test function"""
    print_colored("🚀 Admin API Setup and Testing Tool", Colors.GREEN)
    print("=" * 50)
    
    # Check server connection
    print_colored("🔍 Checking server connection...", Colors.BLUE)
    if not check_server_connection():
        print_colored("❌ Cannot connect to Flask server", Colors.RED)
        print_colored("Please ensure:", Colors.YELLOW)
        print("1. Flask server is running on http://127.0.0.1:5000")
        print("2. Check if you need to run: python main.py")
        return
    
    print_colored("✅ Server connection successful", Colors.GREEN)
    
    # Setup admin user and get token
    token = create_admin_user()
    if not token:
        print_colored("❌ Failed to setup admin user", Colors.RED)
        return
    
    # Verify admin role
    if not verify_admin_role(token):
        print_colored("❌ Failed to verify admin role", Colors.RED)
        return
    
    # Run quick tests
    tests_passed = run_quick_tests(token)
    
    # Display results
    print_colored("\n" + "=" * 50, Colors.GREEN)
    if tests_passed:
        print_colored("🎉 All tests passed! Your admin APIs are working correctly.", Colors.GREEN)
    else:
        print_colored("⚠️  Some tests failed. Check the error messages above.", Colors.YELLOW)
    
    # Display usage guide
    display_usage_guide()
    
    # Save token to file for easy access
    with open('admin_token.txt', 'w') as f:
        f.write(token)
    print_colored(f"\n💾 Admin token saved to admin_token.txt", Colors.GREEN)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print_colored("\n❌ Setup interrupted by user", Colors.RED)
    except Exception as e:
        print_colored(f"❌ Unexpected error: {e}", Colors.RED)