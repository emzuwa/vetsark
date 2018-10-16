import sqlite3
import matplotlib.pyplot as plt

import time
import datetime

database_file = 'vetsark.db'

sample_dates = ['1/10/2017', '2/10/2017', '3/10/2017', '4/10/2017', '5/10/2017']
sample_quantities = [10, 13, 20, 7, 0]

def get_timestamp(d): return time.mktime(datetime.datetime.strptime(d, "%d/%m/%Y").timetuple())

def plot_sales(sample_dates, sample_quantities):
    processed_dates = [get_timestamp(i) for i in sample_dates]
    
    plt.title("Quantities sold over time")
    plt.xlabel("Dates")
    plt.xticks(processed_dates, sample_dates)
    
    plt.plot(processed_dates, sample_quantities)
    plt.savefig("plotted_graph" + ".png")

plot_sales(sample_dates, sample_quantities)

#with sqlite3.connect(database_file) as conn:
#    c = conn.cursor()
#    
#    c.execute('SELECT * FROM sales')
#    sales_data = c.fetchall()
#    
#    quantity = [i[3] for i in sales_data]
    
    