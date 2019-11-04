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
    Connect.connect()
    connection, cursor = Connect.connection, Connect.cursor
    if debugLogin == True:
        cursor.execute('SELECT * FROM users')
        debugQuery = 0
        while debugQuery != None:
            debugQuery = cursor.fetchone()
            if debugQuery != None:
                print(debugQuery)
    username = input("Enter username: ").lower()
    password = getpass()
    cursor.execute('SELECT * FROM users WHERE users.uid=?;',(username,))
    userLoginQuery = cursor.fetchone()
    if debugLogin == True:
        print("Username: {}".format(username))
        print("Password: {}".format(password))
        print("userLoginQuery: {}".format(userLoginQuery))
    if userLoginQuery == None:
        print("Invalid username or password. Please try again.")
        return None
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

def logoff():
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