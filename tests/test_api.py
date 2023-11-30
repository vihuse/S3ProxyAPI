def test_upload_endpoint(test_client):
    response = test_client.post(
        "/upload/",
        files={"file": ("testfile.txt", "dummy content")},
        data={"bucket": "testbucket", "object_name": "testfile.txt"},
    )
    assert response.status_code == 200
    assert response.json() == {"message": "File uploaded successfully"}


def test_retrieve_endpoint(test_client):
    response = test_client.get("/retrieve/?bucket=testbucket&object_name=testfile.txt")
    assert response.status_code == 200


def test_upload_invalid_input(test_client):
    response = test_client.post(
        "/upload/",
        files={"file": ("testfile.txt", "dummy content")},
        data={"bucket": "", "object_name": "testfile.txt"},
    )
    assert response.status_code == 422


def test_retrieve_nonexistent_file(test_client):
    response = test_client.get(
        "/retrieve/?bucket=testbucket&object_name=nonexistent.txt"
    )
    assert response.status_code == 404


def test_upload_empty_file(test_client):
    response = test_client.post(
        "/upload/",
        files={"file": ("emptyfile.txt", "")},
        data={"bucket": "testbucket", "object_name": "emptyfile.txt"},
    )
    assert response.status_code == 200
