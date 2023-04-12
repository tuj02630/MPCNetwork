import socket
import threading
import numpy
import DeviceConnection

BUFF_SIZE = 65536
dtype = numpy.uint8

HOST = '172.31.12.186'  # Private server IP
PORT = 9999  # Port to listen on (non-privileged ports are > 1023)

thread_array = []
device_connection_array = []


def listen_for_incoming_connection():
    curr_port = 49152
    print("sender listener thread started")
    connection_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    connection_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
    connection_socket.bind((HOST, PORT))
    while True:
        print('Listening at:', (HOST, PORT))
        data, addr = connection_socket.recvfrom(BUFF_SIZE)
        data = data.decode('utf-8')
        print('GOT connection from ', addr)
        print('\t\tClient type is: ' + data[0])
        print('\t\tDevice ID is: ' + data[1:])
        curr_dc: DeviceConnection.DeviceConnection
        if data[0] == 'S':
            curr_dc = DeviceConnection.DeviceConnection(addr, data[1:], curr_port)
            device_connection_array.append(curr_dc)
            connection_socket.sendto(bytes(str(curr_port), 'utf-8'), addr)
            curr_port += 2
        if data[0] == 'R':
            print("checking device connection array for sender...")
            for dc in device_connection_array:
                if dc.get_device_id() == data[1:]:
                    print("\tmatch found!")
                    dc.add_receiver(addr[0], curr_port)
                    connection_socket.sendto(bytes(str(curr_port), 'utf-8'), addr)
                    curr_port += 2
                    break


thread_array.append(threading.Thread(target=listen_for_incoming_connection()))
for thread in thread_array:
    thread.start()

for thread in thread_array:
    thread.join()
