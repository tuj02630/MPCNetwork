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
    print("11")
    data = {
        "event": event,
        "content": context
    }

    status = 200
    para = {}
    if "queryStringParameters" in event and event["queryStringParameters"] is not None:
        para = event["queryStringParameters"]

    try:
        if event["resource"] in api.handlers:
            path = event["resource"].lower()
            return api.handlers[path](event, para)
        else:
            status = 500
            # data = {"error": "Error Key " + event["path"]}
            data = event
    except Exception as err:
        status = 500
        data = {"error": str(err)}

    return {
        'statusCode': status,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(data)
    }


@api.handle("/")
def home(event, para):
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(event)
    }


@api.handle("/image")
def image_request(event, para):
    if "image_name" in para:
        image_name = para["image_name"]
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
def image_request(event, para):
    if "video_name" in para:
        video_name = para["video_name"]
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
def account_request(event, para):
    if "account_id" not in para:
        accounts = database.get_all(Account)
        dict_list = [account.__dict__ for account in accounts]

        body = json.dumps(dict_list)
    else:
        account = database.get_by_id(Account, para["account_id"])
        body = json.dumps(account.__dict__ )
    return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': body
        }


@api.handle("/recording")
def recording_request(event, para):
    if "recording_id" in para:
        recording = database.get_by_id(Recording, para["recording_id"])
        body = json.dumps(recording.__dict__)
    else:
        if "hardware_id" in para and "account_id" in para:
            recordings = database.get_all_by_account_id_hardware_id(Recording, para["account_id"], para["hardware_id"])

        elif "account_id" in para:
            recordings = database.get_all_by_account_id(Recording, para["account_id"])

        elif "hardware_id" in para:
            recordings = database.get_all_by_hardware_id(Recording, para["hardware_id"])

        else:
            recordings = database.get_all(Recording)
        body = json.dumps([recording.__dict__ for recording in recordings])

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': body
    }


@api.handle("/hardware")
def hardware_request(event, para):
    if "hardware_id" in para:
        hardware = database.get_by_id(Hardware, para["hardware_id"])
        body = json.dumps(hardware.__dict__)
    else:
        if "account_id" in para:
            hardwares = database.get_all_by_account_id(Hardware, para["account_id"])

        else:
            hardwares = database.get_all(Hardware)
        body = json.dumps([hardware.__dict__ for hardware in hardwares])

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': body
    }


if __name__ == "__main__":
    event = {
        "queryStringParameters": {"event_type": "Hardware", "account_id": 312},
        "path": "/a"
    }

    print(lambda_handler(event , None))

