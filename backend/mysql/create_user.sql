-- create_user.sql
CREATE USER IF NOT EXISTS 'ESDPrj'@'%' IDENTIFIED BY 'root';
GRANT ALL PRIVILEGES ON authentication.* TO 'ESDPrj'@'%';
FLUSH PRIVILEGES;
