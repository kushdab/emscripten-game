import requests
from bs4 import BeautifulSoup
import socket
import nmap

# Target website
target_url = "https://nakurugolfclub.co.ke"  # Change this to your authorized domain

# 1. Check HTTP Response Headers (Security Headers)
def check_http_headers():
    response = requests.get(target_url)
    headers = response.headers
    print("Security Headers:")
    for header in ['X-Content-Type-Options', 'X-Frame-Options', 'Strict-Transport-Security', 'Content-Security-Policy']:
        if header in headers:
            print(f"{header}: {headers[header]}")
        else:
            print(f"{header}: Not found")

# 2. Check for common vulnerabilities in forms (SQLi, XSS)
def check_forms():
    response = requests.get(target_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    forms = soup.find_all('form')
    print(f"Found {len(forms)} form(s)")

    for form in forms:
        action = form.get('action')
        method = form.get('method', 'get')
        inputs = form.find_all('input')
        
        print(f"\nForm action: {action}")
        print(f"Form method: {method}")
        for input_field in inputs:
            print(f"Input field: {input_field.get('name')} (type: {input_field.get('type')})")

# 3. Port scanning using Nmap
def port_scan():
    target_domain = socket.gethostbyname("nakurugolfclub.co.ke")  # Resolving IP
    nm = nmap.PortScanner()
    print(f"Scanning target: {target_domain}")
    
    # Scan common ports
    scan_result = nm.scan(target_domain, '20-1024')
    for host in scan_result['scan']:
        print(f"Host: {host} ({nm[host].hostname()})")
        print(f"State: {nm[host].state()}")
        
        for proto in nm[host].all_protocols():
            print(f"Protocol: {proto}")
            ports = nm[host][proto].keys()
            for port in ports:
                print(f"Port: {port}\tState: {nm[host][proto][port]['state']}")

# 4. Check for SSL Certificate details (TLS scan)
def check_ssl_certificate():
    try:
        cert_response = requests.get(target_url, verify=True)
        print(f"SSL certificate is valid: {cert_response}")
    except requests.exceptions.SSLError as ssl_err:
        print(f"SSL Error: {ssl_err}")

# 5. Check for subdomains using DNS brute force (simple approach)
def brute_force_subdomains():
    subdomains = ['www', 'mail', 'dev', 'test', 'ftp']
    target_domain = 'nakurugolfclub.co.ke'  # Change this to your authorized domain
    
    print("Checking subdomains:")
    for sub in subdomains:
        try:
            subdomain = f"{sub}.{target_domain}"
            ip = socket.gethostbyname(subdomain)
            print(f"Subdomain found: {subdomain} -> IP: {ip}")
        except socket.gaierror:
            pass  # No subdomain found

# Main function to run the tests
if __name__ == "__main__":
    print("Starting Penetration Testing...")
    
    # Check HTTP Headers
    check_http_headers()
    
    # Check for Forms and Vulnerabilities
    check_forms()
    
    # Perform a port scan
    port_scan()
    
    # Check SSL certificate
    check_ssl_certificate()
    
    # Brute force subdomain discovery
    brute_force_subdomains()

    print("Testing Complete.")
