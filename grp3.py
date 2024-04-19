import os
import sqlite3
import socket
import tkinter as tk
import time
from cryptography.fernet import Fernet

# Generate a key for encryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Encrypt function
def encrypt_data(data):
    return cipher_suite.encrypt(data.encode()).decode()

# Decrypt function
def decrypt_data(encrypted_data):
    return cipher_suite.decrypt(encrypted_data.encode()).decode()

# Check if the database file exists
DATABASE_FILE = "user_database.db"
if not os.path.exists(DATABASE_FILE):
    # Create a new database file if it doesn't exist
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    # Create a table named "user" with columns "username" and "password"
    c.execute('''CREATE TABLE user
                 (username TEXT, password TEXT)''')
    # Insert an initial entry into the table
    c.execute("INSERT INTO user (username, password) VALUES (?, ?)", ("admin", "ciscoenpa"))
    conn.commit()
    conn.close()

# Define login function
def login():
    global authenticated
    username = username_entry.get()
    password = password_entry.get()

    # Check if the user has reached the maximum number of failed attempts
    if failed_attempts.get(username, 0) >= 5:
        update_label("Too many failed attempts. Please try again later.")
        return

    if authenticate(username, password):
        authenticated = True
        login_button.config(state=tk.DISABLED)
        logout_button.config(state=tk.NORMAL)
        get_ip_button.config(state=tk.NORMAL)
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        update_label("Login successful. Click 'Get Local IP' to view IP.")
        # Reset failed attempts counter upon successful login
        failed_attempts[username] = 0
    else:
        # Increment failed attempts counter
        failed_attempts[username] = failed_attempts.get(username, 0) + 1
        update_label("Incorrect username or password")

        # If maximum attempts reached, lock user out for 1 minute
        if failed_attempts[username] >= 5:
            update_label("Too many failed attempts. Please try again later.")
            time.sleep(60)  # Sleep for 60 seconds before allowing another attempt

def authenticate(username, password):
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM user WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    conn.close()
    return result is not None

def logout():
    global authenticated
    authenticated = False
    login_button.config(state=tk.NORMAL)
    logout_button.config(state=tk.DISABLED)
    get_ip_button.config(state=tk.DISABLED)
    update_label("Please log in to view IP")

# Create the main window
root = tk.Tk()
root.title("Local IP Information")

# Create labels and entry widgets for login
username_label = tk.Label(root, text="Username:")
username_label.pack()
username_entry = tk.Entry(root)
username_entry.pack()

password_label = tk.Label(root, text="Password:")
password_label.pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

login_button = tk.Button(root, text="Login", command=login)
login_button.pack()

logout_button = tk.Button(root, text="Logout", command=logout, state=tk.DISABLED)
logout_button.pack()

# Create a label to display the IP address
ip_label = tk.Label(root, text="Please log in to view IP")
ip_label.pack()

# Create a button to trigger IP retrieval
get_ip_button = tk.Button(root, text="Get Local IP", command=get_local_ip, state=tk.DISABLED)
get_ip_button.pack()

# Variable to track authentication status
authenticated = False

# Variable to track failed login attempts
failed_attempts = {}

# Start the event loop to display the UI
root.mainloop()
