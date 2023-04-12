import base64
import json
import random

from Database.MPCDatabase import MPCDatabase
from Database.Data.Recording import Recording
from Database.Data.Account import Account, AccountStatus
from Database.Data.Hardware import Hardware
from Database.Data.Criteria import Criteria
from Database.Data.Notification import Notification
from Database.Data.Resolution import Resolution
from Database.Data.Saving_Policy import Saving_Policy
from Database.Data.Hardware_has_Saving_Policy import Hardware_has_Saving_Policy
from Database.Data.Hardware_has_Notification import Hardware_has_Notification
from Error import Error

from mpc_api import MPC_API
import boto3
import re

api = MPC_API()
s3 = boto3.client('s3')
database = MPCDatabase()


def lambda_handler(event, context):
    """Manages the database queries and speaks to the imported libraries to make things possible"""
    print(event)
    print(context)

    status = 200
    resource = event["resource"].lower()
    httpMethod = event["httpMethod"].lower()

    queryPara = {}
    pathPara = {}

    if "queryStringParameters" in event and event["queryStringParameters"] is not None:
        queryPara = event["queryStringParameters"]

    if "pathParameters" in event and event["pathParameters"] is not None:
        pathPara = event["pathParameters"]

    if "body" in event and event["body"] is not None:
        event["body"] = json.loads(event["body"])

    try:
        if resource in api.handlers:
            return api.handlers[resource][httpMethod](event, pathPara, queryPara)
        else:
            return api.handlers["/"]["get"]({"event": event, "context": str(context)}, pathPara, queryPara)
    except Exception as err:
        status = 500
        data = {"error": str(err)}

    return {
        'statusCode': status,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(data)
    }


def json_payload(body, error=False):
    """If there's an error, return an error, if not, then return the proper status code, headers, and body"""
    if error:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({"body": body})
        }
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(body)
    }


def check_email(email):
    """Returns true if the email is in the proper format, returns false if it's not"""
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, email):
        return True
    else:
        return False


def check_password(password):
    """Makes sure the password is in the correct format and is at least 8 characters"""
    if re.fullmatch(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$", password):
        return True
    else:
        return False


def get_all(table_class):
    """Gets all specified items in the database"""
    items: list[table_class] = database.get_all(table_class)
    dict_list = table_class.list_object_to_dict_list(items)

    return json_payload(dict_list)


def get_by_id(table_class, pathPara):
    """Gets all information in the database of the specified id"""
    id = pathPara["id"]
    item: table_class = database.get_by_id(table_class, id)
    body = table_class.object_to_dict(item)

    return json_payload(body)


def get_by_name(table_class, pathPara):
    """Gets all information based on the specified name"""
    name = pathPara["name"]
    resolution = database.get_by_name(table_class, name)
    body = table_class.object_to_dict(resolution)

    return json_payload(body)


def delete_by_id(table_class, pathPara):
    """Deletes information based on the specified id"""
    database.delete_by_field(table_class, (table_class.ID, pathPara["id"]))

    return json_payload({})


def delete_by_name(table_class, pathPara):
    """Deletes information from the database based on the specified name"""
    database.delete_by_field(table_class, (table_class.NAME, pathPara["name"]))

    return json_payload({})


def delete_by_hardware_id(table_class, pathPara):
    """Deletes information from the database based on the specified hardware id"""
    database.delete_by_field(table_class, (table_class.HARDWARE_ID, pathPara["hardware_id"]))

    return json_payload({})


def update_by_id(table_class, pathPara, queryPara):
    """Updates the database rows in a table based on the specified id"""
    id = pathPara["id"]
    update_keys = set(table_class.COLUMNS).intersection(queryPara.keys())
    if table_class.ID in update_keys:
        update_keys.remove(table_class.ID)
    database.update_fields(table_class, (table_class.ID, id), [(key, queryPara[key]) for key in update_keys])

    return json_payload({})


@api.handle("/")
def home(event, pathPara, queryPara):
    """Handles query events using the json libraries and returns a labeled array"""
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(event)
    }


@api.handle("/", httpMethod="POST")
def home(event, pathPara, queryPara):
    """Handles Query events using the json libraries and returns a labeled array"""

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(event)
    }


