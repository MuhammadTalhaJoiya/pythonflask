# All APIs and Testing Steps

This document lists all APIs in the Flask application, grouped by blueprint, with step-by-step testing instructions using a tool like Postman. Most endpoints require JWT authentication obtained from /auth/login.

## Authentication APIs (/auth)

### POST /auth/signup
- **Description**: Register a new user.
- **Testing Steps**:
  1. Open Postman and create a POST request to `http://127.0.0.1:5000/auth/signup`.
  2. Set body to raw JSON: {"name": "Test User", "email": "test@example.com", "password": "password123"}.
  3. Send request and check for 201 response with user details.
  4. Verify user is added to the database.

### POST /auth/login
- **Description**: Login and get JWT tokens.
- **Testing Steps**:
  1. POST to `http://127.0.0.1:5000/auth/login` with JSON: {"email": "test@example.com", "password": "password123"}.
  2. Verify 200 response with access_token and refresh_token.
  3. Copy the access_token for use in authenticated requests.

### POST /auth/logout
- **Description**: Logout and invalidate token.
- **Testing Steps**:
  1. POST to `http://127.0.0.1:5000/auth/logout` with Authorization: Bearer <access_token>.
  2. Verify 200 response with message 'Successfully logged out'.
  3. Attempt to use the same token in another request to confirm it's invalid.

### POST /auth/refresh-token
- **Description**: Refresh access token using refresh token.
- **Testing Steps**:
  1. POST to `http://127.0.0.1:5000/auth/refresh-token` with Authorization: Bearer <refresh_token>.
  2. Verify 200 response with new access_token.

### POST /auth/verify-email
- **Description**: Verify user's email (mock).
- **Testing Steps**:
  1. POST to `http://127.0.0.1:5000/auth/verify-email` with Bearer token.
  2. Verify 200 response with 'Email verified successfully'.

### POST /auth/forgot-password
- **Description**: Send password reset link (mock).
- **Testing Steps**:
  1. POST to `http://127.0.0.1:5000/auth/forgot-password` with JSON: {"email": "test@example.com"}.
  2. Verify 200 response with message including the email.

### POST /auth/reset-password
- **Description**: Reset password.
- **Testing Steps**:
  1. POST to `http://127.0.0.1:5000/auth/reset-password` with JSON: {"email": "test@example.com", "password": "newpassword123"}.
  2. Verify 200 response with 'Password reset successfully'.
  3. Attempt login with new password to confirm.

## User APIs (/user)

### GET /user/profile
- **Description**: Get user profile.
- **Testing Steps**:
  1. GET to `http://127.0.0.1:5000/user/profile` with Bearer token.
  2. Verify 200 response with user details.

### PUT /user/profile/update
- **Description**: Update user profile.
- **Testing Steps**:
  1. PUT to `http://127.0.0.1:5000/user/profile/update` with Bearer token and JSON: {"name": "Updated Name"}.
  2. Verify 200 response with updated details.
  3. GET profile to confirm changes.

### POST /user/invite-family-member
- **Description**: Invite a family member.
- **Testing Steps**:
  1. POST to `http://127.0.0.1:5000/user/invite-family-member` with Bearer token and JSON: {"name": "Family", "email": "family@example.com"}.
  2. Verify 201 response with family member details.

### GET /user/family-members
- **Description**: Get family members.
- **Testing Steps**:
  1. GET to `http://127.0.0.1:5000/user/family-members` with Bearer token.
  2. Verify 200 response with list of family members.

## Supplements APIs (/supplements)

### POST /supplements/create
- **Description**: Create a new supplement.
- **Testing Steps**:
  1. POST to `http://127.0.0.1:5000/supplements/create` with Bearer token and JSON: {"name": "Vitamin C", "description": "Daily vitamin"}.
  2. Verify 201 response with supplement_id.

### GET /supplements/all
- **Description**: Get all supplements.
- **Testing Steps**:
  1. GET to `http://127.0.0.1:5000/supplements/all` with Bearer token.
  2. Verify 200 response with list of supplements.

### PUT /supplements/update/<supplement_id>
- **Description**: Update a supplement.
- **Testing Steps**:
  1. PUT to `http://127.0.0.1:5000/supplements/update/1` with Bearer token and JSON: {"name": "Updated Vitamin"}.
  2. Verify 200 response.
  3. GET all to confirm update.

### DELETE /supplements/delete/<supplement_id>
- **Description**: Delete a supplement.
- **Testing Steps**:
  1. DELETE to `http://127.0.0.1:5000/supplements/delete/1` with Bearer token.
  2. Verify 200 response.
  3. GET all to confirm deletion.

