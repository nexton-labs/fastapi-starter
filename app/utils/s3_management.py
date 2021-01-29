from typing import IO, Optional

import boto3
from botocore.config import Config


class S3Management:
    def __init__(self):
        self.s3 = boto3.client("s3", config=Config(signature_version="s3v4"))

    def upload_file(self, file: IO, file_name: str, bucket_name: str) -> str:
        self.s3.upload_fileobj(file, bucket_name, file_name)
        return file_name

    def generate_presigned_url(
        self, object_name: str, bucket_name: str, expiration: Optional[int] = 300
    ) -> str:

        response: str = self.s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=expiration,
        )

        return response


s3_management = S3Management()
