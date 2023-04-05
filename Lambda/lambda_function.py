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


@api.handle("/", httpMethod="POST")
def home(event, pathPara, queryPara):
    # data = event["body"]
    # # stream = base64.b64encode(data.encode()).decode('utf-8')
    # stream = data.encode()
    # print("a")
    # bucket = "mpc-capstone"
    # print("aa")
    # fileName = "sample" + "." + event["multiValueHeaders"]["Content-Type"][0].split("/")[1]
    # print("b")
    # s3.put_object(Bucket=bucket, Key=fileName, Body=stream, ACL="public-read")


    print("Upload done")
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
    accounts: list[Account] = database.get_all(Account)
    dict_list = Account.list_object_to_dict_list(accounts)

    return json_payload(dict_list)


@api.handle("/account/signup", httpMethod="POST")
def account_signup(event, pathPara, queryPara):
    body = event["body"]

    dec = json.loads(base64.b64decode(body).decode('utf-8'))
    print(dec)
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(dec)
    }


@api.handle("/account", httpMethod="POST")
def account_insert(event, pathPara, queryPara):
    account: Account = Account(queryPara["username"], queryPara["password"], queryPara["email"], "C")
    database.insert(account)
    a: Account = database.get_by_name(Account, queryPara["username"])
    return json_payload({"id": a.account_id, "token": a.token})


@api.handle("/account/{id}")
def account_request_by_id(event, pathPara, queryPara):
    id = pathPara["id"]
    account: Account = database.get_by_id(Account, id)
    body = Account.object_to_dict(account)

    return json_payload(body)


@api.handle("/hardware")
def hardware_request(event, pathPara, queryPara):
    hardware: list[Hardware] = database.get_all(Hardware)
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
    recordings: list[Recording] = database.get_all(Recording)
    for rec in recordings:
        # if rec.file_name[-len(".mp4"):] == ".mp4":
        #     stage = "/video/"
        # else:
        #     stage = "/image/"
        # rec.url = event["multiValueHeaders"]["X-Forwarded-Proto"][0] + "://" + event["multiValueHeaders"]["Host"][0] + \
        #           "/" + event["requestContext"]["stage"] + stage + rec.file_name
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
    # if recording.file_name[-len(".mp4"):] == ".mp4":
    #     stage = "/video/"
    # else:
    #     stage = "/image/"
    # recording.url = event["multiValueHeaders"]["X-Forwarded-Proto"][0] + "://" + event["multiValueHeaders"]["Host"][0] + \
    #           "/" + event["requestContext"]["stage"] + stage + recording.file_name
    bucket = "mpc-capstone"
    recording.url = f"https://{bucket}.s3.amazonaws.com/{recording.file_name}"
    host = event["multiValueHeaders"]["Host"][0]
    stage = event["requestContext"]["stage"]
    path = "storage"
    recording.alt_url = f"https://{host}/{stage}/{path}/{bucket}/{recording.file_name}"
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


@api.handle("/criteria/{id}")
def criteria_request_by_type(event, pathPara, queryPara):
    id = pathPara["id"]
    criteria = database.get_by_id(Criteria, id)
    body = Criteria.object_to_dict(criteria)

    return json_payload(body)


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


@api.handle("/notification/{id}/add/{hardware_id}", httpMethod="POST")
def notification_insert(event, pathPara, queryPara):
    hardware_notification = Hardware_has_Notification(pathPara["hardware_id"], pathPara["id"])
    database.insert(hardware_notification)
    return json_payload({})


@api.handle("/notification/{id}/hardware")
def notification_hardware_request(event, pathPara, queryPara):
    data = database.get_all_by_join_id(Hardware, Hardware_has_Notification,
                                       "EXPLICIT_HARDWARE_ID", "EXPLICIT_NOTIFICATION_ID", pathPara["id"])
    return json_payload(Hardware.list_object_to_dict_list(data))

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


if __name__ == "__main__":
    import urllib
    d = "ew0KICAgICJ1c2VybmFtZSI6ICJ1c2VybmFtZSINCn0="
    # d = "LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLTk1NjQwNjEwNjMyNjkxNTMxMDUwMDUyNw0KQ29udGVudC1EaXNwb3NpdGlvbjogZm9ybS1kYXRhOyBuYW1lPSJ1c2VybmFtZSINCg0KdXNlcm5hbWUNCi0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS05NTY0MDYxMDYzMjY5MTUzMTA1MDA1MjctLQ0K"
    # d = base64.b64encode(json.dumps({"a":"aa", "b": "bb"}).encode("utf-8")).decode('utf-8')
    print(d)
    dec = base64.b64decode(d).decode('utf-8')
    print(dec)
    # da = json.loads(d)
    print(json.loads(dec))
    print(json.loads("{\r\n    \"username\": \"username\",\r\n    \"password\": \"password\",\r\n    \"email\": \"email\",\r\n    \"list\": [\"item1\", \"item2\"]\r\n}"))
    # e = base64.b64encode(da)


