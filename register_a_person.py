def pre_reg(person):
    # bdate = True
    bdate = input("Enter the birth date of person to register, in format 'YYYY-MM-DD': ")
    isValidDate = True

    while isValidDate and bdate != '':
        try:
            year, month, day = bdate.split('-')
            datetime.datetime(int(year), int(month), int(day))
            break
        except ValueError:
            bdate = input("Enter the date in format 'YYYY-MM-DD': ")

    if not bdate:
        bdate = None

    bplace = input("birth place of person: ")
    if not bplace:
        bdate = None

    address = input("address of person: ")
    if not address:
        bdate = None

    phone = input("phone number of person: ")
    if not phone:
        bdate = None

    register_a_person(person,bdate,bplace,address,phone)

def register_a_person(person,bdate,bplace,address,phone):
    #persons(fname, lname, bdate, bplace, address, phone)

    #register the person
    #persons(fname, lname, bdate, bplace, address, phone)
    cursor.execute(
        'insert into persons values (:fname, :lname, :bdate, :bplace, :address, :phone);',
        {"fname": person[0], "lname": person[1], "bdate":bdate, "bplace": bplace,
         "address": address, "phone": phone})

    connection.commit()

def check(person):
    global connection, cursor
    cursor.execute('SELECT * FROM persons where fname = :first and lname = :last;', {"first": person[0], "last": person[1]})
    if len(cursor.fetchall()) == 0:
        print('person not in database. registering person-->')
        pre_reg(person)