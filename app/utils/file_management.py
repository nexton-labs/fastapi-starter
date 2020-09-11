# type: ignore
from typing import IO

import boto3


class FileManagement:
    def __init__(self):
        self.s3 = boto3.client("s3")

    def upload_file(self, file: IO, file_name: str, bucket_name: str) -> str:
        self.s3.upload_fileobj(file, bucket_name, file_name)
        return file_name


file_management = FileManagement()
