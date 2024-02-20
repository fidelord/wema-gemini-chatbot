import sqlite3

# Connect to the SQLite database (creates a new file if it doesn't exist)
conn = sqlite3.connect('bank_database2db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()


# Fetch and print all customer records
cursor.execute("SELECT * FROM customers")
all_customers = cursor.fetchall()

print("All Customers:")
for customer in all_customers:
    print(customer)

# # Close the database connection
conn.close()
