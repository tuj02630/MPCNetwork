import sys

import mysql.connector

from Database.Customer import Customer
from Database.Hardware import Hardware


class MatchItem:
    def __init__(self, key: str, value, table: str = None):
        self.key = key
        self.value = f"'{value}'" if type(value) is str else f"{str(value)}"


class JoinItem:
    INNER = "Inner"
    FULL = "Full"
    Left = "Left"
    Right = "Right"

    def __init__(self, join_type: str, join_table: str, join_field1: str, join_field2: str):
        self.join_type = join_type
        self.join_table = join_table
        self.join_field1 = join_field1
        self.join_field2 = join_field2


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
                print("[Select      ]              :" + script)
                cur.execute(script)
                print("[Completed   ]              :" + script)
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
                print("[Insert      ]              :" + script)
                cur.execute(script)
                self.connection.commit()
                print("[Completed   ]              :" + script)
        except mysql.connector.Error as err:
            print("[Error       ]              :" + str(err), file=sys.stderr)
        return

    def gen_select_script(self, table_name: str, keys: list, match_list: list[MatchItem] = [], join_list: list[JoinItem] = []) -> str:
        join_clause = "".join(
                   [" {} Join {} On {} = {}".format(item.join_type, item.join_table, item.join_field1, item.join_field2)
                        for item in join_list]
                    ) if len(join_list) != 0 else ""
        where_clause = " Where " + " and ".join(
                   [f"{item.key} = {item.value}" for item in match_list]) if not len(match_list) == 0 else ""

        return "Select " + ",".join(keys) + \
               " From " + table_name + \
               join_clause + \
               where_clause

    def gen_insert_script(self, table_name: str, keys: list, values: list, ignore: bool) -> str:
        return "Insert " + \
               ("Ignore" if ignore else "") + \
               " Into " + table_name + \
               "(" + ",".join(keys) + ") Values (" + ",".join([(f"'{v}'" if type(v) is str else f"{str(v)}") for v in values]) + ");"

    def select_payload(self, table_name: str, columns: list[str], match_list: list[MatchItem] = [], join_list: list[JoinItem] = []) -> dict:
        script = self.gen_select_script(table_name, columns, match_list, join_list)
        result = self.query(script)
        data = []
        for entry in result:
            data.append(dict(zip(columns, entry)))
        payload = {"column": columns, "script": script, "data": data}

        return payload

    def insert_customer(self, customer: Customer, ignore: bool = False):
        """
            Insert a record of customer to database

            Parameters:
            username: String -> Username that customer defined

            password: String -> User defined password

            Returns:
            None
        """
        self.insert("Customer", [Customer.USERNAME, Customer.PASSWORD], [customer.username, customer.password], ignore)
        return

    def verify_customer_id(self, id: int) -> bool:
        customers = self.select_payload(Customer.TABLE, Customer.COLUMNS, match_list=[MatchItem(Customer.CUSTOMER_ID, id)])
        return len(customers["data"]) == 1

    def get_customers(self) -> list[Customer]:
        """
            Execute query to get the list of customers

            Parameters:
            None

            Returns:
            Lis of dictionary representing list of customers
        """
        payload = self.select_payload(Customer.TABLE, Customer.COLUMNS)
        return Customer.list_dict_to_customer_list(payload["data"])

    def get_customer_by_name(self, name: str) -> Customer:
        """
            Execute query to get the customer information related to the given id

            Parameters:

            id: int -> Id of customer

            Returns:
            Dict contains the customer information
        """
        data = self.select_payload(Customer.TABLE, Customer.COLUMNS, match_list=[MatchItem(Customer.USERNAME, name)])["data"]
        if len(data) != 1:
            return None
        return Customer.dict_to_customer(data[0])

    def get_customer_id_by_name(self, name: str) -> int:
        payload = self.select_payload(Customer.TABLE, [Customer.CUSTOMER_ID], [MatchItem(Customer.USERNAME, name)])["data"]
        if len(payload) == 0:
            return None
        return payload[0][Customer.CUSTOMER_ID]

    def insert_hardware(self, hardware: Hardware, associated_customer_name: str = None, ignore: bool = False) -> bool:
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
        if associated_customer_name is not None and hardware.customer_id is None:
            id = self.get_customer_id_by_name(associated_customer_name)
            if hardware.customer_id is None or id == hardware.customer_id:
                hardware.customer_id = id
            else:
                print("[Error       ]              :Conflicting customer information", file=sys.stderr)
                return False
        if hardware.customer_id is not None and not self.verify_customer_id(hardware.customer_id):
            print("[Error       ]              :" + "Invalid Hardware", file=sys.stderr)
            return False
        if hardware.customer_id is not None:
            self.insert(Hardware.TABLE, Hardware.COLUMNS, [hardware.name, hardware.customer_id], ignore)
        else:
            self.insert(Hardware.TABLE, [hardware.NAME], [hardware.name], ignore)
        return True

    def verify_hardware_id(self, id: int) -> bool:
        hardwares = self.select_payload(Hardware.TABLE, Hardware.COLUMNS, match_list=[MatchItem(Hardware.HARDWARE_ID, id)])
        return len(hardwares["data"]) == 1

    def get_hardwares(self):
        payload = self.select_payload(Hardware.TABLE, Hardware.COLUMNS)
        return Hardware.list_dict_to_customer_list(payload["data"])

    def get_hardwares_by_customer_name(self, customer_name: str):
        payload = self.select_payload(
            Hardware.TABLE, Hardware.EXPLICIT_COLUMNS,
            match_list=[MatchItem(Customer.USERNAME, customer_name)],
            join_list=[JoinItem(JoinItem.INNER, Customer.TABLE, Hardware.EXPLICIT_CUSTOMER_ID, Customer.EXPLICIT_CUSTOMER_ID)])["data"]

        return Hardware.list_dict_to_customer_list(payload, explicit=True)

    def add_recording(self, customer_id, hardware_id, file_name, is_video, file_size, resolution, date, time):
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
    database.insert_customer(Customer("Josh Makia", "01234567"), True)
    database.insert_customer(Customer("Ben Juria", "01234567"), True)
    data = database.get_customers()
    for d in data:
        print(d)
    print(database.get_customer_id_by_name("Ben Juria"))
    database.insert_hardware(Hardware("Rasberry Pi", database.get_customer_id_by_name("Keita Nakashima")), ignore=True)
    hardware = Hardware("Rasperry Pi Extra")
    database.insert_hardware(hardware, ignore=True)
    data = database.get_hardwares()
    for d in data:
        print(d)
    print(database.verify_customer_id(26))
    data = database.get_hardwares_by_customer_name("Keita Nakashima")
    for d in data:
        print(d)
    print(database.get_customer_id_by_name("Keita Nakashima"))
    print(database.verify_hardware_id(3))