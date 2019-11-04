import datetime
import Connect

def get_driver_abstract():
    '''
    number of tickets, 
    the number of demerit notices, 
    the total number of demerit points 
    received both within the past two years and within the lifetime
    '''
    connection, cursor = Connect.connection, Connect.cursor

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