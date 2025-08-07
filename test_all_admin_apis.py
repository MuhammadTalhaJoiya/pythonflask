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
    """Test GET /admin/users endpoint"""
    print_separator("GET USERS TEST")
    
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{base_url}/admin/users', headers=headers)
    
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        print("✅ Successfully retrieved users")
        users = response.json()
        print(f"Total users: {len(users)}")
        print("Sample user data:")
        if users:
            print(json.dumps(users[0], indent=2))
    else:
        print(f"❌ Failed to get users: {response.text}")

def test_get_orders(token):
    """Test GET /admin/orders endpoint"""
    print_separator("GET ORDERS TEST")
    
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{base_url}/admin/orders', headers=headers)
    
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        print("✅ Successfully retrieved orders")
        orders = response.json()
        print(f"Total orders: {len(orders)}")
        if orders:
            print("Sample order data:")
            print(json.dumps(orders[0], indent=2))
        else:
            print("No orders found in the database")
    else:
        print(f"❌ Failed to get orders: {response.text}")

def test_update_product(token):
    """Test POST /admin/product/update endpoint"""
    print_separator("UPDATE PRODUCT TEST")
    
    headers = {'Authorization': f'Bearer {token}'}
    product_data = {
        "id": 1,  # Assuming product with ID 1 exists
        "name": "Updated Product Name",
        "description": "This product was updated via admin API test",
        "price": 29.99
    }
    
    response = requests.post(
        f'{base_url}/admin/product/update', 
        headers=headers,
        json=product_data
    )
    
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        print("✅ Successfully updated product")
        print(f"Response: {response.text}")
    else:
        print(f"❌ Failed to update product: {response.text}")

def test_get_reports(token):
    """Test GET /admin/reports endpoint"""
    print_separator("GET REPORTS TEST")
    
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{base_url}/admin/reports', headers=headers)
    
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        print("✅ Successfully retrieved reports")
        print("Report data:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"❌ Failed to get reports: {response.text}")

def test_broadcast_notification(token):
    """Test POST /admin/notifications/broadcast endpoint"""
    print_separator("BROADCAST NOTIFICATION TEST")
    
    headers = {'Authorization': f'Bearer {token}'}
    notification_data = {
        "message": "This is a test broadcast message from admin API test"
    }
    
    response = requests.post(
        f'{base_url}/admin/notifications/broadcast', 
        headers=headers,
        json=notification_data
    )
    
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        print("✅ Successfully sent broadcast notification")
        print(f"Response: {response.text}")
    else:
        print(f"❌ Failed to send broadcast: {response.text}")

def run_all_tests():
    """Run all admin API tests"""
    print("Starting Admin API Tests...\n")
    
    # First, login and get token
    token = test_admin_login()
    if not token:
        print("\n❌ Cannot proceed with tests without valid admin token")
        return
    
    # Run all other tests
    test_get_users(token)
    test_get_orders(token)
    test_update_product(token)
    test_get_reports(token)
    test_broadcast_notification(token)
    
    print("\n✅ All admin API tests completed!")

if __name__ == '__main__':
    run_all_tests()