-- This script prepares a MySQL server for the project.
-- It creates a project testing database with the name: hbnb_test_db.
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- It creates a new user named: hbnb_test with all privileges on the db hbnb_test_db.
-- If the user doesn't exist, it sets the password as: hbnb_test_pwd.
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- It grants the SELECT privilege for the user hbnb_test on the db performance_schema.
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
FLUSH PRIVILEGES;

-- It grants all privileges to the new user on hbnb_test_db.
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';
FLUSH PRIVILEGES;
