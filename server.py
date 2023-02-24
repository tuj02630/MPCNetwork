import base64
import time
import numpy
import socket
from threading import *


class Server:
    def __init__(self,
                 r_lock: Lock,
                 s_lock: Lock,
                sv_port_lock: Lock,
                rv_port_lock: Lock,
                sa_port_lock: Lock,
                ra_port_lock: Lock):
        # socket setup
        self.BUFF_SIZE = 65536
        self.host_ip = '172.31.12.186'
        # self.host_ip = '127.0.0.1'
        self.sv_port = 9999  # sender video port
        self.sa_port = 9998  # sender audio port
        self.rv_port = 8888  # receiver video port
        self.ra_port = 8887  # receiver audio port
        self.host_name = socket.gethostname()
        # S: Sending
        # R: Receiving
        # V: Video
        # A: Audio
        self.rv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.BUFF_SIZE)
        self.sv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.BUFF_SIZE)
        self.sa_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sa_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.BUFF_SIZE)
        self.ra_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ra_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.BUFF_SIZE)
        self.dtype = numpy.uint8

        # audio settings are unused here but i figure it can't hurt to have them on the server
        self.CHUNK = 1024
        # FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        self.FRAMES_PER_BUFFER = 1000

        # other variables
        self.thread_array = []
        self.found_rv_client = False
        self.found_ra_client = False
        self.rv_addr = ('', 0)
        self.ra_addr = ('', 0)

        self.stop_lock = Lock()

        self.active = True

        self.r_lock = r_lock
        self.s_lock = s_lock
        self.sv_port_lock = sv_port_lock
        self.rv_port_lock = rv_port_lock
        self.sa_port_lock = sa_port_lock
        self.ra_port_lock = ra_port_lock


    def find_video_receiver(self):
        try:
            self.rv_socket.bind((self.host_ip, self.rv_port))
        except OSError:
            return

        print('Listening at:', (self.host_ip, self.rv_port))
        rc_msg, self.rv_addr = self.rv_socket.recvfrom(self.BUFF_SIZE)
        print(self.rv_addr)
        print('GOT connection from ', self.rv_addr, ', Client type is ', str(rc_msg))
        self.rv_socket.sendto(b'Confirmed', self.rv_addr)
        self.found_rv_client = True
        self.rv_port_lock.release()
        return


    def find_audio_receiver(self):
        self.ra_socket.bind((self.host_ip, self.ra_port))
        print('Listening at:', (self.host_ip, self.ra_port))
        msg, self.ra_addr = self.ra_socket.recvfrom(self.BUFF_SIZE)
        print('GOT connection from ', self.ra_addr, ', Client type is ', str(msg))
        self.found_ra_client = True
        self.ra_port_lock.release()
        return


    def sender_setup(self, socket: socket.socket, port: int):
        socket.settimeout(500)
        try:
            socket.bind((self.host_ip, port))
        except OSError:
            return None
        print('Listening at:', (self.host_ip, port))
        msg, addr = socket.recvfrom(self.BUFF_SIZE)
        print('GOT connection from ', addr, ', Client type is ', str(msg))
        socket.sendto(b'Confirmed', addr)
        socket.settimeout(5)
        return (msg, addr)


    def sender_operation(self, port_lock: Lock, sender_socket: socket.socket, receiver_socket: socket.socket, addr,
                         found_client: bool):
        if not self.active:
            return None
        try:
            packet, _ = sender_socket.recvfrom(self.BUFF_SIZE)
        except socket.timeout:
            print("Timeout video here")
            sender_socket.close()
            port_lock.release()
            self.stop()

            return None

        data = base64.b64decode(packet, ' /')

        if found_client:
            receiver_socket.sendto(packet, addr)

        return data


    def find_video_sender(self):
        msg, self.sv_addr = self.sender_setup(self.sv_socket, self.sv_port)
        fps, st, frames_to_count, cnt = (0, 0, 20, 0)
        while True:
            data = self.sender_operation(self.sv_port_lock, self.sv_socket, self.rv_socket, self.rv_addr,
                                         self.found_rv_client)
            if data is None:
                return
            ##### Analysis
            # data = numpy.frombuffer(data, self.dtype)  # the actual data if the server wants to do anything with it
            # if cnt == frames_to_count:
            #     # noinspection PyBroadException
            #     try:
            #         fps = round(frames_to_count / (time.time() - st))
            #         st = time.time()
            #         cnt = 0
            #     except:
            #         pass
            # cnt += 1


    def find_audio_sender(self):
        msg, self.sa_addr = self.sender_setup(self.sa_socket, self.sa_port)
        while True:
            data = self.sender_operation(self.sa_port_lock, self.sa_socket, self.ra_socket, self.ra_addr,
                                         self.found_ra_client)
            if data is None:
                return


    def run(self):
        self.server_lock.acquire()
        vid_sender_thread = Thread(target=self.find_video_sender)
        aud_sender_thread = Thread(target=self.find_audio_sender)
        vid_receiver_thread = Thread(target=self.find_video_receiver)
        aud_receiver_thread = Thread(target=self.find_audio_receiver)

        self.thread_array.append(vid_sender_thread)
        self.thread_array.append(aud_sender_thread)
        self.thread_array.append(vid_receiver_thread)
        self.thread_array.append(aud_receiver_thread)

        for thread in self.thread_array:
            thread.start()
            time.sleep(0.25)

        self.sv_port_lock.acquire()
        self.rv_port_lock.acquire()
        self.sa_port_lock.acquire()
        self.ra_port_lock.acquire()


    def stop(self):
        self.stop_lock.acquire()
        if self.active == True:
            self.active = False
            print("Stoppeds")
            self.server_lock.release()
        self.stop_lock.release()


if __name__ == "__main__":
    server_lock = Lock()
    sv_port_lock = Lock()
    rv_port_lock = Lock()
    sa_port_lock = Lock()
    ra_port_lock = Lock()

    server = Server(server_lock, sv_port_lock, rv_port_lock, sa_port_lock, ra_port_lock)
    server.run()

    server = Server(server_lock, sv_port_lock, rv_port_lock, sa_port_lock, ra_port_lock)
    server.run()

