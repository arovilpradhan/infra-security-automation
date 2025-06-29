# This Script is used to change the IP Status Basically from Used to Available in Solarwinds portal.
import requests
from requests.auth import HTTPBasicAuth
import warnings

# Suppress the InsecureRequestWarning
warnings.simplefilter('ignore', requests.packages.urllib3.exceptions.InsecureRequestWarning)

# Replace with your SolarWinds credentials and the server URL
solarwinds_url = 'https://server.domainname.com:17774/SolarWinds/InformationService/v3/Json/Invoke/IPAM.SubnetManagement/ChangeIpStatus'
username = 'domain\\username'  # Replace with your SolarWinds username
password = 'yourpassword'  # Replace with your SolarWinds password

# The payload for changing the IP status (adjust based on API structure)
payload = {
    "IPAddress": "10.xxx.xxx.xxx",   # IP address to update
    "Status": "Available"                # New status (e.g., 'Reserved' or 'Used' or 'Available')
}

# Headers for JSON content
headers = {
    'Content-Type': 'application/json',
}

# Sending the POST request to update the IP status
response = requests.post(solarwinds_url, json=payload, auth=HTTPBasicAuth(username, password), headers=headers, verify=False)

# Check the response status and print the result
if response.status_code == 200:
    print(f"Successfully updated IP status to Available")
else:
    print(f"Failed to update IP status. Status Code: {response.status_code}, Error: {response.text}")