@api.handle("/image")
def image_request(event, pathPara, queryPara):
    """Handles query events using the json libraries and handles images in jpeg format"""
    image_name = "bird-thumbnail.jpg"
    response = s3.get_object(
        Bucket='mpc-capstone',
        Key=image_name,
    )
    content_type = "image/jpeg"
    image = response['Body'].read()
    print(base64.b64encode(image).decode('utf-8'))
    return {
        'headers': {"Content-Type": content_type},
        'statusCode': 200,
        'body': base64.b64encode(image).decode('utf-8'),
        'isBase64Encoded': True
    }


@api.handle("/image/{image_name}")
def image_request(event, pathPara, queryPara):
    """Requests an image from the server and makes sure it's in the right format"""
    image_name = pathPara["image_name"]
    response = s3.get_object(
        Bucket='mpc-capstone',
        Key=image_name,
    )
    if image_name[-4:] == ".png":
        content_type = "image/png"
    elif image_name[-4:] == ".jpg" or image_name[-4:] == ".jpeg":
        content_type = "image/jpeg"
    else:
        raise ValueError("Invalid image name: " + image_name)
    image = response['Body'].read()
    print(base64.b64encode(image).decode('utf-8'))
    return {
        'headers': {"Content-Type": content_type},
        'statusCode': 200,
        'body': base64.b64encode(image).decode('utf-8'),
        'isBase64Encoded': True
    }


@api.handle("/video")
def video_request(event, pathPara, queryPara):
    """Requests video from the server and makes sure it's in the correct format"""
    video_name = "cat.mp4"
    response = s3.get_object(
        Bucket='mpc-capstone',
        Key=video_name,
    )
    content_type = "video/mp4"
    image = response['Body'].read()
    print(base64.b64encode(image).decode('utf-8'))
    return {
        'headers': {"Content-Type": content_type},
        'statusCode': 200,
        'body': base64.b64encode(image).decode('utf-8'),
        'isBase64Encoded': True
    }


@api.handle("/video/{video_name}")
def video_request_by_filename(event, pathPara, queryPara):
    """Requests video based on the given file path"""
    video_name = pathPara["video_name"]

    response = s3.get_object(
        Bucket='mpc-capstone',
        Key=video_name,
    )
    if video_name[-4:] == ".mp4":
        content_type = "video/mp4"
    else:
        raise ValueError("Invalid image name: " + video_name)
    image = response['Body'].read()
    print(base64.b64encode(image).decode('utf-8'))
    return {
        'headers': {"Content-Type": content_type},
        'statusCode': 200,
        'body': base64.b64encode(image).decode('utf-8'),
        'isBase64Encoded': True
    }


@api.handle("/account")
def accounts_request(event, pathPara, queryPara):
    """Gets all rows and columns of the Account table"""
    return get_all(Account)


@api.handle("/account/signup", httpMethod="POST")
def account_signup(event, pathPara, queryPara):
    """Handles new accounts from users and makes sure user information is in the correct format"""
    body = event["body"]
    error = []
    if database.verify_name(Account, body[Account.NAME]):
        error.append(Error.NAME_DUPLICATE)
    if database.verify_field(Account, Account.EMAIL, body[Account.EMAIL]):
        error.append(Error.EMAIL_DUPLICATE)
    if not check_email(body["email"]):
        error.append(Error.INVALID_EMAIL_FORMAT)
    if not check_password(body["password"]):
        error.append(Error.PASSWORD_WEAK)

    if len(error) == 0:
        database.insert(Account(body["username"], body["password"], body["email"], timestamp="NOW()"))
        return json_payload({"message": "Account created"})
    return json_payload({"message": "\n".join(error)}, True)


@api.handle("/account/signin", httpMethod="POST")
def account_signin(event, pathPara, queryPara):
    """Handles users signing into their account by verifying their username and password in the database"""
    body: dict = event["body"]

    if database.verify_fields(
            Account, [(Account.NAME, body[Account.NAME]), (Account.PASSWORD, body[Account.PASSWORD])]):
        field = Account.NAME

    elif database.verify_fields(
            Account, [(Account.EMAIL, body[Account.NAME]), (Account.PASSWORD, body[Account.PASSWORD])]):
        field = Account.EMAIL
    else:
        return json_payload({"message": "login failed: " + Error.LOGIN_FAILED}, True)

    timestamp_check = database.varidate_timestamp(Account, field, body[Account.NAME])
    database.update_fields(Account, (field, body[field]),
                           [(Account.TOKEN, "md5(ROUND(UNIX_TIMESTAMP(CURTIME(4)) * 1000))"),
                            (Account.TIMESTAMP, "NOW()")])
    if not timestamp_check:
        return json_payload({"message": "login failed: " + Error.TIMESTAMP_ERROR}, True)

    account: Account = database.get_by_field(Account, field, body[field])
    return json_payload({"message": "Signed in to Account",
                         Account.TOKEN: account.token, Account.NAME: account.username, Account.EMAIL: account.email})


