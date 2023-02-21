import base64
import time
import cv2
import imutils
import socket
import threading
import pyaudio

thread_array = []

# audio settings
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
FRAMES_PER_BUFFER = 1000

BUFF_SIZE = 65536
vid_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
vid_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
aud_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
aud_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
host_name = socket.gethostname()
host_ip = '44.212.17.188'
# host_ip = socket.gethostbyname("ec2-44-212-17-188.compute-1.amazonaws.com")
v_port = 9999
a_port = 9998
v_addr = (host_ip, v_port)
a_addr = (host_ip, a_port)
WIDTH = 400


def audio_sending_thread():
    aud_socket.sendto(b'CLIENT_TYPE_SA', a_addr)
    try:
        aud_socket.recvfrom(BUFF_SIZE)
    except TimeoutError or ConnectionResetError:
        print("No response from server. Is it running?")
        exit(1)
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    while True:
        data = stream.read(FRAMES_PER_BUFFER)
        print(data)
        data = base64.b64encode(data)
        aud_socket.sendto(data, a_addr)


def video_sending_thread():
    vid = cv2.VideoCapture(0)  # replace 'rocket.mp4' with 0 for webcam
    fps, st, frames_to_count, cnt = (0, 0, 20, 0)

    vid_socket.settimeout(15)
    vid_socket.sendto(b'CLIENT_TYPE_SV', v_addr)
    try:
        vid_socket.recvfrom(BUFF_SIZE)
    except TimeoutError or ConnectionResetError:
        print("No response from server. Is it running?")
        exit(1)
    while True:
        while vid.isOpened():
            _, frame = vid.read()
            frame = imutils.resize(frame, WIDTH)
            encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            message = base64.b64encode(buffer)
            vid_socket.sendto(message, v_addr)
            frame = cv2.putText(frame, 'FPS: ' + str(fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.imshow('TRANSMITTING VIDEO', frame)
            cv2.setWindowTitle('TRANSMITTING VIDEO', 'TRANSMITTING VIDEO ' + str(fps))
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


vid_send_thread = threading.Thread(target=video_sending_thread)
aud_send_thread = threading.Thread(target=audio_sending_thread)
thread_array.append(vid_send_thread)
thread_array.append(aud_send_thread)
for thread in thread_array:
    thread.start()
