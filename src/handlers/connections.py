import json
import os
from dataclasses import dataclass
from os import environ
import boto3


class ConnectionLogger:
    def __init__(self):
        self.connections_table_name = environ.get("CONNECTIONS_TABLE_NAME")
        self.dynamo = boto3.client('dynamodb')

    def store_connection(self, connection_id):
        return self.dynamo.put_item(
            TableName=self.connections_table_name, Item={"connection_id": {"S": connection_id}}
        )

    def delete_connection(self, connection_id):
        return self.dynamo.delete_item(
            TableName=self.connections_table_name, Key={"connection_id": {"S": connection_id}}
        )

    def store_login(self, connection_id, email):
        return self.dynamo.update_item(
            TableName=self.connections_table_name,
            Key={"connection_id": {"S": connection_id}},
            UpdateExpression=" SET email = :email",
            ExpressionAttributeValues={":email": {"S": email}},
        )

    def handle_connect(self, event, context):
        print("========================")
        print("stored record")
        print(event)
        # TODO: now that this handles both connect and disconnect
        try:
            connection_id = event["requestContext"]["connectionId"]
            print("------------------------")
            print(event["requestContext"]["connectionId"])
            print("------------------------")
            print("Connection id:")
            print(connection_id)
            result = self.store_connection(connection_id)
            print(result)
            return {"statusCode": 200, "body": json.dumps({"message": "ur connected!"})}
        except RuntimeError as e:
            print("exception")
            print(e)
            return {"statusCode": 500, "body": json.dumps({"error": e})}

    def handle_disconnect(self, event, context):
        print("xxxxxxxxxxxxxxxxxxxxxxxx")
        print("disconnect")
        print(event)
        try:
            connection_id = event["requestContext"]["connectionId"]
            print("------------------------")
            print(event["requestContext"]["connectionId"])
            print("------------------------")
            print("Connection id:")
            print(connection_id)
            result = self.delete_connection(connection_id)
            print(result)
            return {"statusCode": 200, "body": json.dumps({"message": "ur connected!"})}
        except RuntimeError as e:
            print("exception")
            print(e)
            return {"statusCode": 500, "body": json.dumps({"error": e})}

    def handle_login(self, event, context):
        try:
            print("^^^^^^^^^^^^^^")
            print(event)
            connection_id = event["requestContext"]["connectionId"]
            email = event["body"]["email"]
            print([connection_id, email])
            result = self.store_login(connection_id, email)
            print(result)
            return {"statusCode": 200, "body": json.dumps({"message": "ur connected!"})}
        except RuntimeError as e:
            print("exception")
            print(e)
            return {"statusCode": 500, "body": json.dumps({"error": e})}
