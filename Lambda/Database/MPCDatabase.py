import sys

import mysql.connector
try:
    from Database.Data.Account import Account
except:
    from Lambda.Database.Data.Account import Account


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

    def insert(self, object_instance, ignore: bool = False):
        """
            Perform insert into database

            Parameters:
            script: String -> sql script to be executed

            Returns:
            None
        """
        keys = []
        values = []
        object_dict = object_instance.__dict__
        for key in object_dict:
            if object_dict[key] is not None:
                keys.append(key)
                values.append(object_dict[key])
        script = self.gen_insert_script(object_instance.__class__.TABLE, keys, values, ignore)
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

    def get_all(self, table_class) -> list:
        payload = self.select_payload(table_class.TABLE, table_class.COLUMNS)
        return table_class.list_dict_to_object_list(payload["data"])

    def verify_id(self, table_class, id: int) -> bool:
        entries = self.select_payload(table_class.TABLE, table_class.COLUMNS, match_list=[MatchItem(table_class.ID, id)])
        return len(entries["data"]) == 1

    def get_by_name(self, table_class, name: str):
        """
            Execute query to get the account information related to the given id

            Parameters:

            id: int -> Id of account

            Returns:
            Dict contains the account information
        """
        data = self.select_payload(table_class.TABLE, table_class.COLUMNS, match_list=[MatchItem(table_class.NAME, name)])["data"]
        if len(data) != 1:
            return None
        return table_class.dict_to_object(data[0])

    def get_by_id(self, table_class, id: int):
        data = self.select_payload(table_class.TABLE, table_class.COLUMNS, match_list=[MatchItem(table_class.ID, id)])["data"]
        if len(data) != 1:
            return None
        return table_class.dict_to_object(data[0])

    def get_id_by_name(self, table_class, name: str) -> int:
        payload = self.select_payload(table_class.TABLE, [table_class.ID], [MatchItem(table_class.NAME, name)])["data"]
        if len(payload) == 0:
            return None
        return payload[0][table_class.ID]

    def delete_all_accounts(self):

        return

    def delete_account(self, id):
        return

    def get_all_by_account_id(self, table_class, account_id: int) -> list:
        payload = self.select_payload(table_class.TABLE, table_class.COLUMNS,
                                      match_list=[MatchItem(table_class.ACCOUNT_ID, account_id)])["data"]
        return table_class.list_dict_to_object_list(payload)

    def get_all_by_account_name(self, table_class, account_name: str) -> list:
        payload = self.select_payload(
            table_class.TABLE, table_class.EXPLICIT_COLUMNS,
            match_list=[MatchItem(Account.NAME, account_name)],
            join_list=[JoinItem(JoinItem.INNER, Account.TABLE, table_class.EXPLICIT_ACCOUNT_ID, Account.EXPLICIT_ID)])["data"]

        return table_class.list_dict_to_object_list(payload, explicit=True)

    def get_ids_by_account_id(self, table_class, account_id) -> list[int]:
        payload = self.select_payload(table_class.TABLE, [table_class.ID], [MatchItem(table_class.ACCOUNT_ID, account_id)])
        return [v[table_class.ID] for v in payload["data"]]

    def get_ids_by_account_name(self, table_class, account_name):
        payload = self.select_payload(
            table_class.TABLE, [table_class.ID],
            match_list=[MatchItem(Account.NAME, account_name)],
            join_list=[JoinItem(JoinItem.INNER, Account.TABLE, table_class.EXPLICIT_ACCOUNT_ID,
                                Account.EXPLICIT_ID)])

        return [v[table_class.ID] for v in payload["data"]]

    def get_all_by_hardware_id(self, table_class,  hardware_id):
        payload = self.select_payload(table_class.TABLE, table_class.COLUMNS,
                                      match_list=[MatchItem(table_class.HARDWARE_ID, hardware_id)])["data"]

        return table_class.list_dict_to_object_list(payload)

    def get_all_by_account_id_hardware_id(self, table_class, account_id, hardware_id):
        payload = self.select_payload(table_class.TABLE, table_class.COLUMNS,
                                      match_list=[
                                          MatchItem(table_class.ACCOUNT_ID, account_id),
                                          MatchItem(table_class.HARDWARE_ID, hardware_id)])["data"]

        return table_class.list_dict_to_object_list(payload)


if __name__ == "__main__":
    # print("Started")
    #
    database = MPCDatabase()
    # database.insert_account(Account("Keita Nakashima", "1234567"), True)
    # database.insert_account(Account("Josh Makia", "01234567"), True)
    # database.insert_account(Account("Ben Juria", "01234567"), True)
    # data = database.get_accounts()
    # for d in data:
    #     print(d)
    # print(database.get_account_id_by_name("Ben Juria"))
    # database.insert_hardware(Hardware("Rasberry Pi Keita", database.get_account_id_by_name("Keita Nakashima")), ignore=True)
    # hardware = Hardware("Rasperry Pi Extra")
    #
    # now = datetime.datetime(2009, 5, 5)
    # a_id = database.get_account_id_by_name("Keita Nakashima")
    # h_id = database.get_hardware_ids_by_account_name("Keita Nakashima")[0]
    # recording = Recording("filename7.mp4", now.strftime('%Y-%m-%d %H:%M:%S'), "NOW()", account_id=a_id, hardware_id=h_id)
    # database.insert_recording(recording, ignore=True)
    # data = database.get_recordings()
    # for d in data:
    #     print(d)
    #
    # data = database.get_hardwares()
    # for d in data:
    #     print(d)
    # id = database.get_account_id_by_name("Keita Nakashima")
    # database.insert_hardware(Hardware("Rasberry Pi Keita1"), associated_account_id=id, ignore=True)
    # database.insert(Account("Keita Nakashima", "Password"))
    print(database.gen_select_script("AA", ["Key1"], [MatchItem("Item1", "Value1"), MatchItem("Item2", "Value2")]))