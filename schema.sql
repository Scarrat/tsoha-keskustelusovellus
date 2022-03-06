CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT, admin BOOLEAN DEFAULT FALSE);
CREATE TABLE cats (id SERIAL PRIMARY KEY, topic TEXT, last_sent TIMESTAMP);
INSERT INTO cats (topic) VALUES ('General');
INSERT INTO cats (topic) VALUES ('Help');
CREATE TABLE threads(id SERIAL PRIMARY KEY, topic TEXT, cat_id INTEGER REFERENCES cats, creator TEXT, created_at TIMESTAMP, last_sent TIMESTAMP);
CREATE TABLE messages (id SERIAL PRIMARY KEY, content TEXT, sender TEXT, user_id INTEGER REFERENCES users, thread_id INTEGER REFERENCES threads, sent_at TIMESTAMP);
CREATE TABLE secretthreads(id SERIAL PRIMARY KEY, topic TEXT, firstmess TEXT, creator TEXT, created_at TIMESTAMP);
CREATE TABLE secretmessages (id SERIAL PRIMARY KEY, content TEXT, sender TEXT, user_id INTEGER REFERENCES users, secretthread_id INTEGER REFERENCES secretthreads, sent_at TIMESTAMP);
