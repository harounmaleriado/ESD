-- create_user.sql
CREATE USER IF NOT EXISTS 'reviewUser'@'%' IDENTIFIED BY 'reviewPass';
GRANT ALL PRIVILEGES ON authentication.* TO 'reviewUser'@'%';
FLUSH PRIVILEGES;
