# Updated Admin API Documentation

## Overview
This guide covers the updated admin APIs with enhanced functionality, improved error handling, and new endpoints. All endpoints require admin authentication via JWT token.

## Prerequisites
1. Flask server running on `http://127.0.0.1:5000`
2. Admin account credentials (default: `admin@example.com` / `adminpassword`)
3. Valid JWT token obtained through login

## Authentication
All admin endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## Updated Admin Endpoints

### 1. Get Users (Enhanced)
**GET** `/admin/users`

**Query Parameters:**
- `page` (int): Page number (default: 1)
- `per_page` (int): Items per page (default: 20)
- `role` (string): Filter by role ('user' or 'admin')
- `search` (string): Search in email and name
- `sort_by` (string): Sort field ('id', 'email', 'created_at')
- `sort_order` (string): Sort order ('asc' or 'desc')

**Example Request:**
```bash
curl -X GET "http://127.0.0.1:5000/admin/users?page=1&per_page=5&role=user&search=test" \
  -H "Authorization: Bearer <token>"
```

**Response:**
```json
{
  "users": [
    {
      "id": 1,
      "email": "user@example.com",
      "name": "Test User",
      "role": "user",
      "created_at": "2024-01-15T10:30:00",
      "is_verified": true
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 5,
    "total": 100,
    "pages": 20
  }
}
```

### 2. Get User by ID (NEW)
**GET** `/admin/users/<user_id>`

**Example Request:**
```bash
curl -X GET "http://127.0.0.1:5000/admin/users/1" \
  -H "Authorization: Bearer <token>"
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "Test User",
  "role": "user",
  "created_at": "2024-01-15T10:30:00",
  "is_verified": true,
  "orders_count": 5
}
```

### 3. Update User Role (NEW)
**PUT** `/admin/users/<user_id>/role`

**Request Body:**
```json
{
  "role": "admin"
}
```

**Example Request:**
```bash
curl -X PUT "http://127.0.0.1:5000/admin/users/5/role" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"role": "admin"}'
```

**Response:**
```json
{
  "message": "User role updated successfully",
  "user_id": 5,
  "new_role": "admin"
}
```

### 4. Get Orders (Enhanced)
**GET** `/admin/orders`

**Query Parameters:**
- `page` (int): Page number (default: 1)
- `per_page` (int): Items per page (default: 20)
- `status` (string): Filter by order status
- `user_id` (int): Filter by user ID
- `sort_by` (string): Sort field ('id', 'created_at', 'total_price')
- `sort_order` (string): Sort order ('asc' or 'desc')

**Example Request:**
```bash
curl -X GET "http://127.0.0.1:5000/admin/orders?status=pending&page=1&per_page=10" \
  -H "Authorization: Bearer <token>"
```

**Response:**
```json
{
  "orders": [
    {
      "id": 1,
      "user_id": 1,
      "user_email": "user@example.com",
      "status": "pending",
      "total_price": 99.99,
      "created_at": "2024-01-15T10:30:00",
      "items": [...]
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 50,
    "pages": 5
  }
}
```

### 5. Get Products (NEW)
**GET** `/admin/products`

**Query Parameters:**
- `page` (int): Page number (default: 1)
- `per_page` (int): Items per page (default: 20)
- `search` (string): Search in name and description
- `sort_by` (string): Sort field ('id', 'name', 'price', 'stock')
- `sort_order` (string): Sort order ('asc' or 'desc')

**Example Request:**
```bash
curl -X GET "http://127.0.0.1:5000/admin/products?search=laptop&page=1&per_page=10" \
  -H "Authorization: Bearer <token>"
```

**Response:**
```json
{
  "products": [
    {
      "id": 1,
      "name": "Laptop Pro",
      "description": "High-performance laptop",
      "price": 999.99,
      "stock": 50,
      "created_at": "2024-01-15T10:30:00"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 100,
    "pages": 10
  }
}
```

### 6. Update Product (Enhanced)
**POST** `/admin/product/update`

**Request Body:**
```json
{
  "id": 1,
  "name": "Updated Product Name",
  "description": "Updated description",
  "price": 29.99,
  "stock": 100
}
```

**Example Request:**
```bash
curl -X POST "http://127.0.0.1:5000/admin/product/update" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"id": 1, "name": "Updated Product", "price": 29.99, "stock": 100}'
```

**Response:**
```json
{
  "message": "Product updated successfully",
  "product": {
    "id": 1,
    "name": "Updated Product",
    "price": 29.99,
    "stock": 100
  }
}
```

### 7. Delete Product (NEW)
**DELETE** `/admin/products/<product_id>`

**Example Request:**
```bash
curl -X DELETE "http://127.0.0.1:5000/admin/products/1" \
  -H "Authorization: Bearer <token>"
```

