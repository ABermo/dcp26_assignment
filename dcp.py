import os
import pandas as pd
import sqlite3 as sql

CSV = "dcp26.csv"

def data_connect():
    global conn
    conn = sql.connect("trains.db")
    
    if os.path.exists(CSV):
        df = pd.read_csv(CSV)
        df.to_sql('train_times', conn, if_exists='replace', index=False)
    

data_connect()
query = conn.execute("SELECT * FROM train_times")

for row in query:
    print(row)
    
conn.close()