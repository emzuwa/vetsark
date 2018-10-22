from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import os, sqlite3

from sqlite_database import data_entry, create_table, read_data, stock_data_entry, generic_data_entry

#For Jusibe:
from sms import get_number_and_send_sms

#For MongoDb:
from mongodb_data import db, insert_data

app = Flask(__name__)
app.secret_key = "vetsark-secret_key"

database_file = 'vetsark.db'

@app.route("/prime")
def prime_tracker():
    return render_template('prime_tracker.html')

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/sign_out")
def sign_out():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route("/signup", methods=['POST', "GET"])
def signup():
    #Session handling;
    if "username" in session:
        return redirect(url_for('dashboard'))
    else:
        return render_template('signup.html')
  
@app.route("/signup_entry", methods=['POST', "GET"])
def signup_entry():
    if request.method == 'POST':
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["pass"]
        re_password = request.form["re_pass"]
        
        user_category = request.form["user_category"]
        prime_category = request.form["prime_category"]
        
        #Check if any form is not filled:
        for i in [name, email, password, re_password]:
            if i == "": return render_template('signup_blank.html', email=email)
        
        #Check if passwords entered does not match:
        if password != re_password:
            return render_template('signup_password.html', email=email)
    
        #Check if email already exists.
        result = list(db.user_details.find({"email": email}))
        if len(result) > 0: return render_template('signup_error.html', email=email)
        else: #Else enter new database entry for new user.
            #Get user_id first [get last user id in database and increase by one]
            new_user_id = list(db.user_details.find())[-1]["user_id"] + 1
            
            #Then insert to database:
            insert_arguments = [new_user_id, name, email, password, re_password, user_category, prime_category]
            insert_data(type="user_details", arg=insert_arguments)
            
            return render_template('signin.html')

@app.route("/signin", methods=['POST', "GET"])
def signin():
    #Session handling;
    if "username" in session:
        return redirect(url_for('dashboard'))
    else:
        return render_template('signin.html')
   
@app.route("/dashboard", methods=['POST', "GET"])
def dashboard():
    if request.method == 'POST':
            
        email = request.form["email"]
        password = request.form["pass"]
        
        #Check if Email and Password is correct:
        result = list(db.user_details.find({"email":email, "password":password}))
        if result == []: return render_template('signin_error.html', email=email)
        else:
            #Get user id:
            user_id = result[0]["user_id"]
        
            #Make new Session with the user name:
            session["username"] = result[0]["name"]
            session["user_id"] = result[0]["user_id"]
            
    ##########################################################################
    ##### For Get method only:
    #Incase someone just routes to /dashboard without being signed in:
    if not "username" in session:
        return render_template('signin.html')
        
    # If the user is already signed in.
    else:
        # Get user id for use down here:
        user_id = session["user_id"]
    ########################################################################## 
    
    ################# Getting Stock data:
    #Get stock data based on user_id:
    result = list(db.stocks.find({"user_id":user_id}))
    #Get stock data to list, omitting vendor and date column:
    stock_data = []
    for item in result:
        arg = [ item["category"], item["name"], item["quantity"], item["unit_cost"], item["unit_sales"], item["amount"] ]
        stock_data.append(arg)
    
    stock_items = set([item[1] for item in stock_data])
        
    #Making a dictionary pair of stock item and it's cost
    stock_dictionary = {}
    for row in stock_data:
        if row[1] not in stock_dictionary:
            stock_dictionary[row[1]] = row[4]
    stock_dictionary_items = list(stock_dictionary.keys())
    stock_dictionary_values = [float(value) for value in list(stock_dictionary.values())]
    #################
    
    ################# Getting Category data:
    #Get stock data based on user_id:
    result = list(db.stock_category.find({"user_id":user_id}))
    #Get category data to list:
    category_data = []
    for item in result:
        arg = [ item["name"] ]
        category_data.append(arg)
    #################
    
    ################# Getting Vendors data:
    #Get vendors data based on user_id:
    result = list(db.vendors.find({"user_id":user_id}))
    #Get vendors data to list:
    vendors_data = []
    for item in result:
        arg = [ item["name"], item["address"] ]
        vendors_data.append(arg)
    #################
    
    ################# Getting Customers data:
    #Get customers data based on user_id:
    result = list(db.customers.find({"user_id":user_id}))
    #Get customers data to list:
    customers_data = []
    for item in result:
        arg = [ item["name"], item["address"], item["phone"], item["email"], item["opening_balance"], item["debt"] ]
        customers_data.append(arg)
    #################
    
    ################# Getting Clinical Service data:
    #Get clinical service data based on user_id:
    result = list(db.clinical_service.find({"user_id":user_id}))
    #Get clinical service data to list, Omiting some items:
    service_data = []
    for item in result:
        arg = [ item["client_name"], item["specie"], item["diagnosis"], item["report_date"],
            item["medications"], item["service_cost"] ]
        service_data.append(arg)
    #################
    
    ################# Getting Sales data:
    #Get sales data based on user_id:
    result = list(db.sales.find({"user_id":user_id}))
    #Get sales data to list, Omiting some items:
    sales_data = []
    sales_total, sales_outstanding = 0, 0
    
    for item in result:
        arg = [ item["receipt_no"], item["date"], item["customer"], item["item"],
            item["total_value"], item["outstanding"], item["payment_type"] ]
            
        sales_total += float(item["total_value"])
        sales_outstanding += float(item["outstanding"])
        sales_data.append(arg)
    #################
    
    #Number of records for Clinical service, stocks, sales:
    numbers = [ len(list(db.clinical_service.find({"user_id":user_id}))),
                len(list(db.stocks.find({"user_id":user_id}))),
                len(list(db.sales.find({"user_id":user_id})))
              ]
    
    #No time: (deal with this later.)
    view_stock_data = stock_data
    return render_template('index.html', view_stock_data=view_stock_data,
                            category_data=category_data,
                            vendors_data=vendors_data,
                            customers_data=customers_data,
                            stock_items=stock_items,
                            
                            stock_dictionary_items=stock_dictionary_items,
                            stock_dictionary_values=stock_dictionary_values,
                            
                            service_data=service_data,
                            sales_data=sales_data,
                            sales_total=sales_total,
                            sales_outstanding=sales_outstanding,
                            
                            numbers = numbers,
                            user_name = session["username"],

                            list_=list)