@api.handle("/account/reset", httpMethod="POST")
def account_signin(event, pathPara, queryPara):
    """Handles users reset their account by verifying their username in the database"""
    body: dict = event["body"]

    if database.verify_fields(
            Account, [(Account.NAME, body[Account.NAME])]):
        field = Account.NAME

    elif database.verify_fields(
            Account, [(Account.EMAIL, body[Account.NAME])]):
        field = Account.EMAIL
    else:
        return json_payload({"message": "Code sent: "})
    code = str(random.randint(100000, 999999))
    database.update_fields(Account, (field, body[Account.NAME]), [(Account.CODE, code)])
    print(code)

    ## TODO send email
    return json_payload({"message": "Code sent"})


@api.handle("/account/code", httpMethod="POST")
def account_signin(event, pathPara, queryPara):
    """Handles users reset their account by verifying their username in the database"""
    body: dict = event["body"]

    if database.verify_fields(Account, [(Account.NAME, body[Account.NAME])]):
        field = Account.NAME

    elif database.verify_fields(Account, [(Account.EMAIL, body[Account.NAME])]):
        field = Account.EMAIL
    else:
        return json_payload({"message": Error.INCORRECT_CODE}, True)

    timestamp_check = database.varidate_timestamp(Account, field, body[Account.NAME])
    database.update_fields(Account, (field, body[Account.NAME]), [(Account.TIMESTAMP, "NOW()")])
    if not timestamp_check:
        return json_payload({"message": "login failed: " + Error.TIMESTAMP_ERROR}, True)

    if database.verify_fields(Account, [(field, body[field]), (Account.CODE, body[Account.CODE])]):
        database.update_fields(Account, (field, body[Account.NAME]),
                               [(Account.TOKEN, "md5(ROUND(UNIX_TIMESTAMP(CURTIME(4)) * 1000))"),
                                (Account.TIMESTAMP, "NOW()")])

        token = database.get_field_by_field(Account, Account.TOKEN, field, body[Account.NAME])
        return json_payload({"message": "Code confirmed", Account.TOKEN: token})
    return json_payload({"message": Error.INCORRECT_CODE}, True)


@api.handle("/account/password", httpMethod="POST")
def account_signin(event, pathPara, queryPara):
    """Handles users reset their account by verifying their username in the database"""
    body: dict = event["body"]

    if database.verify_fields(
            Account, [(Account.NAME, body[Account.NAME]), (Account.CODE, body[Account.CODE]),
                      (Account.TOKEN, body[Account.TOKEN])]
    ):
        field = Account.NAME

    elif database.verify_fields(
            Account, [(Account.EMAIL, body[Account.NAME]), (Account.CODE, body[Account.CODE]),
                      (Account.TOKEN, body[Account.TOKEN])]
    ):
        field = Account.EMAIL
    else:
        return json_payload({"message": Error.UNKNOWN_ACCOUNT}, True)

    timestamp_check = database.varidate_timestamp(Account, field, body[Account.NAME])
    database.update_fields(Account, (field, body[Account.NAME]),
                           [(Account.TOKEN, "md5(ROUND(UNIX_TIMESTAMP(CURTIME(4)) * 1000))"),
                            (Account.PASSWORD, body[Account.PASSWORD]),
                            (Account.CODE, None),
                            (Account.TIMESTAMP, "NOW()")])
    if not timestamp_check:
        return json_payload({"message": "login failed: " + Error.TIMESTAMP_ERROR}, True)

    token = database.get_field_by_field(Account, Account.TOKEN, field, body[Account.NAME])
    return json_payload({"message": "Password reset successful", Account.TOKEN: token})


