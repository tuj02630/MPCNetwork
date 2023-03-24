import datetime
import sys

import mysql.connector

from Database.Account import Account
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

    def insert_account(self, account: Account, ignore: bool = False):
        """
            Insert a record of account to database

            Parameters:
            username: String -> Username that account defined

            password: String -> User defined password

            Returns:
            None
        """
        self.insert(Account.TABLE, [Account.USERNAME, Account.PASSWORD], [account.username, account.password], ignore)
        return

    def verify_account_id(self, id: int) -> bool:
        accounts = self.select_payload(Account.TABLE, Account.COLUMNS, match_list=[MatchItem(Account.ACCOUNT_ID, id)])
        return len(accounts["data"]) == 1

    def get_accounts(self) -> list[Account]:
        """
            Execute query to get the list of accounts

            Parameters:
            None

            Returns:
            Lis of dictionary representing list of accounts
        """
        payload = self.select_payload(Account.TABLE, Account.COLUMNS)
        return Account.list_dict_to_account_list(payload["data"])

    def get_account_by_name(self, name: str) -> Account:
        """
            Execute query to get the account information related to the given id

            Parameters:

            id: int -> Id of account

            Returns:
            Dict contains the account information
        """
        data = self.select_payload(Account.TABLE, Account.COLUMNS, match_list=[MatchItem(Account.USERNAME, name)])["data"]
        if len(data) != 1:
            return None
        return Account.dict_to_account(data[0])

    def get_account_id_by_name(self, name: str) -> int:
        payload = self.select_payload(Account.TABLE, [Account.ACCOUNT_ID], [MatchItem(Account.USERNAME, name)])["data"]
        if len(payload) == 0:
            return None
        return payload[0][Account.ACCOUNT_ID]

    def delete_all_accounts(self):

        return

    def delete_account(self, id):
        return

    def insert_hardware(self, hardware: Hardware, associated_account_id: int = None, ignore: bool = False) -> bool:
        """
            Execute query to register new hardware

            Parameters:

            account_id: int -> Id of account related to the hardware

            is_camera: bool -> True for if the device is camera

            is_thermal: bool -> True for if the device is thermal camera

            price: int -> optional field to store the price of the device.

            Returns:
            None
        """
        if associated_account_id is not None and hardware.account_id is None:
            id = associated_account_id
            if hardware.account_id is None or id == hardware.account_id:
                hardware.account_id = id
            else:
                print("[Error       ]              :Conflicting account information", file=sys.stderr)
                return False
        if hardware.account_id is not None and not self.verify_account_id(hardware.account_id):
            print("[Error       ]              :" + "Invalid Hardware", file=sys.stderr)
            return False
        if hardware.account_id is not None:
            self.insert(Hardware.TABLE, [Hardware.NAME, Hardware.ACCOUNT_ID], [hardware.name, hardware.account_id], ignore)
        else:
            self.insert(Hardware.TABLE, [Hardware.NAME], [hardware.name], ignore)
        return True

    def verify_hardware_id(self, id: int) -> bool:
        hardwares = self.select_payload(Hardware.TABLE, Hardware.COLUMNS, match_list=[MatchItem(Hardware.HARDWARE_ID, id)])
        return len(hardwares["data"]) == 1

    def get_hardwares(self):
        payload = self.select_payload(Hardware.TABLE, Hardware.COLUMNS)
        return Hardware.list_dict_to_hardware_list(payload["data"])

    def get_hardwares_by_account_name(self, account_name: str):
        payload = self.select_payload(
            Hardware.TABLE, Hardware.EXPLICIT_COLUMNS,
            match_list=[MatchItem(Account.USERNAME, account_name)],
            join_list=[JoinItem(JoinItem.INNER, Account.TABLE, Hardware.EXPLICIT_ACCOUNT_ID, Account.EXPLICIT_ACCOUNT_ID)])["data"]

        return Hardware.list_dict_to_hardware_list(payload, explicit=True)

    def get_hardware_ids_by_account_id(self, id):
        payload = self.select_payload(Hardware.TABLE, [Hardware.HARDWARE_ID], [MatchItem(Hardware.ACCOUNT_ID, id)])
        return [v[Hardware.HARDWARE_ID] for v in payload["data"]]

    def get_hardware_ids_by_account_name(self, account_name):
        payload = self.select_payload(
            Hardware.TABLE, [Hardware.HARDWARE_ID],
            match_list=[MatchItem(Account.USERNAME, account_name)],
            join_list=[JoinItem(JoinItem.INNER, Account.TABLE, Hardware.EXPLICIT_ACCOUNT_ID,
                                Account.EXPLICIT_ACCOUNT_ID)])

        return [v[Hardware.HARDWARE_ID] for v in payload["data"]]

    def insert_recording(self, recording: Recording, ignore: bool = False):
        """
            Add recoding record to the database

            Parameters:

            account_id: int -> Id of account related to the recording

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
                    [Recording.FILE_NAME, Recording.DATE, Recording.TIMESTAMP, Recording.ACCOUNT_ID, Recording.HARDWARE_ID],
                    [recording.file_name, recording.date, recording.timestamp, recording.ACCOUNT_ID, recording.hardware_id],
                    ignore)
        return

    def get_recordings(self) -> list[Recording]:
        """
            Execute query to get the list of accounts

            Parameters:
            None

            Returns:
            Lis of dictionary representing list of accounts
        """
        payload = self.select_payload(Recording.TABLE, Recording.COLUMNS)
        return Recording.list_dict_to_recording_list(payload["data"])

    def get_recordings_by_account_id(self, id):
        """
            Retrieve the list of videos saved in the cloud related to the account id

            Parameters:

            account_id: int -> Id of account related to the recording

            Returns:
            List of video id
        """

        payload = self.select_payload(Recording.TABLE, Recording.COLUMNS, [MatchItem(Recording.ACCOUNT_ID, id)])["data"]
        return Recording.list_dict_to_recording_list(payload)

    def get_recordings_by_account_name(self, account_name):
        payload = self.select_payload(
            Recording.TABLE, Recording.EXPLICIT_COLUMNS,
            match_list=[MatchItem(Account.USERNAME, account_name)],
            join_list=[JoinItem(JoinItem.INNER, Account.TABLE, Recording.EXPLICIT_ACCOUNT_ID,
                                Account.EXPLICIT_ACCOUNT_ID)])["data"]

        return Recording.list_dict_to_recording_list(payload, explicit=True)


if __name__ == "__main__":
    print("Started")

    database = MPCDatabase()
    database.insert_account(Account("Keita Nakashima", "1234567"), True)
    database.insert_account(Account("Josh Makia", "01234567"), True)
    database.insert_account(Account("Ben Juria", "01234567"), True)
    data = database.get_accounts()
    for d in data:
        print(d)
    print(database.get_account_id_by_name("Ben Juria"))
    database.insert_hardware(Hardware("Rasberry Pi Keita", database.get_account_id_by_name("Keita Nakashima")), ignore=True)
    hardware = Hardware("Rasperry Pi Extra")

    now = datetime.datetime(2009, 5, 5)
    recording = Recording("filename7.mp4", now.strftime('%Y-%m-%d %H:%M:%S'), "NOW()", account_id=201, hardware_id=131)
    database.insert_recording(recording, ignore=True)
    data = database.get_recordings()
    for d in data:
        print(d)

    data = database.get_hardwares()
    for d in data:
        print(d)
    id = database.get_account_id_by_name("Keita Nakashima")
    database.insert_hardware(Hardware("Rasberry Pi Keita1"), associated_account_id=id, ignore=True)