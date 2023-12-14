import socket

class RootServer:
    def __init__(self):
        self.cache = {
            "com": ("localhost", 5051),  # TLD server for .com
            "org": ("localhost", 5052)   # TLD server for .org
            # Add other TLD mappings here
        }

    def resolve_query(self, domain):
        if domain in self.cache:
            # If TLD information is found in the Root Server's cache
            return f"Root server: Referring to TLD '{domain}'", True
        else:
            # Referring to TLD servers for domain resolution
            if domain.endswith(".com"):
                tld_server_address = self.cache["com"]
            elif domain.endswith(".org"):
                tld_server_address = self.cache["org"]
            else:
                return f"Root server: No information for TLD '{domain}'", False

            # Connect to the appropriate TLD server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tld_client_socket:
                tld_client_socket.connect(tld_server_address)

                # Send domain query to TLD server
                tld_client_socket.send(domain.encode())

                # Receive response from TLD server
                response = tld_client_socket.recv(1024).decode()

            return response, True  # Assuming the TLD server responds with IP or error

# Create an instance of the Root Server
root_server = RootServer()

# Set up the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 5050))  # Bind to localhost on port 5050
server_socket.listen(5)  # Listen for incoming connections

print("Root Server is running...")

while True:
    client_socket, addr = server_socket.accept()  # Accept incoming connection
    print(f"Connection established with {addr}")

    # Receive domain query from client
    domain = client_socket.recv(1024).decode()

    # Resolve domain query using the Root Server
    response, found = root_server.resolve_query(domain)

    # Send response to client
    client_socket.send(response.encode())

    client_socket.close()  # Close connection
