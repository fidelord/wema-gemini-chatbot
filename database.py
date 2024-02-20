import sqlite3

# Connect to the SQLite database (creates a new file if it doesn't exist)
conn = sqlite3.connect('bank_database2.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Create a table for customers in the database
cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL,
        address TEXT NOT NULL,
        password TEXT NOT NULL,
        account_number INTEGER NOT NULL,
        account_balance REAL NOT NULL,
        token INTEGER NOT NULL DEFAULT 123456  -- Set the default constant value
    )
''')

# Insert customer data into the table with a generated password and constant token
customer_data = [
    ('John', 'Doe', 'john.doe@email.com', '123 Main St', 'johnDoe@123', 123456789, 5000.00),
    ('Jane', 'Smith', 'jane.smith@email.com', '456 Oak Ave', 'janeSmith@123', 987654321, 7500.50),
    ('Alice', 'Johnson', 'alice.johnson@email.com', '789 Pine Rd', 'aliceJohnson@123', 456789123, 10000.25),
    ('Bob', 'Jones', 'bob.jones@email.com', '567 Maple Ln', 'bobJones@123', 789012345, 12000.75),
    ('Eva', 'Williams', 'eva.williams@email.com', '890 Cedar Dr', 'evaWilliams@123', 234567890, 15000.50),
    ('Chris', 'Taylor', 'chris.taylor@email.com', '123 Elm St', 'chrisTaylor@123', 345678901, 8000.25),
    ('David', 'Miller', 'david.miller@email.com', '456 Birch Rd', 'davidMiller@123', 456789012, 9500.00),
    ('Sophie', 'Wilson', 'sophie.wilson@email.com', '789 Pine Ln', 'sophieWilson@123', 567890123, 11000.75),
    ('Michael', 'Clark', 'michael.clark@email.com', '234 Oak Dr', 'michaelClark@123', 678901234, 6000.50),
    ('Olivia', 'Moore', 'olivia.moore@email.com', '567 Maple Rd', 'oliviaMoore@123', 789012345, 8700.25),
]

cursor.executemany('''
    INSERT INTO customers (first_name, last_name, email, address, password, account_number, account_balance)
    VALUES (?, ?, ?, ?, ?, ?, ?)
''', customer_data)

# Commit the changes to the database
conn.commit()

# Fetch and print all customer records
cursor.execute("SELECT * FROM customers")
all_customers = cursor.fetchall()

print("All Customers:")
for customer in all_customers:
    print(customer)

# Close the database connection
conn.close()


# import sqlite3
# import random
# import string

# # Connect to the SQLite database (creates a new file if it doesn't exist)
# conn = sqlite3.connect('bank_database.db')

# # Create a cursor object to execute SQL queries
# cursor = conn.cursor()

# # Create a table for customers in the database
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS customers (
#         id INTEGER PRIMARY KEY,
#         first_name TEXT NOT NULL,
#         last_name TEXT NOT NULL,
#         email TEXT NOT NULL,
#         address TEXT NOT NULL,
#         password TEXT NOT NULL,
#         account_number INTEGER NOT NULL,
#         account_balance REAL NOT NULL
#     )
# ''')

# # Insert customer data into the table with a generated password
# customer_data = [
#     ('John', 'Doe', 'john.doe@email.com', '123 Main St', 'johnDoe@123', 123456789, 5000.00),
#     ('Jane', 'Smith', 'jane.smith@email.com', '456 Oak Ave', 'janeSmith@123', 987654321, 7500.50),
#     ('Alice', 'Johnson', 'alice.johnson@email.com', '789 Pine Rd', 'aliceJohnson@123', 456789123, 10000.25),
#     ('Bob', 'Jones', 'bob.jones@email.com', '567 Maple Ln', 'bobJones@123', 789012345, 12000.75),
#     ('Eva', 'Williams', 'eva.williams@email.com', '890 Cedar Dr', 'evaWilliams@123', 234567890, 15000.50),
#     ('Chris', 'Taylor', 'chris.taylor@email.com', '123 Elm St', 'chrisTaylor@123', 345678901, 8000.25),
#     ('David', 'Miller', 'david.miller@email.com', '456 Birch Rd', 'davidMiller@123', 456789012, 9500.00),
#     ('Sophie', 'Wilson', 'sophie.wilson@email.com', '789 Pine Ln', 'sophieWilson@123', 567890123, 11000.75),
#     ('Michael', 'Clark', 'michael.clark@email.com', '234 Oak Dr', 'michaelClark@123', 678901234, 6000.50),
#     ('Olivia', 'Moore', 'olivia.moore@email.com', '567 Maple Rd', 'oliviaMoore@123', 789012345, 8700.25),
# ]

# cursor.executemany('''
#     INSERT INTO customers (first_name, last_name, email, address, password, account_number, account_balance)
#     VALUES (?, ?, ?, ?, ?, ?, ?)
# ''', customer_data)

# # Commit the changes to the database
# conn.commit()

# # Fetch and print all customer records
# cursor.execute("SELECT * FROM customers")
# all_customers = cursor.fetchall()

# print("All Customers:")
# for customer in all_customers:
#     print(customer)

# # Close the database connection
# conn.close()
