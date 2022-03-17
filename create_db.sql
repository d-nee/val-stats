DROP DATABASE IF EXISTS val_stats;
CREATE DATABASE val_stats;
USE val_stats;
source setup.sql;
source load-data.sql;
source setup-passwords.sql;
source grant-permissions.sql;
source setup-routines.sql;