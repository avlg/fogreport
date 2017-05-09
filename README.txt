This is a Hello World application for my GitHub account.

A Python 3 script for the FOG Project http://fogproject.org
implementing some graphical reporting from the FOG database.

GETTING STARTED:
- clone this repository
- add a read-only user into the FOG MySQL database (see db_createuser.sql)
- copy config.ini to config-my.ini
- edit config-my.ini
- see requirements.txt for the list of required Python modules.
  Install all required modules using pip.
- read the script
- run the script
- consult fog_db_schema.txt for extending the script.
  Connect to the MySQL database with the mysql client using the previously
  configured user to issue some commands like
  USE fog; SHOW TABLES; SHOW COLUMNS FROM inventory;
  for more information on the database schema.

USAGE:
TODO

FEATURES:
- Inventory report (work in progress)

BUGS:
- Alot! :)

Enjoy!
Vladimir Afanasiev
May 2017
