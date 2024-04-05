import json


def handle(event, context):
    print("~~~> default route")
    print(event)

    return {"statusCode": 200, "body": json.dumps({"message": "default works"})}
