# Supplements API Testing Guide

## Overview
This guide provides instructions for testing the Supplements API endpoints using Postman or any HTTP client with JSON payloads.

## Authentication

All endpoints require authentication with a JWT token. First, obtain a token:

```
POST /auth/login
Content-Type: application/json

{
  "email": "your_email@example.com",
  "password": "your_password"
}
```

Use the returned token in the Authorization header for all subsequent requests:

```
Authorization: Bearer your_jwt_token
```

## Endpoints

### 1. Create Supplement

Create a new supplement in the system.

```
POST /supplements/create
Authorization: Bearer your_jwt_token
Content-Type: application/json

{
  "name": "Vitamin D3",
  "description": "Supports bone health and immune function",
  "dosage": "1000 IU daily",
  "stock_level": 30,
  "low_stock_threshold": 5,
  "image_url": "https://example.com/vitamind.jpg"
}
```

Required fields:
- `name`: Name of the supplement

Optional fields:
- `description`: Description of the supplement
- `dosage`: Recommended dosage
- `stock_level`: Current inventory level (default: 0)
- `low_stock_threshold`: Level at which to alert low stock (default: 5)
- `image_url`: URL to an image of the supplement

Response (201 Created):
```json
{
  "message": "Supplement created successfully",
  "supplement_id": 1,
  "name": "Vitamin D3"
}
```

### 2. Get All Supplements

Retrieve all supplements for the authenticated user.

```
GET /supplements/all
Authorization: Bearer your_jwt_token
```

Response (200 OK):
```json
[
  {
    "id": 1,
    "name": "Vitamin D3",
    "description": "Supports bone health and immune function",
    "dosage": "1000 IU daily",
    "stock_level": 30,
    "low_stock_threshold": 5,
    "image_url": "https://example.com/vitamind.jpg",
    "created_at": "2023-06-15T10:00:00"
  },
  {
    "id": 2,
    "name": "Vitamin C",
    "description": "Supports immune function",
    "dosage": "500 mg daily",
    "stock_level": 20,
    "low_stock_threshold": 5,
    "image_url": "https://example.com/vitaminc.jpg",
    "created_at": "2023-06-16T10:00:00"
  }
]
```

### 3. Update Supplement

Update an existing supplement.

```
PUT /supplements/update/{supplement_id}
Authorization: Bearer your_jwt_token
Content-Type: application/json

{
  "name": "Vitamin D3 + K2",
  "description": "Supports bone health and immune function with added K2",
  "dosage": "1000 IU D3 + 100 mcg K2 daily",
  "stock_level": 25,
  "low_stock_threshold": 10,
  "image_url": "https://example.com/vitamind_k2.jpg"
}
```

All fields are optional. Only the fields you include will be updated.

Response (200 OK):
```json
{
  "message": "Supplement updated successfully",
  "supplement_id": 1
}
```

### 4. Delete Supplement

Delete a supplement from the system.

```
DELETE /supplements/delete/{supplement_id}
Authorization: Bearer your_jwt_token
```

Response (200 OK):
```json
{
  "message": "Supplement deleted successfully"
}
```

### 5. Get Supplement Details

Get detailed information about a specific supplement.

```
GET /supplements/{supplement_id}
Authorization: Bearer your_jwt_token
```

Response (200 OK):
```json
{
  "id": 1,
  "name": "Vitamin D3",
  "description": "Supports bone health and immune function",
  "dosage": "1000 IU daily",
  "stock_level": 30,
  "low_stock_threshold": 5,
  "image_url": "https://example.com/vitamind.jpg",
  "created_at": "2023-06-15T10:00:00"
}
```

## Error Responses

### Authentication Errors

- **401 Unauthorized**: Missing or invalid token
  ```json
  {
    "msg": "Missing Authorization Header"
  }
  ```

- **422 Unprocessable Entity**: Malformed token
  ```json
  {
    "msg": "Not enough segments"
  }
  ```

### Resource Errors

- **404 Not Found**: Supplement not found
  ```json
  {
    "error": "Supplement not found"
  }
  ```

- **403 Forbidden**: Attempting to access a supplement that belongs to another user
  ```json
  {
    "error": "Unauthorized access to supplement"
  }
  ```

- **400 Bad Request**: Missing required fields
  ```json
  {
    "error": "Supplement name is required"
  }
  ```

## Testing with Helper Script

You can use the provided `api_test_helper.py` script to test the API:

```bash
# Get a token
python api_test_helper.py --email your_email@example.com --password your_password --action login

# Create a supplement (automatically handles login)
python api_test_helper.py --email your_email@example.com --password your_password --action create_supplement
```

## Migration Information

The database is currently at migration revision `b4b5b84225fb`, but there is a merge migration `c066c820c9ed` that needs to be applied. To update the database schema, run:

```bash
python -m flask --app run.py db upgrade
```

This will apply the merged migration which includes the `image_url` column in the supplements table.