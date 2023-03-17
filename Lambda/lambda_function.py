import json
import os
from flask import Flask, request, jsonify


def lambda_handler(event, context):
    print(event)
    print(context)
    print("11")
    data = "Event\n" + str(event) + "\nContext\n" + str(context)

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(data)
    }

# app = Flask(__name__)
# @app.route('/', methods=['GET'])
# def home():
#     return jsonify({'message': 'Hello, World!'})
