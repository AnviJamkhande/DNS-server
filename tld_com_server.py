import socket

class TLDComServer:
    def __init__(self):
        self.cache = {}
        self.load_mappings("tld_com_mappings.txt")

    def load_mappings(self, filename):
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    domain, ip = line.strip().split()
                    self.cache[domain] = ip
        except FileNotFoundError:
            print(f"Mappings file '{filename}' not found.")

    def update_cache(self, domain, ip):
        self.cache[domain] = ip
        with open("tld_com_mappings.txt", 'a') as file:
            file.write(f"\n{domain} {ip}")

    def resolve_com_domain(self, domain):
        if domain in self.cache:
            return self.cache[domain], True
        else:
            return f"TLD .com server: No information for '{domain}'", False

    def query_authoritative_servers(self, domain):
        # Simulating querying authoritative servers
        try:
            # Create a socket to communicate with authoritative server
            authoritative_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Connect to the authoritative server on port 5054
            authoritative_socket.connect(('localhost', 5054))

            # Send the domain name to the authoritative server
            authoritative_socket.send(domain.encode())

            # Receive the response from the authoritative server (simulated response)
            authoritative_response = authoritative_socket.recv(1024).decode()
            domain_info = authoritative_response.split(', ')
            # domain_name = domain_info[0][len("Domain: "):]
            ip_address = domain_info[1][len("IP: "):]
            # print(authoritative_response)

            # Close the socket connection to the authoritative server
            authoritative_socket.close()

            # Simulated response from authoritative server - replace this with actual response handling
            # For demonstration, let's assume authoritative server responds with an IP address
            authoritative_ip = ip_address  # Replace this with the actual IP received from authoritative server

            return authoritative_ip
        
        except ConnectionRefusedError:
            print("Connection to authoritative server failed.")
            return None

    def resolve_query(self, domain):
        if domain.endswith(".com"):
            response, found = self.resolve_com_domain(domain)
            if not found:
                print(f"No information found in the cache for '{domain}'. Querying authoritative servers...")

                # Simulating querying authoritative servers
                authoritative_ip = self.query_authoritative_servers(domain)
                if authoritative_ip:
                    self.update_cache(domain, authoritative_ip)
                    response, _ = self.resolve_org_domain(domain)
                    print(f"Updated cache with information for '{domain}': {response}")
                    return response.encode(), True
                else:
                    response = f"No information available for '{domain}' from authoritative servers."
                    return response.encode(), False
            else:
                print(f"IP address for domain '{domain}': {response}")
                return response.encode(), True
        else:
            response = "Invalid domain format"
            return response.encode(), False

# Create an instance of the TLD .com Server
tld_com_server = TLDComServer()

# Set up the server socket for .com TLD Server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 5051))  # Bind to localhost on port 5051 for .com TLD
server_socket.listen(5)  # Listen for incoming connections

print("TLD .com Server is running...")

while True:
    client_socket, addr = server_socket.accept()  # Accept incoming connection
    print(f"Connection established with {addr}")

    while True:
        domain = client_socket.recv(1024).decode()
        response, found = tld_com_server.resolve_query(domain)
        client_socket.send(response)

        if not found in response:
            break

    client_socket.close()  # Close connection
