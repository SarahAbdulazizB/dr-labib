# app/models.py
import mysql.connector
import mysql.connector.cursor  # New line
import config  # Config import (wait, better from config)
# Fix: config.py root mein hai, to import config

from config import Config

# app/models.py (Replace get_db_connection function)

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            # cursor_class=mysql.connector.cursor.MySQLCursorDict  # Yeh line add karo
        )
        return conn
    except mysql.connector.Error as err:
        print(f"DB Error: {err}")
        return None

# Test function (baad mein delete kar dena)
def test_connection():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()
        print(f"Connected to database: {db_name}")
        cursor.close()
        conn.close()
    else:
        print("Connection failed!")

# Run test once: Uncomment below line, run.py se call kar ke test
# test_connection()