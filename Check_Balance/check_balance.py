import sqlite3
# question = input()
def Check_balance(email):
    # Connect to the SQLite database
    conn = sqlite3.connect('bank_database.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Fetch the account balance based on the email
    cursor.execute("SELECT account_balance FROM customers WHERE email = ?", (email,))
    balance = cursor.fetchone()

    # Check if the email exists in the database
    if balance is not None:
        return f"Account Balance for {email}: ${balance[0]}"
    else:
        return f"Invalid email: {email}"


Check_balance("jane.smith@email.com")











# import sqlite3

# def Check_balance(email):
#     # Connect to the SQLite database
#     conn = sqlite3.connect('bank_database.db')

#     # Create a cursor object to execute SQL queries
#     cursor = conn.cursor()

#     # Fetch the account balance based on the email
#     cursor.execute("SELECT account_balance FROM customers WHERE email = ?", (email,))
#     balance = cursor.fetchone()

#     # Check if the email exists in the database
#     if balance:
#         print(f"Account Balance for {email}: ${balance[0]}")
#     else:
#         print(f"Invalid email: {email}")

#     # Close the database connection
#     conn.close()

# # Example usage
# Check_balance('jane.smith@email.com')
# Check_balance("john.doe@email.com")
