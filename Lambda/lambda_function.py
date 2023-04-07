import base64
import json

from Database.MPCDatabase import MPCDatabase
from Database.Data.Recording import Recording
from Database.Data.Account import Account
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
        if resource in  api.handlers:
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


def json_payload(body, error: list = []):
    if len(error) != 0:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({"body": body, "error": error})
        }
    return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(body)
    }


def check_email(email):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, email):
        return True
    else:
        return False


def check_password(password):
    if re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
        return True
    else:
        return False


def get_all(table_class):
    items: list[table_class] = database.get_all(table_class)
    dict_list = table_class.list_object_to_dict_list(items)

    return json_payload(dict_list)


def get_by_id(table_class, pathPara):
    id = pathPara["id"]
    item: table_class = database.get_by_id(table_class, id)
    body = table_class.object_to_dict(item)

    return json_payload(body)


def get_by_name(table_class, pathPara):
    name = pathPara["name"]
    resolution = database.get_by_name(table_class, name)
    body = table_class.object_to_dict(resolution)

    return json_payload(body)


def delete_by_id(table_class, pathPara):
    database.delete_by_field(table_class, (table_class.ID, pathPara["id"]))

    return json_payload({})


def delete_by_name(table_class, pathPara):
    database.delete_by_field(table_class, (table_class.NAME, pathPara["name"]))

    return json_payload({})


def delete_by_hardware_id(table_class, pathPara):
    database.delete_by_field(table_class, (table_class.HARDWARE_ID, pathPara["hardware_id"]))

    return json_payload({})


def update_by_id(table_class, pathPara, queryPara):
    id = pathPara["id"]
    update_keys = set(table_class.COLUMNS).intersection(queryPara.keys())
    update_keys.remove(table_class.ID)
    database.update_fields(table_class, (table_class.ID, id), [(key, queryPara[key]) for key in update_keys])

    return json_payload({})


@api.handle("/")
def home(event, pathPara, queryPara):
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(event)
    }


@api.handle("/", httpMethod="POST")
def home(event, pathPara, queryPara):

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(event)
    }


@api.handle("/image")
def image_request(event, pathPara, queryPara):
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
    return get_all(Account)


@api.handle("/account/signup", httpMethod="POST")
def account_signup(event, pathPara, queryPara):
    body = event["body"]
    error = []
    if database.verify_name(Account, body[Account.NAME]):
        error.append(Error.NAME_DUPLICATE)
    if not check_email(body["email"]):
        error.append(Error.INVALID_EMAIL_FORMAT)
    if not check_password(body["password"]):
        error.append(Error.PASSWORD_WEAK)

    if len(error) == 0:
        database.insert(Account(body["username"], body["password"], body["email"]))
        return json_payload({"message": "Account created"})
    return json_payload(None, error)


@api.handle("/account/signin", httpMethod="POST")
def account_signin(event, pathPara, queryPara):
    body: dict = event["body"]
    error = []
    if not database.verify_name(Account, body[Account.NAME]):
        error.append(Error.NAME_NOT_FOUND)
    if not database.verify_fields(
            Account, [(Account.NAME, body[Account.NAME]), (Account.PASSWORD, body[Account.PASSWORD])]):
        error.append(Error.PASSWORD_MISMATCH)

    # update_keys = set(Account.COLUMNS).intersection(body.keys())

    if len(error) == 0:
        database.update_fields(Account,
                               (Account.NAME, body[Account.NAME]),
                               [(Account.TOKEN, "md5(ROUND(UNIX_TIMESTAMP(CURTIME(4)) * 1000))")])
        token = database.get_field_by_name(Account, Account.TOKEN, body[Account.NAME])
        return json_payload({"message": "Signed in to Account", Account.TOKEN:  token})
    return json_payload(None, error)


@api.handle("/account", httpMethod="POST")
def account_insert(event, pathPara, queryPara):
    account: Account = Account(queryPara["username"], queryPara["password"], queryPara["email"], "C")
    database.insert(account)
    a: Account = database.get_by_name(Account, queryPara["username"])
    return json_payload({"id": a.account_id, "token": a.token})


@api.handle("/account/{id}")
def account_request_by_id(event, pathPara, queryPara):
    return get_by_id(Account, pathPara)


@api.handle("/hardware")
def hardware_request(event, pathPara, queryPara):
    return get_all(Hardware)


