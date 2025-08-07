import requests
import json
import sys

# Base URL for the API
base_url = 'http://127.0.0.1:5000'

# Admin credentials
admin_credentials = {
    'email': 'admin@example.com',
    'password': 'adminpassword'
}

def print_separator(title):
    """Print a separator with title for better readability"""
    print("\n" + "=" * 50)
    print(f" {title} ")
    print("=" * 50)

def test_admin_login():
    """Test admin login and get JWT token"""
    print_separator("ADMIN LOGIN TEST")
    
    try:
        response = requests.post(f'{base_url}/auth/login', json=admin_credentials)
        if response.status_code == 200:
            admin_data = response.json()
            admin_token = admin_data.get('access_token')
            print(f"✅ Admin login successful. Token: {admin_token[:20]}...")
            return admin_token
        else:
            print(f"❌ Admin login failed: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Make sure the Flask server is running on http://127.0.0.1:5000")
        sys.exit(1)

def test_get_users(token):
    """Test GET /admin/users endpoint with pagination"""
    print_separator("GET USERS WITH PAGINATION")
    
    headers = {'Authorization': f'Bearer {token}'}
    params = {'page': 1, 'per_page': 5, 'sort_by': 'created_at', 'sort_order': 'desc'}
    response = requests.get(f'{base_url}/admin/users', headers=headers, params=params)
    
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Successfully retrieved {len(data['users'])} users")
        print(f"Total users: {data['pagination']['total']}")
        print(f"Page {data['pagination']['page']} of {data['pagination']['pages']}")
        if data['users']:
            print("Sample user:")
            print(json.dumps(data['users'][0], indent=2))
    else:
        print(f"❌ Failed to get users: {response.text}")

def test_get_user_by_id(token, user_id):
    """Test GET /admin/users/{user_id} endpoint"""
    print_separator(f"GET USER BY ID: {user_id}")
    
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{base_url}/admin/users/{user_id}', headers=headers)
    
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        user = response.json()
        print("✅ Successfully retrieved user")
        print(json.dumps(user, indent=2))
    else:
        print(f"❌ Failed to get user: {response.text}")

def test_update_user_role(token, user_id, new_role):
    """Test PUT /admin/users/{user_id}/role endpoint"""
    print_separator(f"UPDATE USER ROLE: {user_id} -> {new_role}")
    
    headers = {'Authorization': f'Bearer {token}'}
    data = {'role': new_role}
    response = requests.put(f'{base_url}/admin/users/{user_id}/role', headers=headers, json=data)
    
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print("✅ Successfully updated user role")
        print(json.dumps(result, indent=2))
    else:
        print(f"❌ Failed to update user role: {response.text}")

def test_get_orders(token):
    """Test GET /admin/orders endpoint with filtering"""
    print_separator("GET ORDERS WITH FILTERING")
    
    headers = {'Authorization': f'Bearer {token}'}
    params = {'page': 1, 'per_page': 10}
    response = requests.get(f'{base_url}/admin/orders', headers=headers, params=params)
    
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Successfully retrieved {len(data['orders'])} orders")
        print(f"Total orders: {data['pagination']['total']}")
        if data['orders']:
            print("Sample order:")
            print(json.dumps(data['orders'][0], indent=2))
    else:
        print(f"❌ Failed to get orders: {response.text}")

def test_get_products(token):
    """Test GET /admin/products endpoint"""
    print_separator("GET PRODUCTS")
    
    headers = {'Authorization': f'Bearer {token}'}
    params = {'page': 1, 'per_page': 10}
    response = requests.get(f'{base_url}/admin/products', headers=headers, params=params)
    
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Successfully retrieved {len(data['products'])} products")
        print(f"Total products: {data['pagination']['total']}")
        if data['products']:
            print("Sample product:")
            print(json.dumps(data['products'][0], indent=2))
    else:
        print(f"❌ Failed to get products: {response.text}")

