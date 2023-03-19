import os
import socket
import base64
import threading
import time

import cv2
import imutils
import pyaudio

thread_array = []

BUFF_SIZE = 65536
HOST = '44.212.17.188'  # The server's hostname or IP address
PORT = 9999  # The port used by the server
DEVICE_ID = "ABCDEFGH"

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
FRAMES_PER_BUFFER = 1000
WIDTH = 400

v_port = 9998
a_port = 9999

server_port = 0

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
print("hostname = " + hostname)
print("IP_Addr = " + IPAddr)

v_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
a_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
c_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
v_sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
a_sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
c_sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)


def video_sending_thread():
    """
        Thread for sending video to the server
        Parameters: None
        Returns: None
        Loops while getting video from device camera and sends that over UDP to the server
    """
    vid = cv2.VideoCapture(0)  # replace 'rocket.mp4' with 0 for webcam
    fps, st, frames_to_count, cnt = (0, 0, 20, 0)
    title = 'SENDING VIDEO ' + str(os.getpid())
    while True:
        while vid.isOpened():
            _, frame = vid.read()
            frame = imutils.resize(frame, WIDTH)
            encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            msg = base64.b64encode(buffer)
            v_sock.sendto(msg, (HOST, server_port))
            frame = cv2.putText(frame, 'FPS: ' + str(fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.imshow(title, frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                v_sock.close()
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


def audio_sending_thread():
    """
            Thread for sending audio to the server
            Parameters: None
            Returns: None
            Loops while getting audio from device microphone and sends that over UDP to the server
        """
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    while True:
        data = stream.read(FRAMES_PER_BUFFER)
        data = base64.b64encode(data)
        a_sock.sendto(data, (HOST, server_port+1))


message = "S" + DEVICE_ID
print("Sending initial message to " + str((HOST, PORT)))
c_sock.settimeout(15)
c_sock.sendto(bytes(message, 'utf-8'), (HOST, PORT))
response, addr = c_sock.recvfrom(BUFF_SIZE)
server_port = int(response.decode('utf-8'))
print("Received server port: "+str(server_port))
thread_array.append(threading.Thread(target=video_sending_thread))
thread_array.append(threading.Thread(target=audio_sending_thread))
for thread in thread_array:
    thread.start()


