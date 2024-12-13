import threading
import mysql.connector
from datetime import datetime

# Database Configuration
DB_CONFIG = {
    'host': 'companydb-server.mysql.database.azure.com',
    'database': 'project_db',
    'user': 'mysqladmin',
    'password': '@junyan123'
}

# Functions for Queries
def insert_query():
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()
    query = "INSERT INTO ClimateData (location, record_date, temperature, precipitation, humidity) VALUES (%s, %s, %s, %s, %s)"
    data = ("Edmonton", datetime.now().date(), -15.0, 10.0, 80.0)
    cursor.execute(query, data)
    connection.commit()
    connection.close()

def select_query():
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()
    query = "SELECT * FROM ClimateData WHERE temperature > %s"
    cursor.execute(query, (20,))
    print(cursor.fetchall())
    connection.close()

def update_query():
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()
    query = "UPDATE ClimateData SET humidity = humidity + 5 WHERE location = %s"
    cursor.execute(query, ("Toronto",))
    connection.commit()
    connection.close()

# Create Threads
threads = []
for _ in range(5):  # Run each query 5 times concurrently
    threads.append(threading.Thread(target=insert_query))
    threads.append(threading.Thread(target=select_query))
    threads.append(threading.Thread(target=update_query))

# Start and Join Threads
for thread in threads:
    thread.start()

for thread in threads:
    thread.join()
