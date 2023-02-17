# This is client code to receive video frames over UDP
import base64
import time
import numpy as np
import socket
import threading

BUFF_SIZE = 65536
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
host_name = socket.gethostname()
host_ip = '172.31.12.186'  # socket.gethostbyname(host_name)
print(host_ip)
port = 9999

# this should eventually go in a loop
socket_address = (host_ip, port)
server_socket.bind(socket_address)
print('Listening at:', socket_address)
fps, st, frames_to_count, cnt = (0, 0, 20, 0)
msg, client_addr = server_socket.recvfrom(BUFF_SIZE)
print('GOT connection from ', client_addr)
dtype = np.uint8
# this should eventually be a thread that's created for each connection
while True:
    packet, _ = server_socket.recvfrom(BUFF_SIZE)
    data = base64.b64decode(packet, ' /')
    npdata = np.frombuffer(data, dtype)


    print(npdata)

    if cnt == frames_to_count:
        try:
            fps = round(frames_to_count / (time.time() - st))
            st = time.time()
            cnt = 0
        except:
            pass
    cnt += 1
