import mysql.connector
import pandas as pd

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Soumik@123_mysql",
        database="tennis"
    )

def run_query(query, params=None):
    conn = get_connection()
    try:
        df = pd.read_sql_query(query, conn, params=params)
    finally:
        conn.close()
    return df

