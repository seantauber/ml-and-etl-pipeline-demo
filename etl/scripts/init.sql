/*

-- This script initializes the database schema and roles for the application.

-- It performs the following tasks:
-- 1. Creates the main 'users' table if it does not already exist.
-- 2. Defines a function 'mask_email' to mask email addresses for privacy.
-- 3. Creates a view 'masked_users' that uses the 'mask_email' function to mask email addresses.
-- 4. Creates roles 'analyst', 'manager', and 'admin' if they do not already exist.
-- 5. Grants appropriate permissions to the roles:
--    - 'analyst' and 'manager' roles can select from the 'masked_users' view.
--    - 'manager' role can also select from the 'users' table.
--    - 'admin' role has all privileges on both 'users' and 'masked_users' tables.
*/
-- Create the main users table
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    email TEXT UNIQUE,
    gender TEXT,
    ip_address TEXT
);

-- Create masking function
CREATE OR REPLACE FUNCTION mask_email(email text) RETURNS text AS $$
BEGIN
  RETURN SUBSTRING(email, 1, 1) || '****' || SUBSTRING(email FROM POSITION('@' IN email));
END;
$$ LANGUAGE plpgsql;

-- Create masked view
CREATE OR REPLACE VIEW masked_users AS
SELECT id, first_name, last_name, mask_email(email) AS email, gender, ip_address
FROM users;

-- Create roles
DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'analyst') THEN
    CREATE ROLE analyst;
  END IF;
  IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'manager') THEN
    CREATE ROLE manager;
  END IF;
  IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'admin') THEN
    CREATE ROLE admin;
  END IF;
END
$$;

-- Grant permissions
GRANT SELECT ON masked_users TO analyst;
GRANT SELECT ON masked_users TO manager;
GRANT SELECT ON users TO manager;
GRANT ALL PRIVILEGES ON users TO admin;
GRANT ALL PRIVILEGES ON masked_users TO admin;
