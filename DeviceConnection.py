import socket
import threading


class DeviceConnection:
    """
    A DeviceConnection is created for each sender client
    DeviceConnections maintain existing sender connections and are responsible for routing packets from a sender to zero or more receivers
    """

    def __init__(self, s_addr: tuple, device_id: str, curr_port: int):
        self.BUFF_SIZE = 65536
        """Data buffer size for the video and audio stream"""
        self.HOST = '172.31.12.186'
        """Private ip for the server"""
        self.DEBUG = False
        """Debugging backend option"""
        self.device_id = device_id
        """String containing sending device's ID"""
        self.s_addr = s_addr
        """Tuple containing the IP and Port of the sending device"""
        self.curr_port = curr_port  # video port, audio port is + 1
        """Tuple containing the IP and Port of the sending device"""
        self.v_socket_array: tuple = []
        """Array of IP/Port Tuples to send video to"""
        self.a_socket_array: tuple = []
        """Array of IP/Port Tuples to send audio to"""
        self.v_receiver_array: socket.socket = []  #
        """Array of sockets to send video data to the respective v_socket_array address"""
        self.a_receiver_array: socket.socket = []  #
        """Array of sockets to send audio data to the respective a_socket_array address"""
        self.sv_socket: socket.socket = None
        """Socket for receiving video from sender"""
        self.sa_socket: socket.socket = None
        """Socket for receiving audio from sender"""
        self.sv_addr: tuple = ('', 0)
        """Tuple for storing address of video sender"""
        self.sa_addr: tuple = ('', 0)
        """Tuple for storing address of audio sender"""
        self.shutoff = False
        """Boolean to shut off threads"""
        self.vid_thread: threading.Thread
        """Thread for handling video packets"""
        self.aud_thread: threading.Thread
        """Thread for handling audio packets"""
        print("\t\tCreated new DeviceConnection with Device ID: " + self.device_id + " and address: " + str(self.s_addr))
        self.vid_thread = threading.Thread(target=self.video_sending_handler)
        self.aud_thread = threading.Thread(target=self.audio_sending_handler)
        self.vid_thread.start()
        self.aud_thread.start()

    def video_sending_handler(self):
        """
            Function for handling a video sender's packets and routing them to video receievers

            Parameters:
            None

            Returns:
            None
        """
        self.sv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.BUFF_SIZE)
        # self.sv_socket.bind((local_ip, self.curr_port))

        # start connection
        self.sv_socket.bind((self.HOST, self.curr_port))
        while True:
            if self.shutoff:
                return
            packet, self.sv_addr = self.sv_socket.recvfrom(self.BUFF_SIZE)
            # print("Packet length: " + str(len(packet)))
            if self.DEBUG:
                print("\nReceiving Video: " + str(packet))
            # send packet to all rv ips here
            i = 0
            for sock in self.v_receiver_array:
                # print("SENDING PACKET IN SOCKET: " + str(sock) + ", TO " + str(self.v_socket_array[i]))
                sock.sendto(packet, (self.v_socket_array[i]))
                i += 1

    def audio_sending_handler(self):
        """
            Function for handling an audio sender's packets and routing them to audio receievers

            Parameters:
            None

            Returns:
            None
        """
        self.sa_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sa_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.BUFF_SIZE)
        # start connection
        self.sa_socket.bind((self.HOST, self.curr_port + 1))

        while True:
            if self.shutoff:
                return
            packet, self.sa_addr = self.sa_socket.recvfrom(self.BUFF_SIZE)
            # send packet to all ra ips here
            i = 0
            for sock in self.a_receiver_array:
                # print("sending packet to " + str(self.a_socket_array[i]))
                sock.sendto(packet, self.a_socket_array[i])
                i += 1

    def add_receiver(self, ip: str, port: int):
        """
            Function for adding a receiver to an existing DeviceConnection

            Parameters:
            ip: Target receiver's IP address in string format
            port: Target receiver's port as an integer


            Returns:
            None
        """
        print("\tOpening two new sockets with ports: " + str(port) + " and " + str(port + 1))
        rv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        rv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.BUFF_SIZE)
        rv_socket.bind((self.HOST, port))
        ra_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ra_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.BUFF_SIZE)
        ra_socket.bind((self.HOST, (port + 1)))
        threading.Thread(target=self.start_v_receiver_socket, args=(rv_socket,)).start()
        threading.Thread(target=self.start_a_receiver_socket, args=(ra_socket,)).start()

    def start_v_receiver_socket(self, v_socket: socket.socket):
        """
            Helper function for add_receiver, waits for a receiver to send a packet to confirm starting the video connection

            Parameters:
            v_socket: The socket to listen for the receiver's packet on


            Returns:
            None
        """
        data, addr = v_socket.recvfrom(self.BUFF_SIZE)
        print("Socket: " + str(v_socket.getsockname()) + " received message: " + data.decode('utf-8'))
        self.v_socket_array.append(addr)
        self.v_receiver_array.append(v_socket)
        # print("There are now " + str(len(self.v_socket_array)) + " addresses in the socket array")
        return

    def start_a_receiver_socket(self, a_socket: socket.socket):
        """
            Helper function for add_receiver, waits for a receiver to send a packet to confirm starting the audio connection

            Parameters:
            a_socket: The socket to listen for the receiver's packet on


            Returns:
            None
        """
        data, addr = a_socket.recvfrom(self.BUFF_SIZE)
        print("Socket: " + str(a_socket.getsockname()) + " received message: " + data.decode('utf-8'))
        self.a_socket_array.append(addr)
        self.a_receiver_array.append(a_socket)
        return

    def get_device_id(self):
        """
            Simple getter for device_id

            Parameters:
            None

            Returns:
            device_id: string
        """
        return self.device_id

    def reroute(self, s_addr: tuple):
        """
            A function for changing an existing DeviceConnection's sender fields to a new sender without interrupting the connection for receivers

            Parameters:
            s_addr: The new address to receive packets from

            Returns:
            None
        """
        print("\t" + self.device_id + ": Shutting down threads...")
        self.shutoff = True
        self.vid_thread.join()
        self.aud_thread.join()
        self.sv_socket.close()
        self.sa_socket.close()
        print("\t" + self.device_id + ": Threads have been shut down. Restarting...")
        self.s_addr = s_addr
        self.vid_thread = threading.Thread(target=self.video_sending_handler)
        self.aud_thread = threading.Thread(target=self.audio_sending_handler)
        self.vid_thread.start()
        self.aud_thread.start()

    def get_curr_port(self):
        return self.curr_port

    def destroy(self):
        """
            A function for killing a DeviceConnection object.

            Parameters:
            None

            Returns:
            None
        """
        self.shutoff = True
        self.vid_thread.join()
        self.vid_thread.join()
        self.sv_socket.close()
        self.sa_socket.close()
        for sock in self.v_receiver_array:
            sock.close()
        for sock in self.a_receiver_array:
            sock.close()
