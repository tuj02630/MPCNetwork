import base64
import json

from Database.MPCDatabase import MPCDatabase
from Database.Data.Recording import Recording
from Database.Data.Account import Account
from Database.Data.Hardware import Hardware
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
    dict_list = [account.__dict__ for account in accounts]

    body = json.dumps(dict_list)
    return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': body
    }


@api.handle("/account", httpMethod="POST")
def account_insert(event, pathPara, queryPara):
    account = Account(queryPara["username"], queryPara["password"])
    database.insert(account)
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({"result": "processed"})
    }


@api.handle("/account/{id}")
def account_request_by_id(event, pathPara, queryPara):
    id = pathPara["id"]
    account = database.get_by_id(Account, id)
    if account is None:
        body = json.dumps({})
    else:
        body = json.dumps(account.__dict__)

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': body
    }


@api.handle("/hardware")
def hardwares_request(event, pathPara, queryPara):
    hardwares = database.get_all(Hardware)
    dict_list = [hardware.__dict__ for hardware in hardwares]

    body = json.dumps(dict_list)
    return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': body
    }


@api.handle("/hardware", httpMethod="POST")
def hardware_insert(event, pathPara, queryPara):
    try:
        if "account_id" in queryPara:
            hardware = Hardware(queryPara["name"], queryPara["max_resolution"], account_id=queryPara["account_id"])
        else:
            hardware = Hardware(queryPara["name"], queryPara["max_resolution"])
        database.insert(hardware)
    except Exception as err:
        return {
        'statusCode': 500,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({"result": "error: " + str(err)})
    }
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({"result": "processed"})
    }


@api.handle("/hardware/{id}")
def hardware_request_by_id(event, pathPara, queryPara):
    id = pathPara["id"]
    hardware = database.get_by_id(Hardware, id)
    if hardware is None:
        body = json.dumps({})
    else:
        body = json.dumps(hardware.__dict__)

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': body
    }


@api.handle("/recording")
def recordings_request(event, pathPara, queryPara):
    recordings = database.get_all(Recording)
    dict_list = [recording.__dict__ for recording in recordings]

    body = json.dumps(dict_list)
    return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': body
    }


@api.handle("/recording", httpMethod="POST")
def recording_insert(event, pathPara, queryPara):
    recording = Recording(queryPara["file_name"], "CURDATE()", "NOW()",
                          account_id=queryPara["account_id"], hardware_id=queryPara["hardware_id"])
    if "date" in queryPara:
        recording.date = queryPara["date"]
    if "timestamp" in queryPara:
        recording.timestamp = queryPara["timestamp"]
    database.insert(recording)
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({"result": "processed"})
    }


@api.handle("/recording/{id}")
def recording_request_by_id(event, pathPara, queryPara):
    id = pathPara["id"]
    recording = database.get_by_id(Recording, id)
    if recording is None:
        body = json.dumps({})
    else:
        body = json.dumps(recording.__dict__)

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': body
    }


if __name__ == "__main__":
    event = {
        "queryStringParameters": {"event_type": "Hardware", "account_id": 312},
        "resource": "/account/{id}",
        "pathParameters": {"id": "2"},
        "httpMethod": "GET"
    }

    print(lambda_handler(event , None))