@api.handle("/hardware", httpMethod="POST")
def hardware_insert(event, pathPara, queryPara):
    if "account_id" in queryPara:
        hardware = Hardware(queryPara["name"], queryPara["max_resolution"], account_id=queryPara["account_id"])
    else:
        hardware = Hardware(queryPara["name"], queryPara["max_resolution"])
    database.insert(hardware)
    id = database.get_id_by_name(Hardware, queryPara["name"])
    return json_payload({"id": id})


@api.handle("/hardware/{id}")
def hardware_request_by_id(event, pathPara, queryPara):
    return get_by_id(Hardware, pathPara)


@api.handle("/hardware/{id}", httpMethod="DELETE")
def hardware_delete_by_id(event, pathPara, queryPara):
    return delete_by_id(Hardware, pathPara)


@api.handle("/hardware/{id}", httpMethod="PUT")
def hardware_update_by_id(event, pathPara, queryPara):
    return update_by_id(Hardware, pathPara, queryPara)


@api.handle("/recording")
def recordings_request(event, pathPara, queryPara):
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
    recording = Recording(queryPara["file_name"], "CURDATE()", "NOW()",
                          account_id=queryPara["account_id"], hardware_id=queryPara["hardware_id"])
    recording.add_date_timestamp_from_query_para(queryPara)
    database.insert(recording)
    id = database.get_id_by_name(Recording, queryPara["file_name"])
    return json_payload({"id": id})


@api.handle("/recording/{id}")
def recording_request_by_id(event, pathPara, queryPara):
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
    return delete_by_id(Recording, pathPara)


@api.handle("/recording/{id}", httpMethod="PUT")
def recording_update_by_id(event, pathPara, queryPara):
    return update_by_id(Recording, pathPara, queryPara)


@api.handle("/criteria")
def criteria_request(event, pathPara, queryPara):
    return get_all(Criteria)


@api.handle("/criteria", httpMethod="POST")
def criteria_insert(event, pathPara, queryPara):
    criteria = Criteria(queryPara["criteria_type"], queryPara["magnitude"], queryPara["duration"])
    database.insert(criteria)
    return json_payload({})


@api.handle("/criteria/{id}")
def criteria_request_by_id(event, pathPara, queryPara):
    return get_by_id(Criteria, pathPara)


@api.handle("/criteria/{id}", httpMethod="DELETE")
def criteria_delete_by_id(event, pathPara, queryPara):
    return delete_by_id(Criteria, pathPara)


@api.handle("/criteria/{id}", httpMethod="PUT")
def criteria_update_by_id(event, pathPara, queryPara):
    return update_by_id(Criteria, pathPara, queryPara)


@api.handle("/notification")
def notification_request(event, pathPara, queryPara):
    notifications: list[Notification] = database.get_all(Notification)
    for notification in notifications:
        notification.hardware = database.get_hardware_ids_by_notification_id(Hardware_has_Notification, notification.notification_id)
    dict_list = Notification.list_object_to_dict_list(notifications)

    return json_payload(dict_list)


@api.handle("/notification", httpMethod="POST")
def notification_insert(event, pathPara, queryPara):
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
    id = pathPara["id"]
    notification = database.get_by_id(Notification, id)
    notification.hardware = database.get_hardware_ids_by_notification_id(Hardware_has_Notification,
                                                                          notification.notification_id)
    body = Notification.object_to_dict(notification)

    return json_payload(body)


@api.handle("/notification/{id}", httpMethod="DELETE")
def notification_delete_by_id(event, pathPara, queryPara):
    return delete_by_id(Notification, pathPara)


@api.handle("/notification/{id}", httpMethod="PUT")
def notification_update_by_id(event, pathPara, queryPara):
    return update_by_id(Notification, pathPara, queryPara)


@api.handle("/notification/{id}/add/{hardware_id}", httpMethod="POST")
def notification_insert_hardware(event, pathPara, queryPara):
    hardware_notification = Hardware_has_Notification(pathPara["hardware_id"], pathPara["id"])
    database.insert(hardware_notification)
    return json_payload({})


@api.handle("/notification/{id}/hardware")
def notification_hardware_request(event, pathPara, queryPara):
    data = database.get_all_by_join_id(Hardware, Hardware_has_Notification,
                                       "EXPLICIT_HARDWARE_ID", "EXPLICIT_NOTIFICATION_ID", pathPara["id"])
    return json_payload(Hardware.list_object_to_dict_list(data))


