import requests
import json
import argparse
import os
from datetime import datetime

BASE_URL = "http://localhost:5000"
TOKEN_FILE = "token.txt"

def save_token(token):
    """Save JWT token to file"""
    with open(TOKEN_FILE, "w") as f:
        f.write(token)

def load_token():
    """Load JWT token from file"""
    if not os.path.exists(TOKEN_FILE):
        return None
    with open(TOKEN_FILE, "r") as f:
        return f.read().strip()

def login(email, password):
    """Login and get JWT token"""
    url = f"{BASE_URL}/auth/login"
    payload = {"email": email, "password": password}
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        token = response.json().get("access_token")
        if token:
            save_token(token)
            print(f"Login successful. Token saved.")
            return token
        else:
            print(f"Login successful but no token found in response.")
            return None
    else:
        print(f"Login failed: {response.status_code} - {response.text}")
        return None

def get_all_supplements(token):
    """Get all supplements"""
    url = f"{BASE_URL}/supplements/all"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        supplements = response.json()
        print(f"Found {len(supplements)} supplements:")
        for supplement in supplements:
            print(f"  - {supplement['name']} (ID: {supplement['id']})")
        return supplements
    else:
        print(f"Failed to get supplements: {response.status_code} - {response.text}")
        return None

def log_supplement_intake(token, supplement_id, family_member_id=None, dosage_taken="1 tablet", notes=None):
    """Log supplement intake"""
    url = f"{BASE_URL}/supplements/log-intake"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "supplement_id": supplement_id,
        "dosage_taken": dosage_taken
    }
    
    if family_member_id:
        payload["family_member_id"] = family_member_id
    
    if notes:
        payload["notes"] = notes
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 201:
        result = response.json()
        print(f"Intake logged successfully. ID: {result.get('intake_id')}")
        return result
    else:
        print(f"Failed to log intake: {response.status_code} - {response.text}")
        return None

def get_today_intake(token, member_id):
    """Get today's intake for a member"""
    url = f"{BASE_URL}/supplements/today-intake/{member_id}"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        intakes = response.json()
        print(f"Found {len(intakes)} intakes for today:")
        for intake in intakes:
            print(f"  - {intake['supplement_name']} at {intake['taken_at']}")
        return intakes
    else:
        print(f"Failed to get today's intake: {response.status_code} - {response.text}")
        return None

def upload_photo_confirmation(token, intake_id, photo_path):
    """Upload photo confirmation"""
    url = f"{BASE_URL}/supplements/photo-confirmation"
    headers = {"Authorization": f"Bearer {token}"}
    
    files = {"photo": open(photo_path, "rb")}
    data = {"intake_id": intake_id}
    
    response = requests.post(url, files=files, data=data, headers=headers)
    
    if response.status_code == 201:
        result = response.json()
        print(f"Photo confirmation uploaded successfully.")
        return result
    else:
        print(f"Failed to upload photo: {response.status_code} - {response.text}")
        return None

def set_reminder_settings(token, supplement_id, time, days, family_member_id=None):
    """Set reminder settings"""
    url = f"{BASE_URL}/supplements/reminder-settings"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "supplement_id": supplement_id,
        "time": time,
        "days": days
    }
    
    if family_member_id:
        payload["family_member_id"] = family_member_id
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 201:
        result = response.json()
        print(f"Reminder settings saved successfully. ID: {result.get('reminder_id')}")
        return result
    else:
        print(f"Failed to set reminder: {response.status_code} - {response.text}")
        return None

def get_supplement_stats(token, member_id):
    """Get supplement stats for a member"""
    url = f"{BASE_URL}/supplements/stats/{member_id}"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        stats = response.json()
        print(f"Supplement stats for member {member_id}:")
        for stat in stats:
            print(f"  - {stat['supplement_name']}: {stat['adherence_rate']}% adherence")
        return stats
    else:
        print(f"Failed to get stats: {response.status_code} - {response.text}")
        return None

def get_low_stock_alerts(token):
    """Get low stock alerts"""
    url = f"{BASE_URL}/supplements/low-stock-alerts"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        alerts = response.json()
        print(f"Found {len(alerts)} low stock alerts:")
        for alert in alerts:
            print(f"  - {alert['supplement_name']}: {alert['current_stock']}/{alert['threshold']}")
        return alerts
    else:
        print(f"Failed to get alerts: {response.status_code} - {response.text}")
        return None

