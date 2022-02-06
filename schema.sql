CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT, admin BOOLEAN);
CREATE TABLE cats (id SERIAL PRIMARY KEY, topic TEXT);
INSERT INTO cats (topic) VALUES ('General');
INSERT INTO cats (topic) VALUES ('Help');
CREATE TABLE threads (id SERIAL PRIMARY KEY, topic TEXT, category_id INTEGER REFERENCES categories, created_at TIMESTAMP);
CREATE TABLE messages (id SERIAL PRIMARY KEY, content TEXT, user_id INTEGER REFERENCES users, thread_id REFERENCES threads, sent_at TIMESTAMP )
