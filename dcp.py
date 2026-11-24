import os
import pandas as pd
import sqlite3 as sql

CSV = "dcp26.csv"

def data_connect():
    global conn
    conn = sql.connect("trains.db")
    
    # Create Database
    if os.path.exists(CSV):
        df = pd.read_csv(CSV)
        df.to_sql('train_times', conn, if_exists='replace', index=False)
    

def look_over():
    print("Would you like to look over: ")
    print("\t1. All")
    print("\t2. Certain Time")
    print("\t3. Certain Station Arrival")
    print("\t4. Certain Station Destination")
    
    # Keeping as string as to prevent program crashing when they enter a letter
    opt = input("")
    
    while (opt not in ('1','2','3','4')):
        print("Invalid option")
        print("Would you like to look over: ")
        print("\t1. All")
        print("\t2. Certain Time")
        print("\t3. Certain Station Arrival")
        print("\t4. Certain Station Destination")
        
        opt = input("")
    
    if (opt == '1'):
        df = pd.read_sql("SELECT * FROM train_times", conn)

        display(df)
    elif (opt == '2'):
        print("Are you interested in: ")
        print("\tP. Pick Up Time")
        print("\tA. Arrival Time")
        print("\tB. Both")
        
        cho = input("")
        while (cho.lower() not in ('p', 'a', 'b')):
            print("Invalid Option")
            cho = input("")

        print("What time are you interested in? Leave in HH:MM form: ")
        time = input("")
        
        if (cho.lower() == 'p'):
            df = pd.read_sql(f"SELECT * FROM train_times WHERE due_time = ?", conn, params=(time,))
            
            display(df)
        elif (cho.lower() == 'a'):
            df = pd.read_sql(f"SELECT * FROM train_times WHERE arrival_time = ?", conn, params=(time,))
                        
            display(df)
        elif (cho.lower() == 'b'):
            df = pd.read_sql(f"SELECT * FROM train_times WHERE due_time = ? OR arrival_time = ?", conn, params=(time,time,))
                        
            display(df)
def display(df):
    choice = ""
    i = 0
    
    print("Press enter to go next")
    print("Press b to go back")
    print("Press q to exit\n")
    
    while (i < len(df) and choice != 'q'):
        print(f"ID: {df['ID'][i]}")
        print(f"Origin: {df['train_origin'][i]}")
        print(f"My Origin: {df['my_origin'][i]}")
        print(f"Train Destination: {df['train_destination'][i]}")
        print(f"My Destionation: {df['my_destination'][i]}")
        print(f"Scheduled Pick Up Time: {df['due_time'][i]}")
        print(f"Actual Pick Up Time: {df['actual_due_time'][i]}")
        print(f"Arrival Time: {df['arrival_time'][i]}")
        print(f"Actual Arrival Time: {df['actual_arrival_time'][i]}")
        print(f"Stops Before My Origin: {df['previous_stops'][i]}")
        print(f"Stops After My Origin: {df['later_stops'][i]}")
        
        choice = input("")
        if (choice == 'b'):
            i -= 1
        else:
            i += 1

        # In case they press b on the first value
        if i < 0:
            i = 0
    
    if (i == len(df)):
        print("Looked through the full dataset")
data_connect()
look_over()