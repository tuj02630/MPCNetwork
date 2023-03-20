import base64

from mpc_api import MPC_API
import boto3

api = MPC_API()
s3 = boto3.client('s3')

def lambda_handler(event, context):
    print(event)
    print(context)
    print("11")
    data = {
        "event": event,
        "content": context
    }

    status = 200

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

    return {
        'statusCode': status,
        'headers': {'Content-Type': 'application/json'},
        'body': str(data)
    }


@api.handle("Video")
def video_request(para):
    if "image_name" in para:
        image_name = para["image_name"]
    else:
        image_name = "image.png"
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


@api.handle("Account")
def account_request(para):
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'text/plain'},
        'body': "Account"
    }


@api.handle("Recording")
def recording_request(para):
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'text/plain'},
        'body': "Recording"
    }


if __name__ == "__main__":
    api.handlers["Message"](None)
    api.handlers["Post"](None)
    api.handlers["Message"](None)

