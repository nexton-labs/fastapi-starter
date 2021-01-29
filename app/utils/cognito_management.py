from typing import Optional
from uuid import UUID

import boto3
from botocore.exceptions import ClientError

from app.settings.globals import COGNITO_POOL_ID, COGNITO_APP_CLIENT_ID
from app.utils import password as password_utils


class CognitoManagement:
    def __init__(self, cognito_pool_id: str, app_client_id: str):
        self.cidp = boto3.client("cognito-idp")
        self.app_client_id = app_client_id
        self.cognito_pool_id = cognito_pool_id

    def sign_up_by_email(
        self, email: str, password: str, user_id: UUID, phone: Optional[str] = None
    ) -> str:
        sign_up_response: str = self.cidp.sign_up(
            ClientId=self.app_client_id,
            Username=email,
            Password=password,
            UserAttributes=[
                {"Name": "email", "Value": email},
                {"Name": "phone_number", "Value": phone if phone else ""},
                {"Name": "custom:id", "Value": str(user_id)},
            ],
        )

        return sign_up_response

    def sign_up_by_phone(
        self, phone: str, password: str, user_id: UUID, email: Optional[str] = None
    ) -> str:
        sign_up_response: str = self.cidp.sign_up(
            ClientId=self.app_client_id,
            Username=phone,
            Password=password,
            UserAttributes=[
                {"Name": "email", "Value": email if email else ""},
                {"Name": "phone_number", "Value": phone},
                {"Name": "custom:id", "Value": str(user_id)},
            ],
        )

        return sign_up_response

    def invite_user_by_email(
        self,
        user_id: UUID,
        email: str,
        resend: Optional[bool] = False,
        phone: Optional[str] = None,
    ) -> str:
        temporary_password = password_utils.generate_random()
        additional_args = {}
        if resend:
            additional_args["MessageAction"] = "RESEND"

        create_response: str = self.cidp.admin_create_user(
            UserPoolId=self.cognito_pool_id,
            TemporaryPassword=temporary_password,
            Username=email,
            DesiredDeliveryMediums=["EMAIL"],
            UserAttributes=[
                {"Name": "email", "Value": email},
                {"Name": "email_verified", "Value": "True"},
                {"Name": "phone_number", "Value": phone if phone else ""},
                {"Name": "custom:id", "Value": str(user_id)},
            ],
            **additional_args,
        )

        return create_response

    def invite_user_by_phone(
        self,
        user_id: UUID,
        phone: Optional[str] = None,
        resend: Optional[bool] = False,
        email: Optional[str] = None,
    ) -> str:
        temporary_password = password_utils.generate_random()
        additional_args = {}
        if resend:
            additional_args["MessageAction"] = "RESEND"

        create_response: str = self.cidp.admin_create_user(
            UserPoolId=self.cognito_pool_id,
            TemporaryPassword=temporary_password,
            Username=phone,
            DesiredDeliveryMediums=["SMS"],
            UserAttributes=[
                {"Name": "phone_number", "Value": phone},
                {"Name": "phone_number_verified", "Value": "True"},
                {"Name": "email", "Value": email if email else ""},
                {"Name": "custom:id", "Value": str(user_id)},
            ],
            **additional_args,
        )

        return create_response

    def delete_user(self, username: str) -> str:

        try:
            delete_user_response: str = self.cidp.admin_delete_user(
                UserPoolId=self.cognito_pool_id, Username=username,
            )
            return delete_user_response
        except ClientError as error:
            if error.response["Error"]["Code"] == "UserNotFoundException":
                raise ValueError(str(error.response["Error"]["Message"]))
            else:
                raise error


cognito_management = CognitoManagement(COGNITO_POOL_ID, COGNITO_APP_CLIENT_ID)
