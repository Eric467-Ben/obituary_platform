CREATE DATABASE obituary_platform;

-- SQLite implementation used by the Flask app.
CREATE TABLE IF NOT EXISTS obituaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    date_of_death DATE NOT NULL,
    content TEXT NOT NULL,
    author VARCHAR(100) NOT NULL,
    submission_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    slug VARCHAR(255) UNIQUE NOT NULL
);

-- MySQL version of the same table structure.
CREATE TABLE obituaries_mysql (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    date_of_death DATE NOT NULL,
    content TEXT NOT NULL,
    author VARCHAR(100) NOT NULL,
    submission_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    slug VARCHAR(255) UNIQUE NOT NULL
);
