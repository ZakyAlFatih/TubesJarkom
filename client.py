#import library
import socket #digunakan untuk membuat socket sebagai komunikasi jaringan
import sys #digunakan untuk akses ke parameter dan fungsi sistem

'''
Fungsi http_client digunakan untuk mengirimkan permintaan HTTP GET ke sebuah server, 
menerima responnya, dan menampilkannya. Fungsi ini membuat objek socket untuk 
koneksi jaringan, menghubungkan ke server menggunakan alamat dan port yang diberikan, 
kemudian mengirimkan permintaan HTTP GET yang mencakup nama file yang diminta.
Setelah permintaan dikirim, fungsi ini terus menerima data dari server hingga tidak ada
data lagi yang diterima, menyimpan respon tersebut, menutup koneksi socket, dan akhirnya 
mencetak respon dari server ke terminal.
'''

def http_client(server_host, server_port, filename):
    # Membuat sebuah socket menggunakan IPv4 ('AF_INET') dan TCP('SOCK_STREAM')
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Menghubungkan socket ke server dengan alamat server_host dan port server_port
    client_socket.connect((server_host, int(server_port)))
    
    # request berisikan string yang berisi permintaan HTTP GET. Permintaan ini mengikuti
    #format HTTP/1.1, di mana 'filename' adalah path dari resource yang diminta
    request = f"GET {filename} HTTP/1.1\r\nHost: {server_host}\r\nConnection: close\r\n\r\n"
    
    # Mengirimkan permintaan HTTP GET yang telah dibuat ke server. Permintaan di-encode ke dalam format byte sebelum dikirim.
    client_socket.sendall(request.encode())
    
    # Menerima respons server
    # Inisialisasi variabel response sebagai byte string kosong untuk menyimpan data yang diterima dari server.
    response = b""      
    
    #loop untuk terus menerima data dari server
    while True:
        #Menerima data hingga 1024 byte dari server
        data = client_socket.recv(1024)
        
        #Jika tidak ada data yang diterima (koneksi ditutup oleh server), loop berhenti.
        if not data: 
            break

        #Menambahkan data yang diterima ke dalam variabel response.
        response += data 
    
    # Menutup koneksi socket ke server.
    client_socket.close()
    
    # Mencetak respon yang diterima dari server setelah di-decode dari byte string ke string.
    print(response.decode())

if __name__ == "__main__":

    #Memeriksa apakah jumlah argumen command line yang diberikan adalah 4 
    if len(sys.argv) != 4:
        
        #Jika jumlah argumen tidak tepat, cetak pesan penggunaan yang benar dan keluar dari program.
        print("Please use this command line format on your terminal: python client.py <server_host> <server_port> <filename>")
        sys.exit(1)

    #Mengambil nilai server_host, server_port, dan filename dari argumen command line.
    server_host = sys.argv[1]
    server_port = sys.argv[2]
    filename = sys.argv[3]

    #Memanggil fungsi http_client dengan argumen yang diberikan.
    http_client(server_host, server_port, filename)
