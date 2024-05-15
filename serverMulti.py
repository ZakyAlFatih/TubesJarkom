import socket
import threading
import os

def handle_client(client_socket):
    with client_socket:
        request = client_socket.recv(1024).decode()
        print(f"Received request: {request}")
        headers = request.split('\n')
        filename = headers[0].split()[1]

        if filename == '/':
            filename = '/Hello.html'

        filepath = os.getcwd() + filename

        try:
            with open(filepath, 'rb') as file:
                response_content = file.read()
                response_headers = 'HTTP/1.1 200 OK\n'
                response_headers += 'Content-Type: text/html\n'
                response_headers += 'Content-Length: ' + str(len(response_content)) + '\n'
                response_headers += 'Connection: close\n\n'
            response = response_headers.encode() + response_content
        except FileNotFoundError:
            response_headers = 'HTTP/1.1 404 Not Found\n'
            response_headers += 'Content-Type: text/html\n'
            response_headers += 'Connection: close\n\n'
            response_content = b'<html><body><h1>404 Not Found</h1></body></html>'
            response = response_headers.encode() + response_content

        client_socket.sendall(response)
        print(f"Response sent to {client_socket.getpeername()}")

def main():
    server_ip = '0.0.0.0'
    server_port = 7000
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, server_port))
    server.listen(5)
    print(f"[*] Listening on {server_ip}:{server_port}")

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()
