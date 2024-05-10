# Google Cloud Storage (gcs.py) Documentation

## Introduction
...

## Usage
...

### Initializing GCSHandler
...

### Methods
...

#### 1. `create_bucket(bucket_name, region_name='us-central1')`

Creates a new bucket in the Google Cloud project if it doesn't exist already.

**Sample Usage:**
```python
gcs_handler = GCSHandler(project_id='my-project-id', credentials_path='path/to/credentials.json')
gcs_handler.create_bucket("test-bucket-1")
```

#### 2. `upload_file(local_file_path, bucket_name, remote_file_path)`

Uploads a file to a Google Cloud Storage bucket.

**Sample Usage:**
```python
gcs_handler.upload_file("./local/file.txt", "my-bucket", "folder/file.txt")
```

#### 3. `upload_folder(local_folder_path, bucket_name, remote_folder_path)`

Uploads a local folder to a Google Cloud Storage bucket.

**Sample Usage:**
```python
gcs_handler.upload_folder("terraform", "my-bucket", "terraform")
```

#### 4. `download_file(bucket_name, remote_file_path, local_file_path)`

Downloads a file from a Google Cloud Storage bucket.

**Sample Usage:**
```python
gcs_handler.download_file("my-bucket", "folder/file.txt", "./downloaded_file.txt")
```

#### 5. `download_folder(bucket_name, remote_folder_path, local_folder_path)`

Downloads a folder from a Google Cloud Storage bucket.

**Sample Usage:**
```python
gcs_handler.download_folder("my-bucket", "folder", "./downloaded_folder")
```

#### 6. `get_bucket_contents(bucket_name)`

Gets the contents of a bucket.

**Sample Usage:**
```python
files = gcs_handler.get_bucket_contents("my-bucket")
print(files)
```

#### 7. `delete_file(bucket_name, remote_file_path)`

Deletes a file from a Google Cloud Storage bucket.

**Sample Usage:**
```python
gcs_handler.delete_file("my-bucket", "folder/file.txt")
```

#### 8. `delete_folder(bucket_name, remote_folder_path)`

Deletes a folder and all its contents from a Google Cloud Storage bucket.

**Sample Usage:**
```python
gcs_handler.delete_folder("my-bucket", "folder")
```

#### 9. `read_file_from_bucket(bucket_name, remote_file_path)`

Reads the contents of a file from a Google Cloud Storage bucket.

**Sample Usage:**
```python
content = gcs_handler.read_file_from_bucket("my-bucket", "folder/file.txt")
print(content)
```

#### 10. `delete_bucket(bucket_name)`

Deletes a bucket from the Google Cloud project if it exists.

**Sample Usage:**
```python
gcs_handler.delete_bucket("my-bucket")
```
