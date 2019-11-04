import datetime
import Connect

def process_a_payment():
    connection, cursor = Connect.connection, Connect.cursor

    ticket = None
    today = datetime.date.today()
    #get ticket number
    ticket_num = input("Ticket number: ")
    #check if valid
    invalid_tno = True
    while not ticket_num.isdigit() or invalid_tno:
        if ticket_num.isdigit():
            cursor.execute('SELECT * FROM tickets where tno = :ticket_num', {"ticket_num": ticket_num})
            ticket = cursor.fetchall()
            print(len(ticket))
            if len(ticket) != 0:
                invalid_tno = False
            else:
                ticket_num = input("No such Ticket, input a valid ticket number: ")
        else:
            ticket_num = input("Input a valid Ticket number: ")

    #grab ticket fine
    fine_total = ticket[0][1]
    #grab summ of ticket payments
    cursor.execute('SELECT sum(amount) FROM payments where tno = :ticket_num', {"ticket_num": ticket_num})
    payments = cursor.fetchall()
    payment_total = payments[0][0]
    #find difference left
    difference = fine_total-payment_total
    #get amount
    amount = input("payment amount: ")
    invalid_amount = True
    while not ticket_num.isdigit() or invalid_amount:
        if amount.isdigit() and int(amount) <= difference:
            invalid_amount = False
        else:
            amount = input("Input a valid payment amount: ")

    #process payment
    cursor.execute(
        'insert into payments values (:tno, :pdate, :amount);',
        {"tno": ticket_num, "pdate": today, "amount": amount})

    connection.commit()