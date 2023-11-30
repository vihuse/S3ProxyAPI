import boto3
from botocore.client import Config
from botocore.exceptions import NoCredentialsError, ClientError
from fastapi import UploadFile, HTTPException
from decouple import config
import io
import logging

AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
S3_ENDPOINT_URL = config("S3_ENDPOINT_URL")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_s3_client():
    """
    Create and configure an S3 client for AWS or MinIO.

    :return: Configured S3 client.
    """
    return boto3.client(
        "s3",
        endpoint_url=S3_ENDPOINT_URL,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name="us-east-1",
        config=Config(signature_version="s3v4"),
    )


def upload_file_to_s3(bucket: str, object_name: str, file: UploadFile, s3_client):
    """
    Upload a file to an S3 bucket.

    :param bucket: The S3 bucket name.
    :param object_name: The object name in the S3 bucket.
    :param file: The file to be uploaded.
    :param s3_client: The S3 client.
    :raises HTTPException: If any error occurs during file upload.
    """
    try:
        s3_client.upload_fileobj(file.file, bucket, object_name)
    except NoCredentialsError:
        logger.error("AWS credentials not found")
        raise HTTPException(status_code=500, detail="AWS credentials not found")
    except ClientError as e:
        logger.error(f"ClientError during file upload: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


def get_file_from_s3(bucket: str, object_name: str, s3_client):
    """
    Retrieve a file from an S3 bucket.

    :param bucket: The S3 bucket name.
    :param object_name: The object name to retrieve.
    :param s3_client: The S3 client.
    :return: StreamingResponse with the file content.
    :raises HTTPException: If the file is not found or any other error occurs.
    """
    try:
        file_obj = s3_client.get_object(Bucket=bucket, Key=object_name)
        return io.BytesIO(file_obj["Body"].read())
    except ClientError as e:
        if "NoSuchKey" in str(e):
            raise HTTPException(status_code=404, detail="File not found")
        else:
            raise HTTPException(status_code=500, detail=str(e))
