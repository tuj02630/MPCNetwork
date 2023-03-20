import json


def lambda_handler(event, context):
    print(event)
    print(context)
    print("11")
    data = "Event\n" + str(event) + "\nContext\n" + str(context)

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json', "x-api-key": "3hz1jabJZ08Ee9ZsTzGEc9NlkLM0U5uF7inDPeoW"},
        'body': json.dumps(data)
    }

# app = Flask(__name__)
# @app.route('/', methods=['GET'])
# def home():
#     return jsonify({'message': 'Hello, World!'})
