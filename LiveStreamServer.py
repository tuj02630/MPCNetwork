import socket
import threading
import DeviceConnection


class LiveStreamServer:
    """
    Server class that will be running in server and manages the connection from clients
    """

    def __init__(self, port):
        self.BUFF_SIZE = 65536
        """Data buffer size for the video and audio stream"""
        self.HOST = '172.31.12.186'  # Private server IP
        """Private ip for the server"""
        self.PORT = port
        """Port that is used to listen for incoming connections"""
        self.thread_array = []
        """Array of threads"""
        self.device_connection_array = []
        """Array of DeviceConnection Objects"""
        self.receiver_backlog = []
        """Array of Receivers waiting for DeviceConnection Objects"""

        self.thread_array.append(threading.Thread(target=self.listen_for_incoming_connection))
        for thread in self.thread_array:
            thread.start()

    def listen_for_incoming_connection(self):
        """
            The function tries to find both sender and receiver clients.
            The function will run in the thread and act as callback function.
            When a sender connects, a new DeviceConnection with the Sender's Device ID will be created.
            When a receiver connects, the DeviceConnection matching the receiver's requested Device ID will be given the receiver's address and begin sending packets to the receiver.

            Parameters:
            None

            Returns:
            None
        """
        curr_port = 49152
        print("sender listener thread started")
        connection_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        connection_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.BUFF_SIZE)
        connection_socket.bind((self.HOST, self.PORT))
        while True:
            print('Listening at:', (self.HOST, self.PORT))
            data, addr = connection_socket.recvfrom(self.BUFF_SIZE)
            data = data.decode('utf-8')
            print('GOT connection from ', addr)
            print('\t\tClient type is: ' + data[0])
            print('\t\tDevice ID is: ' + data[1:])
            curr_dc: DeviceConnection.DeviceConnection
            if data[0] == 'S':
                print("checking device connection array for sender...")
                found = False
                for dc in self.device_connection_array:
                    if dc.get_device_id() == data[1:]:
                        print("\tmatch found!")
                        found = True
                        print("\tRerouting old DeviceConnection with ID: " + str(dc.get_device_id()))
                        dc.reroute(addr)
                        connection_socket.sendto(bytes(str(dc.get_curr_port()), 'utf-8'), addr)
                        break
                if not found:
                    curr_dc = DeviceConnection.DeviceConnection(addr, data[1:], curr_port)
                    self.device_connection_array.append(curr_dc)
                    connection_socket.sendto(bytes(str(curr_port), 'utf-8'), addr)
                    for receiver in self.receiver_backlog:
                        if receiver[0] == data[1:]:
                            curr_port += 2
                            curr_dc.add_receiver(receiver[1], curr_port)
                            print("\t\tSending packet to: " + str(addr))
                            connection_socket.sendto(bytes(str(curr_port), 'utf-8'), receiver[1])
                            self.receiver_backlog.remove(receiver)
                    curr_port += 2
            elif data[0] == 'R':
                found = False
                print("checking device connection array for sender...")
                for dc in self.device_connection_array:
                    if dc.get_device_id() == data[1:]:
                        found = True
                        print("\tmatch found!")
                        dc.add_receiver(addr[0], curr_port)
                        print("\t\tSending packet to: " + str(addr))
                        connection_socket.sendto(bytes(str(curr_port), 'utf-8'), addr)
                        curr_port += 2
                        break
                if not found:
                    print("\tDevice ID not found. Adding to waitlist...")
                    connection_socket.sendto(b'CWAIT', addr)
                    self.receiver_backlog.append((data[1:], addr))
            else:
                print("Data: " + data)
                print(
                    "Unrecognized connection attempt. Format should be '[DEVICE_TYPE_CHAR][DEVICE_ID] encoded in utf-8'")

# lss = LiveStreamServer(9999)