@api.handle("/account", httpMethod="POST")
def account_insert(event, pathPara, queryPara):
    """Inserts new row into the account table which represents a new user"""
    account: Account = Account(queryPara["username"], queryPara["password"], queryPara["email"], "C")
    database.insert(account)
    a: Account = database.get_by_name(Account, queryPara["username"])
    return json_payload({"id": a.account_id, "token": a.token})


@api.handle("/account/{id}")
def account_request_by_id(event, pathPara, queryPara):
    """Gets account based on specified id"""
    return get_by_id(Account, pathPara)


@api.handle("/hardware")
def hardware_request(event, pathPara, queryPara):
    """Gets all rows and columns of the hardware table"""
    return get_all(Hardware)


@api.handle("/hardware", httpMethod="POST")
def hardware_insert(event, pathPara, queryPara):
    """Inserts new rows into the hardware table based on account id"""
    if "account_id" in queryPara:
        hardware = Hardware(queryPara["name"], queryPara["max_resolution"], account_id=queryPara["account_id"])
    else:
        hardware = Hardware(queryPara["name"], queryPara["max_resolution"])
    database.insert(hardware)
    id = database.get_id_by_name(Hardware, queryPara["name"])
    return json_payload({"id": id})


@api.handle("/hardware/{id}")
def hardware_request_by_id(event, pathPara, queryPara):
    """Gets information from the hardware table based on specified id"""
    return get_by_id(Hardware, pathPara)


@api.handle("/hardware/{id}", httpMethod="DELETE")
def hardware_delete_by_id(event, pathPara, queryPara):
    """Deletes rows from the hardware table of the specified id"""
    return delete_by_id(Hardware, pathPara)


@api.handle("/hardware/{id}", httpMethod="PUT")
def hardware_update_by_id(event, pathPara, queryPara):
    """Updates the hardware table based on the specified id"""
    return update_by_id(Hardware, pathPara, queryPara)


@api.handle("/recording")
def recordings_request(event, pathPara, queryPara):
    """Gets recordings from the server and and formats the information from AWS into appropriate variables for processing"""
    recordings: list[Recording] = database.get_all(Recording)
    for rec in recordings:
        bucket = "mpc-capstone"
        rec.url = f"https://{bucket}.s3.amazonaws.com/{rec.file_name}"
        host = event["multiValueHeaders"]["Host"][0]
        stage = event["requestContext"]["stage"]
        path = "storage"
        rec.alt_url = f"https://{host}/{stage}/{path}/{bucket}/{rec.file_name}"

    dict_list = Recording.list_object_to_dict_list(recordings)

    return json_payload(dict_list)


@api.handle("/recording", httpMethod="POST")
def recording_insert(event, pathPara, queryPara):
    """Inserts a recording into the database of the specified account id"""
    recording = Recording(queryPara["file_name"], "CURDATE()", "NOW()",
                          account_id=queryPara["account_id"], hardware_id=queryPara["hardware_id"])
    recording.add_date_timestamp_from_query_para(queryPara)
    database.insert(recording)
    id = database.get_id_by_name(Recording, queryPara["file_name"])
    return json_payload({"id": id})


@api.handle("/recording/{id}")
def recording_request_by_id(event, pathPara, queryPara):
    """Gets recording from AWS and stores it in appropriate variables for processing"""
    id = pathPara["id"]
    recording = database.get_by_id(Recording, id)
    bucket = "mpc-capstone"
    recording.url = f"https://{bucket}.s3.amazonaws.com/{recording.file_name}"
    host = event["multiValueHeaders"]["Host"][0]
    stage = event["requestContext"]["stage"]
    path = "storage"
    recording.alt_url = f"https://{host}/{stage}/{path}/{bucket}/{recording.file_name}"
    body = Recording.object_to_dict(recording)

    return json_payload(body)


@api.handle("/recording/{id}", httpMethod="DELETE")
def recording_delete_by_id(event, pathPara, queryPara):
    """Deletes recording from table based on specified id"""
    return delete_by_id(Recording, pathPara)


@api.handle("/recording/{id}", httpMethod="PUT")
def recording_update_by_id(event, pathPara, queryPara):
    """Updates recording table based on specified id"""
    return update_by_id(Recording, pathPara, queryPara)


@api.handle("/criteria")
def criteria_request(event, pathPara, queryPara):
    """Gets all rows and columns from the Criteria table"""
    return get_all(Criteria)


