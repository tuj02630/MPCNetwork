classDiagram
direction BT
class node7 {
    password
    account_id
    email
    username
    status
    token
    timestamp
    TABLE
    NAME
    PASSWORD
    EMAIL
    STATUS
    TOKEN
    TIMESTAMP
    ID
    COLUMNS
    EXPLICIT_NAME
    EXPLICIT_PASSWORD
    EXPLICIT_EMAIL
    EXPLICIT_STATUS
    EXPLICIT_TOKEN
    EXPLICIT_TIMESTAMP
    EXPLICIT_ID
    EXPLICIT_COLUMNS
   __init__(self, username: str, password: str, email: str, status: str = "N",
                 token: str = "md5(ROUND(UNIX_TIMESTAMP(CURTIME(4)) * 1000))", timestamp: str = "NOW()",
                 account_id: int = None) 
   __str__(self) 
   dict_to_object(payload: dict, explicit=False) 
}
class node12 {
    duration
    criteria_id
    magnitude
    criteria_type
    TABLE
    MAGNITUDE
    DURATION
    ID
    TYPE
    COLUMNS
    EXPLICIT_MAGNITUDE
    EXPLICIT_DURATION
    EXPLICIT_TYPE
    EXPLICIT_ID
    EXPLICIT_COLUMNS
   __init__(self, criteria_type: int, magnitude: int, duration: int, criteria_id: int=None) 
   __str__(self) 
   dict_to_object(payload: dict, explicit=False) 
}
class node6 {
   object_to_dict(object: object) 
   list_object_to_dict_list(list_object: list[object]) 
   dict_to_object(payload: dict, explicit=False) 
   list_dict_to_object_list(cls, data_list: list[dict], explicit=False) 
}
class node8 {
    account_id
    name
    max_resolution
    hardware_id
    TABLE
    NAME
    ID
    ACCOUNT_ID
    RESOLUTION_NAME
    COLUMNS
    EXPLICIT_ID
    EXPLICIT_HARDWARE_ID
    EXPLICIT_NAME
    EXPLICIT_ACCOUNT_ID
    EXPLICIT_RESOLUTION_NAME
    EXPLICIT_COLUMNS
   __init__(self, name: str, max_resolution: str, hardware_id: int = None, account_id: int = None) 
   __str__(self) 
   dict_to_object(payload: dict, explicit=False) 
}
class node13 {
    notification_id
    hardware_id
    TABLE
    HARDWARE_ID
    NOTIFICATION_ID
    COLUMNS
    EXPLICIT_HARDWARE_ID
    EXPLICIT_NOTIFICATION_ID
    EXPLICIT_COLUMNS
   __init__(self, hardware_id: int, notification_id: int) 
   __str__(self) 
   dict_to_object(payload: dict, explicit=False) 
}
class node9 {
    saving_policy_id
    hardware_id
    TABLE
    HARDWARE_ID
    SAVING_POLICY_ID
    COLUMNS
    EXPLICIT_HARDWARE_ID
    EXPLICIT_SAVING_POLICY_ID
    EXPLICIT_COLUMNS
   __init__(self, hardware_id: int, saving_policy_id: int) 
   __str__(self) 
   dict_to_object(payload: dict, explicit=False) 
}
class node15 {
    notification_type
    criteria_id
    notification_id
    TABLE
    TYPE
    ID
    CRITERIA_ID
    COLUMNS
    EXPLICIT_TYPE
    EXPLICIT_ID
    EXPLICIT_CRITERIA_ID
    EXPLICIT_COLUMNS
   __init__(self, notification_type: int, criteria_id: int, notification_id: int = None) 
   __str__(self) 
   dict_to_object(payload: dict, explicit=False) 
}
class node10 {
    date
    recording_id
    account_id
    file_name
    hardware_id
    timestamp
    TABLE
    NAME
    DATE
    TIMESTAMP
    ID
    ACCOUNT_ID
    HARDWARE_ID
    COLUMNS
    EXPLICIT_FILE_NAME
    EXPLICIT_DATE
    EXPLICIT_TIMESTAMP
    EXPLICIT_ID
    EXPLICIT_ACCOUNT_ID
    EXPLICIT_HARDWARE_ID
    EXPLICIT_COLUMNS
   __init__(self,
                 file_name: str, date: str, timestamp: str,
                 recording_id: int = None, account_id: int = None, hardware_id: int = None) 
   __str__(self) 
   add_date_timestamp_from_query_para(self, queryPara) 
   dict_to_object(payload: dict, explicit=False) 
}
class node11 {
    resolution_name
    width
    height
    TABLE
    NAME
    WIDTH
    HEIGHT
    COLUMNS
    EXPLICIT_NAME
    EXPLICIT_WIDTH
    EXPLICIT_HEIGHT
    EXPLICIT_COLUMNS
   __init__(self, resolution_name: str, width: int, height: int) 
   __str__(self) 
   dict_to_object(payload: dict, explicit=False) 
}
class node14 {
    resolution_name
    max_time
    saving_policy_id
    TABLE
    ID
    MAX_TIME
    RESOLUTION_NAME
    COLUMNS
    EXPLICIT_ID
    EXPLICIT_MAX_TIME
    EXPLICIT_RESOLUTION_NAME
    EXPLICIT_COLUMNS
   __init__(self, max_time: int, resolution_name: str, saving_policy_id: int = None) 
   __str__(self) 
   dict_to_object(payload: dict, explicit=False) 
}
class node1 {
    join_type
    join_table
    join_field1
    join_field2
    INNER
    FULL
    Left
    Right
   __init__(self, join_type: str, join_table: str, join_field1: str, join_field2: str) 
}
class node4 {
    connection
   __init__(self) 
   close(self) 
   query(self, script: str) 
   insert(self, object_instance, ignore: bool = False) 
   truncate(self, table_class, foreign_key_check: bool = True, auto_increment_reset: bool = False) 
   update(self, table_class, condition_item: MatchItem, update_list: list[MatchItem]) 
   delete(self, table_class, condition_item: MatchItem) 
   gen_select_script(self, table_name: str, keys: list, match_list: list[MatchItem] = [], join_list: list[JoinItem] = []) 
   gen_insert_script(self, table_name: str, keys: list, values: list, ignore: bool) 
   gen_update_script(self, table_name: str, condition_item: MatchItem, update_items: list[MatchItem]) 
   select_payload(self, table_name: str, columns: list[str], match_list: list[MatchItem] = [], join_list: list[JoinItem] = []) 
   verify_field(self, table_class, field: str, value: str) 
   verify_fields(self, table_class, field_value_list: list[tuple]) 
   verify_id(self, table_class, id: int) 
   verify_name(self, table_class, name: str) 
   get_all(self, table_class) 
   get_field_by_name(self, table_class, field: str, name: str) 
   get_by_name(self, table_class, name: str) 
   get_by_id(self, table_class, id: int) 
   get_id_by_name(self, table_class, name: str) 
   get_max_id(self, table_class) 
   get_all_by_account_id(self, table_class, account_id: int) 
   get_all_by_account_name(self, table_class, account_name: str) 
   get_ids_by_account_id(self, table_class, account_id) 
   get_ids_by_account_name(self, table_class, account_name: str) 
   get_all_by_hardware_id(self, table_class,  hardware_id: int) 
   get_all_by_account_id_hardware_id(self, table_class, account_id: int, hardware_id: int) 
   get_by_type(self, table_class, type: int) 
   get_id_by_type(self, table_class, type: int) 
   get_saving_policy_ids_by_hardware_id(self, table_class, hardware_id: int) 
   get_hardware_ids_by_saving_policy_id(self, table_class, saving_policy_id: int) 
   get_notification_ids_by_hardware_id(self, table_class, hardware_id: int) 
   get_hardware_ids_by_notification_id(self, table_class, notification_id: int) 
   get_all_by_join_id(self, table_class, join_table_class, join_field: str, match_field: str, match_id: int) 
   update_fields(self, table_class, condition_tuple: tuple[str, str], update_list: list[tuple[str, str]]) 
   delete_by_field(self, table_class, condition_field: tuple[str, str]) 
}
class node3 {
    value
    key
   __init__(self, key: str, value, table: str = None) 
}
class node5 {
    handlers
   __init__(self) 
   get_key(self, value) 
   handle(self, action: str, httpMethod="GET") 
   add_handler(self, fun, action, httpMethod) 
}
class object {
    __doc__
    __dict__
    __slots__
    __module__
    __annotations__
   __class__(self: _T) 
   __class__(self, __type: Type[object]) 
   __init__(self) 
   __new__(cls: Type[_T]) 
   __setattr__(self, name: str, value: Any) 
   __eq__(self, o: object) 
   __ne__(self, o: object) 
   __str__(self) 
   __repr__(self) 
   __hash__(self) 
   __format__(self, format_spec: str) 
   __getattribute__(self, name: str) 
   __delattr__(self, name: str) 
   __sizeof__(self) 
   __reduce__(self) 
   __reduce_ex__(self, protocol: SupportsIndex) 
   __reduce_ex__(self, protocol: int) 
   __dir__(self) 
   __init_subclass__(cls) 
}
class node2 {
   __hash__(self) 
}

node6  -->  node7 
node6  -->  node12 
object  -->  node6 
node6  -->  node8 
node6  -->  node13 
node6  -->  node9 
node6  -->  node15 
node6  -->  node10 
node6  -->  node11 
node6  -->  node14 
object  -->  node1 
object  -->  node4 
object  -->  node3 
object  -->  node5 
node2  ..>  object 
