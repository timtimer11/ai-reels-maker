import os
import boto3
from io import BytesIO

# Configuration
S3_CONFIG = {
    'service_name': 's3',
    'endpoint_url': os.environ.get('CLOUDFLARE_ENDPOINT_URL'),
    'aws_access_key_id': os.environ.get('CLOUDFLARE_ACCESS_KEY_ID'),
    'aws_secret_access_key': os.environ.get('CLOUDFLARE_SECRET_ACCESS_KEY'),
    'region_name': 'auto'
}

CLOUDFLARE_PUBLIC_BUCKET_URL = os.environ.get('CLOUDFLARE_PUBLIC_BUCKET_URL')

class CloudflareS3:
    """
    This class is used to read and write files to a Cloudflare S3 bucket
    """
    def __init__(self, s3_client=None):
        self.s3_client = s3_client or boto3.client(**S3_CONFIG)

    def read_file_from_s3(self, bucket_name: str, file_name: str) -> BytesIO:
        """
        Read a file from S3 bucket and return its content as a BytesIO object
        """
        try:
            full_path = f"{bucket_name}/{file_name}"
            # Get the file from S3
            response = self.s3_client.get_object(Bucket=bucket_name, Key=full_path)
            # Read the file content
            file_content = response['Body'].read()
            # Return the file content as a BytesIO object
            return BytesIO(file_content)
        except Exception as e:
            print(f"Error reading file from S3: {e}")
            raise e

    def upload_file_to_s3(self, object_name: BytesIO, bucket_name: str, file_name_in_s3: str, ) -> str:
        """
        Upload an audio buffer to S3 bucket and return its URL
        """
        try:
            # Ensure the object is a BytesIO
            if not isinstance(object_name, BytesIO):
                object_name = BytesIO(object_name)

            # Reset the position to the beginning of the file
            object_name.seek(0)
            
            # Use the full path including bucket name
            full_path = f"{bucket_name}/{file_name_in_s3}"
            
            # Upload file to S3
            self.s3_client.upload_fileobj(
                object_name,
                bucket_name,
                full_path
            )
            return True
        except Exception as e:
            raise e

    def get_s3_url(self, bucket_name: str, file_name: str) -> str:
        """
        Get the public URL for a file in S3 bucket
        """
        try:
            # Generate the URL
            url = f"{CLOUDFLARE_PUBLIC_BUCKET_URL}/{bucket_name}/{file_name}"
            return url
        except Exception as e:
            raise e