def get_supplement_history(token, member_id, start_date=None, end_date=None, supplement_id=None):
    """Get supplement history for a member"""
    url = f"{BASE_URL}/supplements/history/{member_id}"
    headers = {"Authorization": f"Bearer {token}"}
    
    params = {}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    if supplement_id:
        params["supplement_id"] = supplement_id
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        history = response.json()
        print(f"Found {len(history)} history records:")
        for record in history[:5]:  # Show first 5 records
            print(f"  - {record['supplement_name']} at {record['taken_at']}")
        if len(history) > 5:
            print(f"  ... and {len(history) - 5} more records")
        return history
    else:
        print(f"Failed to get history: {response.status_code} - {response.text}")
        return None

def run_all_tests(token, member_id, supplement_id):
    """Run all API tests"""
    print("\n=== Running all API tests ===")
    
    # Get all supplements
    supplements = get_all_supplements(token)
    
    if supplements:
        # Use the first supplement if supplement_id not provided
        if not supplement_id and supplements:
            supplement_id = supplements[0]["id"]
        
        # Log intake
        intake = log_supplement_intake(token, supplement_id, notes="Test intake")
        
        # Get today's intake
        today_intake = get_today_intake(token, member_id)
        
        # Set reminder
        reminder = set_reminder_settings(token, supplement_id, "08:00", "Mon,Tue,Wed,Thu,Fri")
        
        # Get stats
        stats = get_supplement_stats(token, member_id)
        
        # Get low stock alerts
        alerts = get_low_stock_alerts(token)
        
        # Get history
        history = get_supplement_history(token, member_id)
        
        print("\n=== All tests completed ===")
        return True
    
    return False

def main():
    parser = argparse.ArgumentParser(description="Test the supplement compliance API endpoints")
    parser.add_argument("--action", choices=[
        "login", "get-supplements", "log-intake", "today-intake", 
        "set-reminder", "get-stats", "low-stock-alerts", "get-history", "all"
    ], required=True, help="Action to perform")
    
    # Login parameters
    parser.add_argument("--email", help="Email for login")
    parser.add_argument("--password", help="Password for login")
    
    # Other parameters
    parser.add_argument("--member-id", type=int, default=1, help="Member ID")
    parser.add_argument("--supplement-id", type=int, help="Supplement ID")
    parser.add_argument("--dosage", default="1 tablet", help="Dosage taken")
    parser.add_argument("--notes", help="Notes for intake")
    parser.add_argument("--photo", help="Path to photo file")
    parser.add_argument("--time", default="08:00", help="Time for reminder (HH:MM)")
    parser.add_argument("--days", default="Mon,Tue,Wed,Thu,Fri", help="Days for reminder")
    parser.add_argument("--start-date", help="Start date for history (YYYY-MM-DD)")
    parser.add_argument("--end-date", help="End date for history (YYYY-MM-DD)")
    
    args = parser.parse_args()
    
    # Handle login action
    if args.action == "login":
        if not args.email or not args.password:
            print("Email and password are required for login")
            return
        login(args.email, args.password)
        return
    
    # For other actions, load token
    token = load_token()
    if not token:
        print("No token found. Please login first.")
        return
    
    # Handle other actions
    if args.action == "get-supplements":
        get_all_supplements(token)
    
    elif args.action == "log-intake":
        if not args.supplement_id:
            print("Supplement ID is required for log-intake")
            return
        log_supplement_intake(token, args.supplement_id, None, args.dosage, args.notes)
    
    elif args.action == "today-intake":
        get_today_intake(token, args.member_id)
    
    elif args.action == "set-reminder":
        if not args.supplement_id:
            print("Supplement ID is required for set-reminder")
            return
        set_reminder_settings(token, args.supplement_id, args.time, args.days)
    
    elif args.action == "get-stats":
        get_supplement_stats(token, args.member_id)
    
    elif args.action == "low-stock-alerts":
        get_low_stock_alerts(token)
    
    elif args.action == "get-history":
        get_supplement_history(token, args.member_id, args.start_date, args.end_date, args.supplement_id)
    
    elif args.action == "all":
        run_all_tests(token, args.member_id, args.supplement_id)

if __name__ == "__main__":
    main()