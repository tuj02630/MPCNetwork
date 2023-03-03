import base64
import socket
import threading
import time
import numpy

BUFF_SIZE = 65536
dtype = numpy.uint8

loopback = '127.0.0.1'
local_v_port = 3000
local_a_port = 3001

rv_port = 50010
ra_port = 50020


class DeviceConnection:
    device_id = ""

    client_ip = ''
    client_port = 0
    thread_array = []
    rv_socket: socket.socket
    ra_socket: socket.socket
    sv_socket: socket.socket
    sa_socket: socket.socket

    rv_to_sv: socket.socket
    ra_to_sa: socket.socket

    rv_addr: tuple = ('', 0)
    ra_addr: tuple = ('', 0)
    sv_addr: tuple = ('', 0)
    sa_addr: tuple = ('', 0)

    rv_ready_event = threading.Event()
    ra_ready_event = threading.Event()
    sv_ready_event = threading.Event()
    sa_ready_event = threading.Event()

    rv_thread: threading.Thread
    ra_thread: threading.Thread
    sv_thread: threading.Thread
    sa_thread: threading.Thread

    def __init__(self, client_addr: tuple):
        self.client_ip, self.client_port = client_addr
        # local communication
        self.rv_to_sv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rv_to_sv.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
        self.ra_to_sa = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ra_to_sa.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
        # self.rv_to_sv.bind((loopback, local_v_port))
        # self.ra_to_sa.bind((loopback, local_a_port))
        # threads

        self.rv_thread = threading.Thread(target=self.video_receiver_thread)
        self.ra_thread = threading.Thread(target=self.audio_receiver_thread)
        self.rv_thread.start()
        self.ra_thread.start()

    def video_receiver_thread(self):
        fps, st, frames_to_count, cnt = (0, 0, 20, 0)
        self.rv_addr = (self.client_ip, rv_port)
        self.rv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
        self.rv_socket.sendto(b'Audio Confirmation', self.rv_addr)
        while True:
            packet, _ = self.rv_socket.recvfrom(BUFF_SIZE)
            if self.sv_ready_event.is_set():
                self.rv_to_sv.sendto(packet, (loopback, local_v_port))
            if cnt == frames_to_count:
                # noinspection PyBroadException
                try:
                    fps = round(frames_to_count / (time.time() - st))
                    st = time.time()
                    cnt = 0
                except:
                    pass
            cnt += 1
        return

    def audio_receiver_thread(self):
        self.ra_addr = (self.client_ip, ra_port)
        self.ra_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ra_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
        self.ra_socket.sendto(b'Audio Confirmation', self.ra_addr)
        while True:
            try:
                packet, _ = self.ra_socket.recvfrom(BUFF_SIZE)
            except TimeoutError:
                self.ra_socket.close()
                break
            # data = base64.b64decode(packet, ' /')  # the actual data if the server wants to do anything with it
            if self.sa_ready_event.is_set():
                self.ra_to_sa.sendto(packet, (loopback, local_a_port))
        return

    def video_sender_thread(self):
        self.sv_socket = socket.socket(socket.AF_INET, socket)
        self.sv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
        while True:
            if self.sv_addr != ('', 0):
                packet, _ = self.ra_to_sa.recvfrom(BUFF_SIZE)
                self.sv_socket.sendto(packet, self.sv_addr)
            else:
                time.sleep(1)
        return

    def find_receiver(self):
