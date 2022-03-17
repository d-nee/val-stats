Names:
Daniel Nee - dnee@caltech.edu
Amy Pham - apham@caltech.edu


Our project is a Valorant stats database.

Our data is scraped from the website tracker.gg
We took all the matches cataloged that were played by the players in data/page_players.csv
We then took all the players in all those games and added them and their statistics to the various tables.
Scraping was slow, and anti-bot measures limited us to starting with 4 'seed' players,
and we collected data on 156 games.

A complete setup of our database can be found in 'create_db.sql', which includes
'CREATE DATABASE' code in addition to loading the data and sql code very much
in line with the 'Testing your project' section at the bottom of the spec, with
the exception of 'queries.sql', which should be run in isolation.

Running 'source create_db.sql' with the working directory as the root folder
in mysql should completely setup the project.


As for the command line, there are two files - app-client.py and app-admin.py
Both can be run with 'python3 app-*.py', replacing * with the desired suffix.
Once started, both should provide enough information to operate.


The only difference between the two is the ability of admin to run a 
'remove_player_game' action described in the menu. Otherwise, both have
the same query functionality, with the exception of being unable to login
with the basic client login information for app-admin.

The logins are as below. User 'client' cannot use app_admin.

User: client
Pass: 3478

User: admin
Pass: stronk_pw


IGNs (names) and Tags (discriminators) of the 4 initial 'players' in page are listed
below for convenience of querying:

IGN: synesthesiac
Tag: 1881

IGN: amypham4
Tag: 7708

IGN: burnell
Tag: 6969

IGN: vale
Tag: bop