# This is server code to send video frames over UDP
import base64
import threading
import time
import cv2
import imutils
import socket
import sys
import os

BUFF_SIZE = 65536
client_c_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_c_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
rv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
ra_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ra_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)

server_rv_addr = ("", 0)
server_ra_addr = ("", 0)

host_name = socket.gethostname()
host_ip = '127.0.0.1'  # socket.gethostbyname(host_name)
print(host_ip)
port = 9999
client_addr = (host_ip, port)
WIDTH = 300

rv_port = 50010
ra_port = 50020


def rv_listen_thread():
    rv_socket.bind((host_ip, rv_port))
    global server_rv_addr
    _, server_rv_addr = rv_socket.recvfrom(BUFF_SIZE)
    print("Video confirmation")
    return


def ra_listen_thread():
    ra_socket.bind((host_ip, ra_port))
    global server_ra_addr
    _, server_ra_addr = ra_socket.recvfrom(BUFF_SIZE)
    print("Audio confirmation")
    return


thread_array = [threading.Thread(target=rv_listen_thread), threading.Thread(target=ra_listen_thread)]
for thread in thread_array:
    thread.start()
client_c_socket.sendto(b'Initial Connection', client_addr)
for thread in thread_array:
    thread.join()
if len(sys.argv) <= 1:
    vid = cv2.VideoCapture(0)
else:
    vid = cv2.VideoCapture(os.getcwd() + "\\videos\\" + str(sys.argv[1]))
# replace 'rocket.mp4' with 0 for webcam
fps, st, frames_to_count, cnt = (0, 0, 20, 0)
title = 'SENDING VIDEO ' + str(os.getpid())

while True:
    while vid.isOpened():
        _, frame = vid.read()
        if not _:
            print("No more video, closing...")
            # cv2.destroyWindow(title)
            vid.release()
            client_c_socket.close()
            exit(0)
        frame = imutils.resize(frame, WIDTH)
        encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        message = base64.b64encode(buffer)
        client_c_socket.sendto(message, server_t_addr)
        # frame = cv2.putText(frame, 'FPS: ' + str(fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow(title, frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            client_c_socket.close()
            break
        if cnt == frames_to_count:
            try:
                fps = round(frames_to_count / (time.time() - st))
                st = time.time()
                cnt = 0
            except:
                pass
        cnt += 1
