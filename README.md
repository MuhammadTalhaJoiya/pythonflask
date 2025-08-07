# Mobile App Backend

## Features

### Authentication
- User registration
- User login
- Token refresh
- Logout

### User Management
- Get user profile
- Update user profile
- Invite family members
- View family members

### Supplements Management
- View all supplements
- Log supplement intake
- View today's intake for a member
- Upload photo confirmation of intake
- Set reminder settings
- View supplement statistics
- Get low stock alerts
- View supplement history

## Models

### User
- id: Primary key
- name: User's name
- email: User's email (unique)
- password_hash: Hashed password
- created_at: Timestamp
- verified: Boolean flag

### FamilyMember
- id: Primary key
- user_id: Foreign key to User
- name: Family member's name
- email: Family member's email
- status: Status of invitation (pending, accepted)
- created_at: Timestamp

### Supplement
- id: Primary key
- name: Supplement name
- description: Supplement description
- dosage: Recommended dosage
- stock_level: Current stock level
- low_stock_threshold: Threshold for low stock alerts
- created_at: Timestamp
- user_id: Foreign key to User

### SupplementIntake
- id: Primary key
- supplement_id: Foreign key to Supplement
- user_id: Foreign key to User
- family_member_id: Foreign key to FamilyMember (optional)
- taken_at: Timestamp of intake
- dosage_taken: Actual dosage taken
- notes: Additional notes
- photo_confirmation: Path to photo confirmation

### Reminder
- id: Primary key
- supplement_id: Foreign key to Supplement
- user_id: Foreign key to User
- family_member_id: Foreign key to FamilyMember (optional)
- time: Time of day for reminder
- days: Days of week for reminder
- active: Boolean flag
- created_at: Timestamp

## API Endpoints

### Authentication
- POST /auth/register - Register a new user
- POST /auth/login - Login and get tokens
- POST /auth/refresh-token - Refresh access token
- POST /auth/logout - Logout and invalidate token

### User Management
- GET /user/profile - Get user profile
- PUT /user/profile/update - Update user profile
- POST /user/invite-family-member - Invite a family member
- GET /user/family-members - Get all family members

### Supplements Management
- GET /supplements/all - Get all supplements
- POST /supplements/log-intake - Log supplement intake
- GET /supplements/today-intake/:memberId - Get today's intake for a member
- POST /supplements/photo-confirmation - Upload photo confirmation
- POST /supplements/reminder-settings - Set reminder settings
- GET /supplements/stats/:memberId - Get supplement statistics
- GET /supplements/low-stock-alerts - Get low stock alerts
- GET /supplements/history/:memberId - View supplement history