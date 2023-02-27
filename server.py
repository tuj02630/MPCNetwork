import base64
import time
import numpy
import socket
from threading import *


class Server:
    """
    Server class that will be running in server and manages the connection from clients
    """
    def __init__(self,
                 server_lock: Lock,
                 sv_port_lock: Lock,
                 rv_port_lock: Lock,
                 sa_port_lock: Lock,
                 ra_port_lock: Lock):
        # socket setup
        """Data buffer size for the video and audio stream"""
        self.BUFF_SIZE = 65536
        """Private ip for the server"""
        self.host_ip = '172.31.12.186'
        # self.host_ip = '127.0.0.1'
        """Port that is used to send video data"""
        self.sv_port = 9999  # sender video port
        """Port that is used to send audio data"""
        self.sa_port = 9998  # sender audio port
        """Port that is used to receive video data"""
        self.rv_port = 8888  # receiver video port
        """Port that is used to receive audio data"""
        self.ra_port = 8887  # receiver audio port
        self.host_name = socket.gethostname()
        # S: Sending
        # R: Receiving
        # V: Video
        # A: Audio
        """Video socket to receive video data from the server"""
        self.rv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.BUFF_SIZE)
        """Video socket to send video data from the server"""
        self.sv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.BUFF_SIZE)
        """Audio socket to send audio data from the server"""
        self.sa_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sa_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.BUFF_SIZE)
        """Audio socket to receive audio data from the server"""
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
        """Thread list to store video and audio thread"""
        self.thread_array = []
        """Flag for the """
        self.found_rv_client = False
        self.found_ra_client = False
        self.rv_addr = ('', 0)
        self.ra_addr = ('', 0)

        self.stop_lock = Lock()

        self.active = True
        """Flag to indicate the status of server instance"""

        self.server_lock = server_lock
        """Lock to secure the server instance from the threads"""
        self.sv_port_lock = sv_port_lock
        """Lock to secure the send video port"""
        self.rv_port_lock = rv_port_lock
        """Lock to secure the receive video port"""
        self.sa_port_lock = sa_port_lock
        """Lock to secure the send audio port"""
        self.ra_port_lock = ra_port_lock
        """Lock to secure the receive audio port"""

    def find_video_receiver(self):
        self.rv_socket.bind((self.host_ip, self.rv_port))
        print('Listening at:', (self.host_ip, self.rv_port))
        rc_msg, self.rv_addr = self.rv_socket.recvfrom(self.BUFF_SIZE)
        print('GOT connection from ', self.rv_addr, ', Client type is ', str(rc_msg))
        self.rv_socket.sendto(b'Confirmed', self.rv_addr)
        self.found_rv_client = True
        return

    def find_audio_receiver(self):
        self.ra_socket.bind((self.host_ip, self.ra_port))
        print('Listening at:', (self.host_ip, self.ra_port))
        msg, self.ra_addr = self.ra_socket.recvfrom(self.BUFF_SIZE)
        print('GOT connection from ', self.ra_addr, ', Client type is ', str(msg))
        self.found_ra_client = True
        return

    def sender_setup(self, socket: socket.socket, port: int):
        socket.settimeout(500)
        socket.bind((self.host_ip, port))
        print('Listening at:', (self.host_ip, port))
        msg, addr = socket.recvfrom(self.BUFF_SIZE)
        print('GOT connection from ', addr, ', Client type is ', str(msg))
        socket.sendto(b'Confirmed', addr)
        socket.settimeout(0.5)
        return (msg, addr)

    def sender_operation(self, port_lock: Lock, sender_socket: socket.socket, receiver_socket: socket.socket, addr,
                         found_client: bool):
        try:
            packet, _ = sender_socket.recvfrom(self.BUFF_SIZE)
        except socket.timeout:
            print("Timeout here")
            self.stop()
            return None
        except OSError:
            if not self.active:
                print("Timeout OS here")
                return None
            else:
                print("Something wrong")

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
        time.sleep(1)
        vid_sender_thread = Thread(target=self.find_video_sender)
        aud_sender_thread = Thread(target=self.find_audio_sender)
        self.sv_port_lock.acquire()
        self.sa_port_lock.acquire()
        vid_sender_thread.start()
        aud_sender_thread.start()

        vid_receiver_thread = Thread(target=self.find_video_receiver)
        aud_receiver_thread = Thread(target=self.find_audio_receiver)
        self.rv_port_lock.acquire()
        self.ra_port_lock.acquire()
        vid_receiver_thread.start()
        aud_receiver_thread.start()

    def stop(self):
        self.stop_lock.acquire()
        if self.active == True:
            self.active = False
            print("Stoppeds")
            self.sa_socket.close()
            self.ra_socket.close()
            self.sv_socket.close()
            self.rv_socket.close()
            self.sv_port_lock.release()
            self.sa_port_lock.release()
            self.ra_port_lock.release()
            self.rv_port_lock.release()
            self.server_lock.release()

        self.stop_lock.release()


if __name__ == "__main__":
    server_lock = Lock()
    sv_port_lock = Lock()
    rv_port_lock = Lock()
    sa_port_lock = Lock()
    ra_port_lock = Lock()

    while True:
        server = Server(server_lock, sv_port_lock, rv_port_lock, sa_port_lock, ra_port_lock)
        server.run()

