import sqlite3

database_file = 'vetsark.db'

def start_connection():
    conn = sqlite3.connect(database_file)
    c = conn.cursor()
    return conn, c

conn, c = start_connection()

def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS user_details(user_id INTEGER, name TEXT, email TEXT, password Text, user_category TEXT, prime_category TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS stocks(user_id INTEGER, vendor TEXT, category TEXT, date TEXT, name TEXT, quantity REAL, cost REAL, sales REAL, price REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS purchases(user_id INTEGER, vendor TEXT, item TEXT, quantity REAL, cost REAL, sales REAL, price REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS sales(user_id INTEGER, receipt_no Text, date TEXt, customer TEXT, item TEXT, quantity REAL, price REAL, amount REAL, discount REAL, total_value REAL, amount_paid REAL, outstanding REAL)")
    
    c.execute("""CREATE TABLE IF NOT EXISTS clinical_service(user_id INTEGER, client_name TEXT, specie TEXT, diagnosis TEXT,
                observation_date REAL, report_date REAL, morbidity Text, mortality TEXT, medications TEXT, service_cost REAL)""")
    
    #Table for categories, vendors and customers:
    c.execute("CREATE TABLE IF NOT EXISTS stock_category(user_id INTEGER, name Text)")
    c.execute("CREATE TABLE IF NOT EXISTS vendors(user_id INTEGER, name TEXT, address TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS customers(user_id INTEGER, name TEXT, address TEXT, phone REAL, email TEXT, opening_balance REAL, debt REAL)")

def data_entry(c, user_id=1):
    c.execute("INSERT INTO user_details VALUES({}, 'default', 'default@default.com', 'default', 'default', 'default')".format(user_id))
    c.execute("INSERT INTO stocks VALUES({}, 'default', 'default', '01/01/2000', 'default', 0, 0, 0, 0)".format(user_id))
    c.execute("INSERT INTO purchases VALUES({}, 'default', 'default', 0, 0, 0, 0)".format(user_id))
    c.execute("INSERT INTO sales VALUES({}, '01/01/2000', 'default', 'default', 0, 0, 0)".format(user_id))
    
    c.execute("INSERT INTO clinical_service VALUES({}, 'default', 'default', 'default', 0, 0, 'default', 'default', 'default', 'default')".format(user_id))
    
    c.execute("INSERT INTO stock_category VALUES({}, 'default')".format(user_id))
    c.execute("INSERT INTO vendors VALUES({}, 'default', 'default')".format(user_id))
    c.execute("INSERT INTO customers VALUES({}, 'default', 'default', 'default', 'default', 0, 0)".format(user_id))
    conn.commit()

def read_data(c, table = "stocks", user_id=1):
    c.execute('SELECT * FROM {}'.format(table))
    data = c.fetchall()
    return data

def stock_data_entry(c, data = ['Emzor', 'Drug', '04/10/2018', 'Femi Mene', 10, 250, 300, 2500], user_id=1):
    c.execute("INSERT INTO stocks (user_id, vendor, category, date, name, quantity, cost, sales, price) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (user_id, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]))

#generic data entry function for stock_category, vendors, customers and sales.
def generic_data_entry(c, type="stock_category", data=["Medicine"], user_id=1):
    #The content of data argument is different depending on type argument specified.
    if type == "vendors":
        c.execute("INSERT INTO {} VALUES('{}', '{}', '{}')".format(type, user_id, data[0], data[1]))
    
    elif type == "customers":
        c.execute("INSERT INTO {} VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(type,
        user_id, data[0], data[1], data[2], data[3], data[4], data[5]))

    
    elif type == "sales":
        c.execute("INSERT INTO sales VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(user_id,
        data[0], data[1], data[2], data[3], data[4], data[5], data[6]))

    elif type == "stock_category":
        c.execute("INSERT INTO {} VALUES('{}', '{}')".format(type, user_id, data[0]))
    
    
    elif type == "clinical_service":
        c.execute("INSERT INTO clinical_service VALUES({}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(user_id,
        data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]))
    
if __name__ == "__main__":
    create_table()
    # data_entry(c)
    # stock_data_entry(c, data = [1, 'Emzor', 'Drug', '04/10/2018', 'Femi Mene', 10, 250, 300, 2500])
    # generic_data_entry(c, type="stock_category", data=[1, "Dangote"])
    # data = read_data(c, table = "stock_category")
    
    c.close()
    conn.close()