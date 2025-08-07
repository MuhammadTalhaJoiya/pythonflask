# Compliance API Testing Guide

This guide provides information on testing the compliance-related API endpoints for the supplement tracking application.

## Required API Endpoints

The following API endpoints should be implemented and tested for compliance:

### 1. GET /supplements/all
**Description**: Retrieves all supplements for the authenticated user.
**Authentication**: JWT token required
**Response**: List of supplement objects

### 2. POST /supplements/log-intake
**Description**: Logs the intake of a supplement for a user or family member
**Authentication**: JWT token required
**Request Body**:
```json
{
  "supplement_id": 1,
  "family_member_id": 2, // Optional, if for a family member
  "dosage_taken": "10mg",
  "notes": "Taken after breakfast" // Optional
}
```

### 3. GET /supplements/today-intake/:memberId
**Description**: Retrieves all supplement intakes for today for a specific member
**Authentication**: JWT token required
**URL Parameters**: memberId - ID of the user or family member
**Response**: List of intake records for today

### 4. POST /supplements/photo-confirmation
**Description**: Uploads a photo confirmation of supplement intake
**Authentication**: JWT token required
**Request**: Multipart form data with intake_id and photo file

### 5. POST /supplements/reminder-settings
**Description**: Sets reminder settings for a supplement
**Authentication**: JWT token required
**Request Body**:
```json
{
  "supplement_id": 1,
  "family_member_id": 2, // Optional
  "time": "08:00", // Format: HH:MM
  "days": "Mon,Tue,Wed,Thu,Fri,Sat,Sun"
}
```

### 6. GET /supplements/stats/:memberId
**Description**: Retrieves supplement statistics for a specific member
**Authentication**: JWT token required
**URL Parameters**: memberId - ID of the user or family member
**Response**: Statistics including adherence rate and intake history

### 7. GET /supplements/low-stock-alerts
**Description**: Retrieves alerts for supplements with stock below threshold
**Authentication**: JWT token required
**Response**: List of supplements with low stock

### 8. GET /supplements/history/:memberId
**Description**: Retrieves supplement intake history for a specific member
**Authentication**: JWT token required
**URL Parameters**: memberId - ID of the user or family member
**Query Parameters**:
- start_date (optional): Filter by start date (YYYY-MM-DD)
- end_date (optional): Filter by end date (YYYY-MM-DD)
- supplement_id (optional): Filter by specific supplement
**Response**: List of intake records

## Testing the API Endpoints

### Authentication

All endpoints require JWT authentication. To obtain a token:

```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'
```

Use the returned token in subsequent requests:

```bash
curl -X GET http://localhost:5000/supplements/all \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Testing with Postman

1. Import the provided Postman collection
2. Set up an environment variable for your JWT token
3. Run the requests in the collection to test each endpoint

### Testing with the API Test Helper

Use the `api_test_helper.py` script to test the endpoints:

```bash
python api_test_helper.py --action login --email user@example.com --password password123
python api_test_helper.py --action get-supplements
python api_test_helper.py --action log-intake --supplement-id 1 --dosage "10mg"
```

## Common Error Codes

- **401 Unauthorized**: Missing or invalid JWT token
- **403 Forbidden**: Attempting to access resources not owned by the authenticated user
- **404 Not Found**: Resource not found (supplement, family member, etc.)
- **400 Bad Request**: Missing or invalid request parameters

## Compliance Requirements

When testing these endpoints, ensure they meet the following compliance requirements:

1. All endpoints must require proper authentication
2. User data must be properly isolated (users can only access their own data)
3. Family member data must be properly associated with the authenticated user
4. Photo confirmations must be securely stored and accessible only to authorized users
5. Reminder settings must be properly stored and associated with the correct supplement and user/family member