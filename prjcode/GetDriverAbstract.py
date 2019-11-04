import datetime
import Connect

debugGetDriverAbstract = True

def get_driver_abstract():
    connection, cursor = Connect.connection, Connect.cursor
    if debugGetDriverAbstract == True:
        cursor.execute('SELECT fname, lname FROM users')
        debugQuery = 0
        while debugQuery != None:
            debugQuery = cursor.fetchone()
            if debugQuery != None:
                print(debugQuery)

    '''
    number of tickets, 
    the number of demerit notices, 
    the total number of demerit points 
    received both within the past two years and within the lifetime
    '''

    name = input("Enter full name: ")
    fname, lname = name.split()

    regno_list = []
    reg_list = []
    tno_list = []
    t_list = []
    dem_list = []    

    cursor.execute("""  SELECT  regno 
                        FROM    registrations
                        WHERE   fname = :f_name AND lname = :l_name; """,
                    {"f_name":fname, "l_name":lname}
                    )
    # cursor.execute('SELECT address, phone FROM persons where fname = :first and lname = :last;',
    #                {"first": Mother[0], "last": Mother[1]})
    rows = cursor.fetchall()
    for rn in rows:
        regno_list.append(rn[0])

    """
    TODO
    """
    while True:
        ordering = input("Order from latest to oldest? (Y/n)")

        if debugGetDriverAbstract == True:
            # cursor.execute('SELECT * FROM demeritNotices JOIN registrations JOIN tickets WHERE demeritNotices.fname = :fname AND demeritNotices.lname = :lname AND demeritNotices.fname = registrations.fname AND demeritNotices.lname = registrations.lname AND tickets.regno = registrations.regno', {"fname": fname, "lname": lname})
            cursor.execute("SELECT regno from tickets")
            debugQuery = 0
            noTickets = 0
            while debugQuery != None:
                debugQuery = cursor.fetchone()
                noTickets += 1
                if debugQuery != None:
                    print(debugQuery)

            cursor.execute('SELECT registrations.fname, registrations.lname, tickets.tno, tickets.vdate, tickets.violation, tickets.fine, tickets.regno, vehicles.make, vehicles.model FROM demeritNotices JOIN registrations JOIN tickets JOIN vehicles WHERE demeritNotices.fname = :fname AND demeritNotices.lname = :lname AND demeritNotices.fname = registrations.fname AND demeritNotices.lname = registrations.lname AND tickets.regno = registrations.regno AND vehicles.vin = registrations.vin', {"fname": fname, "lname": lname})

            debugQuery = 0
            while debugQuery != None:
                debugQuery = cursor.fetchone()
                if debugQuery != None:
                    print(debugQuery)


        if ordering.upper() == "Y" or ordering.upper() == "":

            ##
            break
        elif ordering.upper() == "N":
            ##
            break
        else:
            continue

    while True:
        view_more = input("View more? (Y/n)")

        if view_more.upper() == "Y" or ordering.upper() == "":
            ##
            break
        elif view_more.upper() == "N":
            ##
            break
        else:
            continue

    return