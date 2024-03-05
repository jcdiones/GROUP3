import requests
import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Public IP Information")

# Define functions
def get_ip_info():
    # Retrieve and process IP information as before
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            ip_v4 = data["ip"]
            ip_v6 = data.get("ipv6", "N/A")
            update_labels(ip_v4, ip_v6)
        else:
            update_labels("Error", "Error")
    except requests.exceptions.RequestException as e:
        update_labels("Error", f"Error: {e}")

def update_labels(ip_v4, ip_v6):
    ip_v4_label.config(text=f"IPv4: {ip_v4}")
    ip_v6_label.config(text=f"IPv6: {ip_v6}")

# API endpoint
url = "https://api.ipify.org?format=json"

# Create labels for displaying information
ip_v4_label = tk.Label(root, text="Retrieving IPv4...")
ip_v6_label = tk.Label(root, text="Retrieving IPv6...")

# Create a button to trigger information retrieval
get_ip_button = tk.Button(root, text="Get IP Info", command=get_ip_info)

# Arrange elements in the window
ip_v4_label.pack()
ip_v6_label.pack()
get_ip_button.pack()

# Start the event loop to display the UI
root.mainloop()
