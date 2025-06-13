
import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create channels table (fixed syntax)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS channels (
        channel TEXT PRIMARY KEY
    )
''')

# Create users table (was missing)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        name TEXT PRIMARY KEY
    )
''')

# Insert some test data
cursor.execute("INSERT OR IGNORE INTO users (name) VALUES (?)", ("Alice",))
cursor.execute("INSERT OR IGNORE INTO users (name) VALUES (?)", ("Bob",))

# Delete Alice
cursor.execute("DELETE FROM users WHERE name = ?", ("Alice",))

# Select and display all users
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Commit changes and close connection
conn.commit()
conn.close()
