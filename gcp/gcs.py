import os
import logging
from google.cloud import storage

class GCSHandler:
    def __init__(self, project_id, credentials_path=None):
        """
        Initialize the GCS handler with the GCP project ID and credentials.

        :param project_id: The ID of your GCP project.
        :param credentials_path: Path to the service account key file.
        """
        self.project_id = project_id
        self.credentials_path = credentials_path
        self.storage_client = self._create_storage_client()
        self.logger = logging.getLogger(__name__)

    def _create_storage_client(self):
        """
        Create a storage client for connecting to GCS.

        :return: A client object for accessing GCS.
        """
        if self.credentials_path:
            return storage.Client.from_service_account_json(
                self.credentials_path,
                project=self.project_id
            )
        else:
            return storage.Client(project=self.project_id)

    def create_bucket(self, bucket_name, region_name="us-central1"):
        """
        Create a new bucket in the GCP project if it doesn't exist already.

        :param bucket_name: Name of the new bucket to be created.
        :param region_name: Region where the bucket will be located (default: "us-central1").
        :param storage_class: Storage class of the bucket (default: "STANDARD").
        :return: The newly created bucket object if successful, None otherwise.
        """
        buckets = self.list_buckets()
        bucket_names = [bucket.name for bucket in buckets]

        if bucket_name in bucket_names:
            self.logger.warning(f"Bucket '{bucket_name}' already exists.")
            return None

        try:
            bucket = self.storage_client.create_bucket(bucket_name, location=region_name)
            self.logger.info(f"Bucket '{bucket_name}' created successfully.")
            return bucket
        except Exception as e:
            self.logger.error(f"Error creating bucket '{bucket_name}': {str(e)}")
            return None

    def delete_bucket(self, bucket_name):
        """
        Delete a bucket from the GCP project if it exists.

        :param bucket_name: Name of the bucket to be deleted.
        """
        buckets = self.list_buckets()
        bucket_names = [bucket.name for bucket in buckets]

        if bucket_name not in bucket_names:
            self.logger.warning(f"Bucket '{bucket_name}' does not exist.")
            return

        bucket = self.storage_client.bucket(bucket_name)
        bucket.delete(force=True)
        self.logger.info(f"Bucket '{bucket_name}' deleted successfully.")

    def upload_file(self, local_file_path, bucket_name, remote_file_path):
        """
        Upload a file to a GCS bucket.

        :param local_file_path: Local path of the file to be uploaded.
        :param bucket_name: Name of the GCS bucket.
        :param remote_file_path: Path to save the file in the bucket.
        """
        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(remote_file_path)
        blob.upload_from_filename(local_file_path)
        self.logger.info(f"File '{local_file_path}' uploaded to '{bucket_name}/{remote_file_path}'.")

    def download_file(self, bucket_name, remote_file_path, local_file_path):
        """
        Download a file from a GCS bucket.

        :param bucket_name: Name of the GCS bucket.
        :param remote_file_path: Path of the file in the bucket.
        :param local_file_path: Local path to save the downloaded file.
        """
        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(remote_file_path)
        blob.download_to_filename(local_file_path)
        self.logger.info(f"File '{bucket_name}/{remote_file_path}' downloaded to '{local_file_path}'.")

    def read_file_from_bucket(self, bucket_name, remote_file_path):
        """
        Read the contents of a file from a GCS bucket.

        :param bucket_name: Name of the GCS bucket.
        :param remote_file_path: Path of the file in the bucket.
        :return: Contents of the file as string.
        """
        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(remote_file_path)
        return blob.download_as_string()

    def upload_folder(self, local_folder_path, bucket_name, remote_folder_path):
        """
        Upload a local folder to a GCS bucket.

        :param local_folder_path: Local path of the folder to be uploaded.
        :param bucket_name: Name of the GCS bucket.
        :param remote_folder_path: Path to save the folder in the bucket.
        """    
        for root, dirs, files in os.walk(local_folder_path):
            for file in files:
                local_file_path = os.path.join(root, file)
                remote_file_path = os.path.join(remote_folder_path, os.path.relpath(local_file_path, local_folder_path)).replace("\\", "/")
                self.upload_file(local_file_path, bucket_name, remote_file_path)

    def download_folder(self, bucket_name, remote_folder_path, local_folder_path):
        """
        Download a folder from a GCS bucket.

        :param bucket_name: Name of the GCS bucket.
        :param remote_folder_path: Path of the folder in the bucket.
        :param local_folder_path: Local path to save the downloaded folder.
        """
        bucket = self.storage_client.bucket(bucket_name)
        blobs = list(bucket.list_blobs(prefix=remote_folder_path))
        for blob in blobs:
            if not blob.name.endswith('/'):
                local_file_path = os.path.join(local_folder_path, os.path.relpath(blob.name, remote_folder_path))
                os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
                blob.download_to_filename(local_file_path)
                self.logger.info(f"File '{bucket_name}/{blob.name}' downloaded to '{local_file_path}'.")

    def delete_file(self, bucket_name, remote_file_path):
        """
        Delete a file from a GCS bucket.

        :param bucket_name: Name of the GCS bucket.
        :param remote_file_path: Path of the file in the bucket to be deleted.
        """
        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(remote_file_path)
        blob.delete()
        self.logger.info(f"File '{bucket_name}/{remote_file_path}' deleted.")

    def delete_folder(self, bucket_name, remote_folder_path):
        """
        Delete a folder and all its contents from a GCS bucket.

        :param bucket_name: Name of the GCS bucket.
        :param remote_folder_path: Path of the folder in the bucket to be deleted.
        """
        bucket = self.storage_client.bucket(bucket_name)
        blobs = bucket.list_blobs(prefix=remote_folder_path)
        for blob in blobs:
            blob.delete()
            self.logger.info(f"File '{bucket_name}/{blob.name}' deleted.")

    def list_buckets(self):
        """
        Get a list of all buckets in the GCP project.

        :return: A list of bucket objects.
        """
        return list(self.storage_client.list_buckets())

    def get_bucket_contents(self, bucket_name):
        """
        Get the contents of a bucket.

        :param bucket_name: Name of the GCS bucket.
        :return: A list of blob objects in the bucket.
        """
        bucket = self.storage_client.bucket(bucket_name)
        return list(bucket.list_blobs())
