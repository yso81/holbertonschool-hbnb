-- TEST 1: READ (Verify Initial Data) --

SELECT '--> Verify Admin User:' AS 'Check';
SELECT id, email, is_admin FROM users WHERE email = 'admin@hbnb.io';

SELECT '--> Verify Amenities:' AS 'Check';
SELECT * FROM amenities;

-- TEST 2: CREATE & CONSTRAINTS (Verify Integrity) --

-- INSERT INTO users (id, email, first_name, last_name, password) 
-- Create a regular user for testing updates
INSERT INTO users (id, email, first_name, last_name, password, is_admin)
VALUES ('11111111-1111-1111-1111-111111111111', 'test@test.com', 'Test', 'User', 'pass', FALSE);

SELECT '--> User Created:' AS 'Check';
SELECT * FROM users WHERE email = 'test@test.com';

-- TEST 3: UPDATE (Verify Data Modification) --

UPDATE users SET first_name = 'UpdatedName' WHERE email = 'test@test.com';

SELECT '--> User Updated:' AS 'Check';
SELECT first_name FROM users WHERE email = 'test@test.com';

-- TEST 4: DELETE (Verify Removal) --

DELETE FROM users WHERE email = 'test@test.com';

SELECT '--> User Deleted (Should be empty):' AS 'Check';
SELECT * FROM users WHERE email = 'test@test.com';
