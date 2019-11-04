import IssueTicket
import ProcessSale
import ProcessPayment
import IssueTicket
import FindCarOwner
import RegisterMarriage
import Login
import Connect

debugInterface = True

def interface(connection, cursor, userLoginQuery):
    connection, cursor = Connect.connection, Connect.cursor
    uid = userLoginQuery[0]
    pwd = userLoginQuery[1]
    utype = userLoginQuery[2]
    fname = userLoginQuery[3]
    lname = userLoginQuery[4]
    city = userLoginQuery[5]
    q = False
    print("Welcome, {} {}.".format(fname, lname))
    if debugInterface == True:
        print("cursor: {}".format(cursor))
    if utype == "a":
        while q == False:
            userInput = input("What would you like to do?:\n    rb - Register a Birth\n    rm - Register a marriage\n    rvr - Renew Vehicle Registration\n    pbs - Process a Bill of Sale\n    pp - Process a Payment\n    gda - Get a Driver Abstract\n    lo - log out\n    q - Quit\n")
            if userInput == "rb":
                break
            elif userInput == "rm":
                RegisterMarriage.register_a_marriage(uid)
            elif userInput == "rvr":
                break
            elif userInput == "pbs":
                ProcessSale.process_a_bill_of_sale()
            elif userInput == "pp":
                ProcessPayment.process_a_payment()
            elif userInput == "gda":
                break
            elif userInput == "lo":
                Login.logoff(connection, cursor)
            elif userInput == "q":
                exit()
            else:
                print("Invalid command. Please try again.")
    elif utype == "o":
        while q == False:
            userInput = input("What would you like to do?:\n    it - Issue a Ticket\n    fca - Find a Car Owner\n    lo - log out\n    q - Quit\n")
            if userInput == "it":
                IssueTicket.issue_a_ticket()
            elif userInput == "fca":
                FindCarOwner.find_a_car_owner()
            elif userInput == "lo":
                Login.logoff()
            elif userInput == "q":
                exit()
            else:
                print("Invalid command. Please try again.")
    return 0