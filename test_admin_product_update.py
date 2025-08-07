import requests
import json

# Base URL for the API
base_url = 'http://127.0.0.1:5000'

# Admin credentials
admin_credentials = {
    'email': 'admin@example.com',
    'password': 'adminpassword'
}

def test_admin_product_update():
    # Login as admin
    response = requests.post(f'{base_url}/auth/login', json=admin_credentials)
    if response.status_code == 200:
        admin_data = response.json()
        admin_token = admin_data.get('access_token')
        print(f"Admin login successful. Token: {admin_token[:20]}...")
        
        # Test admin product update endpoint
        headers = {'Authorization': f'Bearer {admin_token}'}
        product_data = {
            "id": 1,  # Assuming product with ID 1 exists
            "name": "Updated Product Name",
            "description": "Updated product description",
            "price": 29.99
        }
        
        update_response = requests.post(
            f'{base_url}/admin/product/update', 
            headers=headers,
            json=product_data
        )
        
        print(f"Product update response status: {update_response.status_code}")
        if update_response.status_code == 200:
            print("Product update successful!")
            print(f"Response: {update_response.text}")
        else:
            print(f"Product update failed: {update_response.text}")
    else:
        print(f"Admin login failed: {response.text}")

# Run the test
if __name__ == '__main__':
    test_admin_product_update()