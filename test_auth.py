import requests
import json
import sys

# Base URL for the API
base_url = 'http://127.0.0.1:5000'

# Test user credentials
email = 'test@example.com'
password = 'password123'

def test_login_and_create_supplement():
    # Step 1: Login to get JWT token
    login_url = f'{base_url}/auth/login'
    login_data = {
        'email': email,
        'password': password
    }
    
    print(f"\n1. Attempting login with {email}...")
    login_response = requests.post(login_url, json=login_data)
    
    if login_response.status_code != 200:
        print(f"Login failed with status code: {login_response.status_code}")
        print(f"Response: {login_response.text}")
        return
    
    login_json = login_response.json()
    access_token = login_json.get('access_token')
    
    if not access_token:
        print("No access token in response")
        print(f"Response: {login_json}")
        return
    
    print("Login successful! Access token received.")
    print(f"Token: {access_token[:20]}...")
    
    # Step 2: Create a supplement using the token
    create_url = f'{base_url}/supplements/create'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    supplement_data = {
        'name': 'Test Vitamin D',
        'description': 'Test supplement for API testing',
        'dosage': '1000 IU daily',
        'stock_level': 30,
        'low_stock_threshold': 5,
        'image_url': 'https://example.com/vitamind.jpg'
    }
    
    print("\n2. Creating supplement with token...")
    print(f"Headers: {headers}")
    create_response = requests.post(create_url, headers=headers, json=supplement_data)
    
    print(f"Status code: {create_response.status_code}")
    print(f"Response: {create_response.text}")

def test_invalid_token():
    # Test with invalid token
    create_url = f'{base_url}/supplements/create'
    headers = {
        'Authorization': 'Bearer invalid_token',
        'Content-Type': 'application/json'
    }
    
    supplement_data = {
        'name': 'Test Vitamin D',
        'description': 'Test supplement for API testing',
        'dosage': '1000 IU daily',
        'stock_level': 30,
        'low_stock_threshold': 5,
        'image_url': 'https://example.com/vitamind.jpg'
    }
    
    print("\n3. Testing with invalid token...")
    create_response = requests.post(create_url, headers=headers, json=supplement_data)
    
    print(f"Status code: {create_response.status_code}")
    print(f"Response: {create_response.text}")

def test_no_token():
    # Test with no token
    create_url = f'{base_url}/supplements/create'
    headers = {
        'Content-Type': 'application/json'
    }
    
    supplement_data = {
        'name': 'Test Vitamin D',
        'description': 'Test supplement for API testing',
        'dosage': '1000 IU daily',
        'stock_level': 30,
        'low_stock_threshold': 5,
        'image_url': 'https://example.com/vitamind.jpg'
    }
    
    print("\n4. Testing with no token...")
    create_response = requests.post(create_url, headers=headers, json=supplement_data)
    
    print(f"Status code: {create_response.status_code}")
    print(f"Response: {create_response.text}")

# Run the tests
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'all':
        test_login_and_create_supplement()
        test_invalid_token()
        test_no_token()
    else:
        test_login_and_create_supplement()