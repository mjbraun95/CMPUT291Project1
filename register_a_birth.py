#function 1
#Register a birth.The agent should be able to register a birth by providing the first name, the last name, the gender,
# the birth date, the birth place of the newborn, as well as the first and last names of the parents. The registration
# date is set to the day of registration (today's date) and the registration place is set to the city of the user.
# The system should automatically assign a unique registration number to the birth record. The address and the phone of
# the newborn are set to those of the mother. If any of the parents is not in the database, the system should get
# information about the parent including first name, last name, birth date, birth place, address and phone.
# For each parent, any column other than the first name and last name can be null if it is not provided.
def register_a_birth(username):
    #get first name and last name
    newborn_name = get_name("newborn")

    #get gender
    gender = input("gender of newborn. 'F' for female and 'M' fro male: ")
    gender = gender.capitalize()
    while gender != 'F' and gender != 'M':
        gender = input("input a valid gender of newborn. 'F' for female and 'M' fro male: ")

    #birth date
    bdate = input("Enter the birth date in format 'YYYY-MM-DD': ")
    isValidDate = True

    while isValidDate:
        try:
            year, month, day = bdate.split('-')
            datetime.datetime(int(year), int(month), int(day))
            break
        except ValueError:
            bdate = input("Enter the date in format 'YYYY-MM-DD': ")

    if not bdate:
        bdate = None

    #birth place
    birth_place = input("birth place of newborn: ")
    #what if null must give something
    while birth_place == '':
        birth_place = input("birth place of newborn: ")
    #first and last name of father
    Father = get_name("father")
    check(Father)

    #first and last name of mother
    Mother = get_name("mother")
    check(Mother)

    #registration num
    cursor.execute('SELECT max(regno) FROM births')
    maxregno = cursor.fetchall()
    newregno = maxregno[0][0] + 1

    #registration date
    today = datetime.date.today()

    #registration place
    cursor.execute('select * from users')
    user = cursor.fetchall()
    print (user)
    cursor.execute('select * from users where uid = :username', {"username": username})
    print (username)
    user = cursor.fetchall()
    print(user)
    reg_place = user[0][5]

    #address of mother
    cursor.execute('SELECT address, phone FROM persons where fname = :first and lname = :last;',
                   {"first": Mother[0], "last": Mother[1]})
    row = cursor.fetchall()
    print(row)
    if len (row)==0:
        address = None
        phone = None
    else:
        address = row[0][0]
        phone = row[0][1]

    #phone number of mother

    # register the person
    register_a_person(newborn_name, bdate, birth_place, address, phone)

    #register the birth
    #insert into births values (1,'Mary','Smith','1920-04-04','Ohaton,AB','F','James','Smith','Linda','Smith');
    #births(regno, fname, lname, regdate, reg_place, gender, f_fname, f_lname, m_fname, m_lname)
    cursor.execute(
        'insert into births values (:regno, :fname, :lname, :today, :reg_place, :gender, :f_fname, :f_lname, :m_fname, :m_lname);',
        {"regno": newregno, "fname": newborn_name[0], "lname": newborn_name[1], "today": today, "reg_place": reg_place, "gender": gender, "f_fname": Father[0],
         "f_lname": Father[1],  "m_fname": Mother[0],  "m_lname": Mother[1]})

    connection.commit()