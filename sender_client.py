import base64
import os
import time
import cv2
import imutils
import socket
import threading
import pyaudio

class SenderClient:
    """Reference for Sender Client, the network script in the camera. Used to send video and audio to the server"""

    def __init__(self):
        self.thread_array = []
        """Thread list to store video and audio thread"""
        # audio settings, might want to make a simple api for these later on
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        self.FRAMES_PER_BUFFER = 1000

        self.BUFF_SIZE = 6553
        """Data buffer size for the video and audio stream"""

        self.vid_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.vid_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.BUFF_SIZE)
        """Video socket to send video data from the server"""

        self.aud_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.aud_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.BUFF_SIZE)
        """Audio socket to send audio data from the server"""

        self.host_name = socket.gethostname()
        """Server host name"""

        self.host_ip = '44.212.17.188'
        """Server ip"""

        # self.host_ip = '127.0.0.1'
        # self.host_ip = socket.gethostbyname("ec2-44-212-17-188.compute-1.amazonaws.com")
        self.v_port = 9999
        """Server port for video stream"""

        self.a_port = 9998
        """Server port for audio stream"""

        self.v_addr = (self.host_ip, self.v_port)
        """Server address for video stream"""

        self.a_addr = (self.host_ip, self.a_port)
        """Server address for audio stream"""

        self.WIDTH = 400

    def audio_sending_thread(self):
        """
            Thread for sending audio to the server
            Parameters: None
            Returns: None
            Loops while getting audio from device microphone and sends that over UDP to the server
        """
        self.aud_socket.sendto(b'CLIENT_TYPE_SA', self.a_addr)
        try:
            self.aud_socket.recvfrom(self.BUFF_SIZE)
        except TimeoutError or ConnectionResetError:
            print("No response from server. Is it running?")
            exit(1)
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True,
                        frames_per_buffer=self.CHUNK)
        while True:
            data = stream.read(self.FRAMES_PER_BUFFER)
            # print(data)
            data = base64.b64encode(data)
            self.aud_socket.sendto(data, self.a_addr)

    def video_sending_thread(self):
        """
            Thread for sending video to the server
            Parameters: None
            Returns: None
            Loops while getting video from device camera and sends that over UDP to the server
        """
        vid = cv2.VideoCapture(0)  # replace 'rocket.mp4' with 0 for webcam
        fps, st, frames_to_count, cnt = (0, 0, 20, 0)
        title = 'SENDING VIDEO ' + str(os.getpid())
        self.vid_socket.settimeout(15)
        self.vid_socket.sendto(b'CLIENT_TYPE_SV', self.v_addr)
        try:
            self.vid_socket.recvfrom(self.BUFF_SIZE)
        except TimeoutError or ConnectionResetError:
            print("No response from server. Is it running?")
            exit(1)
        while True:
            while vid.isOpened():
                _, frame = vid.read()
                frame = imutils.resize(frame, self.WIDTH)
                encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                message = base64.b64encode(buffer)
                self.vid_socket.sendto(message, self.v_addr)
                frame = cv2.putText(frame, 'FPS: ' + str(fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.imshow(title, frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    self.vid_socket.close()
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

    def run(self):
        """
           Inherited from Thread
           Parameters:
           None
           Returns:
           None
       """
        vid_send_thread = threading.Thread(target=self.video_sending_thread)
        aud_send_thread = threading.Thread(target=self.audio_sending_thread)
        self.thread_array.append(vid_send_thread)
        # self.thread_array.append(aud_send_thread)
        for thread in self.thread_array:
            thread.start()


if __name__ == "__main__":
    client = SenderClient()
    client.run()
