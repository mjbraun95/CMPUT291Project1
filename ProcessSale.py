import datetime
import Connect
import GetName
import RegisterPerson

debugProcessSale = True

def process_a_bill_of_sale():
    connection, cursor = Connect.connection, Connect.cursor
    if debugProcessSale == True:
        cursor.execute('SELECT * FROM vehicles JOIN registrations WHERE vehicles.vin = registrations.vin')
        debugQuery = 0
        while debugQuery != None:
            debugQuery = cursor.fetchone()
            if debugQuery != None:
                print(debugQuery)
    
    current_reg = None
    #get vin
    vin = input("vehicle vin: ")
    vin_not_exist = True
    # while vin is not valid keep asking
    while vin_not_exist:
        cursor.execute('SELECT * FROM registrations where vin = :vin',
                       {"vin": vin})
        current_reg = cursor.fetchall()
        print(current_reg)
        if len(current_reg) != 0:
            vin_not_exist = False
        else:
            vin = input("input a valid vehicle vin: ")
    #get current owner
    current_owner = GetName.get_name("current owner")
                # current_owner = input("first name followed by last name of current owner, seperated by a space: ")
                # current_owner = current_owner .split()
                # current_owner = [current_owner[0].capitalize(), current_owner[1].capitalize()]
    #if invalid current owner cancel
    if current_reg[0][5] != current_owner[0] or current_reg[0][6] != current_owner[1]:
        print("data provided does not match, transfer cannot be made")
        return
    else:
        #else if valid current owner continue
        #get new owner
        new_owner = GetName.get_name("new owner")
                    # new_owner = input("first name followed by last name of new owner, seperated by a space: ")
                    # new_owner = new_owner.split()
                    # new_owner = [new_owner[0].capitalize(), new_owner[1].capitalize()]
        #if new owner not in persons register a birth()
        cursor.execute("Select * from persons where fname = :fname and lname = :lname", {"fname": new_owner[0], "lname": new_owner[1]})
        temp_row = cursor.fetchall()
        if len(temp_row) != 1:
            print("new owner not in database, cannot process sale")
            return
        #if RegisterPerson.check(new_owner) == 1:
            #return
        # else continue
        #get plate number
        invalid_plate = True
        plate = input("plate number, with maximum of 7 characters: ")

        if debugProcessSale == True:
            print("REGISTRATIONS BEFORE")
            cursor.execute('SELECT * FROM vehicles JOIN registrations WHERE vehicles.vin = registrations.vin')
            debugQuery = 0
            while debugQuery != None:
                debugQuery = cursor.fetchone()
                if debugQuery != None:
                    print(debugQuery)

        while invalid_plate:
            if len(plate) <= 7:
                invalid_plate = False
            else:
                plate = input("input a valid plate number, with maximum of 7 characters: ")

        #process sale

        #update expiry of old registration
        today = datetime.date.today()
        cursor.execute('UPDATE registrations SET expiry = :today where regno = :current;', {"today": today, "current": current_reg[0][0]})

        #insert new registration
        cursor.execute('SELECT max(regno) FROM registrations ')
        maxregno = cursor.fetchall()

        # registration number = unique
        newregno = maxregno[0][0] + 1

        #expirydate
        expiry = today.replace(year=today.year + 1)

        cursor.execute(
            'insert into registrations values (:newregno, :today, :expiry, :plate, :vin, :fname, :lname);',
            {"newregno": newregno, "today": today, "expiry": expiry, "plate": plate,
             "vin": vin, "fname": new_owner[0], "lname": new_owner[1]})

        if debugProcessSale == True:
            print("REGISTRATIONS AFTER")
            cursor.execute('SELECT * FROM vehicles')# JOIN registrations WHERE vehicles.vin = registrations.vin')
            debugQuery = 0
            while debugQuery != None:
                debugQuery = cursor.fetchone()
                if debugQuery != None:
                    print(debugQuery)

    connection.commit()

# def check(new_owner):
#     connection, cursor = Connect.connection, Connect.cursor
#     cursor.execute('SELECT * FROM persons where fname = :first and lname = :last;', {"first": new_owner[0], "last": new_owner[1]})
#     if len(cursor.fetchall()) == 0:
#         #call register a birth function
#         print("ERROR: New Owner could not be found in the database! Returning to menu...")
#         return 1
#     else:
#         return 0