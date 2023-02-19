# This is client code to receive video frames over UDP
import base64
import time
import numpy
import socket
import threading

# socket setup
BUFF_SIZE = 65536
host_ip = '127.0.0.1'
rc_port = 8888  # receiver client port
sc_port = 9999  # sender client port
host_name = socket.gethostname()
rc_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rc_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
dtype = numpy.uint8

# other variables
thread_array = []
found_ls_client = False
rc_client_addr = ('', 0)


def find_receiver_client():
    time.sleep(0.25)  # delay a tiny bit
    ls_address = (host_ip, rc_port)
    rc_socket.bind(ls_address)
    print('Listening at:', ls_address)
    global rc_client_addr
    rc_msg, rc_client_addr = rc_socket.recvfrom(BUFF_SIZE)
    print('GOT connection from ', rc_client_addr, ', Client type is ', str(rc_msg))
    rc_socket.sendto(b'Confirmed', rc_client_addr)
    global found_ls_client
    found_ls_client = True
    return


def find_sender_client():
    socket_address = (host_ip, sc_port)
    server_socket.bind(socket_address)
    print('Listening at:', socket_address)
    msg, client_addr = server_socket.recvfrom(BUFF_SIZE)
    print('GOT connection from ', client_addr, ', Client type is ', str(msg))
    server_socket.sendto(b'Confirmed', client_addr)
    fps, st, frames_to_count, cnt = (0, 0, 20, 0)
    while True:
        packet, _ = server_socket.recvfrom(BUFF_SIZE)
        data = base64.b64decode(packet, ' /')
        npdata = numpy.frombuffer(data, dtype) # the actual data if the server wants to do anything with it

        if found_ls_client:
            rc_socket.sendto(packet, rc_client_addr)

        if cnt == frames_to_count:
            # noinspection PyBroadException
            try:
                fps = round(frames_to_count / (time.time() - st))
                st = time.time()
                cnt = 0
            except:
                pass
        cnt += 1


receiver_client_thread = threading.Thread(target=find_receiver_client)
sender_client_thread = threading.Thread(target=find_sender_client)
thread_array.append(sender_client_thread)
thread_array.append(receiver_client_thread)
for thread in thread_array:
    thread.start()
