import base64
import io
import socket
import threading
import time
import cv2
import numpy

BUFF_SIZE = 65536
dtype = numpy.uint8

local_ip = '127.0.0.1'
local_v_port = 3000
local_a_port = 3001


class DeviceConnection(threading.Thread):
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



    def run(self):
        # local communication
        self.rv_to_sv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rv_to_sv.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
        self.ra_to_sa = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ra_to_sa.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
        self.rv_to_sv.bind((local_ip, local_v_port))
        self.ra_to_sa.bind((local_ip, local_a_port))
        # threads
        self.thread_array.append(threading.Thread(target=self.video_receiver_thread))
        self.thread_array.append(threading.Thread(target=self.audio_receiver_thread))
        self.thread_array.append(threading.Thread(target=self.video_sender_thread))
        self.thread_array.append
        for thread in self.thread_array:
            thread.start()

    def video_receiver_thread(self):
        fps, st, frames_to_count, cnt = (0, 0, 20, 0)
        self.rv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
        # self.rv_socket.sendto(b'Audio Confirmation', REPLACE_ME_WITH_ADDR)
        while True:
            packet, _ = self.rv_socket.recvfrom(BUFF_SIZE)
            self.rv_to_sv.sendto(packet, (local_ip, local_v_port))
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
        self.rv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
        self.rv_socket.sendto(b'Audio Confirmation', sock)
        return

    def video_sender_thread(self):
        self.sv_socket = socket.socket(socket.AF_INET, socket)
        self.sv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
        while True:
            if self.sv_addr != ('', 0):
                packet, _ = self.v_packet_stream.read1(BUFF_SIZE)
                self.sv_socket.sendto(packet, self.sv_addr)
            else:
                time.sleep(1)
        return

    def set_sv_addr(self, sock:tuple):
