# type: ignore
from io import BytesIO

import boto3
from moto import mock_s3

from app.utils.s3_management import S3Management  # type: ignore

REDUCED_PART_SIZE = 256
BUCKET_NAME = "test_bucket"


@mock_s3
def test_upload_file():
    s3 = boto3.client("s3")
    s3.create_bucket(
        Bucket=BUCKET_NAME,
        CreateBucketConfiguration={"LocationConstraint": "us-west-2"},
    )

    part1 = b"0" * REDUCED_PART_SIZE
    file = BytesIO(part1)

    file_management = S3Management()
    file_management.upload_file(file, "file_upload", BUCKET_NAME)

    resp = s3.get_object(Bucket=BUCKET_NAME, Key="file_upload")
    assert resp is not None


@mock_s3
def test_generate_presigned_url():
    s3 = boto3.client("s3")
    s3.create_bucket(
        Bucket=BUCKET_NAME,
        CreateBucketConfiguration={"LocationConstraint": "us-west-2"},
    )

    part1 = b"0" * REDUCED_PART_SIZE
    file = BytesIO(part1)

    file_name = "file_upload"
    s3.upload_fileobj(file, BUCKET_NAME, file_name)

    file_management = S3Management()
    presigned_url = file_management.generate_presigned_url(file_name, BUCKET_NAME)

    assert presigned_url is not None