### POST /supplements/log-intake
- **Description**: Log supplement intake.
- **Testing Steps**:
  1. POST to `http://127.0.0.1:5000/supplements/log-intake` with Bearer token and JSON: {"supplement_id": 1, "dosage_taken": 1}.
  2. Verify 201 response with intake_id.

### GET /supplements/today-intake/<member_id>
- **Description**: Get today's intake for a member.
- **Testing Steps**:
  1. GET to `http://127.0.0.1:5000/supplements/today-intake/1` with Bearer token.
  2. Verify 200 response with list of intakes.

### POST /supplements/upload-image/<supplement_id>
- **Description**: Upload supplement image.
- **Testing Steps**:
  1. POST to `http://127.0.0.1:5000/supplements/upload-image/1` with Bearer token and multipart form with 'image' file.
  2. Verify 201 response with image_url.

### POST /supplements/photo-confirmation
- **Description**: Upload photo confirmation for intake.
- **Testing Steps**:
  1. POST to `http://127.0.0.1:5000/supplements/photo-confirmation` with Bearer token, multipart form with 'photo' file and 'intake_id'.
  2. Verify 201 response.

### POST /supplements/reminder-settings
- **Description**: Set reminder settings.
- **Testing Steps**:
  1. POST to `http://127.0.0.1:5000/supplements/reminder-settings` with Bearer token and JSON: {"supplement_id": 1, "time": "08:00", "days": "Mon,Tue"}.
  2. Verify 201 response with reminder_id.

### GET /supplements/stats/<member_id>
- **Description**: Get supplement stats for a member.
- **Testing Steps**:
  1. GET to `http://127.0.0.1:5000/supplements/stats/1` with Bearer token.
  2. Verify 200 response with stats.

### GET /supplements/low-stock-alerts
- **Description**: Get low stock alerts.
- **Testing Steps**:
  1. GET to `http://127.0.0.1:5000/supplements/low-stock-alerts` with Bearer token.
  2. Verify 200 response with alerts.

### GET /supplements/history/<member_id>
- **Description**: Get intake history for a member.
- **Testing Steps**:
  1. GET to `http://127.0.0.1:5000/supplements/history/1` with Bearer token and optional query params like start_date.
  2. Verify 200 response with history list.

## Compliance APIs (/compliance)

### GET /compliance/daily/<member_id>
- **Description**: Get daily compliance.
- **Testing Steps**:
  1. GET to `http://127.0.0.1:5000/compliance/daily/1` with Bearer token and optional ?date=YYYY-MM-DD.
  2. Verify 200 response with compliance data.

### GET /compliance/weekly/<member_id>
- **Description**: Get weekly compliance.
- **Testing Steps**:
  1. GET to `http://127.0.0.1:5000/compliance/weekly/1` with Bearer token and optional ?date=YYYY-MM-DD.
  2. Verify 200 response with weekly data and breakdown.

### GET /compliance/monthly/<member_id>
- **Description**: Get monthly compliance.
- **Testing Steps**:
  1. GET to `http://127.0.0.1:5000/compliance/monthly/1` with Bearer token and optional ?month=1&year=2023.
  2. Verify 200 response with monthly data and breakdown.

### GET /compliance/leaderboard/<family_id>
- **Description**: Get family compliance leaderboard.
- **Testing Steps**:
  1. GET to `http://127.0.0.1:5000/compliance/leaderboard/0` with Bearer token and optional ?period=weekly.
  2. Verify 200 response with leaderboard.

### POST /compliance/export-report
- **Description**: Export compliance report.
- **Testing Steps**:
  1. POST to `http://127.0.0.1:5000/compliance/export-report` with Bearer token and JSON: {"member_id": 1, "period": "monthly", "format": "csv"}.
  2. Verify response with report data or file.

## Subscription APIs (/subscription)

### GET /subscription/tiers
- **Description**: Get subscription tiers.
- **Testing Steps**:
  1. GET to `http://127.0.0.1:5000/subscription/tiers` with Bearer token.
  2. Verify 200 response with tiers list.

### POST /subscription/start
- **Description**: Start a subscription.
- **Testing Steps**:
  1. POST to `http://127.0.0.1:5000/subscription/start` with Bearer token and JSON: {"family_id": 1, "tier": "premium"}.
  2. Verify 201 response with subscription_id.

### POST /subscription/pause
- **Description**: Pause subscription.
- **Testing Steps**:
  1. POST to `http://127.0.0.1:5000/subscription/pause` with Bearer token and JSON: {"subscription_id": 1}.
  2. Verify 200 response.

