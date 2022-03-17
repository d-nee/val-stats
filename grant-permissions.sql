CREATE USER 'appadmin'@'localhost' IDENTIFIED BY 'adminpw';
CREATE USER 'appclient'@'localhost' IDENTIFIED BY 'clientpw';
GRANT ALL PRIVILEGES ON val_stats.* TO 'appadmin'@'localhost';
GRANT SELECT ON val_stats.* TO 'appclient'@'localhost';
GRANT EXECUTE ON FUNCTION val_stats.authenticate TO 'appclient'@'localhost';
FLUSH PRIVILEGES;
