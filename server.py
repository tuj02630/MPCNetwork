# This is client code to receive video frames over UDP
import base64
import time
import numpy
import socket
import threading
import pyaudio
import winsound
# socket setup
BUFF_SIZE = 65536
host_ip = '44.212.17.188'
sv_port = 9999  # sender video port
sa_port = 9998  # sender audio port
rv_port = 8888  # receiver video port
ra_port = 8887  # receiver audio port
host_name = socket.gethostname()
rv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
sv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
sa_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sa_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
ra_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ra_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
dtype = numpy.uint8

# audio settings are unused but i figure it can't hurt to have them on the server
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
FRAMES_PER_BUFFER = 1000

# other variables
thread_array = []
found_rv_client = False
found_ra_client = False
rv_addr = ('', 0)
ra_addr = ('', 0)


def find_video_receiver():
    rv_socket.bind((host_ip, rv_port))
    print('Listening at:', (host_ip, rv_port))
    global rv_addr
    rc_msg, rv_addr = rv_socket.recvfrom(BUFF_SIZE)
    print('GOT connection from ', rv_addr, ', Client type is ', str(rc_msg))
    rv_socket.sendto(b'Confirmed', rv_addr)
    global found_rv_client
    found_rv_client = True
    return


def find_video_sender():
    sv_socket.bind((host_ip, sv_port))
    print('Listening at:', (host_ip, sv_port))
    msg, sv_addr = sv_socket.recvfrom(BUFF_SIZE)
    print('GOT connection from ', sv_addr, ', Client type is ', str(msg))
    sv_socket.sendto(b'Confirmed', sv_addr)
    fps, st, frames_to_count, cnt = (0, 0, 20, 0)
    while True:
        packet, _ = sv_socket.recvfrom(BUFF_SIZE)
        data = base64.b64decode(packet, ' /')
        npdata = numpy.frombuffer(data, dtype)  # the actual data if the server wants to do anything with it

        if found_rv_client:
            rv_socket.sendto(packet, rv_addr)

        if cnt == frames_to_count:
            # noinspection PyBroadException
            try:
                fps = round(frames_to_count / (time.time() - st))
                st = time.time()
                cnt = 0
            except:
                pass
        cnt += 1


def find_audio_sender():
    # initial socket setup
    sa_socket.bind((host_ip, sa_port))
    print('Listening at:', (host_ip, sa_port))
    msg, sa_addr = sa_socket.recvfrom(BUFF_SIZE)
    print('GOT connection from ', sa_addr, ', Client type is ', str(msg))
    sa_socket.sendto(b'Confirmed', sa_addr)
    sa_socket.settimeout(300)
    while True:
        try:
            packet, _ = sa_socket.recvfrom(BUFF_SIZE)
        except TimeoutError:
            sa_socket.close()
            break
        data = base64.b64decode(packet, ' /')
        if found_ra_client:
            ra_socket.sendto(packet, ra_addr)
        # print(data)
    return


def find_audio_receiver():
    ra_socket.bind((host_ip, ra_port))
    print('Listening at:', (host_ip, ra_port))
    global ra_addr
    msg, ra_addr = ra_socket.recvfrom(BUFF_SIZE)
    print('GOT connection from ', ra_addr, ', Client type is ', str(msg))
    global found_ra_client
    found_ra_client = True
    return


vid_sender_thread = threading.Thread(target=find_video_sender)
aud_sender_thread = threading.Thread(target=find_audio_sender)
vid_receiver_thread = threading.Thread(target=find_video_receiver)
aud_receiver_thread = threading.Thread(target=find_audio_receiver)

thread_array.append(vid_sender_thread)
thread_array.append(aud_sender_thread)
thread_array.append(vid_receiver_thread)
thread_array.append(aud_receiver_thread)

for thread in thread_array:
    thread.start()
    time.sleep(0.25)
