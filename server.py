import socket
import os

HOST = '127.0.0.1'
PORT = 8080
BASE_DIR = './Pagine_web'

def get_mime_type(path):
    if path.endswith('.html'):
        return 'text/html'
    elif path.endswith('.css'):
        return 'text/css'
    elif path.endswith('.jpg'):
        return 'image/jpeg'
    return 'application/octet-stream'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Server in ascolto su http://{HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()
        request = conn.recv(1024).decode('utf-8')
        if not request:
            conn.close()
            continue

        try:
            path = request.split(' ')[1]
            if path == '/':
                path = '/index.html'

            file_path = BASE_DIR + path
            if os.path.isfile(file_path):
                with open(file_path, 'rb') as f:
                    content = f.read()
                mime_type = get_mime_type(file_path)
                header = f"HTTP/1.1 200 OK\r\nContent-Type: {mime_type}\r\n\r\n"
                conn.sendall(header.encode() + content)
            else:
                with open(BASE_DIR + '/error.html', 'rb') as f:
                    content = f.read()
                header = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n"
                conn.sendall(header.encode() + content)
        except Exception as e:
            print(f"Errore: {e}")
        finally:
            conn.close()
