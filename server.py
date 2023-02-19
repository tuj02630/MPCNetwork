# This is client code to receive video frames over UDP
import base64
import time
import numpy as np
import socket
import threading

thread_array = []
BUFF_SIZE = 65536
packet: bytes = b''
found_ls_client = False
ls_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ls_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
ls_client_addr = ("", 0)


def find_livestream_client():
    ls_ip = '127.0.0.1'
    ls_port = 8888
    ls_address = (ls_ip, ls_port)
    ls_socket.bind(ls_address)
    print('Listening at:', ls_address)
    global ls_client_addr
    ls_msg, ls_client_addr = ls_socket.recvfrom(BUFF_SIZE)
    print('GOT connection from ', ls_client_addr, ', Client type is ', str(ls_msg))
    ls_socket.sendto(b'Hi', ls_client_addr)
    global found_ls_client
    found_ls_client = True
    return


BUFF_SIZE = 65536
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
host_name = socket.gethostname()
host_ip = '127.0.0.1'  # socket.gethostbyname(host_name)
print(host_ip)
port_s = 9999
socket_address = (host_ip, port_s)
server_socket.bind(socket_address)
print('Listening at:', socket_address)
fps, st, frames_to_count, cnt = (0, 0, 20, 0)
msg, client_addr = server_socket.recvfrom(BUFF_SIZE)
print('GOT connection from ', client_addr)
dtype = np.uint8

receiver_client_thread = threading.Thread(target=find_livestream_client)
thread_array.append(receiver_client_thread)
receiver_client_thread.start()
# this should eventually be a thread that's created for each connection
while True:
    packet, _ = server_socket.recvfrom(BUFF_SIZE)
    data = base64.b64decode(packet, ' /')
    npdata = np.frombuffer(data, dtype)

    if found_ls_client:
        ls_socket.sendto(packet, ls_client_addr)

    # print(npdata)
    if cnt == frames_to_count:
        try:
            fps = round(frames_to_count / (time.time() - st))
            st = time.time()
            cnt = 0
        except:
            pass
    cnt += 1
