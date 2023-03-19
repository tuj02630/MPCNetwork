import os
import socket
import base64
import threading
import time

import cv2
import numpy
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

v_port = 9998+2
a_port = 9999+2

v_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
a_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
v_sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
a_sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
c_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
c_sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)

server_port: int


def video_receiving_thread():
    """
        Callback function to be executed in the video receiving thread
        and this function receives the video data from the server with loop
        and update the video image in a video frame

        Parameters:
        None

        Returns:
        None
    """
    v_sock.settimeout(300)
    print("v_sock: " + str(v_sock))
    v_sock.sendto(b'Vid_Init', (HOST, server_port))
    fps, st, frames_to_count, cnt = (0, 0, 20, 0)
    dtype = numpy.uint8
    title = 'RECEIVING VIDEO ' + str(os.getpid())
    print('Waiting for video... Socket: ' + str(v_sock))
    while True:
        try:
            packet, _ = v_sock.recvfrom(BUFF_SIZE)
        except TimeoutError:
            cv2.destroyWindow(title)
            v_sock.close()
            break
        data = base64.b64decode(packet, ' /')
        npdata = numpy.frombuffer(data, dtype)
        frame = cv2.imdecode(npdata, 1)
        frame = cv2.putText(frame, 'FPS: ' + str(fps), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
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


def audio_receiving_thread():
    """
        Callback function to be executed in the audio receiving thread
        and this function receives the audio data from the server with loop and plays it as it receives.

        Parameters:
        None

        Returns:
        None
    """
    a_sock.settimeout(300)
    a_sock.sendto(b'Aud_Init', (HOST, server_port + 1))
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True,
                    frames_per_buffer=CHUNK)
    while True:
        try:
            packet, _ = a_sock.recvfrom(BUFF_SIZE)
        except TimeoutError:
            a_sock.close()
            break
        data = base64.b64decode(packet, ' /')
        stream.write(data)


message = "R" + DEVICE_ID
print("Sending initial message to " + str((HOST, PORT)))
c_sock.settimeout(15)
c_sock.sendto(bytes(message, 'utf-8'), (HOST, PORT))
response, addr = c_sock.recvfrom(BUFF_SIZE)
server_port = int(response.decode('utf-8'))
print("Received server port: " + str(server_port))
time.sleep(0.5)
thread_array.append(threading.Thread(target=video_receiving_thread))
thread_array.append(threading.Thread(target=audio_receiving_thread))
for thread in thread_array:
    thread.start()
