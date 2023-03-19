import socket

BUFF_SIZE = 65536


class ReceiverSocket:
    rv_socket: socket.socket
    ra_socket: socket.socket

    def __init__(self, rv: tuple, ra: tuple):
        self.rv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
        self.ra_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ra_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
        self.rv_socket.bind(rv)
        self.ra_socket.bind(ra)

    def get_rv(self):
        return self.rv_socket

    def get_ra(self):
        return self.ra_socket
