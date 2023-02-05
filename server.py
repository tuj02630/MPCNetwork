# This is client code to receive video frames over UDP
import base64
import time
import cv2
import numpy as np
import socket
import threading

BUFF_SIZE = 65536
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
host_name = socket.gethostname()
host_ip = '127.0.0.1'  # socket.gethostbyname(host_name)
print(host_ip)
port = 9999

# this should eventually go in a loop
socket_address = (host_ip, port)
server_socket.bind(socket_address)
print('Listening at:', socket_address)
fps, st, frames_to_count, cnt = (0, 0, 20, 0)
msg, client_addr = server_socket.recvfrom(BUFF_SIZE)
print('GOT connection from ', client_addr)
dtype = np.uint8
# this should eventually be a thread that's created for each connection
while True:
    packet, _ = server_socket.recvfrom(BUFF_SIZE)
    data = base64.b64decode(packet, ' /')
    npdata = np.frombuffer(data, dtype)
    frame = cv2.imdecode(npdata, 1)
    # frame = cv2.putText(frame, 'FPS: ' + str(fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.imshow("RECEIVING VIDEO", frame)
    cv2.setWindowTitle('RECEIVING VIDEO', 'RECEIVING VIDEO ' + str(fps))
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        server_socket.close()
        break
    if cnt == frames_to_count:
        try:
            fps = round(frames_to_count / (time.time() - st))
            st = time.time()
            cnt = 0
        except:
            pass
    cnt += 1
