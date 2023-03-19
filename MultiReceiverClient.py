import socket
import base64

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
DEVICE_ID = "ABCDEFGH"
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    message = "R"+DEVICE_ID
    s.sendall(bytes(message, 'utf-8'))
    data = s.recv(1024)

print(f"Received {data!r}")