### POST /subscription/resume
- **Description**: Resume subscription.
- **Testing Steps**:
  1. POST to `http://127.0.0.1:5000/subscription/resume` with Bearer token and JSON: {"subscription_id": 1}.
  2. Verify 200 response.

### POST /subscription/modify
- **Description**: Modify subscription tier.
- **Testing Steps**:
  1. POST to `http://127.0.0.1:5000/subscription/modify` with Bearer token and JSON: {"subscription_id": 1, "new_tier": "family"}.
  2. Verify 200 response.

### POST /subscription/add-product
- **Description**: Add product to subscription.
- **Testing Steps**:
  1. POST to `http://127.0.0.1:5000/subscription/add-product` with Bearer token and JSON: {"subscription_id": 1, "product_id": 1, "quantity": 2}.
  2. Verify 201 response.

### GET /subscription/status/<family_id>
- **Description**: Get subscription status.
- **Testing Steps**:
  1. GET to `http://127.0.0.1:5000/subscription/status/1` with Bearer token.
  2. Verify 200 response with status list.

### GET /subscription/history/<family_id>
- **Description**: Get subscription history.
- **Testing Steps**:
  1. GET to `http://127.0.0.1:5000/subscription/history/1` with Bearer token.
  2. Verify 200 response with history list.

## Rewards APIs (/rewards)

### GET /rewards/balance
- **Description**: Get reward balance.
- **Testing Steps**:
  1. GET to `http://127.0.0.1:5000/rewards/balance` with Bearer token.
  2. Verify 200 response with balance.

### POST /rewards/earn
- **Description**: Earn points.
- **Testing Steps**:
  1. POST to `http://127.0.0.1:5000/rewards/earn` with Bearer token and JSON: {"points": 10, "description": "Test earn"}.
  2. Verify 200 response with new_balance.

### POST /rewards/spend
- **Description**: Spend points.
- **Testing Steps**:
  1. POST to `http://127.0.0.1:5000/rewards/spend` with Bearer token and JSON: {"points": 5, "description": "Test spend"}.
  2. Verify 200 response with new_balance.

### GET /rewards/history
- **Description**: Get reward history.
- **Testing Steps**:
  1. GET to `http://127.0.0.1:5000/rewards/history` with Bearer token.
  2. Verify 200 response with transactions list.

### GET /rewards/streaks/<member_id>
- **Description**: Get streaks for a member.
- **Testing Steps**:
  1. GET to `http://127.0.0.1:5000/rewards/streaks/1` with Bearer token.
  2. Verify 200 response with streak.

### GET /rewards/challenges
- **Description**: Get active challenges.
- **Testing Steps**:
  1. GET to `http://127.0.0.1:5000/rewards/challenges` with Bearer token.
  2. Verify 200 response with challenges list.

### POST /rewards/claim-challenge
- **Description**: Claim a challenge.
- **Testing Steps**:
  1. POST to `http://127.0.0.1:5000/rewards/claim-challenge` with Bearer token and JSON: {"challenge_id": 1}.
  2. Verify 200 response with new_balance.

### POST /rewards/refer-friend
- **Description**: Refer a friend.
- **Testing Steps**:
  1. POST to `http://127.0.0.1:5000/rewards/refer-friend` with Bearer token and JSON: {"referred_email": "friend@example.com"}.
  2. Verify 200 response with new_balance.

## Admin APIs (/admin)

*Note: Requires 'admin' role.*

### GET /admin/users
- **Description**: Get all users.
- **Testing Steps**:
  1. GET to `http://127.0.0.1:5000/admin/users` with Bearer token (admin).
  2. Verify 200 response with users list.

### GET /admin/orders
- **Description**: Get all orders.
- **Testing Steps**:
  1. GET to `http://127.0.0.1:5000/admin/orders` with Bearer token (admin).
  2. Verify 200 response with orders list.

### POST /admin/product/update
- **Description**: Update a product.
- **Testing Steps**:
  1. POST to `http://127.0.0.1:5000/admin/product/update` with Bearer token (admin) and JSON: {"id": 1, "name": "Updated Product"}.
  2. Verify 200 response.

### GET /admin/reports
- **Description**: Get reports.
- **Testing Steps**:
  1. GET to `http://127.0.0.1:5000/admin/reports` with Bearer token (admin).
  2. Verify 200 response with report data.

### POST /admin/notifications/broadcast
- **Description**: Broadcast notification.
- **Testing Steps**:
  1. POST to `http://127.0.0.1:5000/admin/notifications/broadcast` with Bearer token (admin) and JSON: {"message": "Test broadcast"}.
  2. Verify 200 response.