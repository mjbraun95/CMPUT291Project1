import sqlite3
import time
from random import randint
from random import seed
 
connection = None
cursor = None


def connect(path):
    global connection, cursor
 
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return


def register_birth(user_id):
    global connection, cursor
    current_date = time.strftime("%Y-%m-%d") # get current date
    #print(current_date)
    uid = user_id # to find city
    user_city = "Edmonton" ##set to user's city later

    # generate unique registration number
    #print("before while")
    regno = 0
    while True:
        seed(21)
        regno = randint(0, 10000)
        regno_list = []
        cursor.execute("""  SELECT  regno 
                            FROM    births; """                        
                        )
        rows = cursor.fetchall()
        for i in rows:
            #print(int(i[0]))
            regno_list.append(i[0])
        #print(regno_list)

        if regno in regno_list:
            continue
        else:
            break
    #print("done while")

    name = raw_input("Enter full name: ")
    fname, lname = name.split()
    gender = raw_input("Enter gender (M/F): ")
    bdate = current_date
    bplace = raw_input("Enter place of birth: ")
    f_name = raw_input("Enter name of father: ")
    f_fname, f_lname = f_name.split()
    m_name = raw_input("Enter name of mother: ")
    m_fname, m_lname = m_name.split()
    regdate = current_date
    regplace = user_city

    # create the persons entry
    cursor.execute('''INSERT INTO persons VALUES
                    (:fname, :lname, :bdate,
                     :bplace, NULL, NULL
                    );''',
                    {"fname":fname, "lname":lname, "bdate":bdate, 
                    "bplace":bplace
                    }
                    ) 

    # create the births entry
    cursor.execute('''INSERT INTO births VALUES
                    (:regno, :fname, :lname,
                     :regdate, :regplace, :gender,
                     :f_fname, :f_lname, :m_fname, :m_lname
                    );''',
                    {"regno":regno, "fname":fname, "lname":lname,
                     "regdate":regdate, "regplace":regplace, "gender":gender,
                     "f_fname":f_fname, "f_lname":f_lname, "m_fname":m_fname, "m_lname":m_lname
                    }
                    )     

    print("Birth is now registered")

    return


def renew_vehicle_reg():
    regno = 0

    while True:
        regno = raw_input("Enter the registration number: ")
        #print(regno)
        cursor.execute("""  SELECT  regno 
                            FROM    registrations; """                        
                    )
        rows = cursor.fetchall()
        regno_list = []

        for i in rows:
            regno_list.append(int(i[0]))
        #print(regno_list)

        if int(regno) in regno_list:
            break
        elif regno == 'q':
            return
        else:
            print("invalid number")
            continue

    cursor.execute("""  SELECT  expiry 
                        FROM    registrations
                        WHERE   regno = :rn; """,
                    {"rn":regno}
                    )
    fetch = cursor.fetchone()
    #print(fetch[0])
    exp_date = fetch[0]
    currtime = time.strftime("%Y-%m-%d")
    newexp_date = ""

    # get new exp date
    if exp_date > currtime: # if expiry is not yet here
        exp_year = int(exp_date[0:4])
        exp_year += 1
        newexp_date = str(exp_year) + exp_date[4:]
        #print(newexp_date)
    else:
        exp_date = currtime
        exp_year = int(exp_date[0:4])
        exp_year += 1
        newexp_date = str(exp_year) + exp_date[4:]
        #print(newexp_date)

    # update db
    cursor.execute("""  UPDATE  registrations 
                        SET     expiry = :new_exp_date
                        WHERE   regno = :reg_no; """,
                    {"new_exp_date":newexp_date, "reg_no":regno}
                  )
    
    # print update on new date
    print("Expiration date updated to:",newexp_date)

    return


def get_driver_abs():
    '''
    number of tickets, 
    the number of demerit notices, 
    the total number of demerit points 
    received both within the past two years and within the lifetime
    '''
    name = raw_input("Enter full name: ")
    fname, lname = name.split()

    regno_list = []
    reg_list = []
    tno_list = []
    t_list = []
    dem_list = []    

    cursor.execute("""  SELECT  regno 
                        FROM    registrations
                        WHERE   fname = :f_name, lname = :l_name; """,
                    {"f_name":fname, "l_name":lname}
                    )
    rows = cursor.fetchall()
    for rn in rows:
        regno_list.append(rn[0])

    """
    TODO
    """
    while True:
        ordering = raw_input("Order from latest to oldest?")

        if ordering.upper() == "Y":
            ##
            break
        elif ordering.upper() == "N":
            ##
            break
        else:
            continue

    while True:
        view_more = raw_input("View more?")

        if view_more.upper() == "Y":
            ##
            break
        elif view_more.upper() == "N":
            ##
            break
        else:
            continue

    return


def main(user_id, db_path):
    # connect to db
    global connection, cursor 
    path = db_path
    connect(path)
    uid = user_id

    # selection of 1,3,6
    valid_selection = False
    while (not valid_selection):
        user_selection = raw_input( "\nEnter action to perform: \n"
                                    "1 for Registering a birth \n" 
                                    "3 for Renewing a vehicle registration \n" 
                                    "6 for Getting a driver abstract \n" 
                                    "'q' to exit \n")

        if user_selection == "1":
            register_birth(uid)
        elif user_selection == "3":
            renew_vehicle_reg()
        elif user_selection == "6":
            get_driver_abs()
        elif user_selection == "q":
            valid_selection = True
        else:
            print("invalid selection")       
    
    # close db
    print("exiting...")
    connection.commit()
    connection.close()
    return


dbpath = "./vreg.db" ##put path here
user_id = 00000000 ##put user id here
main(user_id, dbpath)