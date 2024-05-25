import socket
import threading
import urllib.parse
import os
import algorithm


def handle_client(client_socket):
    with client_socket:
        request = client_socket.recv(4096).decode()
        headers,body = request.split("\r\n\r\n",1)
        headers = headers.split("\r\n")
        method,path,_ = headers[0].split()
        if method == "POST" and path == "/extract":
            data = urllib.parse.parse_qs(body)
            file_content = data.get("fileContent")[0]
            keyword = data.get("keyword")[0]
            algorithm = data.get("algorithm")[0]

            if file_content and keyword and algorithm:
                if algorithm == "bf":
                    results = algorithm.NEBF(file_content, keyword)
                elif algorithm == "kmp":
                    results = algorithm.NEKMP(file_content, keyword)

                results_str = "<br>".join(f"Found at index: {index}" for index in results) if results else "Keyword not found."
                message_body = f"""
                <html>
                <body>
                    <h1>Search Results</h1>
                    <p><strong>Keyword:</strong> {keyword}</p>
                    <p><strong>Algoritma yang dipilih:</strong> {algorithm}</p>
                    <p><strong>Hasil ekstraksi berita:</strong> {results_str}</p>
                </body>
                </html>
                """
                response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + message_body
                client_socket.sendall(response.encode())
            else:
                response = "HTTP/1.1 400 Bad Request\r\nContent-Type: text/html\r\n\r\n<html><body><h1>400 Bad Request</h1></body></html>"
                client_socket.sendall(response.encode())
        else:
            if path == '/':
                path = '/index.html'
            filepath = os.getcwd() + path

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
    print(f"Listening on {server_ip}:{server_port}")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()
