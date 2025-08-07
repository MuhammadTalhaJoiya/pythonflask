# API Authentication Guide

## Overview

This guide explains how to authenticate with the API to avoid 401 Unauthorized errors when making requests.

## Authentication Process

1. **Login to get a JWT token**
   - Send a POST request to `/auth/login` with your email and password
   - Save the returned access token

2. **Use the token in subsequent requests**
   - Include the token in the Authorization header
   - Format: `Authorization: Bearer your_token_here`

## Example Using curl

```bash
# 1. Login to get token
curl -X POST http://127.0.0.1:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"your_email@example.com","password":"your_password"}'

# 2. Use token to create a supplement
curl -X POST http://127.0.0.1:5000/supplements/create \
  -H "Authorization: Bearer your_token_here" \
  -H "Content-Type: application/json" \
  -d '{"name":"Vitamin D","description":"Daily vitamin","dosage":"1000 IU","stock_level":30,"low_stock_threshold":5,"image_url":"https://example.com/vitamind.jpg"}'
```

## Example Using the Helper Script

We've provided a helper script to simplify API testing:

```bash
# Get a token
python api_test_helper.py --email your_email@example.com --password your_password --action login

# Create a supplement (automatically handles login)
python api_test_helper.py --email your_email@example.com --password your_password --action create_supplement
```

## Common Authentication Errors

- **401 Unauthorized**: Missing or invalid token
  - Solution: Ensure you're including the token in the Authorization header
  
- **422 Unprocessable Entity**: Malformed token
  - Solution: Check that your token format is correct and not expired

## Token Expiration

JWT tokens expire after a certain period. If you receive a 401 error after previously successful requests, your token may have expired. Simply login again to get a new token.