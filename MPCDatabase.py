import mysql.connector


class MPCDatabase:
    def __init__(self):
        """Reference for my sql instance. Used to perform query in database"""
        self.connection = mysql.connector.connect(host='mpcdb.casix5st3sf8.us-east-1.rds.amazonaws.com',
                                                  user='root',
                                                  password='jGG4UqJNp4KGUZw63kA=',
                                                  database="mydb")
        print("Connected")

    def query(self, script: str) -> list:
        """
            Perform query in database

            Parameters:
            script: String -> sql script to be executed

            Returns:
            Lis of dictionary representing the result of the execution of sql script given
        """
        if "select" not in script.lower():
            raise TypeError("Script should only be Select")

        try:
            with self.connection.cursor() as cur:
                print("[Executing]              :" + script)
                cur.execute(script)
                print("[Completed]              :" + script)
                return list(cur)
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))

    def insert(self, table_name, keys: list, values: list, ignore: bool = False):
        """
            Perform insert into database

            Parameters:
            script: String -> sql script to be executed

            Returns:
            None
        """
        script = self.gen_insert_script(table_name, keys, values, ignore)
        try:
            with self.connection.cursor() as cur:
                print("[Executing]              :" + script)
                cur.execute(script)
                self.connection.commit()
                print("[Completed]              :" + script)
        except mysql.connector.Error as err:
            print("[Error    ]              :" + err)
        return

    def gen_select_script(self, table_name: str, keys: list, match_list: list = []) -> str:
        return "Select " + ",".join(keys) + \
               " From " + table_name + \
               (" Where " + " and ".join(
                   [f"{key} = '{value}'" for key, value in match_list]
               ) if not len(match_list) == 0
                else "")

    def gen_insert_script(self, table_name: str, keys: list, values: list, ignore: bool) -> str:
        return "Insert " + \
               ("Ignore" if ignore else "") + \
               " Into " + table_name + \
               "(" + ",".join(keys) + ") Values (" + ",".join([f"'{v}'" for v in values]) + ");"

    def select_payload(self, table_name: str, columns: list, match_list: list = []):
        script = self.gen_select_script(table_name, columns, match_list)
        result = self.query(script)
        data = []
        for entry in result:
            data.append(dict(zip(columns, entry)))
        payload = {"column": columns, "script": script, "data": data}

        return payload

    def insert_customer(self, username, password, ignore: bool = False, match_list: list = []):
        """
            Insert a record of customer to database

            Parameters:
            username: String -> Username that customer defined

            password: String -> User defined password

            Returns:
            None
        """
        self.insert("Customer", ["username", "password"], [username, password], ignore)
        return

    def getCustomers(self) -> dict:
        """
            Execute query to get the list of customers

            Parameters:
            None

            Returns:
            Lis of dictionary representing list of customers
        """
        columns = ["customer_id", "username", "password"]
        return self.select_payload("Customer", columns)

    def getCustomerByName(self, name):
        """
            Execute query to get the customer information related to the given id

            Parameters:

            id: int -> Id of customer

            Returns:
            Dict contains the customer information
        """
        columns = ["customer_id", "username", "password"]
        return self.select_payload("Customer", columns, [(columns[1], name)])

    def registerHardware(self, name: str, customer_name: str = None, ignore: bool = False):
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
        customer_data = []
        if customer_name is not None:
            customer_data = self.getCustomerByName(customer_name)["data"]

        if len(customer_data) == 0:
            print("[Error    ]              :" + "Customer name [" + customer_name + "] not found")
            return

        self.insert("Hardware", ["name", "customer_id"], [name, "NULL" if customer_name is None else customer_data[0]["customer_id"]], ignore)
        return

    def getAllHardwares(self):
        columns = ["hardware_id", "name", "customer_id"]
        return self.select_payload("Hardware", columns)

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


if __name__ == "__main__":
    print("Started")

    database = MPCDatabase()
    # data = database.getCustomers()
    # print(data)
    # database.insert_customer("Keita Nakashima", "01234567", True)
    data = database.getCustomerByName("Keita Nakashima")
    print(data)
    database.registerHardware("Test2", customer_name="Keita Nakashima", ignore=True)
    print(database.getAllHardwares())