**Response:**
```json
{
  "message": "Product deleted successfully",
  "product_id": 1
}
```

### 8. Get Reports (Enhanced)
**GET** `/admin/reports`

**Example Request:**
```bash
curl -X GET "http://127.0.0.1:5000/admin/reports" \
  -H "Authorization: Bearer <token>"
```

**Response:**
```json
{
  "overview": {
    "total_users": 100,
    "total_orders": 200,
    "total_products": 50,
    "total_revenue": 15000.00
  },
  "user_distribution": {
    "users": 90,
    "admins": 10
  },
  "order_distribution": {
    "pending": 20,
    "processing": 15,
    "shipped": 50,
    "delivered": 100,
    "cancelled": 15
  },
  "recent_activity": {
    "users_last_7_days": 15,
    "orders_last_7_days": 25,
    "revenue_last_7_days": 2500.00
  }
}
```

### 9. Broadcast Notification (Enhanced)
**POST** `/admin/notifications/broadcast`

**Request Body:**
```json
{
  "message": "Important system update",
  "target_audience": "all",
  "priority": "high"
}
```

**Parameters:**
- `message` (string, required): The notification message
- `target_audience` (string): Target audience ('all', 'users', 'admins')
- `priority` (string): Priority level ('low', 'normal', 'high')

**Example Request:**
```bash
curl -X POST "http://127.0.0.1:5000/admin/notifications/broadcast" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"message": "System maintenance at 2 AM", "target_audience": "all", "priority": "high"}'
```

**Response:**
```json
{
  "message": "Broadcast sent successfully",
  "recipients": 100,
  "target_audience": "all",
  "priority": "high",
  "timestamp": "2024-01-15T10:30:00"
}
```

### 10. System Health (NEW)
**GET** `/admin/system/health`

**Example Request:**
```bash
curl -X GET "http://127.0.0.1:5000/admin/system/health" \
  -H "Authorization: Bearer <token>"
```

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2024-01-15T10:30:00",
  "counts": {
    "users": 100,
    "orders": 200,
    "products": 50
  }
}
```

## Error Handling
All endpoints return consistent error responses:

**400 Bad Request:**
```json
{
  "error": "INVALID_DATA",
  "message": "Invalid input data",
  "details": "Price must be a positive number"
}
```

**403 Forbidden:**
```json
{
  "error": "ADMIN_REQUIRED",
  "message": "Admin access required"
}
```

**404 Not Found:**
```json
{
  "error": "NOT_FOUND",
  "message": "User not found"
}
```

## Testing
Use the provided `test_updated_admin_apis.py` script to test all endpoints:

```bash
python test_updated_admin_apis.py
```

## Postman Collection
You can import the following Postman collection structure:

```json
{
  "info": {
    "name": "Updated Admin APIs",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Authentication",
      "item": [
        {
          "name": "Admin Login",
          "request": {
            "method": "POST",
            "url": "http://127.0.0.1:5000/auth/login",
            "body": {
              "mode": "raw",
              "raw": "{\"email\": \"admin@example.com\", \"password\": \"adminpassword\"}"
            }
          }
        }
      ]
    },
    {
      "name": "Users",
      "item": [
        {
          "name": "Get Users",
          "request": {
            "method": "GET",
            "url": "http://127.0.0.1:5000/admin/users?page=1&per_page=10"
          }
        },
        {
          "name": "Get User by ID",
          "request": {
            "method": "GET",
            "url": "http://127.0.0.1:5000/admin/users/1"
          }
        },
        {
          "name": "Update User Role",
          "request": {
            "method": "PUT",
            "url": "http://127.0.0.1:5000/admin/users/5/role",
            "body": {
              "mode": "raw",
              "raw": "{\"role\": \"admin\"}"
            }
          }
        }
      ]
    }
  ]
}
```

## Troubleshooting

### Common Issues and Solutions

1. **403 Forbidden Error**
   - Ensure you're using admin credentials
   - Check that the user has 'admin' role in database
   - Verify token is correctly formatted in Authorization header

2. **400 Bad Request**
   - Check required fields in request body
   - Validate data types (e.g., price must be number)
   - Ensure JSON format is correct

3. **404 Not Found**
   - Verify resource exists (user/product ID)
   - Check URL path is correct

4. **Connection Errors**
   - Ensure Flask server is running
   - Check port number (default: 5000)
   - Verify base URL is correct

### Quick Setup Checklist
- [ ] Flask server running
- [ ] Admin user exists with role='admin'
- [ ] JWT secret key configured
- [ ] Database connected
- [ ] All blueprints registered

## Rate Limiting
Consider implementing rate limiting for production use:
- Login attempts: 5 per minute
- API requests: 100 per minute per IP
- Admin endpoints: 50 per minute per user