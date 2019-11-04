import datetime
import Connect

debugIssueTicket = True

def searchCar():
    make = None 
    model = None 
    year = None 
    color = None 
    plate = None
    connection, cursor = Connect.connection, Connect.cursor
    searchParameter = None
    while searchParameter != "":
        if searchParameter == None:
            searchParameter = input("Please choose a search parameter:\n    make\n    model\n    year\n    color\n    plate\n")
        else:
            searchParameter = input("Please choose another search parameter, or just press enter to search:\n    make\n    model\n    year\n    color\n    plate\n")
        if searchParameter == "make":
            make = input("enter make: ")
        elif searchParameter == "model":
            model = input("enter model: ")
        elif searchParameter == "year":
            year = input("enter year: ")
        elif searchParameter == "color":
            color = input("enter color: ")
        elif searchParameter == "plate":
            plate = input("enter plate: ")
        elif searchParameter != "":
            print("Invalid parameter. Please try again.")

    #query results
    if debugIssueTicket == True:
        cursor.execute('SELECT * FROM registrations JOIN vehicles WHERE registrations.vin = vehicles.vin')
        debugQuery = 0
        while debugQuery != None:
            debugQuery = cursor.fetchone()
            if debugQuery != None:
                print(debugQuery)

    cursor.execute('SELECT * FROM registrations JOIN vehicles WHERE registrations.vin = vehicles.vin AND (:make IS NULL OR vehicles.make=:make) AND (:model IS NULL OR vehicles.model=:model) AND (:year IS NULL OR vehicles.year=:year) AND (:color IS NULL OR vehicles.color=:color) AND (:plate IS NULL OR registrations.plate=:plate)', {"make": make, "model": model, "year": year, "color": color, "plate": plate})
    querylen = len(cursor.fetchall())
    # More than 4 results case
    if querylen > 4:
        cursor.execute('SELECT vehicles.make, vehicles.model, vehicles.year, vehicles.color, registrations.plate FROM registrations JOIN vehicles WHERE registrations.vin = vehicles.vin AND (:make IS NULL OR vehicles.make=:make) AND (:model IS NULL OR vehicles.model=:model) AND (:year IS NULL OR vehicles.year=:year) AND (:color IS NULL OR vehicles.color=:color) AND (:plate IS NULL OR registrations.plate=:plate)', {"make": make, "model": model, "year": year, "color": color, "plate": plate})

    # No search results case
    elif querylen == 0:
        tryAgain = print("No results found.")
        return
    #4 or less results case
    else:
        cursor.execute('SELECT vehicles.make, vehicles.model, vehicles.year, vehicles.color, registrations.plate, registrations.regdate, registrations.expiry, registrations.fname, registrations.lname FROM registrations JOIN vehicles WHERE registrations.vin = vehicles.vin AND (:make IS NULL OR vehicles.make=:make) AND (:model IS NULL OR vehicles.model=:model) AND (:year IS NULL OR vehicles.year=:year) AND (:color IS NULL OR vehicles.color=:color) AND (:plate IS NULL OR registrations.plate=:plate)', {"make": make, "model": model, "year": year, "color": color, "plate": plate})
    query = 0
    print("Search Results: ")
    while query != None:
        query = cursor.fetchone()
        if query != None:
            print(query)
    return



def find_a_car_owner():
    connection, cursor = Connect.connection, Connect.cursor
    # define search parameter
    tryAgain = None
    searchCar()
    while tryAgain != "n":
        tryAgain = input("Would you like to try another search query? (Y/n): ")
        if tryAgain == "" or tryAgain == "y":
            searchCar()
        elif tryAgain != "n":
            print("Invalid command. Please try again.")
    connection.commit()
    return