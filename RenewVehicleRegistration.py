import datetime
import Connect

debugRenewVehicleRegistration = True

#function 3
# Renew a vehicle registration.The user should be able to provide an existing registration number and renew the registration.
# The system should set the new expiry date to one year from today's date if the current registration either has expired
# or expires today. Otherwise, the system should set the new expiry to one year after the current expiry date.
def renew_vehicle_registration():
    connection, cursor = Connect.connection, Connect.cursor
    if debugRenewVehicleRegistration == True:
        cursor.execute('SELECT * FROM registrations')
        debugQuery = 0
        while debugQuery != None:
            debugQuery = cursor.fetchone()
            if debugQuery != None:
                print(debugQuery)
    
    #get registration number
    reg = None
    regno = None
    while not reg:
        regno = input("Enter the registrations number of the registration to renew: ")
        cursor.execute('SELECT * FROM registrations where regno = :regno ',
                       {"regno": regno})
        reg = cursor.fetchall()
        if len(cursor.fetchall()) != 0:
            reg = reg[0]

    #set expiry to one year from today if expired or expiring today
    year, month, day = reg[0][2].split('-')
    expiry = datetime.date(int(year), int(month), int(day))
    today = datetime.date.today()
    if (expiry == today) or (expiry < today):
        expiry = today.replace(year=today.year + 1)
    else:
        expiry = expiry.replace(year=expiry.year + 1)

    
    if debugRenewVehicleRegistration == True:
        print("REGISTRATIONS BEFORE")
        cursor.execute('SELECT * FROM registrations')
        debugQuery = 0
        while debugQuery != None:
            debugQuery = cursor.fetchone()
            if debugQuery != None:
                print(debugQuery)
    #update table
    cursor.execute('UPDATE registrations SET expiry = :expiry where regno = :regno;',
                   {"expiry":expiry, "regno": regno})

    if debugRenewVehicleRegistration == True:
        print("REGISTRATIONS AFTER")
        cursor.execute('SELECT * FROM registrations')
        debugQuery = 0
        while debugQuery != None:
            debugQuery = cursor.fetchone()
            if debugQuery != None:
                print(debugQuery)

    connection.commit()