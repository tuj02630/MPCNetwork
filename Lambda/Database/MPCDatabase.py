import sys
from typing import Match

import mysql.connector
from matplotlib.table import table

try:
    from Database.Data.Account import Account
except:
    from Lambda.Database.Data.Account import Account


class MatchItem:
    def __init__(self, key: str, value, table: str = None):
        self.key = key
        self.value = f"'{value}'" if type(value) is str and value[-1:] != ")" else f"{str(value)}"


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
                                                  database="mydb2")
        print("Connected")

    def close(self):
        self.connection.close()

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

    def update(self, table_class, condition_item: MatchItem, update_list: list[MatchItem]):
        script = self.gen_update_script(table_class.__name__, condition_item, update_list)
        if "update" not in script.lower():
            raise TypeError("Update should only be Update")
        try:
            with self.connection.cursor() as cur:
                print("[Update      ]              :" + script)
                cur.execute(script)
                # return list(cur)
                self.connection.commit()
        except mysql.connector.Error as err:
            print("[Error   ]: {}".format(err), file=sys.stderr)
            raise err

    def delete(self, table_class, condition_item: MatchItem):
        script = f"Delete From {table_class.__name__} Where {condition_item.key} = {condition_item.value}"
        if "delete" not in script.lower():
            raise TypeError("Delete should only be delete")
        try:
            with self.connection.cursor() as cur:
                print("[Delete      ]              :" + script)
                cur.execute(script)
                # return list(cur)
                self.connection.commit()
        except mysql.connector.Error as err:
            print("[Error   ]: {}".format(err), file=sys.stderr)
            raise err

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
               "(" + ",".join(keys) + ") Values (" + ",".join([(f"'{v}'" if type(v) is str and v[-1:] != ")" else f"{str(v)}") for v in values]) + ");"

    def gen_update_script(self, table_name: str, condition_item: MatchItem, update_items: list[MatchItem]):
        return  "Update " + table_name + \
                " Set " + ", ".join([f"{item.key} = {item.value}"for item in update_items]) + \
                " Where " + f"{condition_item.key} = {condition_item.value}"

    def select_payload(self, table_name: str, columns: list[str], match_list: list[MatchItem] = [], join_list: list[JoinItem] = []) -> dict:
        script = self.gen_select_script(table_name, columns, match_list, join_list)
        result = self.query(script)
        data = []
        for entry in result:
            data.append(dict(zip(columns, entry)))
        payload = {"column": columns, "script": script, "data": data}

        return payload

    def verify_field(self, table_class, field: str, value: str):
        entries = self.select_payload(table_class.TABLE, table_class.COLUMNS,
                                      match_list=[MatchItem(field, value)])
        return len(entries["data"]) == 1

    def verify_fields(self, table_class, field_value_list: list[tuple]):
        entries = self.select_payload(table_class.TABLE, table_class.COLUMNS,
                                      match_list=[MatchItem(item[0], item[1]) for item in field_value_list])
        return len(entries["data"]) == 1

    def verify_id(self, table_class, id: int) -> bool:
        return self.verify_field(table_class, table_class.ID, str(id))

    def verify_name(self, table_class, name: str) -> bool:
        return self.verify_field(table_class, table_class.NAME, name)

    def get_all(self, table_class) -> list:
        payload = self.select_payload(table_class.TABLE, table_class.COLUMNS)
        return table_class.list_dict_to_object_list(payload["data"])

    def get_field_by_name(self, table_class, field: str, name: str):
        entries = self.select_payload(table_class.TABLE, [field],
                                      match_list=[MatchItem(table_class.NAME, name)])
        if len(entries["data"]) == 0:
            return None
        return entries["data"][0][field]

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

    def get_max_id(self, table_class):
        payload = self.select_payload(table_class.TABLE, [f"max({table_class.ID})"])["data"]
        if len(payload) == 0:
            return None
        return payload[0][f"max({table_class.ID})"]

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

    def get_ids_by_account_name(self, table_class, account_name: str):
        payload = self.select_payload(
            table_class.TABLE, [table_class.ID],
            match_list=[MatchItem(Account.NAME, account_name)],
            join_list=[JoinItem(JoinItem.INNER, Account.TABLE, table_class.EXPLICIT_ACCOUNT_ID,
                                Account.EXPLICIT_ID)])

        return [v[table_class.ID] for v in payload["data"]]

    def get_all_by_hardware_id(self, table_class,  hardware_id: int):
        payload = self.select_payload(table_class.TABLE, table_class.COLUMNS,
                                      match_list=[MatchItem(table_class.HARDWARE_ID, hardware_id)])["data"]

        return table_class.list_dict_to_object_list(payload)

    def get_all_by_account_id_hardware_id(self, table_class, account_id: int, hardware_id: int):
        payload = self.select_payload(table_class.TABLE, table_class.COLUMNS,
                                      match_list=[
                                          MatchItem(table_class.ACCOUNT_ID, account_id),
                                          MatchItem(table_class.HARDWARE_ID, hardware_id)])["data"]

        return table_class.list_dict_to_object_list(payload)

    def get_by_type(self, table_class, type: int):
        data = self.select_payload(table_class.TABLE, table_class.COLUMNS, match_list=[MatchItem(table_class.TYPE, type)])[
            "data"]
        if len(data) != 1:
            return None
        return table_class.dict_to_object(data[0])

    def get_id_by_type(self, table_class, type: int) -> id:
        payload = self.select_payload(table_class.TABLE, [table_class.ID], [MatchItem(table_class.TYPE, type)])["data"]
        if len(payload) == 0:
            return None
        return payload[0][table_class.ID]

    def get_saving_policy_ids_by_hardware_id(self, table_class, hardware_id: int) -> list[int]:
        payload = self.select_payload(table_class.TABLE, [table_class.SAVING_POLICY_ID], [MatchItem(table_class.HARDWARE_ID, hardware_id)])
        return [v[table_class.SAVING_POLICY_ID] for v in payload["data"]]

    def get_hardware_ids_by_saving_policy_id(self, table_class, saving_policy_id: int) -> list[int]:
        payload = self.select_payload(table_class.TABLE, [table_class.HARDWARE_ID], [MatchItem(table_class.SAVING_POLICY_ID, saving_policy_id)])
        return [v[table_class.HARDWARE_ID] for v in payload["data"]]

    def get_notification_ids_by_hardware_id(self, table_class, hardware_id: int) -> list[int]:
        payload = self.select_payload(table_class.TABLE, [table_class.NOTIFICATION_ID], [MatchItem(table_class.HARDWARE_ID, hardware_id)])
        return [v[table_class.NOTIFICATION_ID] for v in payload["data"]]

    def get_hardware_ids_by_notification_id(self, table_class, notification_id: int) -> list[int]:
        payload = self.select_payload(table_class.TABLE, [table_class.HARDWARE_ID], [MatchItem(table_class.NOTIFICATION_ID, notification_id)])
        return [v[table_class.HARDWARE_ID] for v in payload["data"]]

    def get_all_by_join_id(self, table_class, join_table_class, join_field: str, match_field: str, match_id: int):
        match_id = int(match_id)
        if join_field[:len("EXPLICIT")] != "EXPLICIT":
            raise ValueError("join_field should be explicit name")
        payload = self.select_payload(
            table_class.TABLE, table_class.EXPLICIT_COLUMNS,
            match_list=[MatchItem(join_table_class.__dict__[match_field], match_id)],
            join_list=[JoinItem(JoinItem.INNER, join_table_class.TABLE, table_class.__dict__[join_field],
                                join_table_class.__dict__[join_field])])["data"]

        return table_class.list_dict_to_object_list(payload, explicit=True)

    def update_fields(self, table_class, condition_tuple: tuple[str, str], update_list: list[tuple[str, str]]):
        self.update(table_class, MatchItem(condition_tuple[0], condition_tuple[1]),
                    [MatchItem(item[0], item[1]) for item in update_list])

    def delete_by_field(self, table_class, condition_field: tuple[str, str]):
        self.delete(table_class, MatchItem(condition_field[0], condition_field[1]))




