import requests
import json

# Base URL for the API
base_url = 'http://127.0.0.1:5000'

# Admin credentials
admin_credentials = {
    'email': 'admin@example.com',
    'password': 'adminpassword'
}

# Regular user credentials (for comparison)
user_credentials = {
    'email': 'user@example.com',
    'password': 'userpassword'
}

def test_admin_login():
    # Login as admin
    response = requests.post(f'{base_url}/auth/login', json=admin_credentials)
    if response.status_code == 200:
        admin_data = response.json()
        admin_token = admin_data.get('access_token')
        print(f"Admin login successful. Token: {admin_token[:20]}...")
        
        # Test admin endpoint with admin token
        headers = {'Authorization': f'Bearer {admin_token}'}
        admin_response = requests.get(f'{base_url}/admin/users', headers=headers)
        print(f"Admin endpoint response status: {admin_response.status_code}")
        if admin_response.status_code == 200:
            print("Admin access successful!")
            print(f"Users data: {json.dumps(admin_response.json(), indent=2)}")
        else:
            print(f"Admin access failed: {admin_response.text}")
    else:
        print(f"Admin login failed: {response.text}")

# Run the test
if __name__ == '__main__':
    test_admin_login()