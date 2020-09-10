# type: ignore
from typing import IO

import boto3

from app.settings.globals import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


class FileManagement:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )

    def upload_file(self, file: IO, file_name: str, bucket_name: str) -> str:
        self.s3.upload_fileobj(file, bucket_name, file_name)
        return file_name


file_management = FileManagement()
