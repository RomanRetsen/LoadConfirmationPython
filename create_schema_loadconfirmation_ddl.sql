CREATE USER loadconfirmation
IDENTIFIED BY loadconfirmation
DEFAULT TABLESPACE USERS
TEMPORARY TABLESPACE TEMP
/
GRANT UNLIMITED TABLESPACE TO loadconfirmation
/
GRANT CONNECT TO loadconfirmation
/
GRANT RESOURCE TO loadconfirmation
/
ALTER USER loadconfirmation DEFAULT ROLE ALL
/