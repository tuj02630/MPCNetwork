import base64
import os
import threading
import time
import cv2
import socket
import numpy
import pyaudio


class ReceiverClient:
    def __init__(self):
        self.thread_array = []

        self.BUFF_SIZE = 65536
        self.vid_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.vid_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.BUFF_SIZE)
        self.aud_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.aud_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.BUFF_SIZE)

        self.host_name = socket.gethostname()
        self.host_ip = '44.212.17.188'
        # host_ip = '127.0.0.1'

        self.v_port = 8888
        self.a_port = 8887
        self.v_addr = (self.host_ip, self.v_port)
        self.a_addr = (self.host_ip, self.a_port)

        # audio settings, might want to make a simple api for these later on
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        self.FRAMES_PER_BUFFER = 1000


    def audio_receiving_thread(self):
        message = b'CLIENT_TYPE_RA'
        self.aud_socket.sendto(message, self.a_addr)
        self.aud_socket.settimeout(300)
        try:
            msg, server_t_addr = self.vid_socket.recvfrom(self.BUFF_SIZE)
        except TimeoutError or ConnectionResetError:
            print("No response from server. Is it running?")
            exit(1)
        self.aud_socket.settimeout(300)
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, output=True, frames_per_buffer=self.CHUNK)
        while True:
            try:
                packet, _ = self.aud_socket.recvfrom(self.BUFF_SIZE)
            except TimeoutError:
                self.aud_socket.close()
                break
            data = base64.b64decode(packet, ' /')
            stream.write(data)


    def video_receiving_thread(self):
        message = b'CLIENT_TYPE_RV'
        self.vid_socket.sendto(message, self.v_addr)
        self.vid_socket.settimeout(300)
        try:
            msg, server_t_addr = self.vid_socket.recvfrom(self.BUFF_SIZE)
        except TimeoutError or ConnectionResetError:
            print("No response from server. Is it running?")
            exit(1)
        fps, st, frames_to_count, cnt = (0, 0, 20, 0)
        dtype = numpy.uint8
        title = 'RECEIVING VIDEO ' + str(os.getpid())
        print('Waiting for video...')
        while True:
            try:
                packet, _ = self.vid_socket.recvfrom(self.BUFF_SIZE)
            except TimeoutError:
                cv2.destroyWindow(title)
                self.vid_socket.close()
                break
            data = base64.b64decode(packet, ' /')
            npdata = numpy.frombuffer(data, dtype)
            frame = cv2.imdecode(npdata, 1)
            frame = cv2.putText(frame, 'FPS: ' + str(fps), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
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
        vid_receive_thread = threading.Thread(target=self.video_receiving_thread)
        aud_receive_thread = threading.Thread(target=self.audio_receiving_thread)
        self.thread_array.append(vid_receive_thread)
        self.thread_array.append(aud_receive_thread)
        for thread in self.thread_array:
            thread.start()

if __name__ == "__main__":
    client = ReceiverClient()
    client.run()