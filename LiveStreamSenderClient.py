import os
import socket
import base64
import threading
import time
import cv2
import imutils
import pyaudio


class LiveStreamSenderClient:
    """
    LiveStreamSenderClients initialize a connection with the server and are the source of a livestream.
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
        message = "S" + self.DEVICE_ID
        print("Sending initial message to " + str((self.HOST, self.PORT)))
        self.c_sock.settimeout(300)
        self.c_sock.sendto(bytes(message, 'utf-8'), (self.HOST, self.PORT))
        response, addr = self.c_sock.recvfrom(self.BUFF_SIZE)
        port_args = int(response.decode('utf-8'))
        print("Received server port: " + str(port_args))
        self.thread_array.append(threading.Thread(target=self.video_sending_thread, args=(port_args,)))
        self.thread_array.append(threading.Thread(target=self.audio_sending_thread, args=(port_args+1,)))
        for thread in self.thread_array:
            thread.start()

    def video_sending_thread(self, port):
        """
            Thread for sending video to the server
            Parameters: Port: The open server video port provided
            Returns: None
            Loops while getting video from device camera and sends that over UDP to the server
        """
        vid = cv2.VideoCapture(0)  # replace 'rocket.mp4' with 0 for webcam
        fps, st, frames_to_count, cnt = (0, 0, 20, 0)
        title = 'SENDING VIDEO ' + str(os.getpid())
        while True:
            while vid.isOpened():
                _, frame = vid.read()
                frame = imutils.resize(frame, self.WIDTH)
                encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                msg = base64.b64encode(buffer)
                self.v_sock.sendto(msg, (self.HOST, port))
                frame = cv2.putText(frame, 'FPS: ' + str(fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
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

    def audio_sending_thread(self, port):
        """
                Thread for sending audio to the server
                Parameters: Port: The open server audio port provided
                Returns: None
                Loops while getting audio from device microphone and sends that over UDP to the server
            """
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True,
                        frames_per_buffer=self.CHUNK)
        while True:
            data = stream.read(self.FRAMES_PER_BUFFER, exception_on_overflow=False)
            data = base64.b64encode(data)
            self.a_sock.sendto(data, (self.HOST, port))


lssc = LiveStreamSenderClient()
