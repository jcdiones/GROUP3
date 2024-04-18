import requests
import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Public IP Information")

# Define functions
def get_ip_info():
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            ip_v4 = data["ip"]
            ip_v6 = data.get("ipv6", "N/A")
            country, postal_code = get_location_info(ip_v4)
            update_labels(ip_v4, ip_v6, country, postal_code)
        else:
            update_labels("Error", "Error", "N/A", "N/A")
    except requests.exceptions.RequestException as e:
        update_labels("Error", f"Error: {e}", "N/A", "N/A")

def update_labels(ip_v4, ip_v6, country, postal_code):
    ip_v4_label.config(text=f"IPv4: {ip_v4}")
    ip_v6_label.config(text=f"IPv6: {ip_v6}")
    location_textbox.config(state=tk.NORMAL)
    location_textbox.delete("1.0", tk.END)
    location_textbox.insert(tk.END, f"Country: {country}\nPostal Code: {postal_code}")
    location_textbox.config(state=tk.DISABLED)

def get_location_info(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        if response.status_code == 200:
            data = response.json()
            country = data["country"]
            postal_code = data.get("zip", "N/A")
            return country, postal_code
        else:
            return "N/A", "N/A"
    except requests.exceptions.RequestException:
        return "N/A", "N/A"

# API endpoint
url = "https://api.ipify.org?format=json"

# Create labels for displaying information
ip_v4_label = tk.Label(root, text="Retrieving IPv4...")
ip_v6_label = tk.Label(root, text="Retrieving IPv6...")

# Create a text box to display country and postal code information
location_textbox = tk.Text(root, height=2, width=30)
location_textbox.config(state=tk.DISABLED)

# Create a button to trigger information retrieval
get_ip_button = tk.Button(root, text="Get IP Info", command=get_ip_info)

# Arrange elements in the window
ip_v4_label.pack()
ip_v6_label.pack()
location_textbox.pack()
get_ip_button.pack()

# Start the event loop to display the UI
root.mainloop()


