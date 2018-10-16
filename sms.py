from jusibe import Jusibe
import sqlite3

public_key = '547ab5e4e9721983ea8a6c9390dc4b6d'
access_token = '89a80757a16e4d9ab0eadc0e3fb7f7cf'
jusibe = Jusibe(public_key, access_token)

#send SMS
# response = jusibe.send_message('2348136694562', 'From Myself', 'Testing my api tokens.')
# print(response)

database_file = 'vetsark.db'
def get_number_and_send_sms(customer_name):
    with sqlite3.connect(database_file) as conn:
        c = conn.cursor()
        
        #number = c.execute('SELECT name FROM customers WHERE phone = {}'.format(customer_name))
        c.execute('SELECT * FROM customers')
        customer_data = c.fetchall()
        
        number = None
        for row in customer_data:
            if row[0] == customer_name:
                number = row[2]
        
        customer_number = "234" + str(round(number))
        print("customer number:", customer_number)
        
        jusibe_data = (customer_number, 'From Vetsark:', 'Your sales reciept has been processed.')
        response = jusibe.send_message(jusibe_data[0], jusibe_data[1], jusibe_data[2])

        return response
        
#response = get_number_and_send_sms('kk')
#print(response)

def get_number_and_send_sms2():
    with sqlite3.connect(database_file) as conn:
        c = conn.cursor()
        
        #number = c.execute('SELECT name FROM customers WHERE phone = {}'.format(customer_name))
        c.execute('SELECT * FROM customers')
        customer_data = c.fetchall()
        
        with open("number.txt", "r") as f:
            customer_name = f.read()
        
        number = None
        for row in customer_data:
            if row[0] == customer_name:
                number = row[2]
        
        if number.startswith('234') == True:
            customer_number = str(round(number))
        elif number.startswith('+234') == True:
            customer_number = number.replace("+", "")
        else:
            customer_number = "234" + str(round(number))
            
        if len(customer_number) != 13:
            print("Invalid customer number:", customer_number)
            return "Invalid Number Entered by Customer."
        else:
            print("customer number:", customer_number)
            
            jusibe_data = (customer_number, 'From Vetsark:', 'Your sales reciept has been processed.')
            response = jusibe.send_message(jusibe_data[0], jusibe_data[1], jusibe_data[2])
                
            return ["OK"]#response

#data = get_number_and_send_sms2()