@api.handle("/criteria", httpMethod="POST")
def criteria_insert(event, pathPara, queryPara):
    """Inserts new rows into the criteria table"""
    criteria = Criteria(queryPara["criteria_type"], queryPara["magnitude"], queryPara["duration"])
    database.insert(criteria)
    return json_payload({})


@api.handle("/criteria/{id}")
def criteria_request_by_id(event, pathPara, queryPara):
    """Gets all information from Criteria table based on specified id"""
    return get_by_id(Criteria, pathPara)


@api.handle("/criteria/{id}", httpMethod="DELETE")
def criteria_delete_by_id(event, pathPara, queryPara):
    """Deletes rows from the criteria table based on the specified id"""
    return delete_by_id(Criteria, pathPara)


@api.handle("/criteria/{id}", httpMethod="PUT")
def criteria_update_by_id(event, pathPara, queryPara):
    """Updates the criteria table rows based on the specified id"""
    return update_by_id(Criteria, pathPara, queryPara)


@api.handle("/notification")
def notification_request(event, pathPara, queryPara):
    """Requests notifications from the hardware based on specified notification id"""
    notifications: list[Notification] = database.get_all(Notification)
    for notification in notifications:
        notification.hardware = database.get_hardware_ids_by_notification_id(Hardware_has_Notification,
                                                                             notification.notification_id)
    dict_list = Notification.list_object_to_dict_list(notifications)

    return json_payload(dict_list)


@api.handle("/notification", httpMethod="POST")
def notification_insert(event, pathPara, queryPara):
    """Inserts rows into the notification table"""
    notification = Notification(queryPara["notification_type"], queryPara["criteria_id"])
    database.insert(notification)
    # id = database.get_id_by_type(Notification, queryPara["notification_type"])
    id = database.get_max_id(Notification)
    if "hardware_id" in queryPara:
        hardware_notification = Hardware_has_Notification(queryPara["hardware_id"], id)
        database.insert(hardware_notification)
    return json_payload({"id": id})


@api.handle("/notification/{id}")
def notification_request_by_id(event, pathPara, queryPara):
    """Gets notification from hardware component based on the notification id"""
    id = pathPara["id"]
    notification = database.get_by_id(Notification, id)
    notification.hardware = database.get_hardware_ids_by_notification_id(Hardware_has_Notification,
                                                                         notification.notification_id)
    body = Notification.object_to_dict(notification)

    return json_payload(body)


@api.handle("/notification/{id}", httpMethod="DELETE")
def notification_delete_by_id(event, pathPara, queryPara):
    """Deletes notification from the table based on specified id"""
    return delete_by_id(Notification, pathPara)


@api.handle("/notification/{id}", httpMethod="PUT")
def notification_update_by_id(event, pathPara, queryPara):
    """Updates notification table with new information"""
    return update_by_id(Notification, pathPara, queryPara)


@api.handle("/notification/{id}/add/{hardware_id}", httpMethod="POST")
def notification_insert_hardware(event, pathPara, queryPara):
    """Adds new notification into the into the system from a hardware component"""
    hardware_notification = Hardware_has_Notification(pathPara["hardware_id"], pathPara["id"])
    database.insert(hardware_notification)
    return json_payload({})


@api.handle("/notification/{id}/hardware")
def notification_hardware_request(event, pathPara, queryPara):
    """Gets notification from specified hardware component based on id"""
    data = database.get_all_by_join_id(Hardware, Hardware_has_Notification,
                                       "EXPLICIT_HARDWARE_ID", "EXPLICIT_NOTIFICATION_ID", pathPara["id"])
    return json_payload(Hardware.list_object_to_dict_list(data))


@api.handle("/notification/{id}/hardware/{hardware_id}", httpMethod="DELETE")
def notification_hardware_delete_by_id(event, pathPara, queryPara):
    """Deletes notification based on id"""
    return delete_by_hardware_id(Hardware_has_Notification, pathPara)


@api.handle("/resolution")
def resolution_request(event, pathPara, queryPara):
    """Gets all rows and columns from the Resolution table"""
    return get_all(Resolution)


@api.handle("/resolution", httpMethod="POST")
def resolution_insert(event, pathPara, queryPara):
    """Inserts new rows into the resolution table"""
    resolution = Resolution(queryPara["resolution_name"], queryPara["width"], queryPara["height"])
    database.insert(resolution)
    return json_payload({})


