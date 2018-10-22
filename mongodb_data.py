from pymongo import MongoClient

#For online use:
# mongo_url = "mongodb://vetsarkdatabase%40gmail.com:vetsark2018.@stitch.mongodb.com:27020/?authMechanism=PLAIN&authSource=%24external&ssl=true&appName=vetsark-tpzdh:mongodb-atlas:local-userpass"
mlab_url = "mongodb://vetsark:vetsark2018@ds133533.mlab.com:33533/vetsark"
client = MongoClient(mlab_url)
db = client['vetsark']

#For offline use:
# client = MongoClient()
# db = client['vetsark']

#arg is supposed to contain list of data to add to mongodb.
def insert_data(arg, type="user_details"):
    user_details = db.user_details
    stocks = db.stocks
    purchases = db.purchases
    sales = db.sales
    clinical_service = db.clinical_service
    stock_category = db.stock_category
    vendors = db.vendors
    customers = db.customers

    if type == "user_details":
        data = {"user_id":arg[0], "name":arg[1], "email":arg[2],
                "password":arg[3], "user_category":arg[4],
                "prime_category":arg[5]}
        
        user_details.insert_one(data)
    
    elif type == "stocks":
        data = {"user_id":arg[0], "vendor":arg[1], "category":arg[2], "date":arg[3], "name":arg[4],
                "quantity":arg[5], "unit_cost":arg[6], "unit_sales":arg[7], "amount":arg[8]}
        stocks.insert_one(data)
    
    elif type == "purchases":
        data = {"user_id":arg[0], "vendor":arg[1], "item":arg[2], "quantity":arg[3], "cost":arg[4],
                    "sales":arg[5], "price":arg[6]}
        purchases.insert_one(data)
    
    elif type == "sales":
        data = {"user_id":arg[0], "receipt_no":arg[1], "date":arg[2], "customer":arg[3], "item":arg[4],
            "quantity":arg[5], "price":arg[6], "amount":arg[7], "discount":arg[8],
            "total_value":arg[9], "amount_paid":arg[10], "outstanding":arg[11], 
            "payment_type":arg[12]}
        sales.insert_one(data)
        print("Sales indeed inserted.")
    
    elif type == "clinical_service":
        data = {"user_id":arg[0], "client_name":arg[1], "specie":arg[2], "diagnosis":arg[3],
                    "observation_date":arg[4], "report_date":arg[5], "morbidity":arg[6],
                    "mortality":arg[7], "medications":arg[8], "service_cost":arg[9]}
        clinical_service.insert_one(data)
    
    elif type == "stock_category":
        data = {"user_id":arg[0], "name":arg[1]}
        stock_category.insert_one(data)
    
    elif type == "vendors":
        data = {"user_id":arg[0], "name":arg[1], "address":arg[2]}
        vendors.insert_one(data)
    
    elif type == "customers":
        data = {"user_id":arg[0], "name":arg[1], "address":arg[2], "phone":arg[3], "email":arg[4],
                "opening_balance":arg[5], "debt":arg[6]}
        customers.insert_one(data)

        
# user_details.find({"name":"King"})
# user_details.remove({"name":"King"})

# client.drop_database('vetsark')
        
if __name__ == "__main__":        
    #Insert admin data:
    data = {"user_id":0, "name":"vetsark", "email":"vetsarkdatabase@gmail.com",
                    "password":"vetsark2018", "user_category":"Others",
                    "prime_category":"Prime Elite"}
    db.user_details.insert_one(data)
    
    pass
    
    
    
    
    
    
    
    