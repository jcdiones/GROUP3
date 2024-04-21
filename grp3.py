import os
import sqlite3
import socket
import tkinter as tk
import time
from cryptography.fernet import Fernet
from pyvirtualdisplay import Display

# Generate a key for encryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Encrypt function
def encrypt_data(data):
    return cipher_suite.encrypt(data.encode()).decode()

# Decrypt function
def decrypt_data(encrypted_data):
    return cipher_suite.decrypt(encrypted_data.encode()).decode()

# Define update_label function (assuming it's a function to update a label widget)
def update_label(text):
    ip_label.config(text=text)

# Define authenticate function (assuming it's a function to authenticate users)
def authenticate(username, password):
    # Code for authentication goes here
    # For demonstration, let's assume all logins are successful
    return True

# Define login function
def login():
    username = username_entry.get()
    password = password_entry.get()
    if authenticate(username, password):
        login_button.config(state=tk.DISABLED)
        logout_button.config(state=tk.NORMAL)
        get_ip_button.config(state=tk.NORMAL)
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        update_label("Login successful. Click 'Get Local IP' to view IP.")
    else:
        update_label("Incorrect username or password")

# Define logout function
def logout():
    login_button.config(state=tk.NORMAL)
    logout_button.config(state=tk.DISABLED)
    get_ip_button.config(state=tk.DISABLED)
    update_label("Please log in to view IP")

# Define get_local_ip function
def get_local_ip():
    ip_address = socket.gethostbyname(socket.gethostname())
    update_label(f"Local IP Address: {ip_address}")

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

# Create a virtual display
display = Display(visible=0, size=(800, 600))
display.start()

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

# Start the event loop to display the UI
root.mainloop()

# Stop the virtual display
display.stop()