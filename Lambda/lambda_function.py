from flask import Flask
import awsgi
import base64
import boto3

app = Flask(__name__)
s3 = boto3.client('s3')


def lambda_handler(event, context):
    # response = s3.get_object(
    #     Bucket='mpc-capstone',
    #     Key='image.png',
    # )
    # image = response['Body'].read()
    # return {
    #     'headers': {"Content-Type": "image/png"},
    #     'statusCode': 200,
    #     'body': base64.b64encode(image),
    #     'isBase64Encoded': True
    # }
    return awsgi.response(app, event, context)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"