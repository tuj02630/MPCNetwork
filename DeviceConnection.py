import socket
import threading
import numpy

BUFF_SIZE = 65536
dtype = numpy.uint8

HOST = '172.31.12.186'
v_port = 9998
a_port = 9999

DEBUG = False

class DeviceConnection:
    thread_array = []
    device_id: str = ""
    s_addr: tuple = ('', 0)
    curr_port: int  # video port, audio port is + 1
    thread_array = []
    socket_array:tuple = []
    receiver_array: socket.socket = []  #
    sv_socket: socket.socket
    sa_socket: socket.socket
    sv_addr: tuple = ('', 0)
    sa_addr: tuple = ('', 0)

    vid_thread: threading.Thread
    aud_thread: threading.Thread

    def video_sending_handler(self):
        self.sv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
        # self.sv_socket.bind((local_ip, self.curr_port))

        # start connection
        self.sv_socket.bind(((HOST, self.curr_port)))
        while True:
            packet, _ = self.sv_socket.recvfrom(BUFF_SIZE)
            if DEBUG:
                print("\nReceiving Video: " + str(packet))
            # send packet to all rv ips here
            i = 0
            for sock in self.receiver_array:
                sock.sendto(packet, self.socket_array[i])
                i+=1
        return

    def audio_sending_handler(self):
        s_ip, s_port = self.s_addr
        self.sa_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sa_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
        # start connection
        self.sa_socket.bind((HOST, self.curr_port + 1))

        while True:
            packet, _ = self.sa_socket.recvfrom(BUFF_SIZE)
            # send packet to all ra ips here
            i = 0
            for sock in self.receiver_array:
                sock.sendto(packet, self.socket_array[i])
                i+=1
        return

    def add_receiver(self, ip:str, port:int):
        print("\tOpening new socket with port: "+str(port))
        r_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        r_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
        r_socket.bind((HOST, port))
        threading.Thread(target=self.start_receiver_socket, args=r_socket).start()
        self.socket_array.append((ip, port))
        self.receiver_array.append(r_socket)

    def start_receiver_socket(self, r_socket:socket.socket):
        r_socket.recv(BUFF_SIZE)
        return

    def set_sender_socket(self, ss: tuple):
        self.s_addr

    def get_device_id(self):
        return self.device_id

    def __init__(self, s_addr: tuple, device_id: str, curr_port: int):
        self.s_addr = s_addr
        self.device_id = device_id
        self.curr_port = curr_port
        print(
            "\t\tCreated new DeviceConnection with Device ID: " + self.device_id + " and address: " + str(self.s_addr))
        self.vid_thread = threading.Thread(target=self.video_sending_handler)
        self.aud_thread = threading.Thread(target=self.audio_sending_handler)
        self.vid_thread.start()
        self.aud_thread.start()
