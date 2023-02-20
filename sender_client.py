# This is server code to send video frames over UDP
import base64
import time
import cv2
import imutils
import socket

BUFF_SIZE = 65536
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
host_name = socket.gethostname()
host_ip = '44.212.17.188'
# host_ip = '127.0.0.1'
# host_ip = socket.gethostbyname("ec2-44-212-17-188.compute-1.amazonaws.com")
port = 9999
client_addr = (host_ip, port)
WIDTH = 400

vid = cv2.VideoCapture(0)  # replace 'rocket.mp4' with 0 for webcam
fps, st, frames_to_count, cnt = (0, 0, 20, 0)

client_socket.settimeout(15)
client_socket.sendto(b'CLIENT_TYPE_S', (host_ip, port))
try:
    client_socket.recvfrom(BUFF_SIZE)
except TimeoutError or ConnectionResetError:
    print("No response from server. Is it running?")
    exit(1)

while True:
    while vid.isOpened():
        _, frame = vid.read()
        frame = imutils.resize(frame, WIDTH)
        encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        message = base64.b64encode(buffer)
        client_socket.sendto(message, client_addr)
        # frame = cv2.putText(frame, 'FPS: ' + str(fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow('TRANSMITTING VIDEO', frame)
        cv2.setWindowTitle('TRANSMITTING VIDEO', 'TRANSMITTING VIDEO ' + str(fps))
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            client_socket.close()
            break
        if cnt == frames_to_count:
            try:
                fps = round(frames_to_count / (time.time() - st))
                st = time.time()
                cnt = 0
            except:
                pass
        cnt += 1
