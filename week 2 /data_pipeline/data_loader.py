################# Open CMD and load the below #################

# pip install mysql-connector-python pandas # 

################# SQL Connector #################
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",       # your server
    user="root",            # your username
    password="1234",
    database="deep_singh"
)

cursor = conn.cursor()
################# Fetch Cleaned Data #################

query = "SELECT * FROM combined_compressed"
cursor.execute(query)

rows = cursor.fetchall()
columns = [col[0] for col in cursor.description]

################# Connect With Pandas #################

import pandas as pd

df = pd.DataFrame(rows, columns=columns)

print(df.head())

################# Convert Date and Time #################

df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], format='mixed', dayfirst=True)

################# Save as CSV File #################

df.to_csv("week2_logic_core/data_pipeline/cleaned_data.csv", index=False)
print("Saved")
