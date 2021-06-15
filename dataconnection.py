import pandas as pd
import pyodbc
from datetime import datetime, timedelta
server = 'svenddata.database.windows.net'
database = 'svenddata'
username = 'Lukas546'
password = 'Idiot546'   
driver= '{ODBC Driver 17 for SQL Server}'   


## Connection ##

# with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
#     with conn.cursor() as cursor:
#         cursor.execute("SELECT TOP 3 name, collation_name FROM sys.databases")
#         row = cursor.fetchone()
#         while row:
#             print (str(row[0]) + " " + str(row[1]))
#             row = cursor.fetchone()

def get_con(): 
    try:
        con
        if not con_alive():
            con = None
    except NameError:
        con = None
        
    if con is None:
        try: 
            con = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
        except:
            con = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)

    return con

def con_alive(con): 
    cursor = con.cursor()
    cursor.execute("SELECT 1 as alive") 
    row = cursor.fetchone() 
    alive = False
    while row: 
        print(row[0])
        alive = True
        row = cursor.fetchone()
    return alive


## Queries ##

# Info table
def get_info_table(): 
    return pd.read_sql(f'SELECT * FROM [dbo].info ORDER BY info_ID', get_con())

# Get newest car
def get_newest_car(): 
    return pd.read_sql(f'SELECT TOP 1 * FROM [dbo].cars ORDER BY car_date_added DESC', get_con())

# Get new cars
def get_newest_cars(): 
    return pd.read_sql(f'SELECT * FROM [dbo].cars ORDER BY car_date_added DESC', get_con())

# Get specific car
def get_specific_car(car_ID): 
    return pd.read_sql(f'''SELECT * FROM [dbo].cars WHERE car_ID = '{car_ID}' ORDER BY car_date_added DESC''', get_con())

# Get specific car image
def get_specific_car_image(car_ID): 
    return pd.read_sql(f'''SELECT * FROM [dbo].images WHERE car_ID = '{car_ID}' ORDER BY image_ID ASC''', get_con())