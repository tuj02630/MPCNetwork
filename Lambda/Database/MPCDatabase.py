import sys
from typing import Match


try:
    from Database.Data.Account import Account
except:
    from Lambda.Database.Data.Account import Account

class MatchItem:
    """
        This class aims to help create the sql scrip in Python by providing the layer of abstraction
         and the class will be mainly used in MPCdatabase.
        MatchItem class takes the key and value items so that MPCdatabase can construct proper sql script
        in WHERE clause to define the conditions.
    """
    def __init__(self, key: str, value, table: str = None):
        """Initializes the key and table variables"""
        self.key = key
        "key that is used to be matched with value"
        self.value = f"'{value}'" if type(value) is str and value[-1:] != ")" else f"{str(value)}"
        "Value that is used to check the match"


class JoinItem:
    INNER = "Inner"
    FULL = "Full"
    Left = "Left"
    Right = "Right"

    def __init__(self, join_type: str, join_table: str, join_field1: str, join_field2: str):
        """
            This class aims to help create the sql scrip in Python by providing the layer of abstraction
             and the class will be mainly used in MPCdatabase.
            JoinItem class takes the JoinType from Inner Full, Left and Right so that user can specify the
            proper type of joining two tables.
            The join table will be joined to the table that will be passed in the MPCdatabase based
            on the given join fields
        """
        self.join_type = join_type
        """Join that used to join two tables"""
        self.join_table = join_table
        """Name of table that is to be joined"""
        self.join_field1 = join_field1
        """Name of variable that is used for the "Join On" clause"""
        self.join_field2 = join_field2
        """Name of variable that is used for the "Join On" clause"""


