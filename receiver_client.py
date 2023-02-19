import base64
import threading
import time
import cv2
import socket

import numpy

BUFF_SIZE = 65536
client_c_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_c_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
host_name = socket.gethostname()
host_ip = '127.0.0.1'

port = 8888
client_addr = (host_ip, port)
WIDTH = 300

message = b'CLIENT_TYPE_R'
client_c_socket.sendto(message, client_addr)
client_c_socket.settimeout(300)
try:
    msg, server_t_addr = client_c_socket.recvfrom(BUFF_SIZE)
except TimeoutError or ConnectionResetError:
    print("No response from server. Is it running?")
    exit(1)
fps, st, frames_to_count, cnt = (0, 0, 20, 0)
dtype = numpy.uint8
title = 'RECEIVING VIDEO ' + str(threading.get_ident())
print('Waiting for video...')
while True:
    try:
        packet, _ = client_c_socket.recvfrom(BUFF_SIZE)
    except TimeoutError:
        cv2.destroyWindow(title)
        client_c_socket.close()
        break
    data = base64.b64decode(packet, ' /')
    npdata = numpy.frombuffer(data, dtype)
    frame = cv2.imdecode(npdata, 1)
    frame = cv2.putText(frame, 'FPS: ' + str(fps), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

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
