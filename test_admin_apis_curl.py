#!/usr/bin/env python3
"""
Test Admin APIs using curl commands
This script tests all admin endpoints to verify 403 issues are resolved
"""

import subprocess
import json
import sys
import platform

def get_curl_command():
    """Get the appropriate curl command based on OS"""
    return "curl"

def run_curl_command(cmd):
    """Run curl command and return response"""
    try:
        if platform.system() == "Windows":
            # Windows PowerShell format
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        else:
            # Unix-like systems
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.stdout:
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError:
                return {"raw": result.stdout, "error": "Invalid JSON"}
        else:
            return {"error": "No response", "stderr": result.stderr}
    except Exception as e:
        return {"error": str(e)}

def test_admin_login():
    """Test admin login"""
    print("🔐 Testing Admin Login...")
    
    curl_cmd = get_curl_command()
    login_cmd = f'{curl_cmd} -s -X POST http://127.0.0.1:5000/auth/login -H "Content-Type: application/json" -d "{{\"email\": \"admin@example.com\", \"password\": \"adminpassword\"}}"'
    
    response = run_curl_command(login_cmd)
    
    if 'access_token' in response:
        print("✅ Login successful")
        return response['access_token']
    else:
        print("❌ Login failed")
        print(f"Response: {response}")
        return None

def test_admin_endpoints(token):
    """Test all admin endpoints"""
    endpoints = [
        ("GET", "/admin/users", "Get All Users"),
        ("GET", "/admin/orders", "Get All Orders"),
        ("GET", "/admin/products", "Get All Products"),
        ("GET", "/admin/reports", "Get System Reports"),
        ("GET", "/admin/system/health", "Get System Health"),
        ("GET", "/admin/users/1", "Get User by ID"),
        ("POST", "/admin/notifications/broadcast", "Broadcast Notification"),
    ]
    
    curl_cmd = get_curl_command()
    results = []
    
    for method, endpoint, description in endpoints:
        print(f"\n🧪 Testing: {description}")
        
        if method == "GET":
            cmd = f'{curl_cmd} -s -X {method} http://127.0.0.1:5000{endpoint} -H "Authorization: Bearer {token}"'
        elif method == "POST":
            cmd = f'{curl_cmd} -s -X {method} http://127.0.0.1:5000{endpoint} -H "Authorization: Bearer {token}" -H "Content-Type: application/json" -d "{{\"message\": \"Test broadcast\", \"target_audience\": \"all\"}}"'
        
        response = run_curl_command(cmd)
        
        # Check for common error patterns
        if isinstance(response, dict):
            if response.get('error') == 'Admin access required' or '403' in str(response).lower():
                status = "❌ 403 Forbidden"
            elif 'error' in str(response).lower() and '401' in str(response).lower():
                status = "❌ 401 Unauthorized"
            elif 'error' in str(response) and str(response.get('error')).lower() == 'no response':
                status = "❌ No Response"
            else:
                status = "✅ Success"
        else:
            status = "✅ Success"
        
        results.append({
            'endpoint': endpoint,
            'description': description,
            'status': status,
            'response': response
        })
        
        print(f"{status} - {endpoint}")
    
    return results

def provide_manual_fixes():
    """Provide manual fixes for common issues"""
    print("\n" + "="*60)
    print("🔧 MANUAL FIXES FOR ADMIN PERMISSIONS")
    print("="*60)
    
    print("\n1. CHECK SERVER STATUS:")
    print("   curl -X GET http://127.0.0.1:5000/health")
    
    print("\n2. CHECK DATABASE (SQL Commands):")
    print("   -- Check users table")
    print("   SELECT id, email, name, role, verified FROM users;")
    
    print("   -- Update admin user role")
    print("   UPDATE users SET role='admin', verified=1 WHERE email='admin@example.com';")
    
    print("   -- Create admin user if missing")
    print("   INSERT INTO users (name, email, password_hash, role, verified, created_at)")
    print("   VALUES ('Admin User', 'admin@example.com', [hashed_password], 'admin', 1, datetime('now'));")
    
    print("\n3. TEST MANUALLY:")
    print("   # Get token")
    print('   curl -X POST http://127.0.0.1:5000/auth/login -H "Content-Type: application/json" -d \'{"email": "admin@example.com", "password": "adminpassword"}\'')
    
    print("\n   # Test admin endpoint")
    print('   curl -X GET http://127.0.0.1:5000/admin/users -H "Authorization: Bearer [YOUR_TOKEN]"')

def main():
    print("🚀 Admin API Test Suite")
    print("=" * 50)
    
    # Test server connection first
    curl_cmd = get_curl_command()
    health_cmd = f'{curl_cmd} -s -X GET http://127.0.0.1:5000/health'
    health_response = run_curl_command(health_cmd)
    
    if 'error' in str(health_response):
        print("❌ Server is not running or not accessible")
        print("Please start the server with: python main.py")
        provide_manual_fixes()
        return
    
    print("✅ Server is running")
    
    # Test admin login
    token = test_admin_login()
    
    if not token:
        print("\n❌ Cannot proceed without valid token")
        provide_manual_fixes()
        return
    
    print(f"\n✅ Token obtained: {token[:20]}...")
    
    # Test all endpoints
    results = test_admin_endpoints(token)
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    success_count = sum(1 for r in results if "✅" in r['status'])
    total_count = len(results)
    
    print(f"Successful: {success_count}/{total_count}")
    
    if success_count < total_count:
        print("\n❌ Issues detected:")
        for result in results:
            if "❌" in result['status']:
                print(f"   {result['endpoint']}: {result['status']}")
        
        provide_manual_fixes()
    else:
        print("✅ All endpoints working correctly!")

if __name__ == "__main__":
    main()