@app.route('/record_stock', methods=['POST'])
def record_stock():
    get_user_id = session["user_id"]
    
    if request.method == 'POST':
    
        vendor = request.form["vendor_select"]
        category = request.form["category_select"]
        stock_date = request.form["stock_date"]
        name = request.form["stock1"]
        quantity = request.form["stock2"]
        purchase_cost = request.form["stock3"]
        selling_cost = request.form["stock4"]
        
        # amount = request.form["stock5"]
        amount = float(quantity) * float(purchase_cost)
        
        arg = [get_user_id, vendor, category, stock_date, name, quantity, purchase_cost, selling_cost, amount]
        
        print("To be added to stocks:", arg, "\n\n\n\n\n\n")
        #Insert data to mongodb database:
        insert_data(arg, type="stocks")
                
    return jsonify({'status':'OK','answer':"stuff"})

@app.route('/record_service', methods=['POST'])
def record_service():
    get_user_id = session["user_id"]
    
    if request.method == 'POST':
        client_name = request.form["client_name"]
        animal_specie = request.form["animal_specie"]
        diagnosis = request.form["diagnosis"]
        observation_date = request.form["observation_date"]
        report_date = request.form["report_date"]
        morbidity = request.form["morbidity"]
        mortality = request.form["mortality"]
        medications = request.form["medications"]
        service_cost = request.form["service_cost"]
        
        arg = [get_user_id, client_name, animal_specie, diagnosis, observation_date, report_date, morbidity, mortality, medications, service_cost]
        
        #Insert data to mongodb database:
        insert_data(arg, type="clinical_service")
    
    return jsonify({'status':'OK','answer':"stuff"})

