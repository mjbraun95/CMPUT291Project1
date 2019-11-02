def process_a_bill_of_sale():
    global connection, cursor

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
    current_owner = input("first name followed by last name of current owner, seperated by a space: ")
    current_owner = current_owner .split()
    current_owner = [current_owner[0].capitalize(), current_owner[1].capitalize()]
    #if invalid current owner cancel
    if current_reg[0][5] != current_owner[0] or current_reg[0][6] != current_owner[1]:
        print("data provided does not match, transfer cannot be made")
        return
    else:
        #else if valid current owner continue
        #get new owner
        new_owner = input("first name followed by last name of new owner, seperated by a space: ")
        new_owner = new_owner.split()
        new_owner = [new_owner[0].capitalize(), new_owner[1].capitalize()]
        #if new owner not in persons register a birth()
        check(new_owner)
        # else continue
        #get plate number
        invalid_plate = True
        plate = input("plate number, with maximum of 7 characters: ")
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

    connection.commit()