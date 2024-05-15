import socket
import sys

def http_client(server_host, server_port, filename):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the server
    client_socket.connect((server_host, int(server_port)))
    
    # Create HTTP GET request
    request = f"GET {filename} HTTP/1.1\r\nHost: {server_host}\r\nConnection: close\r\n\r\n"
    
    # Send the request to the server
    client_socket.sendall(request.encode())
    
    # Receive the response from the server
    response = b""
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        response += data
    
    # Close the socket
    client_socket.close()
    
    # Print the response
    print(response.decode())

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python client.py <server_host> <server_port> <filename>")
        sys.exit(1)

    server_host = sys.argv[1]
    server_port = sys.argv[2]
    filename = sys.argv[3]

    http_client(server_host, server_port, filename)
