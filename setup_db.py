import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('fundraising.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the fundraising table
cursor.execute('''
    CREATE TABLE fundraising (
        id INTEGER PRIMARY KEY,
        total REAL,
        goal REAL
    );
''')

# Insert a row with initial values
cursor.execute('''
    INSERT INTO fundraising (id, total, goal)
    VALUES (1, 0, 10000);  -- Assuming a goal of 10,000
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
