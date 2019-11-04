from getpass import getpass
import Connect
import Interface

uid = None
pwd = None
utype = None
fname = None
lname = None
city = None

connection = None
cursor = None

debugLogin = True

def login():
    username = input("Enter username: ")
    password = getpass()

    Connect.connect()
    # Connect.listTables()
    connection, cursor = Connect.connection, Connect.cursor
    cursor.execute('SELECT * FROM users WHERE users.uid=?;',(username,))
    # cursor.execute("SELECT table FROM sqlite_master WHERE type = 'table' AND tbl_name = 'users'")
    userLoginQuery = cursor.fetchone()
    if userLoginQuery == None:
        print("Invalid username or password. Please try again.")
        return None
    if debugLogin == True:
        print("Username: {}".format(username))
        print("Password: {}".format(password))
        print("userLoginQuery: {}".format(userLoginQuery))
        print("len(userLoginQuery): {}".format(len(userLoginQuery)))
        cursor.execute('SELECT * FROM users')
        for i in range(6):
            debugQuery = cursor.fetchone()
            print(debugQuery)
    connection.commit()

    uid = userLoginQuery[0]
    pwd = userLoginQuery[1]
    utype = userLoginQuery[2]
    fname = userLoginQuery[3]
    lname = userLoginQuery[4]
    city = userLoginQuery[5]

    if password == pwd:
        print("Login successful!")
        return userLoginQuery
    else:
        print("Invalid username or password. Please try again.")
        return None

def logoff(connection, cursor):
    uid = None
    pwd = None
    utype = None
    fname = None
    lname = None
    city = None
    loginPrompt()

def loginPrompt():
    userLoginQuery = None
    while userLoginQuery == None:
        userLoginQuery = login()
    Interface.interface(connection, cursor, userLoginQuery)

if __name__ == "__main__":
    loginPrompt()