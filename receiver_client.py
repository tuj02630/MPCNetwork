import base64
import threading
import time
import cv2
import socket
import numpy
import pyaudio

thread_array = []

BUFF_SIZE = 65536
vid_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
vid_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
aud_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
aud_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)

host_name = socket.gethostname()
host_ip = '44.212.17.188'
v_port = 8888
a_port = 8887
v_addr = (host_ip, v_port)
a_addr = (host_ip, a_port)

# audio settings, might want to make a simple api for these later on
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
FRAMES_PER_BUFFER = 1000


def audio_receiving_thread():
    message = b'CLIENT_TYPE_RA'
    aud_socket.sendto(message, a_addr)
    aud_socket.settimeout(300)
    try:
        msg, server_t_addr = vid_socket.recvfrom(BUFF_SIZE)
    except TimeoutError or ConnectionResetError:
        print("No response from server. Is it running?")
        exit(1)
    aud_socket.settimeout(300)
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
    while True:
        try:
            packet, _ = aud_socket.recvfrom(BUFF_SIZE)
        except TimeoutError:
            aud_socket.close()
            break
        data = base64.b64decode(packet, ' /')
        stream.write(data)


def video_receiving_thread():
    message = b'CLIENT_TYPE_RV'
    vid_socket.sendto(message, v_addr)
    vid_socket.settimeout(300)
    try:
        msg, server_t_addr = vid_socket.recvfrom(BUFF_SIZE)
    except TimeoutError or ConnectionResetError:
        print("No response from server. Is it running?")
        exit(1)
    fps, st, frames_to_count, cnt = (0, 0, 20, 0)
    dtype = numpy.uint8
    title = 'RECEIVING VIDEO ' + str(threading.get_ident())
    print('Waiting for video...')
    while True:
        try:
            packet, _ = vid_socket.recvfrom(BUFF_SIZE)
        except TimeoutError:
            cv2.destroyWindow(title)
            vid_socket.close()
            break
        data = base64.b64decode(packet, ' /')
        npdata = numpy.frombuffer(data, dtype)
        frame = cv2.imdecode(npdata, 1)
        frame = cv2.putText(frame, 'FPS: ' + str(fps), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
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


vid_receive_thread = threading.Thread(target=video_receiving_thread)
aud_receive_thread = threading.Thread(target=audio_receiving_thread)
thread_array.append(vid_receive_thread)
thread_array.append(aud_receive_thread)
for thread in thread_array:
    thread.start()
