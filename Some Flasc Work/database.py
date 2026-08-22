# database.py
import sqlite3

DB_NAME = "sih.db"

def init_db():
    """Runs once when the app starts to set up the tables using her SQL rules."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # She writes the SQL schema string here, right in the triple quotes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_user(username, email):
    """Call this function whenever a new user registers on the website."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    #INSERT and SELECT code here inside the helper functions
    cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", (username, email))
    
    conn.commit()
    conn.close()

def get_all_users():
    """Call this function when you want to display user lists on the dashboard."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # here also the SELECT code of sql
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    
    conn.close()
    return rows