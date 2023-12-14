import socket
import time

# Set up the client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 5050))  # Connect to Root Server on port 5050

while True:
    # Input domain name from user
    domain = input("Enter domain name to resolve: ")

    # Measure the start time before sending the query
    start_time = time.time()

        # Send domain query to Recursive DNS Server
    client_socket.send(domain.encode())

    # while True:

    # Receive response from server
    response = client_socket.recv(1024).decode()

    # Check if the response is an IP address or a referral to another server
    if "No information" in response:
        # Print the message if the domain cannot be resolved
        print(response)
        break  # Exit the loop if the domain cannot be resolved

    # Measure the end time after receiving the response
    end_time = time.time()

    # Calculate the duration for resolution
    duration = end_time - start_time

    # Print the resolved IP address
    print("Resolved IP address:", response)
    print(f"Time taken for resolution: {duration:.6f} seconds")
    break  # Exit the loop after successful resolution

client_socket.close()  # Close connection
