CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT, admin BOOLEAN);
CREATE TABLE cats (id SERIAL PRIMARY KEY, topic TEXT);
INSERT INTO cats (topic) VALUES ('General');
INSERT INTO cats (topic) VALUES ('Help');
CREATE TABLE threads(id SERIAL PRIMARY KEY, topic TEXT, firstmess TEXT, cat_id INTEGER REFERENCES cats, creator TEXT, created_at TIMESTAMP);
CREATE TABLE messages (id SERIAL PRIMARY KEY, content TEXT, sender TEXT, thread_id INTEGER REFERENCES threads, sent_at TIMESTAMP );
