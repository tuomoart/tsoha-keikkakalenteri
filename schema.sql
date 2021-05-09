CREATE TABLE users (id SERIAL PRIMARY KEY, name TEXT, username TEXT, password TEXT, usergroup TEXT, email TEXT, phone TEXT);
CREATE TABLE locations (id SERIAL PRIMARY KEY, name TEXT);
CREATE TABLE jobs (id SERIAL PRIMARY KEY, name TEXT, time TEXT, location INT);
CREATE TABLE participants (id SERIAL PRIMARY KEY, jobId INT, userId INT, status TEXT);