import sqlite3

# Connect to the database
conn = sqlite3.connect('instance/database.db')
cursor = conn.cursor()

# Execute SQL queries
cursor.execute('SELECT * FROM Note')
rows = cursor.fetchall()

# Print the results
for row in rows:
    print(row)

# Close the connection
conn.close()