import socket
import base64
import threading
import time
import cv2
import numpy
import pyaudio


class LiveStreamReceiverClient:
    """
    LiveStreamReceiverClients ask the server if there exists a DeviceConnection matching a provided Device ID.
    If one exists, the LiveStreamReceiver will begin receiving a live video and live audio feed.
    If one doesn't, the LiveStreamReceiver will wait for a packet from the server telling it that a matching Device ID
    has connected.
    """
    def __init__(self):
        self.thread_array = []
        """Array of threads"""
        self.BUFF_SIZE = 65536
        """Data buffer size for the video and audio stream"""
        self.HOST = '44.212.17.188'  # The server's hostname or IP address
        """IP for the server"""
        self.PORT = 9999  # The port used by the server
        """Port that is used by the server to listen for incoming connections"""
        self.DEVICE_ID = "ABCDEFGH"
        """The ID of the device this is running on"""
        self.CHUNK = 1024
        """Size of chunk for audio"""
        self.FORMAT = pyaudio.paInt16
        """Audio format"""
        self.CHANNELS = 2
        """Number of audio channels"""
        self.RATE = 44100
        """Audio sample rate"""
        self.FRAMES_PER_BUFFER = 1000
        """Number of frames per buffer for audio"""
        self.WIDTH = 400
        """Width of Window for imshow"""
        self.v_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        """Socket used for continuous video connection"""
        self.a_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        """Socket used for continuous audio connection"""
        self.c_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        """Socket used for initial connection setup"""

        self.connect()

    def connect(self):
        """
            Function starts the connection process with the server.
            Sends an initial packet asking the server for an open video and audio port
            The server will respond with a 5-digit port and the function will then start the livestream threads with the
            provided port numbers

            Parameters:
            None

            Returns:
            None
        """
        self.v_sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.BUFF_SIZE)
        self.a_sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.BUFF_SIZE)
        self.c_sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.BUFF_SIZE)
        message = "R" + self.DEVICE_ID
        print("Sending initial message to " + str((self.HOST, self.PORT)))
        self.c_sock.settimeout(15)
        self.c_sock.sendto(bytes(message, 'utf-8'), (self.HOST, self.PORT))
        response, addr = self.c_sock.recvfrom(self.BUFF_SIZE)
        port_args = int(response.decode('utf-8'))
        print("Received server port: " + str(port_args))
        time.sleep(0.5)
        self.thread_array.append(threading.Thread(target=self.video_receiving_thread, args=(port_args,)))
        self.thread_array.append(threading.Thread(target=self.audio_receiving_thread, args=(port_args+1,)))
        for thread in self.thread_array:
            thread.start()

    def video_receiving_thread(self, port):
        """
            Callback function to be executed in the video receiving thread
            and this function receives the video data from the server with loop
            and update the video image in a video frame

            Parameters:
            The open server video port provided

            Returns:
            None
        """
        self.v_sock.settimeout(300)
        print("v_sock: " + str(self.v_sock))
        self.v_sock.sendto(b'Vid_Init', (self.HOST, port))
        fps, st, frames_to_count, cnt = (0, 0, 20, 0)
        dtype = numpy.uint8
        title = 'RECEIVING VIDEO FROM ' + self.DEVICE_ID
        print('Waiting for video... Socket: ' + str(self.v_sock))
        while True:
            try:
                packet, _ = self.v_sock.recvfrom(self.BUFF_SIZE)
            except TimeoutError:
                cv2.destroyWindow(title)
                self.v_sock.close()
                break
            data = base64.b64decode(packet, ' /')
            npdata = numpy.frombuffer(data, dtype)
            frame = cv2.imdecode(npdata, 1)
            frame = cv2.putText(frame, 'FPS: ' + str(fps), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.imshow(title, frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                self.v_sock.close()
                break
            if cnt == frames_to_count:
                # noinspection PyBroadException
                try:
                    fps = round(frames_to_count / (time.time() - st))
                    st = time.time()
                    cnt = 0
                except:
                    pass
            cnt += 1

    def audio_receiving_thread(self, port):
        """
            Callback function to be executed in the audio receiving thread
            and this function receives the audio data from the server with loop and plays it as it receives.

            Parameters:
            The open server audio port provided

            Returns:
            None
        """
        self.a_sock.settimeout(300)
        self.a_sock.sendto(b'Aud_Init', (self.HOST, port))
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, output=True,
                        frames_per_buffer=self.CHUNK)
        while True:
            try:
                packet, _ = self.a_sock.recvfrom(self.BUFF_SIZE)
            except TimeoutError:
                self.a_sock.close()
                break
            data = base64.b64decode(packet, ' /')
            stream.write(data)


lsrc = LiveStreamReceiverClient()