@api.handle("/notification/{id}/hardware/{hardware_id}", httpMethod="DELETE")
def notification_hardware_delete_by_id(event, pathPara, queryPara):
    return delete_by_hardware_id(Hardware_has_Notification, pathPara)


@api.handle("/resolution")
def resolution_request(event, pathPara, queryPara):
    return get_all(Resolution)


@api.handle("/resolution", httpMethod="POST")
def resolution_insert(event, pathPara, queryPara):
    resolution = Resolution(queryPara["resolution_name"], queryPara["width"], queryPara["height"])
    database.insert(resolution)
    return json_payload({})


@api.handle("/resolution/{name}")
def resolution_request_by_name(event, pathPara, queryPara):
    return get_by_name(Resolution, pathPara)


@api.handle("/resolution/{name}", httpMethod="DELETE")
def resolution_delete_by_id(event, pathPara, queryPara):
    return delete_by_name(Resolution, pathPara)


@api.handle("/resolution/{name}", httpMethod="PUT")
def resolution_update_by_id(event, pathPara, queryPara):
    return update_by_id(Notification, pathPara, queryPara)


@api.handle("/saving_policy")
def saving_policy_request(event, pathPara, queryPara):
    saving_policies = database.get_all(Saving_Policy)
    for policy in saving_policies:
        policy.hardware = database.get_hardware_ids_by_saving_policy_id(Hardware_has_Saving_Policy, policy.saving_policy_id)
    dict_list = Saving_Policy.list_object_to_dict_list(saving_policies)

    return json_payload(dict_list)


@api.handle("/saving_policy", httpMethod="POST")
def saving_policy_insert(event, pathPara, queryPara):
    saving_policy = Saving_Policy(queryPara["max_time"], queryPara["resolution_name"])
    database.insert(saving_policy)
    return json_payload({})


@api.handle("/saving_policy/{id}")
def saving_policy_request_by_id(event, pathPara, queryPara):
    id = pathPara["id"]
    saving_policy = database.get_by_id(Saving_Policy, id)
    saving_policy.hardware = database.get_hardware_ids_by_saving_policy_id(Hardware_has_Saving_Policy, saving_policy.saving_policy_id)
    body = Saving_Policy.object_to_dict(saving_policy)

    return json_payload(body)


@api.handle("/saving_policy/{id}", httpMethod="DELETE")
def saving_policy_delete_by_id(event, pathPara, queryPara):
    return delete_by_id(Saving_Policy, pathPara)


@api.handle("/saving_policy/{id}", httpMethod="PUT")
def saving_policy_update_by_id(event, pathPara, queryPara):
    return update_by_id(Saving_Policy, pathPara, queryPara)


@api.handle("/saving_policy/{id}/add/{hardware_id}", httpMethod="POST")
def saving_policy_add_hardware(event, pathPara, queryPara):
    saving_policy = Hardware_has_Saving_Policy(pathPara["hardware_id"], pathPara["id"])
    database.insert(saving_policy)
    return json_payload({})


@api.handle("/saving_policy/{id}/hardware")
def saving_policy_hardware_request(event, pathPara, queryPara):
    data = database.get_all_by_join_id(Hardware, Hardware_has_Saving_Policy,
                                       "EXPLICIT_HARDWARE_ID", "EXPLICIT_SAVING_POLICY_ID", pathPara["id"])
    return json_payload(Hardware.list_object_to_dict_list(data))


@api.handle("/saving_policy/{id}/hardware/{hardware_id}", httpMethod="DELETE")
def saving_policy_hardware_delete_by_id(event, pathPara, queryPara):
    return delete_by_hardware_id(Hardware_has_Saving_Policy, pathPara)


if __name__ == "__main__":
    import urllib
    database.insert(Hardware("TestDevice", "720p"), ignore=True)
    max = database.get_max_id(Hardware)
    event = {
        "resource": "/hardware/{id}",
        "httpMethod": "DELETE",
        "body": """{
            "username": "username1",
            "password": "password",
            "email": "default@temple.edu"
        }""",
        "pathParameters": {
            "id": max
        }
    }

    print(lambda_handler(event, None))
    database.close()
