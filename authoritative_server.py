import socket

class AuthoritativeServer:
    def __init__(self):
        self.authoritative_cache = {}
        self.load_cache("authoritative_mappings.txt")

    def load_cache(self, filename):
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    domain, ip = line.strip().split()
                    self.authoritative_cache[domain] = ip
        except FileNotFoundError:
            print(f"Cache file '{filename}' not found.")

    def resolve_query(self, domain):
        if domain in self.authoritative_cache:
            return f"Domain: {domain}, IP: {self.authoritative_cache[domain]}"
        else:
            return f"No information found in the cache for '{domain}'"

# Create an instance of the Authoritative Server
authoritative_server = AuthoritativeServer()

# Set up the server socket for Authoritative Server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 5054))  # Bind to localhost on port 5054 for Authoritative Server
server_socket.listen(5)  # Listen for incoming connections

print("Authoritative Server is running...")

while True:
    client_socket, addr = server_socket.accept()  # Accept incoming connection
    print(f"Connection established with {addr}")

    domain = client_socket.recv(1024).decode()
    response = authoritative_server.resolve_query(domain)
    print(response)
    client_socket.send(response.encode())

    client_socket.close()
