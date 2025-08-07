-- Fix Admin Permissions SQL Script
-- Run this script to ensure admin user has correct permissions

-- Check current users and their roles
SELECT id, email, name, role, verified, created_at 
FROM users 
ORDER BY created_at DESC;

-- Update existing admin user to have admin role
UPDATE users 
SET role = 'admin', verified = 1 
WHERE email = 'admin@example.com';

-- If admin user doesn't exist, create it
-- (Note: You'll need to generate a proper password hash)
INSERT OR IGNORE INTO users (name, email, password_hash, role, verified, created_at)
VALUES ('Admin User', 'admin@example.com', 
        'pbkdf2:sha256:260000$8a9a2c8b9d4e5f6g$h7i8j9k0l1m2n3o4p5q6r7s8t9u0v1w2x3y4z5a6b7c8d9e0f1', 
        'admin', 1, datetime('now'));

-- Verify admin user
SELECT id, email, name, role, verified 
FROM users 
WHERE email = 'admin@example.com';

-- Check if any other users have admin role
SELECT id, email, name, role 
FROM users 
WHERE role = 'admin';