import sqlite3
conn = sqlite3.connect('sih_test.db')
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,college TEXT)")

cursor.execute("INSERT INTO users (name, college) VALUES ('Shaurya', 'DTU')")


conn.commit()
cursor.execute("SELECT * FROM users")
all_users = cursor.fetchall()


print("Data in Database:", all_users)
conn.close()