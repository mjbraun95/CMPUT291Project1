import datetime
import Connect

debugIssueTicket = True

def issue_a_ticket():
    connection, cursor = Connect.connection, Connect.cursor
    current_reg = None
    #get regno
    if debugIssueTicket == True:
        print("cursor: {}".format(cursor))
        cursor.execute('SELECT * FROM registrations')
        debugQuery = 0
        while debugQuery != None:
            debugQuery = cursor.fetchone()
            if debugQuery != None:
                print(debugQuery)

    regno = input("vehicle regno: ")
    regno_not_exist = True
    # while regno is not valid keep askingif debugIssueTicket == True:
    # get owner + vehicle information
    while regno_not_exist:
        cursor.execute('SELECT * FROM registrations JOIN vehicles WHERE registrations.regno = :regno AND registrations.vin = vehicles.vin',
                       {"regno": regno})
        current_reg = cursor.fetchall()
        if len(current_reg) != 0:
            print(current_reg)
            regno_not_exist = False
        else:
            regno = input("input a valid vehicle regno: ")

    fname = current_reg[0][5]
    lname = current_reg[0][6]
    violationDate = input("Please enter the violation date: ")
    if violationDate == "":
        violationDate = datetime.datetime.today().strftime('%Y-%m-%d')
        print("Set violation date to {}".format(violationDate))
    violationText = input("Please enter the violation text: ")
    fineAmount = input("Please enter the fine amount: ")

    #insert new ticket no
    cursor.execute('SELECT max(tno) FROM tickets ')
    maxtno = cursor.fetchall()

    # registration number = unique
    newtno = maxtno[0][0] + 1

    if debugIssueTicket == True:
        print("TICKETS BEFORE:")
        cursor.execute('SELECT * FROM tickets')
        debugQuery = 0
        while debugQuery != None:
            debugQuery = cursor.fetchone()
            if debugQuery != None:
                print(debugQuery)

    cursor.execute(
        'INSERT INTO tickets VALUES (:newtno, :regno, :fineAmount, :violationText, :violationDate);',
        {"newtno": newtno, "regno": regno, "fineAmount": fineAmount, "violationText": violationText,
            "violationDate": violationDate})

    if debugIssueTicket == True:
        print("TICKETS AFTER:")
        cursor.execute('SELECT * FROM tickets')
        debugQuery = 0
        while debugQuery != None:
            debugQuery = cursor.fetchone()
            if debugQuery != None:
                print(debugQuery)

    print("A ticket has been created for {} {}.".format(fname, lname))
    connection.commit()