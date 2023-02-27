import mysql.connector


class MPCDatabase:
    def __init__(self):
        """Reference for my sql instance. Used to perform query in database"""
        self.connection = mysql.connector.connect(host='mpcdb.c7s8y7an5gv1.us-east-1.rds.amazonaws.com',
                                                          user='nick',
                                                          password='uJ8nqdEYTRdnIC339wHF',
                                                          database='mpcdb')
        with self.connection:
            with self.connection.cursor() as cursor:
                print("Connection")
            self.connection.commit()
        cursor.close()


    def query(self, script):
        """
            Perform query in database

            Parameters:
            script: String -> sql script to be executed

            Returns:
            Lis of dictionary representing the result of the execution of sql script given
        """
        return

    def insert_customer(self, name, address, city, state, age, username, password):
        """
            Insert a record of customer to database

            Parameters:

            name: String -> Name of customer

            address: String -> Address of customer

            city: String -> City that customer lives in

            state: String -> State that customer lives in

            age: Int -> Age of customer

            username: String -> Username that customer defined

            password: String -> User defined password

            Returns:
            None
        """
        return

    def getCustomers(self):
        """
            Execute query to get the list of customers

            Parameters:
            None

            Returns:
            Lis of dictionary representing list of customers
        """
        return

    def getCustomerById(self, id):
        """
            Execute query to get the customer information related to the given id

            Parameters:

            id: int -> Id of customer

            Returns:
            Dict contains the customer information
        """
        return

    def registerHardware(self, customer_id, is_camera=True, is_thermal=False, price=0):
        """
            Execute query to register new hardware

            Parameters:

            customer_id: int -> Id of customer related to the hardware

            is_camera: bool -> True for if the device is camera

            is_thermal: bool -> True for if the device is thermal camera

            price: int -> optional field to store the price of the device.

            Returns:
            None
        """
        return

    def addRecording(self, customer_id, hardware_id, file_name, is_video, file_size, resolution, date, time):
        """
            Add recoding record to the database

            Parameters:

            customer_id: int -> Id of customer related to the recording

            hardware_id: int -> Id of hardware used to take the recording

            file_name: String -> Name of video file

            is_video: bool -> True if video, False if not such as picture

            file_size: int -> size of video file

            resolution: int -> resolution of video

            date: date -> date that video is taken

            time: time -> Time that video is taken

            Returns:
            None
        """

    def saveVideo(self, customer_id, hardware_id, data, date, time):
        """
            Save video in the computer and add recoding record to the database

            Parameters:

            customer_id: int -> Id of customer related to the recording

            hardware_id: int -> Id of hardware used to take the recording

            data: byte[] -> Video data

            file_name: String -> Name of video file

            date: date -> date that video is taken

            time: time -> Time that video is taken

            Returns:
            None
        """

    def getRecordingsByCustomerID(self, id):
        """
            Retrieve the list of videos saved in the cloud related to the customer id

            Parameters:

            customer_id: int -> Id of customer related to the recording

            Returns:
            List of video id
        """

