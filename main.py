from fastapi import FastAPI, Depends, UploadFile, File, Request, Form
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel, Field
from s3_client import create_s3_client, upload_file_to_s3, get_file_from_s3

app = FastAPI()


class UploadFileModel(BaseModel):
    bucket: str = Field(..., pattern="^[a-zA-Z0-9.-]+$")
    object_name: str = Field(..., min_length=1)


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500, content={"message": "An unexpected error occurred"}
    )


async def get_s3_client():
    """
    Dependency to get a configured S3 client.

    :return: S3 client instance.
    """
    return create_s3_client()


@app.post("/upload/", response_model=dict, summary="Upload a file to S3")
async def upload_file(
    bucket: str = Form(...),
    object_name: str = Form(...),
    file: UploadFile = File(...),
    s3_client=Depends(get_s3_client),
):
    """
    Uploads a file to the specified S3 bucket.

    - **bucket**: The name of the bucket where the file will be stored.
    - **object_name**: The name of the object in the S3 bucket.
    - **file**: The file to upload.
    """
    upload_file_to_s3(bucket, object_name, file, s3_client)
    return {"message": "File uploaded successfully"}


@app.get("/retrieve/", summary="Retrieve a file from S3")
async def retrieve_file(
    bucket: str, object_name: str, s3_client=Depends(get_s3_client)
):
    """
    Retrieves a file from the specified S3 bucket.

    - **bucket**: The name of the bucket.
    - **object_name**: The name of the object to retrieve.
    """
    file_stream = get_file_from_s3(bucket, object_name, s3_client)
    return StreamingResponse(file_stream, media_type="application/octet-stream")


@app.get("/", summary="Service Status")
async def root():
    """
    Root endpoint to check the service status.
    """
    return {"message": "S3 Proxy Service is running"}
