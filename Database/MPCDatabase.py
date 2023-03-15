import datetime
import sys

import mysql.connector

from Database.Customer import Customer
from Database.Hardware import Hardware
from Database.Recording import Recording


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
        self.connection = mysql.connector.connect(host='mpc.c7s8y7an5gv1.us-east-1.rds.amazonaws.com',
                                                  user='admin',
                                                  password='1234567890',
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
            print("[Error   ]: {}".format(err), file=sys.stderr)
            raise err

    def insert(self, table_name: str, keys: list, values: list, ignore: bool = False):
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
            raise err
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
               "(" + ",".join(keys) + ") Values (" + ",".join([(f"'{v}'" if type(v) is str and v[-2:] != "()" else f"{str(v)}") for v in values]) + ");"

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
        self.insert(Customer.TABLE, [Customer.USERNAME, Customer.PASSWORD], [customer.username, customer.password], ignore)
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

    def delete_all_customers(self):

        return

    def delete_customer(self, id):
        return

    def insert_hardware(self, hardware: Hardware, associated_customer_id: int = None, ignore: bool = False) -> bool:
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
        if associated_customer_id is not None and hardware.customer_id is None:
            id = associated_customer_id
            if hardware.customer_id is None or id == hardware.customer_id:
                hardware.customer_id = id
            else:
                print("[Error       ]              :Conflicting customer information", file=sys.stderr)
                return False
        if hardware.customer_id is not None and not self.verify_customer_id(hardware.customer_id):
            print("[Error       ]              :" + "Invalid Hardware", file=sys.stderr)
            return False
        if hardware.customer_id is not None:
            self.insert(Hardware.TABLE, [Hardware.NAME, Hardware.CUSTOMER_ID], [hardware.name, hardware.customer_id], ignore)
        else:
            self.insert(Hardware.TABLE, [Hardware.NAME], [hardware.name], ignore)
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

    def get_hardware_ids_by_customer_id(self, id):
        payload = self.select_payload(Hardware.TABLE, [Hardware.HARDWARE_ID], [MatchItem(Hardware.CUSTOMER_ID, id)])
        return [v[Hardware.HARDWARE_ID] for v in payload["data"]]

    def get_hardware_ids_by_customer_name(self, customer_name):
        payload = self.select_payload(
            Hardware.TABLE, [Hardware.HARDWARE_ID],
            match_list=[MatchItem(Customer.USERNAME, customer_name)],
            join_list=[JoinItem(JoinItem.INNER, Customer.TABLE, Hardware.EXPLICIT_CUSTOMER_ID,
                                Customer.EXPLICIT_CUSTOMER_ID)])

        return [v[Hardware.HARDWARE_ID] for v in payload["data"]]

    def insert_recording(self, recording: Recording, ignore: bool = False):
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
        self.insert(Recording.TABLE,
                    [Recording.FILE_NAME, Recording.DATE, Recording.TIMESTAMP, Recording.CUSTOMER_ID, Recording.HARDWARE_ID],
                    [recording.file_name, recording.date, recording.timestamp, recording.customer_id, recording.hardware_id],
                    ignore)
        return

    def get_recordings(self) -> list[Recording]:
        """
            Execute query to get the list of customers

            Parameters:
            None

            Returns:
            Lis of dictionary representing list of customers
        """
        payload = self.select_payload(Recording.TABLE, Recording.COLUMNS)
        return Recording.list_dict_to_customer_list(payload["data"])

    def get_recordings_by_customer_id(self, id):
        """
            Retrieve the list of videos saved in the cloud related to the customer id

            Parameters:

            customer_id: int -> Id of customer related to the recording

            Returns:
            List of video id
        """

        payload = self.select_payload(Recording.TABLE, Recording.COLUMNS, [MatchItem(Recording.CUSTOMER_ID, id)])["data"]
        return Recording.list_dict_to_customer_list(payload)

    def get_recordings_by_customer_name(self, customer_name):
        payload = self.select_payload(
            Recording.TABLE, Recording.EXPLICIT_COLUMNS,
            match_list=[MatchItem(Customer.USERNAME, customer_name)],
            join_list=[JoinItem(JoinItem.INNER, Customer.TABLE, Recording.EXPLICIT_CUSTOMER_ID,
                                Customer.EXPLICIT_CUSTOMER_ID)])["data"]

        return Recording.list_dict_to_customer_list(payload, explicit=True)



if __name__ == "__main__":
    print("Started")

    database = MPCDatabase()
    # data = database.getCustomers()
    # print(data)
    database.insert_customer(Customer("Keita Nakashima", "1234567"), True)
    database.insert_customer(Customer("Josh Makia", "01234567"), True)
    database.insert_customer(Customer("Ben Juria", "01234567"), True)
    data = database.get_customers()
    for d in data:
        print(d)
    print(database.get_customer_id_by_name("Ben Juria"))
    database.insert_hardware(Hardware("Rasberry Pi Keita", database.get_customer_id_by_name("Keita Nakashima")), ignore=True)
    hardware = Hardware("Rasperry Pi Extra")

    now = datetime.datetime(2009, 5, 5)
    recording = Recording("filename7.mp4", now.strftime('%Y-%m-%d %H:%M:%S'), "NOW()", customer_id=201, hardware_id=131)
    database.insert_recording(recording, ignore=True)
    data = database.get_recordings()
    for d in data:
        print(d)

    data = database.get_hardwares()
    for d in data:
        print(d)
    id = database.get_customer_id_by_name("Keita Nakashima")
    database.insert_hardware(Hardware("Rasberry Pi Keita1"), associated_customer_id=id, ignore=True)