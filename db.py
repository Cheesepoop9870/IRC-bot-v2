import sqlite3
#note: work in progress
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create channels table (fixed syntax)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS channels (
        channel TEXT PRIMARY KEY
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS logs (
        log TEXT PRIMARY KEY
    )
''')

# Insert some test data
def add_channel(channel):
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO channels (channel) VALUES (?)", (f"{channel}",))
    conn.commit()
    cursor.close()
# cursor.execute("DELETE FROM channels WHERE channel = ?", ("Alice",))
def full_delete():
    cursor = conn.cursor()
    cursor.execute("DELETE FROM channels")
    conn.commit()
    cursor.close()
# Select and display all users
def get_channels():
    chlist = []
    cursor.execute("SELECT * FROM channels")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
        chlist.append(row[0])
    return chlist
def del_channel(args):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM channels WHERE channel = ?", (f"{args}",))
    conn.commit()
def add_log(log):
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO logs (log) VALUES (?)", (f"{log}",))
    conn.commit()
    cursor.close()
def del_log(args):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM logs WHERE log = ?", (f"{args}",))
    conn.commit()


# Commit changes and close connection
conn.commit()

if __name__ == "__main__":
    # full_delete()
    add_channel("#cheesepoop9870")
    add_channel("#facility36")
    get_channels()
    print(get_channels())
    conn.close()
