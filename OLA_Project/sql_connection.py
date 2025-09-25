import pandas as pd
import mysql.connector

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",            
    password="Soumik@123_mysql",   
    database="OLA_db"
)
cursor = conn.cursor()

# create table
cursor.execute("""
CREATE TABLE ola_rides (
    Date VARCHAR(40),
    Time VARCHAR(40),
    Booking_ID VARCHAR(50) PRIMARY KEY,
    Booking_Status VARCHAR(20),
    Customer_ID VARCHAR(20),
    Vehicle_Type VARCHAR(50),
    Pickup_Location VARCHAR(100),
    Drop_Location VARCHAR(100),
    V_TAT FLOAT,
    C_TAT FLOAT,
    Canceled_Rides_by_Customer VARCHAR(100),
    Canceled_Rides_by_Driver VARCHAR(100),
    Incomplete_Rides VARCHAR(10),
    Incomplete_Rides_Reason VARCHAR(100),
    Booking_Value INT,
    Payment_Method VARCHAR(50),
    Ride_Distance INT,
    Driver_Ratings FLOAT,
    Customer_Rating FLOAT
)
""")

# load the dataset
df = pd.read_csv(r"E:\Labmentix Internship\OLA_Project\DATASET\clean_OLA_Dataset.csv")

# Insert data row by row
for _, row in df.iterrows():
    sql = """INSERT INTO ola_rides 
    (Date, Time, Booking_ID, Booking_Status, Customer_ID, Vehicle_Type, 
        Pickup_Location, Drop_Location, V_TAT, C_TAT, Canceled_Rides_by_Customer, Canceled_Rides_by_Driver,
        Incomplete_Rides, Incomplete_Rides_Reason,Booking_Value, Payment_Method, 
        Ride_Distance, Driver_Ratings, Customer_Rating)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    
    cursor.execute(sql, tuple(row))

conn.commit()
cursor.close()
conn.close()

print("Data inserted successfully!")