if __name__ == "__main__":
    from Lambda.Database.Data.Resolution import Resolution
    from Lambda.Database.Data.Saving_Policy import Saving_Policy
    from Lambda.Database.Data.Hardware import Hardware
    from Lambda.Database.Data.Recording import Recording
    from Lambda.Database.Data.Criteria import Criteria
    from Lambda.Database.Data.Notification import Notification
    from Lambda.Database.Data.Hardware_has_Saving_Policy import Hardware_has_Saving_Policy
    import random

    # print("Started")
    #

    database = MPCDatabase()
    # account = Account("John Smith", "Password", "default@exmple.com")
    # account1 = Account("Tom Morgan", "Password", "default@exmple.com")
    # account2 = Account("Tan Pen", "Password", "default@exmple.com")
    # for a in [account, account1, account2]:
    #     database.insert(a, ignore=True)
    #
    # id_a = database.get_id_by_name(Account, "John Smith")
    # id_a1 = database.get_id_by_name(Account, "Tom Morgan")
    # id_a2 = database.get_id_by_name(Account, "Tan Pen")
    #
    # resolution720 = Resolution("720p", 1280, 720)
    # resolution1080 = Resolution("1080p", 1920, 1080)
    # resolution1440 = Resolution("1440p", 2560, 1440)
    # database.insert(resolution720, ignore=True)
    # database.insert(resolution1080, ignore=True)
    # database.insert(resolution1440, ignore=True)
    # data = database.get_all(Resolution)
    # for d in data:
    #     print(str(d))
    #
    # policy10mins720 = Saving_Policy(600, "720p")
    # policy20mins720 = Saving_Policy(1200, "720p")
    # policy10mins1080 = Saving_Policy(600, "1080p")
    # policy12mins1080 = Saving_Policy(720, "720p")
    #
    # for p in [policy10mins720, policy20mins720, policy10mins1080, policy12mins1080]:
    #     database.insert(p)
    #
    # data = database.get_all(Saving_Policy)
    # for d in data:
    #     print(str(d))
    #
    # database.truncate(Hardware)
    # hardware1 = Hardware("Hardware-1", "720p", account_id=id_a1)
    # hardware2 = Hardware("Hardware-2", "1080p", account_id=id_a1)
    # hardware3 = Hardware("Hardware-3", "1080p", account_id=id_a)
    # hardware4 = Hardware("Hardware-4", "1080p", account_id=id_a)
    # hardware5 = Hardware("Hardware-5", "720p", account_id=id_a)
    # hardware6 = Hardware("Hardware-6", "720p", account_id=id_a2)
    # hardware7 = Hardware("Hardware-7", "720p", account_id=id_a2)
    #
    # id_a_h = database.get_ids_by_account_name(Hardware, "John Smith")
    # id_a1_h = database.get_ids_by_account_name(Hardware, "Tom Morgan")
    # id_a2_h = database.get_ids_by_account_name(Hardware, "Tan Pen")
    #
    # for h in [hardware1, hardware2, hardware3, hardware4, hardware5, hardware6, hardware7]:
    #     database.insert(h, ignore=True)
    #
    # data = database.get_all(Hardware)
    # for d in data:
    #     print(str(d))
    #
    # criteria = Criteria(1001, 100, 100)
    # criteria1 = Criteria(1002, 100, 100)
    # database.insert(criteria, ignore=True)
    # database.insert(criteria1, ignore=True)
    # data = database.get_all(Criteria)
    # for d in data:
    #     print(str(d))
    #
    # id_c = database.get_id_by_type(Criteria, 1001)
    # id1_c = database.get_id_by_type(Criteria, 1002)
    #
    # notification = Notification(101, id_c)
    # notification1 = Notification(101, id1_c)
    # database.insert(notification, ignore=True)
    # database.insert(notification1, ignore=True)
    # data = database.get_all(Notification)
    # for d in data:
    #     print(str(d))
    # print("EXPLICIT_"[:len("EXPLICIT")] != "EXPLICIT")
    # data = database.get_all_by_join_id(Hardware, Hardware_has_Saving_Policy,
    #                                    "EXPLICIT_HARDWARE_ID", "EXPLICIT_SAVING_POLICY_ID", 69)
    #
    # for d in data:
    #     print(str(d))
    #
    # recording1 = Recording("_import_616e5dcf2a2362.07330217_preview.mp4", "CURDATE()", "NOW()", account_id=id_a,
    #                        hardware_id=random.choice(id_a_h))
    # recording2 = Recording("_import_616e710b7f2ff0.35776522_preview.mp4", "CURDATE()", "NOW()", account_id=id_a,
    #                        hardware_id=random.choice(id_a_h))
    # recording3 = Recording("_import_616e7d55dc7db8.56370719_preview.mp4", "CURDATE()", "NOW()", account_id=id_a1,
    #                        hardware_id=random.choice(id_a1_h))
    # recording4 = Recording("Cat_Eye_preview.mp4", "CURDATE()", "NOW()", account_id=id_a1,
    #                        hardware_id=random.choice(id_a1_h))
    # recording5 = Recording("cat.mp4", "CURDATE()", "NOW()", account_id=id_a2,
    #                        hardware_id=random.choice(id_a2_h))
    #
    # for f in [recording1, recording2, recording3, recording4, recording5]:
    #     database.insert(f)
    # data = database.get_all(Recording)
    # for d in data:
    #     print(str(d))
    #
    # a = Account("Keita Nakashima", "Password", "tun05036@temple.edu")
    # database.insert(a, ignore=True)
    #
    # database.update(Account, MatchItem(Account.ID, 4), [MatchItem(Account.TOKEN, "md5(ROUND(UNIX_TIMESTAMP(CURTIME(4)) * 1000))")])
    # a = database.get_by_name(Account, "Keita Nakashima")
    # print(a)
    max = database.get_max_id(Account)
    print(database.get_field_by_name(Account, Account.TOKEN, "Keita Nakashima"))
    print(max)

    database.delete(Account, MatchItem(Account.NAME, "username"))
    print("Value" + str(database.get_field_by_name(Account, Account.ID, "username")))
    database.close()

