-- Salt Generation
DELIMITER !
CREATE FUNCTION make_salt(num_chars INT)
RETURNS VARCHAR(20) DETERMINISTIC
BEGIN
    DECLARE salt VARCHAR(20) DEFAULT '';
    -- Don't want to generate more than 20 characters of salt.
    SET num_chars = LEAST(20, num_chars);
    -- Generate the salt!  Characters used are ASCII code 32 (space)
    -- through 126 ('z').
    WHILE num_chars > 0 DO
        SET salt = CONCAT(salt, CHAR(32 + FLOOR(RAND() * 95)));
        SET num_chars = num_chars - 1;
    END WHILE;
    RETURN salt;
END !
DELIMITER ;
-- This table holds information for authenticating users based on
-- a password.  Passwords are not stored plaintext so that they
-- cannot be used by people that shouldn't have them.
-- You may extend that table to include an is_admin or role attribute if you 
-- have admin or other roles for users in your application 
-- (e.g. store managers, data managers, etc.)
CREATE TABLE user_info (
    -- Usernames are up to 20 characters.
    username VARCHAR(20) PRIMARY KEY,
    -- Salt will be 8 characters all the time, so we can make this 8.
    salt CHAR(8) NOT NULL,
    -- We use SHA-2 with 256-bit hashes.  MySQL returns the hash
    -- value as a hexadecimal string, which means that each byte is
    -- represented as 2 characters.  Thus, 256 / 8 * 2 = 64.
    -- We can use BINARY or CHAR here; BINARY simply has a different
    -- definition for comparison/sorting than CHAR.
    password_hash BINARY(64) NOT NULL,
    -- Admin boolean
    is_admin TINYINT,
    CHECK(is_admin IN (0, 1))
);
-- [Problem 1a]
-- Adds a new user to the user_info table, using the specified password (max
-- of 20 characters). Salts the password with a newly-generated salt value,
-- and then the salt and hash values are both stored in the table.
DELIMITER !
CREATE PROCEDURE sp_add_user(
    new_username VARCHAR(20),
    password VARCHAR(20),
    is_admin TINYINT
)
BEGIN
    DECLARE salt          CHAR(8);
    SELECT make_salt(8) INTO salt;
    INSERT INTO user_info
    VALUES (new_username, salt, SHA2(CONCAT(salt, password), 256), is_admin);
END !
DELIMITER ;
-- [Problem 1b]
-- Authenticates the specified username and password against the data
-- in the user_info table.  Returns 1 if the user appears in the table, and the
-- specified password hashes to the value for the user. Otherwise returns 0.
DELIMITER !
CREATE FUNCTION authenticate(username VARCHAR(20), password VARCHAR(20))
RETURNS TINYINT DETERMINISTIC
BEGIN
    DECLARE count_name  TINYINT;
    DECLARE target_salt CHAR(8);
    DECLARE target_hash BINARY(64);
    SELECT COUNT(*) INTO count_name FROM user_info
    WHERE user_info.username = username;
    IF count_name = 0 THEN RETURN 0;
    END IF;
    SELECT salt, password_hash INTO target_salt, target_hash FROM user_info
    WHERE user_info.username = username;
    IF SHA2(CONCAT(target_salt, password), 256) = target_hash THEN RETURN 1;
    ELSE RETURN 0;
    END IF;
    RETURN 0;
END !
DELIMITER ;

-- Authenticates if the specified username and password are an admin
DELIMITER !
CREATE FUNCTION authenticate_admin(username VARCHAR(20), password VARCHAR(20))
RETURNS TINYINT DETERMINISTIC
BEGIN
    DECLARE count_name  TINYINT;
    DECLARE target_salt CHAR(8);
    DECLARE target_hash BINARY(64);
    SELECT COUNT(*) INTO count_name FROM user_info
    WHERE user_info.username = username AND is_admin = 1;
    IF count_name = 0 THEN RETURN 0;
    END IF;
    SELECT salt, password_hash INTO target_salt, target_hash FROM user_info
    WHERE user_info.username = username AND is_admin = 1;
    IF SHA2(CONCAT(target_salt, password), 256) = target_hash THEN RETURN 1;
    ELSE RETURN 0;
    END IF;
    RETURN 0;
END !
DELIMITER ;
-- [Problem 1c]
-- Add at least two users into your user_info table so that when we run this file,
-- we will have examples users in the database.
CALL sp_add_user('client', '3478', 0);
CALL sp_add_user('admin', 'stronk_pw', 1);