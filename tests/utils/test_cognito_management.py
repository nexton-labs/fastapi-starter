# type: ignore
import uuid

import boto3
from moto import mock_cognitoidp

from app.utils.cognito_management import CognitoManagement
from tests.utils import generate_uuid


def create_cognito_pool() -> (str, str):
    conn = boto3.client("cognito-idp")

    pool_name = str(uuid.uuid4())
    client_name = str(uuid.uuid4())
    user_pool_id = conn.create_user_pool(PoolName=pool_name)["UserPool"]["Id"]
    app_client_id = conn.create_user_pool_client(
        UserPoolId=user_pool_id, ClientName=client_name
    )["UserPoolClient"]["ClientId"]

    return user_pool_id, app_client_id


@mock_cognitoidp
def test_sign_up():
    user_pool_id, app_client_id = create_cognito_pool()

    cognito_management = CognitoManagement(user_pool_id, app_client_id)
    email = "test@test.com"
    user_id = generate_uuid()
    result = cognito_management.sign_up_by_email(
        email=email, password="Example1234!", user_id=user_id
    )

    assert result
    assert not result["UserConfirmed"]


@mock_cognitoidp
def test_delete():
    user_pool_id, app_client_id = create_cognito_pool()

    cognito_management = CognitoManagement(user_pool_id, app_client_id)
    cognito_management.sign_up_by_email(
        email="test@test.com", password="Example1234!", user_id=generate_uuid()
    )

    cognito_management.delete_user(username="test@test.com",)


@mock_cognitoidp
def test_invite_user_by_email():
    user_pool_id, app_client_id = create_cognito_pool()

    cognito_management = CognitoManagement(user_pool_id, app_client_id)
    email = "test@test.com"
    user_id = generate_uuid()
    result = cognito_management.invite_user_by_email(email=email, user_id=user_id)

    assert result
    assert result["User"]["Username"] == email
    assert len(result["User"]["Attributes"]) == 4
    assert result["User"]["Attributes"][0]["Name"] == "email"
    assert result["User"]["Attributes"][0]["Value"] == email
    assert result["User"]["Attributes"][1]["Name"] == "email_verified"
    assert result["User"]["Attributes"][1]["Value"] == "True"
    assert result["User"]["Attributes"][2]["Name"] == "phone_number"
    assert result["User"]["Attributes"][2]["Value"] == ""
    assert result["User"]["Attributes"][3]["Name"] == "custom:id"
    assert result["User"]["Attributes"][3]["Value"] == str(user_id)


@mock_cognitoidp
def test_invite_user_by_phone():
    user_pool_id, app_client_id = create_cognito_pool()

    cognito_management = CognitoManagement(user_pool_id, app_client_id)
    phone = "+5493416412234"
    user_id = generate_uuid()
    result = cognito_management.invite_user_by_phone(phone=phone, user_id=user_id)

    assert result
    assert result["User"]["Username"] == phone
    assert len(result["User"]["Attributes"]) == 4
    assert result["User"]["Attributes"][0]["Name"] == "phone_number"
    assert result["User"]["Attributes"][0]["Value"] == phone
    assert result["User"]["Attributes"][1]["Name"] == "phone_number_verified"
    assert result["User"]["Attributes"][1]["Value"] == "True"
    assert result["User"]["Attributes"][2]["Name"] == "email"
    assert result["User"]["Attributes"][2]["Value"] == ""
    assert result["User"]["Attributes"][3]["Name"] == "custom:id"
    assert result["User"]["Attributes"][3]["Value"] == str(user_id)
