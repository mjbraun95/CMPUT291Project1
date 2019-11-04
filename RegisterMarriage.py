import datetime
import RegisterBirth

def register_a_marriage(connection, cursor, username):
    # global connection, cursor

    partner1 = input("first name followed by last name of partner 1, seperated by a space: ")
    partner1 = partner1.split()
    partner1 = [partner1[0].capitalize(), partner1[1].capitalize()]
    check(connection, cursor, partner1)
    partner2 = input("first name followed by last name of partner 2, seperated by a space: ")
    partner2 = partner2.split()
    partner2 = [partner2[0].capitalize(), partner2[1].capitalize()]
    check(connection, cursor, partner2)

    cursor.execute('SELECT max(regno) FROM marriages ')
    maxregno = cursor.fetchall()

    #registration number = unique
    newregno = maxregno[0][0]+1

    #registration date = today
    today = datetime.date.today()

    #registration place = city of user
    cursor.execute('select * from users where uid = :username', {"username": username})
    user = cursor.fetchall()
    regplace = user[0][5]

    #register the marriage
    cursor.execute(
        'insert into marriages values (:newregno, :today, :regplace, :partner1first, :partner1last, :partner2first, :partner2last);',
        {"newregno": newregno, "today": today, "regplace": regplace, "partner1first": partner1[0],
         "partner1last": partner1[1], "partner2first": partner2[0], "partner2last": partner2[1]})
    connection.commit()

def check(connection, cursor, person):
    # global connection, cursor
    cursor.execute('SELECT * FROM persons where fname = :first and lname = :last;', {"first": person[0], "last": person[1]})
    if len(cursor.fetchall()) == 0:
        #call register a birth function
        RegisterBirth.register_a_birth()
