"""
Names:
Daniel Nee - dnee@caltech.edu
Amy Pham - apham@caltech.edu

This is the client interface, which allows 3 different querying actions.
"""
import sys  # to print error messages to sys.stderr
import mysql.connector
# To get error codes from the connector, useful for user-friendly
# error-handling
import mysql.connector.errorcode as errorcode
# Debugging flag to print errors when debugging that shouldn't be visible
# to an actual client. Set to False when done testing.
DEBUG = True
# ----------------------------------------------------------------------
# SQL Utility Functions
# ----------------------------------------------------------------------
def get_conn():
    """"
    Returns a connected MySQL connector instance, if connection is successful.
    If unsuccessful, exits.
    """
    try:
        conn = mysql.connector.connect(
          host='localhost',
          user='appclient',
          port='3306',
          password='clientpw',
          database='val_stats'
        )
        print('Successfully connected.')
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR and DEBUG:
            sys.stderr('Incorrect username or password when connecting to DB.')
        elif err.errno == errorcode.ER_BAD_DB_ERROR and DEBUG:
            sys.stderr('Database does not exist.')
        elif DEBUG:
            sys.stderr(err)
        else:
            sys.stderr('An error occurred, please contact the administrator.')
        sys.exit(1)
# ----------------------------------------------------------------------
# Functions for Command-Line Options/Query Execution
# ----------------------------------------------------------------------
def query_overall():
    # Uses the materializd view to quickly give overall stats
    name = input("IGN of player: ").lower()
    discrim = input("Tag of player: ")
    cursor = conn.cursor()
    sql = """
    SELECT *
    FROM mv_player_overall_stat
    WHERE ign = '%s' AND discrim = '%s';
    """ % (name, discrim, )
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        if result == None:
            print("Invalid IGN/Discrim")
        else:
            print("(IGN, discrim, total_kills, total_deaths, total_matches)")
            print(result)
            print("")
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, check DEBUG')
    show_options()

def query_agent():
    # Queries the database for agent-group summary statistics
    name = input("IGN of player: ").lower()
    discrim = input("Tag of player: ")
    cursor = conn.cursor()
    sql = """
    SELECT agent, AVG(acs) AS a_acs, AVG(adr), AVG(aes)
    FROM game_stat
    WHERE ign = '%s' AND discrim = '%s'
    GROUP BY agent
    ORDER BY a_acs DESC;
    """ % (name, discrim, )
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        if len(rows) == 0:
            print("Invalid IGN/Discrim")
        else:
            print("(Agent, Avg_ACS, Avg_ADR, Avg_AES)")
            for row in rows:
                print(row)
            print("")
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, check DEBUG')
    show_options()

def query_teammates():
    # Queries the database for the most often played with players
    name = input("IGN of player: ").lower()
    discrim = input("Tag of player: ")
    cursor = conn.cursor()
    sql = """
    WITH
        user_games AS (
            SELECT gamehash FROM game_stat
            WHERE ign = '%s' AND discrim = '%s'
        )
    SELECT ign, discrim, COUNT(*) AS num_games
    FROM user_games NATURAL JOIN game_stat
    GROUP BY ign, discrim
    ORDER BY num_games DESC;
    """ % (name, discrim, )
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        if len(rows) == 0:
            print("Invalid IGN/Discrim")
        else:
            print("(IGN, discrim, num_shared_games)")
            for i in range(2, min(7, len(rows))):
                print(rows[i])
            print("")
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, check DEBUG')
    show_options()

# ----------------------------------------------------------------------
# Functions for Logging Users In
# ----------------------------------------------------------------------
def login():
    # Handles authentication, logging in through the general authentication
    cursor = conn.cursor()
    success = False
    print("Enter Username and Password. Program exits after 3 failed attempts.")
    for i in range(3):
        user = input("Username: ")
        pwd = input("Password: ")
        sql = "SELECT authenticate('%s','%s');" % (user, pwd, )
        try:
            cursor.execute(sql)
            result = cursor.fetchone()[0]
            if result == 1:
                success = True
                break
        except mysql.connector.Error as err:
            sys.stderr('User Authentication Error. Check setup-passwords.')
        print("\nFailed\n")
    print("")
    if not success:
        print("Failed Authentication")
        exit(1)

# ----------------------------------------------------------------------
# Command-Line Functionality
# ----------------------------------------------------------------------
def show_options():
    """
    Displays options users can choose in the application, such as
    viewing <x>, filtering results with a flag (e.g. -s to sort),
    sending a request to do <x>, etc.
    """
    print('\nWhat would you like to do? ')
    print('  (1) - pull a player\'s overall stats')
    print('  (2) - pull a player\'s stats grouped by agent')
    print('  (3) - pull a player\'s top 5 teammates by frequency')
    print('  (4) - quit')
    print('')
    ans = input('Enter an option: ').lower()
    if ans == '1':
        query_overall()
    elif ans == '2':
        query_agent()
    elif ans == '3':
        query_teammates()
    elif ans == '4':
        print('Good Bye!')
        exit()
    else:
        print('Pick a valid option.')
        show_options()
        

def main():
    """
    Main function for starting things up.
    """
    login()
    show_options()


if __name__ == '__main__':
    # Initialize the connection and start the program
    conn = get_conn()
    main()