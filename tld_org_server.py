import socket

class TLDOrgServer:
    def __init__(self):
        self.cache = {}
        self.load_mappings("tld_org_mappings.txt")

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
        with open("tld_org_mappings.txt", 'a') as file:
            file.write(f"{domain} {ip}\n")

    def resolve_org_domain(self, domain):
        if domain in self.cache:
            return self.cache[domain], True
        else:
            return f"TLD .org server: No information for '{domain}'", False

    def resolve_query(self, domain):
        if domain.endswith(".org"):
            response, found = self.resolve_org_domain(domain)
            if not found:
                print(response)
                i = 0  # Change this to your starting IP index
                i += 1
                ip = f"192.168.1.{i}"  # Replace with your logic to get IP address
                self.update_cache(domain, ip)
                response, _ = self.resolve_org_domain(domain)
                return response.encode(), found
            else:
                print(f"IP address for domain {domain}: {response}")
                return response.encode(), found
        else:
            response = "No information for domain"
            return response.encode(), False
        
# Create an instance of the TLD .org Server
tld_org_server = TLDOrgServer()

# Set up the server socket for .org TLD Server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 5052))  # Bind to localhost on port 5052 for .org TLD
server_socket.listen(5)  # Listen for incoming connections

print("TLD .org Server is running...")

while True:
    client_socket, addr = server_socket.accept()  # Accept incoming connection
    print(f"Connection established with {addr}")

    while True:
        domain = client_socket.recv(1024).decode()
        response, found = tld_org_server.resolve_query(domain)
        client_socket.send(response)

        if not found in response:
            break
        client_socket.close()