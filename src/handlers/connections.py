import json
import os
from dataclasses import dataclass
import boto3
from os import environ

dynamo = boto3.client("dynamodb")

connections_table_name = environ.get("CONNECTIONS_TABLE_NAME")


def store_connection(connection_id):
    item = {"connection_id": {"S": connection_id}, "email": {"S": "generic@email.biz"}}
    return dynamo.put_item(TableName=connections_table_name, Item=item)


def handle(event, context):
    print("========================")
    print("stored record")
    print(event)
    try:
        connection_id = event["requestContext"]["connectionId"]
        print("------------------------")
        print(event["requestContext"]["connectionId"])
        print("------------------------")
        print("Connection id:")
        print(connection_id)
        result = store_connection(connection_id)
        print(result)
        return {"statusCode": 200, "body": json.dumps({"message": "connect works"})}
    except RuntimeError as e:
        print("exception")
        print(e)
        return {"statusCode": 500, "body": json.dumps({"error": e})}
