-- 1. Insert Administrator User --
-- ID: Fixed as requested
-- Password: 'admin1234' hashed with bcrypt

INSERT INTO users (id, email, first_name, last_name, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'admin@hbnb.io',
    'Admin',
    'HBnB',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj40b6.5E5.O', 
    TRUE
);

 -- 2. Insert Amenities --

 INSERT INTO amenities (id, name) VALUES 
('583f7c46-d5e4-41d3-921c-81f72740a631', 'WiFi'),
('21b3f9be-3898-4c80-9969-d419d45d9471', 'Swimming Pool'),
('7a5241e1-1647-4c46-862d-0453d865c342', 'Air Conditioning');
