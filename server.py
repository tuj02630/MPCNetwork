import base64
import time
import numpy
import socket
from threading import *


class Server:
    def __init__(self, lock: Lock, semaphore: Semaphore):
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

        self.lock = lock
        self.active = True
        self.semi = semaphore
        if self.lock.locked():
            print("Locked")
        self.lock.acquire()
        time.sleep(0.25)
        for i in range(4):
            self.semi.acquire()


    def find_video_receiver(self):
        self.rv_socket.bind((self.host_ip, self.rv_port))
        print('Listening at:', (self.host_ip, self.rv_port))
        rc_msg, self.rv_addr = self.rv_socket.recvfrom(self.BUFF_SIZE)
        print('GOT connection from ', self.rv_addr, ', Client type is ', str(rc_msg))
        self.rv_socket.sendto(b'Confirmed', self.rv_addr)
        self.found_rv_client = True
        self.semi.release()
        return

    def find_video_sender(self):
        self.sv_socket.settimeout(500)

        self.sv_socket.bind((self.host_ip, self.sv_port))
        print('Listening at:', (self.host_ip, self.sv_port))
        msg, self.sv_addr = self.sv_socket.recvfrom(self.BUFF_SIZE)
        print('GOT connection from ', self.sv_addr, ', Client type is ', str(msg))
        self.sv_socket.sendto(b'Confirmed', self.sv_addr)
        fps, st, frames_to_count, cnt = (0, 0, 20, 0)
        self.sv_socket.settimeout(5)
        while True:
            if not self.active:
                self.semi.release()
                self.lock.release()
                return
            try:
                packet, _ = self.sv_socket.recvfrom(self.BUFF_SIZE)
            except socket.timeout:
                print("Timeout video here")
                self.sv_socket.close()
                self.lock.release()
                self.stop()

                return
            data = base64.b64decode(packet, ' /')

            data = numpy.frombuffer(data, self.dtype)  # the actual data if the server wants to do anything with it
            if self.found_rv_client:
                self.rv_socket.sendto(packet, self.rv_addr)
            if cnt == frames_to_count:
                # noinspection PyBroadException
                try:
                    fps = round(frames_to_count / (time.time() - st))
                    st = time.time()
                    cnt = 0
                except:
                    pass
            cnt += 1

    def find_audio_sender(self):
        # initial socket setup
        self.sa_socket.settimeout(500)
        self.sa_socket.bind((self.host_ip, self.sa_port))

        print('Listening at:', (self.host_ip, self.sa_port))
        msg, self.sa_addr = self.sa_socket.recvfrom(self.BUFF_SIZE)
        print('GOT connection from ', self.sa_addr, ', Client type is ', str(msg))
        self.sa_socket.sendto(b'Confirmed', self.sa_addr)
        self.sa_socket.settimeout(5)
        while True:
            if not self.active:
                self.stop()
                self.semi.release()
                self.lock.release()
                return
            try:
                packet, _ = self.sa_socket.recvfrom(self.BUFF_SIZE)
            except socket.timeout:
                self.sa_socket.close()
                print("Timeout audio here")
                self.semi.release()
                self.stop()

                return
            data = base64.b64decode(packet, ' /')  # the actual data if the server wants to do anything with it
            if self.found_ra_client:
                self.ra_socket.sendto(packet, self.ra_addr)

    def find_audio_receiver(self):
        self.ra_socket.bind((self.host_ip, self.ra_port))
        print('Listening at:', (self.host_ip, self.ra_port))
        msg, self.ra_addr = self.ra_socket.recvfrom(self.BUFF_SIZE)
        print('GOT connection from ', self.ra_addr, ', Client type is ', str(msg))
        self.found_ra_client = True
        self.semi.release()
        return

    def run(self):
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

    def stop(self):
        self.active = False
        lock.release()


if __name__ == "__main__":
    semi = Semaphore(4)
    lock = Lock()
    server = Server(lock, semi)
    server.run()
    server = Server(lock, semi)
    server.run()