@api.handle("/resolution/{name}")
def resolution_request_by_name(event, pathPara, queryPara):
    """Gets rows from Resolution table based on name"""
    return get_by_name(Resolution, pathPara)


@api.handle("/resolution/{name}", httpMethod="DELETE")
def resolution_delete_by_id(event, pathPara, queryPara):
    """Deletes rows from Resolution table based on id"""
    return delete_by_name(Resolution, pathPara)


@api.handle("/resolution/{name}", httpMethod="PUT")
def resolution_update_by_id(event, pathPara, queryPara):
    """Updates the resolution table based on specified id"""
    return update_by_id(Notification, pathPara, queryPara)


@api.handle("/saving_policy")
def saving_policy_request(event, pathPara, queryPara):
    """Gets saving policy based on saving policy id"""
    saving_policies = database.get_all(Saving_Policy)
    for policy in saving_policies:
        policy.hardware = database.get_hardware_ids_by_saving_policy_id(Hardware_has_Saving_Policy,
                                                                        policy.saving_policy_id)
    dict_list = Saving_Policy.list_object_to_dict_list(saving_policies)

    return json_payload(dict_list)


@api.handle("/saving_policy", httpMethod="POST")
def saving_policy_insert(event, pathPara, queryPara):
    """Inserts new saving policy into saving_policy table"""
    saving_policy = Saving_Policy(queryPara["max_time"], queryPara["resolution_name"])
    database.insert(saving_policy)
    return json_payload({})


@api.handle("/saving_policy/{id}")
def saving_policy_request_by_id(event, pathPara, queryPara):
    """Gets saving policy based on specified id"""
    id = pathPara["id"]
    saving_policy = database.get_by_id(Saving_Policy, id)
    saving_policy.hardware = database.get_hardware_ids_by_saving_policy_id(Hardware_has_Saving_Policy,
                                                                           saving_policy.saving_policy_id)
    body = Saving_Policy.object_to_dict(saving_policy)

    return json_payload(body)


@api.handle("/saving_policy/{id}", httpMethod="DELETE")
def saving_policy_delete_by_id(event, pathPara, queryPara):
    """Deletes saving policy based on specified id"""
    return delete_by_id(Saving_Policy, pathPara)


@api.handle("/saving_policy/{id}", httpMethod="PUT")
def saving_policy_update_by_id(event, pathPara, queryPara):
    """Updates saving policy table based on id"""
    return update_by_id(Saving_Policy, pathPara, queryPara)


@api.handle("/saving_policy/{id}/add/{hardware_id}", httpMethod="POST")
def saving_policy_add_hardware(event, pathPara, queryPara):
    """Adds hardware component to the saving policy table based on hardware id"""
    saving_policy = Hardware_has_Saving_Policy(pathPara["hardware_id"], pathPara["id"])
    database.insert(saving_policy)
    return json_payload({})


@api.handle("/saving_policy/{id}/hardware")
def saving_policy_hardware_request(event, pathPara, queryPara):
    """Gets information from saving policy and hardware table with a join"""
    data = database.get_all_by_join_id(Hardware, Hardware_has_Saving_Policy,
                                       "EXPLICIT_HARDWARE_ID", "EXPLICIT_SAVING_POLICY_ID", pathPara["id"])
    return json_payload(Hardware.list_object_to_dict_list(data))


@api.handle("/saving_policy/{id}/hardware/{hardware_id}", httpMethod="DELETE")
def saving_policy_hardware_delete_by_id(event, pathPara, queryPara):
    """Deletes saving policy based on the specified hardware id"""
    return delete_by_hardware_id(Hardware_has_Saving_Policy, pathPara)


if __name__ == "__main__":
    import urllib

    # database.insert(Notification(10000, criteria_id=3), ignore=True)
    max = database.get_max_id(Notification)
    event = {
        "resource": "/account/code",
        "httpMethod": "POST",
        "body": """{
            "username": "username1",
            "password": "password",
            "email": "default@temple.edu",
            "code": "227722"
        }""",
        "pathParameters": {
            "id": max
        },
        "queryStringParameters": {
            "notification_type": 10
        }
    }
    print(check_password("password@12Apd"))
    print(lambda_handler(event, None))
    print("{:06}".format(random.randint(100000, 999999)))
    database.close()