class MPCDatabase:
    def __init__(self):
        """Reference for my sql instance. Used to perform query in database"""
        """Reference for my sql instance. Used to perform query in database"""

        print("Connected")

    def close(self):
        """Closes connection to database"""
        return

    def query(self, script: str) -> list:
        """
            Perform query in database

            Parameters:
            script: String -> sql script to be executed

            Returns:
            Lis of dictionary representing the result of the execution of sql script given
        """
        return

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

        return

    def truncate(self, table_class, foreign_key_check: bool = True, auto_increment_reset: bool = False):
        """
            Truncates the information in the table

            Parameters:

                >table_class            : class<: Class that represents the DB table that is to be truncated
                >foreign_key_check      : bool< : Flag variable to disable the foreign_key_check
                >auto_increment_reset   : bool< : Flag variable to reset the auto_increment_reset


            Returns:
            None
        """
        script = "TRUNCATE " + table_class.__name__ + ";"

        return

    def update(self, table_class, condition_item: MatchItem, update_list: list[MatchItem]):
        """
            Updates the information in the table

            Parameters:

                >table_class    : class<            : Class that represents the DB table that is to be updated
                >condition_item : MatchItem<        : Match item that is used to find the DB record in the table
                >update_list    : list[MatchItem]<  : List of pairs of key-value items that will be updated


            Returns:
            None
        """

        return None

    def delete(self, table_class, condition_item: MatchItem):
        """
           Deletes the information in the table

           Parameters:

               >table_class    : class<            : Class that represents the DB table that is to be updated
               >condition_item : MatchItem<        : Match item that is used to find the DB record in the table

           Returns:
           None
       """
        script = f"Delete From {table_class.__name__} Where {condition_item.key} = {condition_item.value}"


    def gen_select_script(self, table_name: str, keys: list, match_list: list[MatchItem] = [], join_list: list[JoinItem] = []) -> str:
        """
           Generates sql scripts and queries to specify information based on certain constraints"

           Parameters:

               >table_class : class<        : Class that represents the DB table that is to be updated
               >match_list  : MatchItem<    : Match item that is used to find the DB record in the table
               >join_list   : JoinItem<     : Join item that is used to join the several table into one table

           Returns:
               >string<     :   SQL script generated based on the parameters
       """
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

        """
           Creates a sql insert statement for adding rows to the database

           Parameters:

               >table_class : class<        : Class that represents the DB table that is to be updated
               >keys        : list[string]< : Keys  used to define the insert columns keys
               >values      : list[string]< : Value used to define the insert values for columns keys
               >ignore      : bool<         : Flag to ignore insert if there is a record of
               the same primary key in the table already

           Returns:
               >string<     :   SQL script generated based on the parameters
       """
        return "Insert " + \
               ("Ignore" if ignore else "") + \
               " Into " + table_name + \
               "(" + ",".join(keys) + ") Values (" + ",".join([(f"'{v}'" if type(v) is str and v[-1:] != ")" else f"{str(v)}") for v in values]) + ");"

    def gen_update_script(self, table_name: str, condition_item: MatchItem, update_items: list[MatchItem]):
        """Creates an sql update statement"""
        return  "Update " + table_name + \
                " Set " + ", ".join([f"{item.key} = {item.value}"for item in update_items]) + \
                " Where " + f"{condition_item.key} = {condition_item.value}"

    def select_payload(self, table_name: str, columns: list[str], match_list: list[MatchItem] = [], join_list: list[JoinItem] = []) -> dict:
        """
           Formats the result of query to dictionary format.

           Parameters:

               >table_class : class<        : Class that represents the DB table that is to be updated
               >match_list  : MatchItem<    : Match item that is used to find the DB record in the table
               >join_list   : JoinItem<     : Join item that is used to join the several table into one table

           Returns:
               >dict<       : Formatted dict response from DB
       """
        script = self.gen_select_script(table_name, columns, match_list, join_list)
        result = self.query(script)
        data = []
        for entry in result:
            data.append(dict(zip(columns, entry)))
        payload = {"column": columns, "script": script, "data": data}

        return payload

    def verify_field(self, table_class, field: str, value: str):
        """
           verifies values to see if the value for the table column exists in the given table

           Parameters:

               >table_class : class<    : Class that represents the DB table that is to be updated
               >field       : bool      : Field that is to be verified
               >value       : bool      : Value that is to be used to see the match with field

           Returns:
               >bool<       : True if the record with given field exists with value in the table
       """
        entries = self.select_payload(table_class.TABLE, table_class.COLUMNS,
                                      match_list=[MatchItem(field, value)])
        return len(entries["data"]) == 1

    def verify_fields(self, table_class, field_value_list: list[tuple]):
        """
           Verifies multiple fields

           Parameters:

               >table_class         : class<       : Class that represents the DB table that is to be updated
               >field_value_list    : list[tuple]  : List of pairs of field and value that will be checked to be matched

           Returns:
               >bool<       : True if the record with given field exists with value in the table
       """

        entries = self.select_payload(table_class.TABLE, table_class.COLUMNS,
                                      match_list=[MatchItem(item[0], item[1]) for item in field_value_list])
        return len(entries["data"]) == 1

    def verify_id(self, table_class, id: int) -> bool:
        """
           verify_field function to verify the id

           Parameters:

               >table_class : class<    : Class that represents the DB table that is to be updated
               >id          : int       : ID that should exist in the table

           Returns:
               >bool<       : True if there is a record with ID given
       """
        return self.verify_field(table_class, table_class.ID, str(id))

    def verify_name(self, table_class, name: str) -> bool:
        """
            verify_field function to verify the name

               Parameters:

                   >table_class : class<    : Class that represents the DB table that is to be updated
                   >name        : string    : Name that should exist in the table

               Returns:
                   >bool<       : True if there is a record with name given

        """
        return self.verify_field(table_class, table_class.NAME, name)

    def get_all(self, table_class) -> list:
        """
            Execute query to get the all objects in the table

            Parameters:
                >table_class   : class<     : Class that represents the DB table

            Returns:
                >list[object]< :    List of objects found in DB
        """
        payload = self.select_payload(table_class.TABLE, table_class.COLUMNS)
        return table_class.list_dict_to_object_list(payload["data"])

    def get_field_by_name(self, table_class, field: str, name: str):
        """Fetches and returns the field of specified data"""
        entries = self.select_payload(table_class.TABLE, [field],
                                      match_list=[MatchItem(table_class.NAME, name)])
        if len(entries["data"]) == 0:
            return None
        return entries["data"][0][field]

    def get_by_name(self, table_class, name: str):
        """
            Execute query to get the object related to the given name in the table

            Parameters:
                >table_class    : class<     : Class that represents the DB table
                >name           : string<   : Name of object

            Returns:
                >object<  : Object found in DB
        """
        data = self.select_payload(table_class.TABLE, table_class.COLUMNS, match_list=[MatchItem(table_class.NAME, name)])["data"]
        if len(data) != 1:
            return None
        return table_class.dict_to_object(data[0])

    def get_by_id(self, table_class, id: int):
        """
            Execute query to get the object related to the given id in the table

            Parameters:

                >table_class    : class<    : Class that represents the DB table
                >id             : int<      : Id of object

            Returns:
                >list[object]<  :    List of objects found in DB
        """
        data = self.select_payload(table_class.TABLE, table_class.COLUMNS, match_list=[MatchItem(table_class.ID, id)])["data"]
        if len(data) != 1:
            return None
        return table_class.dict_to_object(data[0])

    def get_id_by_name(self, table_class, name: str) -> int:
        """
            Execute query to get the id of object related to the given name in the table

            Parameters:
                >table_class    : class<    : Class that represents the DB table
                >name           : string<   : Name of object

            Returns:
                >id<    : Id of object found in DB
        """
        payload = self.select_payload(table_class.TABLE, [table_class.ID], [MatchItem(table_class.NAME, name)])["data"]
        if len(payload) == 0:
            return None
        return payload[0][table_class.ID]

    def get_max_id(self, table_class):
        """
            Execute query to get the max id in the table

            Parameters:
                >table_class    : class<    : Class that represents the DB table
                >name           : string<   : Name of object

            Returns:
                >id<    : Id of object found in DB
        """
        payload = self.select_payload(table_class.TABLE, [f"max({table_class.ID})"])["data"]
        if len(payload) == 0:
            return None
        return payload[0][f"max({table_class.ID})"]

    def get_all_by_account_id(self, table_class, account_id: int) -> list:
        """
            Execute query to get the all objects related to the given account_id in the table

            Parameters:
                >table_class    : class<    : Class that represents the DB table
                >account_id     : int<      : account_id of object

            Returns:
                >list[object]<  : Objects found in DB
        """
        payload = self.select_payload(table_class.TABLE, table_class.COLUMNS,
                                      match_list=[MatchItem(table_class.ACCOUNT_ID, account_id)])["data"]
        return table_class.list_dict_to_object_list(payload)

    def get_all_by_account_name(self, table_class, account_name: str) -> list:
        """
            Execute query to get the all objects related to the given name in the table

            Parameters:
                >table_class    : class<    : Class that represents the DB table
                >name           : string<   : Name of object

            Returns:
                >list[object]<  : Objects found in DB
        """
        payload = self.select_payload(
            table_class.TABLE, table_class.EXPLICIT_COLUMNS,
            match_list=[MatchItem(Account.NAME, account_name)],
            join_list=[JoinItem(JoinItem.INNER, Account.TABLE, table_class.EXPLICIT_ACCOUNT_ID, Account.EXPLICIT_ID)])["data"]

        return table_class.list_dict_to_object_list(payload, explicit=True)

    def get_ids_by_account_id(self, table_class, account_id) -> list[int]:
        """
            Execute query to get the all id of objects related to the given account_id in the table

            Parameters:
                >table_class    : class<    : Class that represents the DB table
                >account_id     : int<      : account_id of object

            Returns:
                >list[int]<     : IDs of Objects found in DB
        """
        payload = self.select_payload(table_class.TABLE, [table_class.ID], [MatchItem(table_class.ACCOUNT_ID, account_id)])
        return [v[table_class.ID] for v in payload["data"]]

    def get_ids_by_account_name(self, table_class, account_name: str):
        """
            Execute query to get the all id of objects related to the given account_name in the table

            Parameters:
                >table_class    : class<    : Class that represents the DB table
                >account_name   : string<   : account_name of object

            Returns:
                >list[int]<     : IDs of Objects found in DB
        """
        payload = self.select_payload(
            table_class.TABLE, [table_class.ID],
            match_list=[MatchItem(Account.NAME, account_name)],
            join_list=[JoinItem(JoinItem.INNER, Account.TABLE, table_class.EXPLICIT_ACCOUNT_ID,
                                Account.EXPLICIT_ID)])

        return [v[table_class.ID] for v in payload["data"]]

    def get_all_by_hardware_id(self, table_class,  hardware_id: int):
        """
            Execute query to get the all objects related to the given hardware_id in the table

            Parameters:
                >table_class    : class<    : Class that represents the DB table
                >hardware_id    : int<     : hardware_id of object

            Returns:
                >list[object]<  : Objects found in DB
        """
        payload = self.select_payload(table_class.TABLE, table_class.COLUMNS,
                                      match_list=[MatchItem(table_class.HARDWARE_ID, hardware_id)])["data"]

        return table_class.list_dict_to_object_list(payload)

    def get_all_by_account_id_hardware_id(self, table_class, account_id: int, hardware_id: int):
        """
            Execute query to get the all objects related to the given account_id and hardware_id in the table

            Parameters:
                >table_class    : class<    : Class that represents the DB table
                >account_id    : int<      : account_id of object
                >hardware_id    : int<     : hardware_id of object

            Returns:
                >list[object]<  : Objects found in DB
        """
        payload = self.select_payload(table_class.TABLE, table_class.COLUMNS,
                                      match_list=[
                                          MatchItem(table_class.ACCOUNT_ID, account_id),
                                          MatchItem(table_class.HARDWARE_ID, hardware_id)])["data"]

        return table_class.list_dict_to_object_list(payload)

    def get_by_type(self, table_class, type: int):
        """
            Execute query to get the object related to the given name in the table

            Parameters:
                >table_class    : class<     : Class that represents the DB table
                >type           : string<   : Type of object

            Returns:
                >object<  : Object found in DB
        """
        data = self.select_payload(table_class.TABLE, table_class.COLUMNS, match_list=[MatchItem(table_class.TYPE, type)])[
            "data"]
        if len(data) != 1:
            return None
        return table_class.dict_to_object(data[0])

    def get_id_by_type(self, table_class, type: int) -> id:
        """
            Execute query to get the id of object related to the given type in the table

            Parameters:
                >table_class    : class<    : Class that represents the DB table
                >type           : string<   : Type of object

            Returns:
                >id<    : Id of object found in DB
        """
        payload = self.select_payload(table_class.TABLE, [table_class.ID], [MatchItem(table_class.TYPE, type)])["data"]
        if len(payload) == 0:
            return None
        return payload[0][table_class.ID]

    def get_saving_policy_ids_by_hardware_id(self, table_class, hardware_id: int) -> list[int]:
        """
            Execute query to get the all saving policy ids of objects related to the given hardware_id in the table

            Parameters:
                >table_class    : class<    : Class that represents the DB table
                >hardware_id    : int<      : hardware_id of object

            Returns:
                >list[int]<     : IDs of Objects found in DB
        """
        payload = self.select_payload(table_class.TABLE, [table_class.SAVING_POLICY_ID], [MatchItem(table_class.HARDWARE_ID, hardware_id)])
        return [v[table_class.SAVING_POLICY_ID] for v in payload["data"]]

    def get_hardware_ids_by_saving_policy_id(self, table_class, saving_policy_id: int) -> list[int]:
        """
            Execute query to get the all hardware ids of objects related to the given saving_policy_id in the table

            Parameters:
                >table_class        : class<    : Class that represents the DB table
                >saving_policy_id   : int<      : saving_policy_id of object

            Returns:
                >list[int]<     : IDs of Objects found in DB
        """
        payload = self.select_payload(table_class.TABLE, [table_class.HARDWARE_ID], [MatchItem(table_class.SAVING_POLICY_ID, saving_policy_id)])
        return [v[table_class.HARDWARE_ID] for v in payload["data"]]

    def get_notification_ids_by_hardware_id(self, table_class, hardware_id: int) -> list[int]:
        """
            Execute query to get the all notification ids of objects related to the given hardware_id in the table

            Parameters:
                >table_class    : class<    : Class that represents the DB table
                >hardware_id    : int<      : hardware_id of object

            Returns:
                >list[int]<     : IDs of Objects found in DB
        """
        payload = self.select_payload(table_class.TABLE, [table_class.NOTIFICATION_ID], [MatchItem(table_class.HARDWARE_ID, hardware_id)])
        return [v[table_class.NOTIFICATION_ID] for v in payload["data"]]

    def get_hardware_ids_by_notification_id(self, table_class, notification_id: int) -> list[int]:
        """
            Execute query to get the all hardware ids of objects related to the given notification_id in the table

            Parameters:
                >table_class    : class<    : Class that represents the DB table
                >notification_id    : int<      : notification_id of object

            Returns:
                >list[int]<     : IDs of Objects found in DB
        """
        payload = self.select_payload(table_class.TABLE, [table_class.HARDWARE_ID], [MatchItem(table_class.NOTIFICATION_ID, notification_id)])
        return [v[table_class.HARDWARE_ID] for v in payload["data"]]

    def get_all_by_join_id(self, table_class, join_table_class, join_field: str, match_field: str, match_id: int):
        """
            Execute query to get the all hardware ids of objects related to the given notification_id in the table

            Parameters:
                >table_class        : class<    : Class that represents the DB table
                >join_table_class   : string<   : name of table that will be joined to the table
                >join_field         : string<   : The name of field that the tables will be joined on
                >match_field        : string<   : The name of field that the tables will be matched with
                >match_id           : int<      : ID that the match field will be matched to

            Returns:
                >list[object]<      : Objects found in DB
        """
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
        """
            Updates the information in the table

            Parameters:

                >table_class    : class<            : Class that represents the DB table that is to be updated
                >condition_item : MatchItem<        : Match item that is used to find the DB record in the table
                >update_list    : list[MatchItem]<  : List of pairs of key-value items that will be updated


            Returns:
            None
        """
        self.update(table_class, MatchItem(condition_tuple[0], condition_tuple[1]),
                    [MatchItem(item[0], item[1]) for item in update_list])

    def delete_by_field(self, table_class, condition_field: tuple[str, str]):
        """
            Deletes the records by given fields

            Parameters:

                >table_class    : class<            : Class that represents the DB table that is to be updated
                >condition_item : MatchItem<        : Match item that is used to find the DB record in the table
                >update_list    : list[MatchItem]<  : List of pairs of key-value items that will be updated


            Returns:
            None
        """
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

