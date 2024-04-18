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
