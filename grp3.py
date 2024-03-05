import requests

# API endpoint
url = "https://api.ipify.org?format=json"

# Send GET request and get response
response = requests.get(url)

# Check for successful response
if response.status_code == 200:
    # Parse JSON data
    data = response.json()

    # Extract and format information
    ip_v4 = data["ip"]
    ip_v6 = data.get("ipv6", "N/A")  # Check if IPv6 exists

    # Print formatted output
    print(f"Your Public IP Information:")
    print(f"\tIPv4: {ip_v4}")
    print(f"\tIPv6: {ip_v6}")
else:
    print("Error: Unable to retrieve IP information.")