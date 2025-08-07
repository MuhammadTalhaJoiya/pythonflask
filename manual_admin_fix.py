#!/usr/bin/env python3
"""
Manual Admin Fix Script

This script provides manual steps to fix 403 Forbidden errors for admin APIs.
It includes curl commands and database queries to ensure admin permissions work correctly.
"""

import requests
import json
import subprocess
import platform

def print_header(title):
    print("\n" + "="*50)
    print(f" {title} ")
    print("="*50)

def print_success(msg):
    print(f"✅ {msg}")

def print_error(msg):
    print(f"❌ {msg}")

def print_warning(msg):
    print(f"⚠️  {msg}")

def print_info(msg):
    print(f"ℹ️  {msg}")

def get_curl_command():
    """Get the appropriate curl command based on OS"""
    return "curl" if platform.system() != "Windows" else "curl"

def test_server_connection():
    """Test if server is running"""
    try:
        response = requests.get("http://127.0.0.1:5000/auth/login", timeout=5)
        return response.status_code < 500
    except:
        return False

def get_admin_token():
    """Get admin token using curl"""
    curl_cmd = get_curl_command()
    
    login_cmd = [
        curl_cmd, "-s", "-X", "POST", 
        "http://127.0.0.1:5000/auth/login",
        "-H", "Content-Type: application/json",
        "-d", '{"email": "admin@example.com", "password": "adminpassword"}'
    ]
    
    try:
        if platform.system() == "Windows":
            # Windows PowerShell format
            cmd = f'{curl_cmd} -s -X POST http://127.0.0.1:5000/auth/login -H "Content-Type: application/json" -d "{{\"email\": \"admin@example.com\", \"password\": \"adminpassword\"}}"'
            import subprocess
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            response_text = result.stdout
        else:
            # Unix-like systems
            result = subprocess.run(login_cmd, capture_output=True, text=True)
            response_text = result.stdout
        
        if response_text:
            response_data = json.loads(response_text)
            return response_data.get('access_token')
    except Exception as e:
        print_error(f"Failed to get token: {e}")
    
    return None

def test_admin_endpoints_manual():
    """Test admin endpoints manually with curl commands"""
    
    print_header("Manual Admin API Testing")
    
    # Check server connection
    if not test_server_connection():
        print_error("Server is not running on http://127.0.0.1:5000")
        print_info("Please start the server with: python main.py")
        return False
    
    print_success("Server is running")
    
    # Get admin token
    print_header("Getting Admin Token")
    token = get_admin_token()
    
    if not token:
        print_error("Failed to get admin token")
        print_info("This might be because:")
        print_info("1. Admin user doesn't exist")
        print_info("2. Admin user doesn't have 'admin' role")
        print_info("3. Wrong credentials")
        
        print_header("Manual Steps to Fix")
        print("1. Check if admin user exists:")
        print("   Run this SQL query:")
        print("   SELECT id, email, role FROM users WHERE email='admin@example.com';")
        print()
        print("2. If user exists but role is not 'admin':")
        print("   UPDATE users SET role='admin', verified=1 WHERE email='admin@example.com';")
        print()
        print("3. If user doesn't exist:")
        print("   INSERT INTO users (name, email, password_hash, role, verified, created_at)")
        print("   VALUES ('Admin User', 'admin@example.com', [hashed_password], 'admin', 1, NOW());")
        return False
    
    print_success(f"Admin token obtained: {token[:20]}...")
    
    # Test endpoints with curl commands
    curl_cmd = get_curl_command()
    
    endpoints = [
        ("GET", "/admin/users", "Get all users"),
        ("GET", "/admin/orders", "Get all orders"),
        ("GET", "/admin/products", "Get all products"),
        ("GET", "/admin/reports", "Get system reports"),
        ("GET", "/admin/system/health", "Get system health"),
    ]
    
    print_header("Testing Admin Endpoints")
    
    for method, endpoint, description in endpoints:
        print(f"\nTesting: {description}")
        
        if platform.system() == "Windows":
            cmd = f'{curl_cmd} -s -X {method} http://127.0.0.1:5000{endpoint} -H "Authorization: Bearer {token}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            response_text = result.stdout
        else:
            cmd = [curl_cmd, "-s", "-X", method, f"http://127.0.0.1:5000{endpoint}", 
                   "-H", f"Authorization: Bearer {token}"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            response_text = result.stdout
        
        try:
            response_data = json.loads(response_text)
            if 'error' in response_data and response_data.get('error') == 'Admin access required':
                print_error(f"403 Forbidden - {endpoint}")
                print_info("Admin role issue detected")
            else:
                print_success(f"200 OK - {endpoint}")
        except:
            if response_text:
                print_success(f"Response received - {endpoint}")
            else:
                print_error(f"No response - {endpoint}")
    
    return True

def provide_sql_fixes():
    """Provide SQL commands to fix admin permissions"""
    
    print_header("SQL Fixes for Admin Permissions")
    
    print("Run these SQL commands to fix admin permissions:")
    print()
    
    print("1. Check current users and roles:")
    print("```sql")
    print("SELECT id, email, name, role, verified FROM users;")
    print("```")
    print()
    
    print("2. Update existing admin user role:")
    print("```sql")
    print("UPDATE users SET role='admin', verified=1 WHERE email='admin@example.com';")
    print("```")
    print()
    
    print("3. Create new admin user if needed:")
    print("```sql")
    print("-- First, check if admin@example.com exists")
    print("SELECT * FROM users WHERE email='admin@example.com';")
    print()
    print("-- If not exists, create with (you'll need to hash the password)")
    print("INSERT INTO users (name, email, password_hash, role, verified, created_at)")
    print("VALUES ('Admin User', 'admin@example.com', 'pbkdf2:sha256:260000$...', 'admin', 1, NOW());")
    print("```")
    print()
    
    print("4. Verify admin permissions:")
    print("```sql")
    print("SELECT id, email, name, role FROM users WHERE role='admin';")
    print("```")

def main():
    """Main function"""
    
    print("🔧 Admin Permission Fix Tool")
    print("=" * 50)
    
    # Test server connection
    if test_server_connection():
        print_success("Server is running")
        test_admin_endpoints_manual()
    else:
        print_error("Server is not accessible")
        provide_sql_fixes()
    
    print_header("Next Steps")
    print("1. Start your Flask server: python main.py")
    print("2. Run the SQL commands above to ensure admin role")
    print("3. Test with: python test_updated_admin_apis.py")
    print("4. Check admin_api_updated_guide.md for full documentation")

if __name__ == "__main__":
    main()