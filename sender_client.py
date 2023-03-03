import base64
import os
import time
import cv2
import imutils
import socket
import threading
import pyaudio

thread_array = []

# audio settings, might want to make a simple api for these later on
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
FRAMES_PER_BUFFER = 1000

BUFF_SIZE = 65536
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
vid_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
vid_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
aud_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
aud_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
host_name = socket.gethostname()
host_ip = '44.212.17.188'
host_ip = '127.0.0.1'
# host_ip = socket.gethostbyname("ec2-44-212-17-188.compute-1.amazonaws.com")
v_port = 50010
a_port = 50020
c_port = 9999
server_rv_addr = ("", 0)
server_ra_addr = ("", 0)
v_addr = (host_ip, v_port)
a_addr = (host_ip, a_port)
WIDTH = 400

device_id = ""


def rv_listen_thread():
    vid_socket.bind((host_ip, v_port))
    global server_rv_addr
    _, server_rv_addr = vid_socket.recvfrom(BUFF_SIZE)
    print("Video confirmation")
    return


def ra_listen_thread():
    aud_socket.bind((host_ip, a_port))
    global server_ra_addr
    _, server_ra_addr = aud_socket.recvfrom(BUFF_SIZE)
    print("Audio confirmation")
    return


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
        # print(data)
        data = base64.b64encode(data)
        aud_socket.sendto(data, server_ra_addr)


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
    vid_socket.settimeout(15)
    while True:
        while vid.isOpened():
            _, frame = vid.read()
            frame = imutils.resize(frame, WIDTH)
            encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            message = base64.b64encode(buffer)
            vid_socket.sendto(message, server_rv_addr)
            frame = cv2.putText(frame, 'FPS: ' + str(fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.imshow(title, frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                vid_socket.close()
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


thread_array = [threading.Thread(target=rv_listen_thread), threading.Thread(target=ra_listen_thread)]
for thread in thread_array:
    thread.start()
client_socket.sendto(b'Initial Connection', (host_ip, c_port))
for thread in thread_array:
    thread.join()
thread_array.clear()


vid_send_thread = threading.Thread(target=video_sending_thread)
aud_send_thread = threading.Thread(target=audio_sending_thread)
thread_array.append(vid_send_thread)
thread_array.append(aud_send_thread)
for thread in thread_array:
    thread.start()
