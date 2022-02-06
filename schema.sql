CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT, admin BOOLEAN);
CREATE TABLE threads (id SERIAL PRIMARY KEY, topic TEXT, created_at TIMESTAMP);
CREATE TABLE categories (topic TEXT);
