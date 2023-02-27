import base64
import time
import numpy
import socket
import threading
from DeviceConnection import DeviceConnection

device_connections = list()

BUFF_SIZE = 65536
dtype = numpy.uint8

host_ip = '127.0.0.1'
port = 9999

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
socket_address = (host_ip, port)
server_socket.bind(socket_address)

print('Listening at:', socket_address)

while True:
    msg, client_addr = server_socket.recvfrom(BUFF_SIZE)
    (client_ip, client_port) = client_addr
    print('GOT connection from ', client_addr)
    device_connections.append(DeviceConnection())
