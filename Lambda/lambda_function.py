import base64
import json

from Database.MPCDatabase import MPCDatabase
from Database.Account import Account
from Database.Hardware import Hardware
from Database.Recording import Recording
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

    if "queryStringParameters" in event and event["queryStringParameters"] is not None and "event_type" in event["queryStringParameters"]:
        print(event["queryStringParameters"]["event_type"])
        print(event["queryStringParameters"])
        event["queryStringParameters"]["event_type"] = event["queryStringParameters"]["event_type"].lower()
        try:
            if event["queryStringParameters"] is not None and "event_type" in event["queryStringParameters"]:
                if event["queryStringParameters"]["event_type"] in api.handlers:
                    return api.handlers[event["queryStringParameters"]["event_type"]](event["queryStringParameters"])
                else:
                    status = 500
                    data = {"error": "Error Key " + event["queryStringParameters"]["event_type"]}
        except Exception as err:
            status = 500
            data = {"error": str(err)}
    else:
        data = event


    return {
        'statusCode': status,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(data)
    }


@api.handle("Image")
def image_request(para):
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


@api.handle("Video")
def image_request(para):
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


@api.handle("Account")
def account_request(para):
    if "account_id" not in para:
        accounts = database.get_accounts()
        dict_list = [account.__dict__ for account in accounts]

        body = json.dumps(dict_list)
    else:
        account = database.get_account_by_id(para["account_id"])
        body = json.dumps(account.__dict__ )
    return  {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': body
        }


@api.handle("Recording")
def recording_request(para):
    if "recording_id" in para:
        recording = database.get_recording_by_id(para["recording_id"])
        body = json.dumps(recording.__dict__)
    else:
        if "hardware_id" in para and "account_id" in para:
            recordings = database.get_recordings_by_account_id_hardware_id(para["account_id"], para["hardware_id"])

        elif "account_id" in para:
            recordings = database.get_recordings_by_account_id(para["account_id"])

        elif "hardware_id" in para:
            recordings = database.get_recordings_by_hardware_id(para["hardware_id"])

        else:
            recordings = database.get_recordings()
        body = json.dumps([recording.__dict__ for recording in recordings])

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': body
    }


@api.handle("Hardware")
def recording_request(para):
    if "hardware_id" in para:
        hardware = database.get_hardware_by_id(para["hardware_id"])
        body = json.dumps(hardware.__dict__)
    else:
        if "account_id" in para:
            hardwares = database.get_hardwares_by_account_id(para["account_id"])

        else:
            hardwares = database.get_recordings()
        body = json.dumps([hardware.__dict__ for hardware in hardwares])

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': body
    }


if __name__ == "__main__":
    event = {
        "queryStringParameters": {"event_type": "Hardware", "account_id": 312}
    }
    print(lambda_handler(event , None))

