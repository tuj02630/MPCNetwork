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

from mpc_api import MPC_API
import boto3

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

    try:
        return api.handlers[resource][httpMethod](event, pathPara, queryPara)
    except Exception as err:
        status = 500
        data = {"error": str(err)}

    return {
        'statusCode': status,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(data)
    }


def json_payload(body):
    return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(body)
    }


@api.handle("/")
def home(event, pathPara, queryPara):
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(event)
    }


@api.handle("/image")
def image_request(event, pathPara, queryPara):
    if "image_name" in queryPara:
        image_name = queryPara["image_name"]
    else:
        image_name = "bird-thumbnail.jpg"
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
    # return {
    #     'statusCode': 200,
    #     'headers': {'Content-Type': 'text/plain'},
    #     'body': "Video"
    # }


@api.handle("/video")
def image_request(event, pathPara, queryPara):
    if "video_name" in queryPara:
        video_name = queryPara["video_name"]
    else:
        video_name = "cat.mp4"
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
    accounts = database.get_all(Account)
    dict_list = Account.list_object_to_dict_list(accounts)

    return json_payload(dict_list)


@api.handle("/account", httpMethod="POST")
def account_insert(event, pathPara, queryPara):
    account = Account(queryPara["username"], queryPara["password"])
    database.insert(account)
    id = database.get_id_by_name(Account, queryPara["username"])
    return json_payload({"id": id})


@api.handle("/account/{id}")
def account_request_by_id(event, pathPara, queryPara):
    id = pathPara["id"]
    account = database.get_by_id(Account, id)
    body = Account.object_to_dict(account)

    return json_payload(body)


@api.handle("/hardware")
def hardware_request(event, pathPara, queryPara):
    hardware = database.get_all(Hardware)
    dict_list = Hardware.list_object_to_dict_list(hardware)

    return json_payload(dict_list)


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
    id = pathPara["id"]
    hardware = database.get_by_id(Hardware, id)
    body = Hardware.object_to_dict(hardware)

    return json_payload(body)


@api.handle("/recording")
def recordings_request(event, pathPara, queryPara):
    recordings = database.get_all(Recording)
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
    body = Recording.object_to_dict(recording)

    return json_payload(body)


@api.handle("/criteria")
def criteria_request(event, pathPara, queryPara):
    criteria = database.get_all(Criteria)
    dict_list = Criteria.list_object_to_dict_list(criteria)

    return json_payload(dict_list)


@api.handle("/criteria", httpMethod="POST")
def criteria_insert(event, pathPara, queryPara):
    criteria = Criteria(queryPara["criteria_type"], queryPara["magnitude"], queryPara["duration"])
    database.insert(criteria)
    return json_payload({})


@api.handle("/criteria/{type}")
def criteria_request_by_type(event, pathPara, queryPara):
    type = pathPara["type"]
    criteria = database.get_by_type(Criteria, type)
    body = Criteria.object_to_dict(criteria)

    return json_payload(body)


@api.handle("/notification")
def notification_request(event, pathPara, queryPara):
    notifications = database.get_all(Notification)
    dict_list = Notification.list_object_to_dict_list(notifications)

    return json_payload(dict_list)


@api.handle("/notification", httpMethod="POST")
def notification_insert(event, pathPara, queryPara):
    notification = Notification(queryPara["notification_type"], queryPara["criteria_type"], queryPara["hardware_id"])
    database.insert(notification)
    id = database.get_id_by_type(Notification, queryPara["notification_type"])
    return json_payload({"id": id})


@api.handle("/notification/{id}")
def notification_request_by_type(event, pathPara, queryPara):
    type = pathPara["id"]
    notification = database.get_by_id(Notification, type)
    body = Notification.object_to_dict(notification)

    return json_payload(body)


@api.handle("/resolution")
def resolution_request(event, pathPara, queryPara):
    resolutions = database.get_all(Resolution)
    dict_list = Resolution.list_object_to_dict_list(resolutions)

    return json_payload(dict_list)


@api.handle("/resolution", httpMethod="POST")
def resolution_insert(event, pathPara, queryPara):
    resolution = Resolution(queryPara["resolution_name"], queryPara["width"], queryPara["height"])
    database.insert(resolution)
    return json_payload({})


@api.handle("/resolution/{name}")
def resolution_request_by_name(event, pathPara, queryPara):
    name = pathPara["name"]
    resolution = database.get_by_name(Resolution, name)
    body = Resolution.object_to_dict(resolution)

    return json_payload(body)


@api.handle("/saving_policy")
def saving_policy_request(event, pathPara, queryPara):
    saving_policies = database.get_all(Saving_Policy)
    dict_list = Resolution.list_object_to_dict_list(saving_policies)

    return json_payload(dict_list)


@api.handle("/saving_policy", httpMethod="POST")
def saving_policy_insert(event, pathPara, queryPara):
    saving_policy = Saving_Policy(queryPara["max_time"], queryPara["resolution_name"])
    database.insert(saving_policy)
    return json_payload({})


@api.handle("/saving_policy/{id}")
def saving_policy_request_by_name(event, pathPara, queryPara):
    id = pathPara["id"]
    saving_policy = database.get_by_name(Saving_Policy, id)
    body = Saving_Policy.object_to_dict(saving_policy)

    return json_payload(body)

## TODO
@api.handle("/saving_policy/{id}/add/{hardware_id}")
def saving_policy_add_hardware(event, pathPara, queryPara):
    id = pathPara["id"]
    hardware_id = pathPara["hardware_id"]
    saving_policy = database.get_by_name(Saving_Policy, type)
    body = Saving_Policy.object_to_dict(saving_policy)

    return json_payload(body)


if __name__ == "__main__":
    event = {
        "queryStringParameters": {"event_type": "Hardware", "account_id": 312},
        "resource": "/notification/{id}",
        "pathParameters": {"id": "101"},
        "httpMethod": "GET"
    }

    print(lambda_handler(event , None))

