# Admin API Testing Guide

## Prerequisites

1. **Flask Server Running**
   - Start the Flask server with: `python run.py`
   - Server should be running at: http://127.0.0.1:5000

2. **Admin Account**
   - Default admin credentials:
     - Email: `admin@example.com`
     - Password: `adminpassword`

## Testing Methods

### 1. Using the Comprehensive Test Script

The easiest way to test all admin APIs at once:

```bash
python test_all_admin_apis.py
```

This script will:
- Login as admin and obtain a JWT token
- Test all admin endpoints
- Display detailed results for each API call

### 2. Testing Individual Admin APIs

#### Admin Login

```bash
python test_admin_login.py
```

#### Product Update

```bash
python test_admin_product_update.py
```

### 3. Manual Testing with curl

#### Step 1: Get Admin Token

```bash
curl -X POST http://127.0.0.1:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"adminpassword"}'
```

#### Step 2: Use Token for Admin APIs

**Get Users**
```bash
curl -X GET http://127.0.0.1:5000/admin/users \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Get Orders**
```bash
curl -X GET http://127.0.0.1:5000/admin/orders \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Update Product**
```bash
curl -X POST http://127.0.0.1:5000/admin/product/update \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{"id":1,"name":"Updated Product Name","price":29.99}'
```

**Get Reports**
```bash
curl -X GET http://127.0.0.1:5000/admin/reports \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Broadcast Notification**
```bash
curl -X POST http://127.0.0.1:5000/admin/notifications/broadcast \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{"message":"Test broadcast message"}'
```

### 4. Testing with Postman

1. Create a new request collection
2. Add a POST request to `/auth/login` with admin credentials
3. Extract the token from the response
4. For each admin endpoint:
   - Create a new request
   - Set the Authorization header to `Bearer YOUR_TOKEN`
   - Send the request and verify the response

## Troubleshooting

### Connection Refused

If you see errors like:
```
ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it
```

Make sure:
1. The Flask server is running (`python run.py`)
2. You're using the correct URL (http://127.0.0.1:5000)

### 403 Forbidden

If you receive 403 errors:
1. Verify you're using admin credentials
2. Check that the token is correctly included in the Authorization header
3. Ensure the token hasn't expired

### 404 Not Found

For product update errors:
1. Make sure the product ID exists in the database
2. You can create a test product with: `python create_test_product.py`