@app.route('/record_sales', methods=['POST', 'GET'])
def record_sales():
    get_user_id = session["user_id"]
    
    # global printer_rows, printer_total, printer_amount_paid, printer_outstanding, sales_customer
    if request.method == 'POST':
        sales_date = request.form["sales_date"]
        sales_customer = request.form["sales_customer"]
        receipt_number = request.form["receipt_number"]
        
        sales_item = request.form["2"]#["item-select"]
        sales_quantity = request.form["3"]#["sales_quantity"]
        sales_price = request.form["4"]#["sales_price"]
        amount = request.form["5"]#["amount"]
        discount_value = request.form["6"]#["discount_value"]
        total_value = request.form["7"]#["total_value"]
        amount_paid = request.form["8"]#["amount_paid"]
        outstanding = request.form["9"]#["outstanding"]
        
        payment_type = request.form["10"]#["payment_type"]
        # arg = [get_user_id, receipt_number, sales_date, sales_customer, sales_item, sales_quantity, sales_price, amount, discount_value, total_value, amount_paid, outstanding, payment_type]
        
        if len(sales_item.split(',')) > 1:
            for index, item in enumerate(range(len(sales_item.split(',')))):
                print(index)
                print(len(sales_item))
                data = [sales_item.split(',')[index], sales_quantity.split(',')[index],
                        sales_price.split(',')[index], amount.split(',')[index],
                        discount_value.split(',')[index], total_value.split(',')[index],
                        amount_paid.split(',')[index], outstanding.split(',')[index],
                        payment_type.split(',')[index]
                        ]
                 
                arg = [get_user_id, receipt_number, sales_date, sales_customer] + data
                
                insert_data(arg, type="sales")
                
                
        else:
            arg = [get_user_id, receipt_number, sales_date, sales_customer, sales_item, sales_quantity, sales_price, amount, discount_value, total_value, amount_paid, outstanding, payment_type]
            insert_data(arg, type="sales")
        
        #For printing:
        items = sales_item.split(',')
        quantities = sales_quantity.split(',')
        total_values = total_value.split(',')
        
                
        if len(sales_item.split(',')) > 1:
            print("hjdh\n\n\n\n")
            print(items)
            print(quantities)
            print(total_values)
            
            print("Outstanging", outstanding.split(',')[index])
            printer_rows = [(items[n], quantities[n], total_values[n]) for n in range(len(items))]
            print("printer_rows:", printer_rows)
            printer_total = sum([float(i) for i in total_values])
            printer_amount_paid = sum([float(i) for i in amount_paid.split(',')])
            printer_outstanding = printer_total - printer_amount_paid
        else:            
            printer_rows = [(sales_item, sales_quantity, total_value)]
            printer_total = total_value
            printer_amount_paid = amount_paid
            printer_outstanding = outstanding
        
        
        #*********************************************************#
        #Deal with this soon
        #Send sms on sales record.
        # response = get_number_and_send_sms(customer_name)
        # if type(response) == str:
            # print("Inavlid Customer Number in the database")
            #*********************************************************#
    return render_template('receipt.html', printer_rows=printer_rows,
                        printer_total=printer_total, printer_amount_paid=printer_amount_paid,
                        printer_outstanding=printer_outstanding,
                        business_name=session["username"], sales_customer=sales_customer)
                        
    # return jsonify({'status':'OK','answer':"stuff"})
    
    # return redirect(url_for('print_receipt'))
    
# @app.route('/print_receipt', methods=['POST', 'GET'])
# def print_receipt():
    # return render_template('receipt.html', printer_rows=printer_rows,
                        # printer_total=printer_total, printer_amount_paid=printer_amount_paid,
                        # business_name=session["username"], sales_customer=sales_customer)
                            
@app.route('/add_category', methods=['POST'])
def add_category():
    get_user_id = session["user_id"]
    
    if request.method == 'POST':
        added_category = request.form["added_category_name"]
        arg = [get_user_id, added_category]
        
        #Insert data to mongodb database:
        insert_data(arg, type="stock_category")
            
    return jsonify({'status':'OK','answer':"stuff"})


@app.route('/add_vendor', methods=['POST'])
def add_vendor():
    get_user_id = session["user_id"]
    
    if request.method == 'POST':
        added_vendor_name = request.form["added_vendor_name"]
        added_vendor_address = request.form["added_vendor_address"]
        
        arg = [get_user_id, added_vendor_name, added_vendor_address]
        #Insert data to mongodb database:
        insert_data(arg, type="vendors")
            
    return jsonify({'status':'OK','answer':"stuff"})

@app.route('/add_customer', methods=['POST'])
def add_customer():
    get_user_id = session["user_id"]
    
    if request.method == 'POST':
        added_customer_name = request.form["added_customer_name"]
        added_customer_address = request.form["added_customer_address"]
        added_customer_phone = request.form["added_customer_phone"]
        added_customer_email = request.form["added_customer_email"]
        added_customer_balance = request.form["added_customer_balance"]
        added_customer_debt = request.form["added_customer_debt"]
        
        arg = [get_user_id, added_customer_name, added_customer_address, added_customer_phone,
                    added_customer_email, added_customer_balance, added_customer_debt]
        
        #Insert data to mongodb database:
        insert_data(arg, type="customers")
            
    return jsonify({'status':'OK','answer':"stuff"})

# @app.route('/record_sales_and_send_sms', methods=['POST'])
# def record_sales_and_send_sms():
    # if request.method == 'POST':
        # customer_name = request.form["customer_select"]
        # print("Customer Name:", customer_name)
            
        # response = get_number_and_send_sms(customer_name)
        # if type(response) == str:
            # print("Inavlid Customer Number in the database")
            
    # return jsonify({'status':'OK','answer':"stuff"})

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return ("""
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500)

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)

# if __name__ == "__main__":
    # app.run(debug=True)
    # app.run(host='0.0.0.0', debug=True)