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

def get_all_supplements(token):
    """Get all supplements for the authenticated user"""
    get_url = f'{base_url}/supplements/all'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    print("Getting all supplements...")
    get_response = requests.get(get_url, headers=headers)
    
    print(f"Status code: {get_response.status_code}")
    if get_response.status_code == 200:
        supplements = get_response.json()
        print(f"Found {len(supplements)} supplements:")
        for supplement in supplements:
            print(f"  - {supplement['name']} (ID: {supplement['id']})")
    else:
        print(f"Response: {get_response.text}")
    
    return get_response

def update_supplement(token, supplement_id, update_data):
    """Update an existing supplement"""
    update_url = f'{base_url}/supplements/update/{supplement_id}'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    print(f"Updating supplement with ID {supplement_id}...")
    update_response = requests.put(update_url, headers=headers, json=update_data)
    
    print(f"Status code: {update_response.status_code}")
    print(f"Response: {update_response.text}")
    return update_response

def delete_supplement(token, supplement_id):
    """Delete a supplement"""
    delete_url = f'{base_url}/supplements/delete/{supplement_id}'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    print(f"Deleting supplement with ID {supplement_id}...")
    delete_response = requests.delete(delete_url, headers=headers)
    
    print(f"Status code: {delete_response.status_code}")
    print(f"Response: {delete_response.text}")
    return delete_response

def get_supplement_details(token, supplement_id):
    """Get detailed information about a specific supplement"""
    get_url = f'{base_url}/supplements/{supplement_id}'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    print(f"Getting details for supplement with ID {supplement_id}...")
    get_response = requests.get(get_url, headers=headers)
    
    print(f"Status code: {get_response.status_code}")
    if get_response.status_code == 200:
        supplement = get_response.json()
        print(f"Supplement details:")
        for key, value in supplement.items():
            print(f"  - {key}: {value}")
    else:
        print(f"Response: {get_response.text}")
    
    return get_response

def run_full_test(email, password):
    """Run a full test of all supplement API endpoints"""
    # Step 1: Login
    token = login(email, password)
    if not token:
        return
    
    # Step 2: Create a supplement
    supplement_data = {
        'name': 'Test Vitamin D3',
        'description': 'Test supplement for API testing',
        'dosage': '1000 IU daily',
        'stock_level': 30,
        'low_stock_threshold': 5,
        'image_url': 'https://example.com/vitamind.jpg'
    }
    create_response = create_supplement(token, supplement_data)
    if create_response.status_code != 201:
        print("Failed to create supplement. Stopping test.")
        return
    
    supplement_id = create_response.json().get('supplement_id')
    print(f"\nCreated supplement with ID: {supplement_id}")
    
    # Step 3: Get all supplements
    print("\n--- Getting all supplements ---")
    get_all_supplements(token)
    
    # Step 4: Get supplement details
    print("\n--- Getting supplement details ---")
    get_supplement_details(token, supplement_id)
    
    # Step 5: Update the supplement
    print("\n--- Updating supplement ---")
    update_data = {
        'name': 'Updated Test Vitamin D3',
        'description': 'Updated test supplement for API testing',
        'dosage': '2000 IU daily',
        'stock_level': 25,
        'low_stock_threshold': 10,
        'image_url': 'https://example.com/updated_vitamind.jpg'
    }
    update_supplement(token, supplement_id, update_data)
    
    # Step 6: Get updated supplement details
    print("\n--- Getting updated supplement details ---")
    get_supplement_details(token, supplement_id)
    
    # Step 7: Delete the supplement
    print("\n--- Deleting supplement ---")
    delete_supplement(token, supplement_id)
    
    # Step 8: Verify deletion
    print("\n--- Verifying deletion ---")
    get_supplement_details(token, supplement_id)
    
    print("\nFull test completed!")

def main():
    parser = argparse.ArgumentParser(description='Supplements API Test Script')
    parser.add_argument('--email', default='test@example.com', help='Email for login')
    parser.add_argument('--password', default='password123', help='Password for login')
    parser.add_argument('--action', choices=['login', 'create', 'get_all', 'get_details', 'update', 'delete', 'full_test'], 
                        default='full_test', help='Action to perform')
    parser.add_argument('--id', type=int, help='Supplement ID for actions that require it')
    
    args = parser.parse_args()
    
    if args.action == 'login':
        token = login(args.email, args.password)
        if token:
            print(f"\nYour access token (save this for API requests):\n{token}")
    
    elif args.action == 'create':
        token = login(args.email, args.password)
        if token:
            supplement_data = {
                'name': 'Test Vitamin D3',
                'description': 'Test supplement for API testing',
                'dosage': '1000 IU daily',
                'stock_level': 30,
                'low_stock_threshold': 5,
                'image_url': 'https://example.com/vitamind.jpg'
            }
            create_supplement(token, supplement_data)
    
    elif args.action == 'get_all':
        token = login(args.email, args.password)
        if token:
            get_all_supplements(token)
    
    elif args.action == 'get_details':
        if not args.id:
            print("Error: --id is required for get_details action")
            return
        token = login(args.email, args.password)
        if token:
            get_supplement_details(token, args.id)
    
    elif args.action == 'update':
        if not args.id:
            print("Error: --id is required for update action")
            return
        token = login(args.email, args.password)
        if token:
            update_data = {
                'name': 'Updated Test Vitamin D3',
                'description': 'Updated test supplement for API testing',
                'dosage': '2000 IU daily',
                'stock_level': 25,
                'low_stock_threshold': 10,
                'image_url': 'https://example.com/updated_vitamind.jpg'
            }
            update_supplement(token, args.id, update_data)
    
    elif args.action == 'delete':
        if not args.id:
            print("Error: --id is required for delete action")
            return
        token = login(args.email, args.password)
        if token:
            delete_supplement(token, args.id)
    
    elif args.action == 'full_test':
        run_full_test(args.email, args.password)

if __name__ == '__main__':
    main()