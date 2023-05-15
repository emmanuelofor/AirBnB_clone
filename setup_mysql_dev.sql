-- This script configures a MySQL server for project-related tasks.
-- A new database 'hbnb_dev_db' is created if it does not exist already.
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- A new user 'hbnb_dev' is created if it does not exist. This user is identified by the password 'hbnb_dev_pwd'.
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- All privileges are granted to the user 'hbnb_dev' on the 'hbnb_dev_db' database.
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';

-- Privilege information in memory is reloaded to ensure that changes take effect immediately.
FLUSH PRIVILEGES;

-- The SELECT privilege is granted to the user 'hbnb_dev' on the 'performance_schema' database.
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';

-- Again, privilege information in memory is reloaded to ensure that changes take effect immediately.
FLUSH PRIVILEGES;
