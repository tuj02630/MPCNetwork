import base64
import time
import cv2
import numpy
import socket
import threading

threads = list()


def thread_receive(*thread_receive_args):
    c_ip, c_port, name = thread_receive_args
    client_address = (c_ip, c_port)
    print("Thread initialized with client_addr = " + str(client_address))
    server_t_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_t_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
    message = b'Hi'
    server_t_socket.sendto(message, client_address)
    fps, st, frames_to_count, cnt = (0, 0, 20, 0)
    title = 'RECEIVING VIDEO ' + str(threading.get_ident())
    server_t_socket.settimeout(15)
    while True:
        try:
            packet, _ = server_t_socket.recvfrom(BUFF_SIZE)
        except TimeoutError:
            cv2.destroyWindow(title)
            server_t_socket.close()
            break
        data = base64.b64decode(packet, ' /')
        npdata = numpy.frombuffer(data, dtype)
        frame = cv2.imdecode(npdata, 1)
        frame = cv2.putText(frame, 'FPS: ' + str(fps), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow(title, frame)
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


BUFF_SIZE = 65536
dtype = numpy.uint8

# server_socket listens for incoming connections
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)

host_name = socket.gethostname()
host_ip = '127.0.0.1'  # socket.gethostbyname(host_name)
print(host_ip)
port = 9999

socket_address = (host_ip, port)
server_socket.bind(socket_address)
print('Listening at:', socket_address)
while True:
    msg, client_addr = server_socket.recvfrom(BUFF_SIZE)
    (client_ip, client_port) = client_addr
    rec_args = (client_ip, client_port, len(threads))
    print('Got connection from ', client_addr)
    curr_thread_receive = threading.Thread(target=thread_receive, args=rec_args)
    threads.append(curr_thread_receive)
    curr_thread_receive.start()
