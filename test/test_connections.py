import json
from unittest.mock import patch, MagicMock
import pytest

from src.handlers.connections import handle_login


@patch.dict("os.environ", {"CONNECTIONS_TABLE_NAME": "some-table"})
@patch("src.handlers.connections.client", name="boto_client_function_mock")
def test_can_store_login_information(boto_client_function_mock):
    mock_dynamo_client = MagicMock(name="dynamo-client-mock")
    boto_client_function_mock.return_value = mock_dynamo_client
    expected_connection_id = "some-connection-id"
    expected_email = "coolguy@important.biz"
    event = read_in_resource_file("login_event.json")
    event_body = json.loads(event["body"])
    event["requestContext"]["connectionId"] = expected_connection_id
    event_body["email"] = expected_email
    event_body["action"] = "login"
    event["body"] = event_body

    handle_login(event, {})

    mock_dynamo_client.update_item.assert_called_with(
        TableName="some-table",
        Key={"connection_id": {"S": expected_connection_id}},
        UpdateExpression=" SET email = :email",
        ExpressionAttributeValues={":email": {"S": expected_email}},
    )


def read_in_resource_file(file_name: str):
    with open(f"./resources/{file_name}", "r") as file:
        return json.load(file)
