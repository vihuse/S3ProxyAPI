from unittest.mock import patch, MagicMock
from fastapi import UploadFile
from s3_client import create_s3_client, upload_file_to_s3, get_file_from_s3
from io import BytesIO


def test_create_s3_client():
    client = create_s3_client()
    assert client is not None


@patch("s3_client.boto3.client")
def test_upload_file_to_s3(mock_boto3_client):
    mock_s3_client = MagicMock()
    mock_boto3_client.return_value = mock_s3_client

    s3_client = create_s3_client()

    # Create a mock file-like object
    mock_file = BytesIO(b"Test file content")
    mock_upload_file = UploadFile(filename="testfile.txt", file=mock_file)

    upload_file_to_s3("testbucket", "testfile.txt", mock_upload_file, s3_client)

    mock_s3_client.upload_fileobj.assert_called_once()


@patch("s3_client.boto3.client")
def test_get_file_from_s3(mock_boto3_client):
    mock_s3_client = MagicMock()
    mock_boto3_client.return_value = mock_s3_client

    # Mock return value for get_object
    mock_s3_client.get_object.return_value = {
        "Body": MagicMock(read=MagicMock(return_value=b"dummy content"))
    }

    s3_client = create_s3_client()
    content = get_file_from_s3("testbucket", "testfile.txt", s3_client)

    assert content.read() == b"dummy content"
