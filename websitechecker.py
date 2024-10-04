import whois
import socket
import requests
import os
from datetime import datetime

# Function to get the domain creation date using WHOIS
def get_domain_creation_date(domain):
    try:
        domain_info = whois.whois(domain)
        return domain_info.creation_date if isinstance(domain_info.creation_date, datetime) else domain_info.creation_date[0]
    except Exception as e:
        return f"Error getting creation date: {str(e)}"

# Function to get the IP address of the domain
def get_ip_address(domain):
    try:
        return socket.gethostbyname(domain)
    except Exception as e:
        return f"Error getting IP address: {str(e)}"

# Function to get geolocation data using an IP address
def get_geolocation(ip_address):
    try:
        response = requests.get(f"https://ipinfo.io/{ip_address}/json")
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Unable to fetch location data"}
    except Exception as e:
        return {"error": str(e)}

# Main function to log website information
def log_website_info(domain):
    # Get domain creation date
    creation_date = get_domain_creation_date(domain)
    
    # Get IP address
    ip_address = get_ip_address(domain)
    
    # Get location information using IP
    if "Error" not in ip_address:
        geolocation = get_geolocation(ip_address)
    else:
        geolocation = {"error": "No geolocation data due to IP error"}

    # Log the information
    log_data = {
        "domain": domain,
        "creation_date": creation_date,
        "ip_address": ip_address,
        "location": geolocation
    }

    # Format the data
    log_message = (
        f"Website: {domain}\n"
        f"Creation Date: {creation_date}\n"
        f"IP Address: {ip_address}\n"
        f"Location Data: {geolocation}\n"
        f"Logged at: {datetime.now()}\n"
        "-----------------------------------\n"
    )

    # Write the log to the Documents folder
    documents_folder = os.path.join(os.path.expanduser('~'), 'Documents')
    log_file_path = os.path.join(documents_folder, 'website_info_log.txt')

    try:
        with open(log_file_path, 'a') as log_file:
            log_file.write(log_message)
        print(f"Log data written to: {log_file_path}")
    except Exception as e:
        print(f"Error writing log: {str(e)}")

# Example usage
if __name__ == '__main__':
    domain = 'ezraondaratv.com'  # Replace with the target website
    log_website_info(domain)
