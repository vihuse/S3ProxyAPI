# FastAPI AWS S3 Proxy Service

This FastAPI application provides a simple yet robust proxy service for AWS S3. It allows users to upload files to S3 buckets and retrieve files from them, utilizing asynchronous operations for efficient performance.

## Features

- Upload files to an AWS S3 bucket
- Retrieve files from an AWS S3 bucket
- Efficient API calls to S3 using boto3
- Secure configuration management
- Comprehensive error handling

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- boto3
- python-decouple
- python-multipart
- pytest
- httpx

## MinIO Server Setup

MinIO provides an S3-compatible object storage server that you can run locally for development. Follow these steps to set it up:

1. **Start MinIO Server**:
   - If using Docker, run the following command:
     ```bash
     docker run -p 9000:9000 -p 9001:9001 --name minio1 \
       -e "MINIO_ROOT_USER=minioadmin" \
       -e "MINIO_ROOT_PASSWORD=minioadmin" \
       -v /mnt/data:/data \
       minio/minio server /data --console-address ":9001"
     ```
   - This command starts a MinIO server accessible at `http://localhost:9000` and its console at `http://localhost:9001`.
   - The `-v /mnt/data:/data` part is for persistent storage. Adjust the path as needed.

2. **Access MinIO Console**:
   - Open a browser and go to `http://localhost:9001`.
   - Log in with the credentials (`minioadmin` for both username and password, as set in the Docker command).

3. **Create a Bucket**:
   - Once logged in, create a new bucket (e.g., `images`) that your application will use.

## Setup and Installation

1. **Clone the repository**:

```
git clone https://github.com/vihuse/S3ProxyAPI.git
cd S3ProxyAPI
```

2. **Set up a virtual environment** (optional, but recommended):

```
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies**:

```
pip install -r requirements.txt
```

4. **Environment Configuration**:

Create a `.env` file in the root directory and fill it with your AWS (MinIO) credentials and S3 endpoint:

```
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
S3_ENDPOINT_URL=http://localhost:9000
```

5. **Running the Application**:

```
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

## Usage

- **Upload a File**:

`POST /upload/`

Payload:

```
{
  "bucket": "your_bucket_name",
  "object_name": "your_object_name",
  "file": "file_to_upload"
}
```

- **Retrieve a File**:

`GET /retrieve/?bucket=your_bucket_name&object_name=your_object_name`

## Documentation

- Swagger UI is available at `http://localhost:8000/docs` for interactive API documentation and testing.

## Testing

- To run tests, execute the following command:

```
python -m pytest -v
```
