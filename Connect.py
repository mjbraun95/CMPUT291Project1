import sqlite3

debugConnect = True
connection = None
cursor = None

def connect():
    global connection, cursor

    connection = sqlite3.connect("./Data/db1.db")
    cursor = connection.cursor()
    cursor.execute(' PRAGMA forteign_keys=ON; ')
    connection.commit()
    return

def listTables():
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cursor.fetchall())

def reload():
    tables = open("./Data/tables.txt")
    data = open("./Data/data.txt")
    tables_sql = tables.readline()

    cnt = 1
    while tables_sql:
        if debugConnect == True:
            print("tables_sql {}: {}".format(cnt, tables_sql))
        tables_sql = tables.readline()
        cnt += 1

def commit():
    print("committing...", end=" ")
    connection.commit()
    print("Done!")

if __name__ == "__main__":
    listTables()
    commit()