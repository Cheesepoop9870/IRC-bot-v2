import sqlite3


conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS channels (
        channel TEXT PRIMARY KEY,
    )
''')
cursor.execute("DELETE FROM users WHERE name = ?", ("Alice",))
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for row in rows:
    print(row)
