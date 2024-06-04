#import library
import socket #Digunakan untuk membuat socket dan mengatur komunikasi jaringan
import os #Digunakan untuk mendapatkan direktori kerja saat ini dan memanipulasi path file


'''
Fungsi handle_client menangani komunikasi dengan klien: menerima permintaan HTTP, menentukan dan membaca file yang diminta, 
serta mengirimkan respon HTTP 200 OK dengan isi file jika ditemukan atau respon 404 Not Found jika tidak. 
Setelah mengirim respon, fungsi menutup koneksi dengan klien.
'''
def handle_client(client_socket):

    #Memastikan bahwa socket akan ditutup secara otomatis ketika blok ini selesai.
    with client_socket:

        #Menerima data hingga 1024 byte dari klien dan mendekodekannya dari byte string ke string.
        request = client_socket.recv(1024).decode()

        #Mencetak permintaan yang diterima untuk tujuan debugging.
        print(f"Received request: {request}")

       #Memecah permintaan HTTP menjadi baris-baris terpisah.
        headers = request.split('\n')

        #Mengambil path file yang diminta dari baris pertama permintaan HTTP.
        filename = headers[0].split()[1]

        #Jika path yang diminta adalah root ('/'), ubah menjadi '/Index.html'.
        if filename == '/':
            filename = '/index.html'

        #Menggabungkan direktori kerja saat ini dengan nama file untuk mendapatkan path lengkap file yang diminta.
        filepath = os.getcwd() + filename

        try:

            #Mencoba membuka file yang diminta dalam mode baca-biner.
            with open(filepath, 'rb') as file:
                #Membaca isi file
                response_content = file.read()

                #Membuat header respon HTTP untuk status 200 OK, termasuk tipe konten dan panjang konten.
                response_headers = 'HTTP/1.1 200 OK\n'
                response_headers += 'Content-Type: text/html\n'
                response_headers += 'Content-Length: ' + str(len(response_content)) + '\n'
                response_headers += 'Connection: close\n\n'
            response = response_headers.encode() + response_content

        #Jika file tidak ditemukan, buat respon 404 Not Found dengan pesan HTML yang sesuai.
        except FileNotFoundError:
            response_headers = 'HTTP/1.1 404 Not Found\n'
            response_headers += 'Content-Type: text/html\n'
            response_headers += 'Connection: close\n\n'
            response_content = b'<html><body><h1>404 Not Found</h1></body></html>'
            response = response_headers.encode() + response_content
       
        #Mengirim seluruh respon (header + isi) ke klien.
        client_socket.sendall(response)

        #Mencetak pesan konfirmasi bahwa respon telah dikirim.
        print(f"Response sent to {client_socket.getpeername()}")

def main():

    #Server akan mendengarkan pada semua antarmuka jaringan.
    server_ip = '0.0.0.0'

    #Mengatur port server ke 7000
    server_port = 7000

    #Membuat socket dengan IPv4 dan TCP.
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Mengikat socket ke alamat IP dan port yang ditentukan
    server.bind((server_ip, server_port))

    #Menyiapkan socket untuk mendengarkan koneksi masuk, dengan backlog maks 5 koneksi.
    server.listen(5)

    #Mencetak pesan bahwa server sedang mendengarkan koneksi pada alamat IP dan port yang ditentukan.
    print(f"Listening on {server_ip}:{server_port}")

    while True:

        #Menerima koneksi dari klien, mengembalikan socket klien dan alamat klien.
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        
        #memanggil fungsi handle_client
        handle_client(client_socket)

if __name__ == "__main__":
    main()
