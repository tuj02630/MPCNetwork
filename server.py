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

        self.BUFF_SIZE = 65536
        """Data buffer size for the video and audio stream"""

        self.host_ip = '172.31.12.186'
        """Private ip for the server"""
        # self.host_ip = '127.0.0.1'

        self.sv_port = 9999  # sender video port
        """Port that is used to send video data"""

        self.sa_port = 9998  # sender audio port
        """Port that is used to send audio data"""

        self.rv_port = 8888  # receiver video port
        """Port that is used to receive video data"""

        self.ra_port = 8887  # receiver audio port
        """Port that is used to receive audio data"""
        self.host_name = socket.gethostname()
        # S: Sending
        # R: Receiving
        # V: Video
        # A: Audio

        self.rv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        """Video socket to receive video data from the server"""
        self.rv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.BUFF_SIZE)

        self.sv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        """Video socket to send video data from the server"""
        self.sv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.BUFF_SIZE)

        self.sa_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        """Audio socket to send audio data from the server"""
        self.sa_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.BUFF_SIZE)

        self.ra_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        """Audio socket to receive audio data from the server"""
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
        """Thread list to store video and audio thread"""

        self.found_rv_client = False
        """Flag for if the video receiver client found. If true, the server will send the data to the client"""
        self.found_ra_client = False
        """Flag for if the audio receiver client found. If true, the server will send the data to the client"""
        self.rv_addr = ('', 0)
        """Client address for video receiver. The video data will be sent to this address"""

        self.ra_addr = ('', 0)
        """Client address for audio receiver. The audio data will be sent to this address"""

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
        """
            The function tries to find the receiver clients that is accessing the video receiver port.
            The function will run in the thread and act as callback function.
            Once connection is secured with receiver client, the video feed from the sender client will be passed to the receiver client

            Parameters:
            None

            Returns:
            None
        """
        self.rv_socket.bind((self.host_ip, self.rv_port))
        print('Listening at:', (self.host_ip, self.rv_port))
        rc_msg, self.rv_addr = self.rv_socket.recvfrom(self.BUFF_SIZE)
        print('GOT connection from ', self.rv_addr, ', Client type is ', str(rc_msg))
        self.rv_socket.sendto(b'Confirmed', self.rv_addr)
        self.found_rv_client = True
        return

    def find_audio_receiver(self):
        """
            The function tries to find the receiver clients that is accessing the audio receiver port.
            The function will run in the thread and act as callback function.
            Once connection is secured with receiver client, the audio feed from the sender client will be passed to the receiver client

            Parameters:
            None

            Returns:
            None
        """
        self.ra_socket.bind((self.host_ip, self.ra_port))
        print('Listening at:', (self.host_ip, self.ra_port))
        msg, self.ra_addr = self.ra_socket.recvfrom(self.BUFF_SIZE)
        print('GOT connection from ', self.ra_addr, ', Client type is ', str(msg))
        self.found_ra_client = True
        return

    def sender_setup(self, socket: socket.socket, port: int):
        """
            Set-up method for the sender client connection. The method will set timeout as 500 seconds
            and the thread will wait for the connection

            Parameters:

            socket: socket.socket -> socket for the sender thread. Socket will be bind to the given port

            port: int -> port number that is used to establish the connection.

            Returns:

            tuple of message and address -> Message from the client for the successful connection
            and address that is used to send video data
        """
        socket.settimeout(500)
        socket.bind((self.host_ip, port))
        print('Listening at:', (self.host_ip, port))
        msg, addr = socket.recvfrom(self.BUFF_SIZE)
        print('GOT connection from ', addr, ', Client type is ', str(msg))
        socket.sendto(b'Confirmed', addr)
        socket.settimeout(0.5)
        return (msg, addr)

    def sender_operation(self, sender_socket: socket.socket, receiver_socket: socket.socket, addr,
                         found_client: bool):
        """
            Method used to operate the live stream feature. The method only updates the video for a frame
            so it should be run in a loop to continuously update the live stream video.
            The method receives the data from the sender client and sends the data to the receiver client
            to simulate the live stream feature.

            Parameters:

            sender_socket: socket.socket -> Socket for the sender client, which sends the data to server

            receiver_socket: socket.socket -> Socket for the receiver client, which the server sends the data to

            port: int -> port number that is used to establish the connection.

            addr: String -> Address to send the data.
            Returns:

            found_client: bool -> True if the receiver client is found and ready to send data to it.

            data: numarray[] -> data that is sent to the receiver in the operation.
            Data is returned to be analyzed later.
        """
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
        """
            The function tries to find the video sender clients that is accessing the video sender port.
            The function will run in the thread and act as callback function.
            Once the video sender is found, the server receives the video data and sends it to the receiver client if it is found

            Parameters:
            None

            Returns:
            None
        """

        msg, self.sv_addr = self.sender_setup(self.sv_socket, self.sv_port)
        fps, st, frames_to_count, cnt = (0, 0, 20, 0)
        while True:
            data = self.sender_operation(self.sv_socket, self.rv_socket, self.rv_addr,
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
        """
            The function tries to find the audio sender clients that is accessing the audio sender port.
            The function will run in the thread and act as callback function.
            Once the audio sender is found, the server receives the audio data and sends it to the receiver client if it is found

            Parameters:
            None

            Returns:
            None
        """
        msg, self.sa_addr = self.sender_setup(self.sa_socket, self.sa_port)
        while True:
            data = self.sender_operation(self.sa_port_lock, self.sa_socket, self.ra_socket, self.ra_addr,
                                         self.found_ra_client)
            if data is None:
                return

    def run(self):
        """
            Method to start the server class. The method will start multiple threads that are needed for the server operations.

            Parameters:
            None

            Returns:
            None
        """
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
        """
            Stops the server instance and release all of locks

            Parameters:
            None

            Returns:
            None
        """
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

