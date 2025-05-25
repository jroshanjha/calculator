# CREATE DATABASE salary_db;

# USE salary_db;

# CREATE TABLE salary_increase (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     old_salary FLOAT,
#     new_salary FLOAT,
#     percentage_increase FLOAT,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );

# CREATE DATABASE salary_db;

# USE salary_db;

# CREATE TABLE users (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     username VARCHAR(100) UNIQUE NOT NULL,
#     password VARCHAR(255) NOT NULL
# );

# CREATE TABLE salary_records (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     user_id INT,
#     old_salary FLOAT,
#     new_salary FLOAT,
#     percentage_increase FLOAT,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
# );

