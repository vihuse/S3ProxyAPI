import pytest
import boto3
from botocore.exceptions import ClientError
from fastapi.testclient import TestClient
from decouple import config
from main import app

AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
S3_ENDPOINT_URL = config("S3_ENDPOINT_URL")


@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module", autouse=True)
def create_test_bucket():
    s3_client = boto3.client(
        "s3",
        endpoint_url=S3_ENDPOINT_URL,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )

    try:
        s3_client.create_bucket(Bucket="testbucket")
    except ClientError as e:
        if e.response["Error"]["Code"] == "BucketAlreadyOwnedByYou":
            # If the bucket already exists and is owned by the user, ignore the error
            pass
        else:
            raise e
    yield