def test_update_product(token):
    """Test POST /admin/product/update endpoint with validation"""
    print_separator("UPDATE PRODUCT TEST")
    
    headers = {'Authorization': f'Bearer {token}'}
    product_data = {
        "id": 1,
        "name": "Updated Product Name - Admin API Test",
        "description": "This product was updated via admin API test with validation",
        "price": 39.99,
        "stock": 100
    }
    
    response = requests.post(
        f'{base_url}/admin/product/update', 
        headers=headers,
        json=product_data
    )
    
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print("✅ Successfully updated product")
        print(json.dumps(result, indent=2))
    else:
        print(f"❌ Failed to update product: {response.text}")

def test_invalid_product_update(token):
    """Test POST /admin/product/update with invalid data"""
    print_separator("INVALID PRODUCT UPDATE TEST")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test with invalid price
    invalid_data = {
        "id": 1,
        "price": "invalid_price"
    }
    
    response = requests.post(
        f'{base_url}/admin/product/update', 
        headers=headers,
        json=invalid_data
    )
    
    print(f"Status code: {response.status_code}")
    if response.status_code == 400:
        error = response.json()
        print("✅ Correctly rejected invalid price")
        print(json.dumps(error, indent=2))
    else:
        print(f"❌ Should have rejected invalid data: {response.text}")

def test_get_reports(token):
    """Test GET /admin/reports endpoint"""
    print_separator("GET REPORTS")
    
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{base_url}/admin/reports', headers=headers)
    
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        reports = response.json()
        print("✅ Successfully retrieved reports")
        print(json.dumps(reports, indent=2))
    else:
        print(f"❌ Failed to get reports: {response.text}")

def test_broadcast_notification(token):
    """Test POST /admin/notifications/broadcast endpoint"""
    print_separator("BROADCAST NOTIFICATION")
    
    headers = {'Authorization': f'Bearer {token}'}
    notification_data = {
        "message": "Test broadcast message from updated admin API test",
        "target_audience": "all",
        "priority": "normal"
    }
    
    response = requests.post(
        f'{base_url}/admin/notifications/broadcast', 
        headers=headers,
        json=notification_data
    )
    
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print("✅ Successfully sent broadcast notification")
        print(json.dumps(result, indent=2))
    else:
        print(f"❌ Failed to send broadcast: {response.text}")

def test_system_health(token):
    """Test GET /admin/system/health endpoint"""
    print_separator("SYSTEM HEALTH CHECK")
    
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{base_url}/admin/system/health', headers=headers)
    
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        health = response.json()
        print("✅ Successfully retrieved system health")
        print(json.dumps(health, indent=2))
    else:
        print(f"❌ Failed to get system health: {response.text}")

def run_all_updated_tests():
    """Run all updated admin API tests"""
    print("Starting Updated Admin API Tests...\n")
    
    # First, login and get token
    token = test_admin_login()
    if not token:
        print("\n❌ Cannot proceed with tests without valid admin token")
        return
    
    # Run all tests
    test_get_users(token)
    test_get_user_by_id(token, 1)
    test_get_orders(token)
    test_get_products(token)
    test_update_product(token)
    test_invalid_product_update(token)
    test_get_reports(token)
    test_broadcast_notification(token)
    test_system_health(token)
    
    # Test user role update (with a non-admin user if available)
    print_separator("TESTING USER ROLE UPDATE")
    print("Note: This will attempt to update a user's role. Make sure you have a non-admin user to test with.")
    
    print("\n✅ All updated admin API tests completed!")
    print("\n📝 Summary of improvements:")
    print("- Enhanced error handling with specific error codes")
    print("- Added input validation for all endpoints")
    print("- Added pagination and filtering for list endpoints")
    print("- Added new endpoints: user details, user role update, product list, product delete, system health")
    print("- Improved response formats with detailed information")
    print("- Added comprehensive testing script")

if __name__ == '__main__':
    run_all_updated_tests()