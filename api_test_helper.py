import requests
import json
import argparse

# Base URL for the API
base_url = 'http://127.0.0.1:5000'

def login(email, password):
    """Login and get JWT token"""
    login_url = f'{base_url}/auth/login'
    login_data = {
        'email': email,
        'password': password
    }
    
    print(f"Attempting login with {email}...")
    login_response = requests.post(login_url, json=login_data)
    
    if login_response.status_code != 200:
        print(f"Login failed with status code: {login_response.status_code}")
        print(f"Response: {login_response.text}")
        return None
    
    login_json = login_response.json()
    access_token = login_json.get('access_token')
    
    if not access_token:
        print("No access token in response")
        print(f"Response: {login_json}")
        return None
    
    print("Login successful! Access token received.")
    return access_token

def create_supplement(token, supplement_data):
    """Create a supplement using the token"""
    create_url = f'{base_url}/supplements/create'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    print("Creating supplement with token...")
    create_response = requests.post(create_url, headers=headers, json=supplement_data)
    
    print(f"Status code: {create_response.status_code}")
    print(f"Response: {create_response.text}")
    return create_response

def main():
    parser = argparse.ArgumentParser(description='API Test Helper')
    parser.add_argument('--email', default='test@example.com', help='Email for login')
    parser.add_argument('--password', default='password123', help='Password for login')
    parser.add_argument('--action', choices=['login', 'create_supplement'], default='login', help='Action to perform')
    
    args = parser.parse_args()
    
    if args.action == 'login':
        token = login(args.email, args.password)
        if token:
            print(f"\nYour access token (save this for API requests):\n{token}")
    
    elif args.action == 'create_supplement':
        token = login(args.email, args.password)
        if token:
            supplement_data = {
                'name': 'Test Vitamin D',
                'description': 'Test supplement for API testing',
                'dosage': '1000 IU daily',
                'stock_level': 30,
                'low_stock_threshold': 5,
                'image_url': 'https://example.com/vitamind.jpg'
            }
            create_supplement(token, supplement_data)

if __name__ == '__main__':
    main()