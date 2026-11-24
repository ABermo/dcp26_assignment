import os
import pandas as pd
import sqlite3 as sql
from datetime import datetime as dt
import matplotlib.pyplot as plt

CSV = "dcp26.csv"

def data_connect():
    global conn
    conn = sql.connect("trains.db")
    
    # Create Database
    if os.path.exists(CSV):
        df = pd.read_csv(CSV)
        df.to_sql('train_times', conn, if_exists='replace', index=False)
    
    

def menu():
    data_connect()
    opt = ""
    
    while opt != '3':
        print("Welcome to Data Centric Programming Project!")
        print("What would like to do?")
        print("\t1. View Raw Data")
        print("\t2. Look at Charts")
        print("\t3. Quit")
        
        opt = input("")
        
        while opt not in ('1', '2', '3'):
            print("Invalid Option")
            opt = input("")
        
        if (opt == '3'): return
        elif (opt == '1'): look_over()
        elif (opt == '2'): chart_menu()
    

def chart_menu():
    print("What graph would you like to see: ")
    print("\t1. Pick Up Delays")
    print("\t2. Drop Off Delays")
    print("\t3. Delays Overall")
    print("\t4. Pick Up Delay Per Stop")
    print("\t5. Drop Off Delay Per Stop")
    
    opt = input("")
    
    while (opt not in ('1', '2', '3', '4', '5')):
        print("Invalid Option")
        opt = input("")
    
    if (opt == '1'): delay_pickup_bar_graph()
    elif (opt == '2'): delay_arrival_bar_graph()
    elif (opt == '3'): delay_bar_graph()
    elif (opt == '4'): due_delay_stop()
    elif (opt == '5'): arrival_delay_stop()
    
    plt.show()
    


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
    elif (opt == '3'):
        print("What station are you interested in")
        cho = input("")
        
        df = pd.read_sql(f"SELECT * FROM train_times WHERE my_destination = ? or train_destination = ?", conn, params=(cho,cho,))
        display(df)
    elif (opt == '4'):
        print("What station are you interested in")
        cho = input("")
            
        df = pd.read_sql(f"SELECT * FROM train_times WHERE my_origin = ? or train_origin = ?", conn, params=(cho,cho,))
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

def delay_calc(scheduled, actual):
    scheduled = dt.strptime(scheduled, '%H:%M')
    actual = dt.strptime(actual, '%H:%M')
    
    delay = actual - scheduled
    return int(delay.total_seconds() / 60)

def delay_pickup_bar_graph():
    df = pd.read_sql("SELECT ID, due_time, actual_due_time FROM train_times", conn)
    
    ids = df['ID']
    due_times = df['due_time']
    actual_due_times = df['actual_due_time']
    due_times_delay = []
    colours = []
    
    for i in range(len(due_times)):
        due_times_delay.append(delay_calc(due_times[i], actual_due_times[i]))
        
    for delay in due_times_delay:
        if delay < 3:
            colours.append("#0b4f09")
        elif delay < 7:
            colours.append('#2f8f2e')
        elif delay < 10:
            colours.append('#9bc924')
        elif delay < 15:
            colours.append("#D09235")
        elif delay < 20:
            colours.append("#C74B38")
        else:
            colours.append("#FF0000")
            
        
    plt.bar(ids, due_times_delay, color = colours)

    plt.xlabel("ID")
    plt.ylabel("Delay (Minutes)")
    plt.title("Train Pick Up Delay")
    
    return (due_times_delay, colours)

def delay_arrival_bar_graph():
    df = pd.read_sql("SELECT ID, arrival_time, actual_arrival_time FROM train_times", conn)
    
    ids = df['ID']
    arrival_times = df['arrival_time']
    actual_arrival_times = df['actual_arrival_time']
    arrival_times_delay = []
    colours = []
    
    for i in range(len(arrival_times)):
        arrival_times_delay.append(delay_calc(arrival_times[i], actual_arrival_times[i]))
        
    for delay in arrival_times_delay:
        if delay < 3:
            colours.append("#0b4f09")
        elif delay < 7:
            colours.append('#2f8f2e')
        elif delay < 10:
            colours.append('#9bc924')
        elif delay < 15:
            colours.append("#D09235")
        elif delay < 20:
            colours.append("#C74B38")
        else:
            colours.append("#FF0000")
            
        
    plt.bar(ids, arrival_times_delay, color = colours)

    plt.xlabel("ID")
    plt.ylabel("Delay (Minutes)")
    plt.title("Train Drop Off Delay")
    
    return (arrival_times_delay, colours)

def delay_bar_graph():
    df = pd.read_sql("SELECT ID FROM train_times", conn)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    due_time_delay, coloursDue = delay_pickup_bar_graph()
    arrival_time_delay, coloursArrival = delay_arrival_bar_graph()
    ids = df['ID']
    
    ax1.bar(ids, due_time_delay, color=coloursDue)
    ax1.set_xlabel("ID")
    ax1.set_ylabel("Delay (Minutes)")
    ax1.set_title("Train Pick Up Delay")

    ax2.bar(ids, arrival_time_delay, color=coloursArrival)
    ax2.set_xlabel("ID")
    ax2.set_ylabel("Delay (Minutes)")
    ax2.set_title("Train Drop Off Delay")

def due_delay_stop():
    df = pd.read_sql("SELECT ID, previous_stops FROM train_times", conn)
    
    ids = df['ID']
    due_times, colours = delay_pickup_bar_graph()
    delay_per_stop = []
    
    for i in range(len(due_times)):
        delay_per_stop.append(due_times[i] / (df['previous_stops'][i] + 1))
    
    plt.bar(ids, delay_per_stop, color = colours)
    
    plt.xlabel("ID")
    plt.ylabel("Delay (Minutes)")
    plt.title("Delay per Stop before Pick Up")

def arrival_delay_stop():
    df = pd.read_sql("SELECT ID, later_stops FROM train_times", conn)
    
    ids = df['ID']
    due_times, colours = delay_arrival_bar_graph()
    delay_per_stop = []
    
    for i in range(len(due_times)):
        delay_per_stop.append(due_times[i] / (df['later_stops'][i] + 1))
    
    plt.bar(ids, delay_per_stop, color = colours)
    
    plt.xlabel("ID")
    plt.ylabel("Delay (Minutes)")
    plt.title("Delay per Stop after Pick Up")
    
menu()
