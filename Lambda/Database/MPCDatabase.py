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
                                                  database="mydb1")
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
        except mysql.connector.Error as err:
            print("[Error       ]              :" + str(err), file=sys.stderr)
            raise err
        return

    def truncate(self, table_class, foreign_key_check: bool = True, auto_increment_reset: bool = False):
        script = "TRUNCATE " + table_class.__name__ + ";"
        try:
            with self.connection.cursor() as cur:
                if not foreign_key_check:
                    key_check_script = "SET FOREIGN_KEY_CHECKS = 0;"
                    print("[Foreign Key Check      ]              :" + key_check_script)
                    cur.execute(script)

                if auto_increment_reset:
                    auto_increment_script = "ALTER TABLE " + table_class.__name__ + " AUTO_INCREMENT = 1;"
                    print("[Auto Increment      ]              :" + key_check_script)
                    cur.execute(script)

                print("[TRUNCATE      ]              :" + script)
                cur.execute(script)
                self.connection.commit()
                if not foreign_key_check:
                    key_check_script = "SET FOREIGN_KEY_CHECKS = 1;"
                    print("[Foreign Key Check      ]              :" + key_check_script)
                    cur.execute(script)
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

    def delete_all_accounts(self):

        return

    def delete_account(self, id):
        return


if __name__ == "__main__":
    from Lambda.Database.Data.Resolution import Resolution
    from Lambda.Database.Data.Saving_Policy import Saving_Policy
    from Lambda.Database.Data.Hardware import Hardware
    from Lambda.Database.Data.Recording import Recording
    from Lambda.Database.Data.Criteria import Criteria
    from Lambda.Database.Data.Notification import Notification


    # print("Started")
    #
    database = MPCDatabase()
    resolution720 = Resolution("720p", 1280, 720)
    resolution1080 = Resolution("1080p", 1920, 1080)
    resolution1440 = Resolution("1440p", 2560, 1440)
    database.insert(resolution720, ignore=True)
    database.insert(resolution1080, ignore=True)
    database.insert(resolution1440, ignore=True)
    data = database.get_all(Resolution)
    for d in data:
        print(str(d))

    policy10mins720 = Saving_Policy(600, "720p")
    policy20mins720 = Saving_Policy(1200, "720p")
    policy10mins1080 = Saving_Policy(600, "1080p")
    policy12mins1080 = Saving_Policy(720, "720p")
    database.insert(policy10mins720, ignore=True)
    database.insert(policy20mins720, ignore=True)
    database.insert(policy10mins1080, ignore=True)
    database.insert(policy12mins1080, ignore=True)
    data = database.get_all(Saving_Policy)
    for d in data:
        print(str(d))

    # database.truncate(Hardware)
    hardware1 = Hardware("Hardware-1", "720p")

    database.insert(hardware1, ignore=True)
    data = database.get_all(Hardware)
    for d in data:
        print(str(d))

    criteria = Criteria(1001, 100, 100)
    criteria1 = Criteria(1002, 100, 100)
    database.insert(criteria)
    database.insert(criteria1)
    data = database.get_all(Criteria)
    for d in data:
        print(str(d))

    # notification = Notification()

    recording = Recording("Filename.mp4", "CURDATE()", "NOW()")
