import os
import boto3
from dotenv import load_dotenv
from io import BytesIO

load_dotenv()

# Initialize S3 client
s3_client = boto3.client(
    service_name='s3',
    endpoint_url=os.getenv('CLOUDFLARE_ENDPOINT_URL'),
    aws_access_key_id=os.getenv('CLOUDFLARE_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('CLOUDFLARE_SECRET_ACCESS_KEY'),
    region_name='auto'
)

CLOUDFLARE_ENDPOINT_URL = os.getenv('CLOUDFLARE_ENDPOINT_URL')

def read_file_from_s3(bucket_name: str, file_name: str) -> BytesIO:
    """
    Read a file from S3 bucket and return its content as a BytesIO object.
    """
    try:
        full_path = f"{bucket_name}/{file_name}"
        response = s3_client.get_object(Bucket=bucket_name, Key=full_path)
        file_content = response['Body'].read()
        return BytesIO(file_content)
    except Exception as e:
        print(f"Error reading file from S3: {e}")
        raise e

def upload_file_to_s3(object_name: BytesIO, bucket_name: str, file_name_in_s3: str, ) -> str:
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
        print(f"Uploading file with full path: {full_path}")
        
        # Upload file to S3
        s3_client.upload_fileobj(
            object_name,
            bucket_name,
            full_path
        )
        
        print(f"Successfully uploaded file to S3 key: {full_path}")

        return True
    except Exception as e:
        print(f"Error uploading file to S3: {e}")
        raise e

def get_s3_url(file_name: str) -> str:
    """
    Get the public URL for a file in S3 bucket.
    
    Args:
        bucket_name (str): Name of the S3 bucket
        file_name (str): Name of the file in S3
        
    Returns:
        str: Public URL of the file
    """
    try:
        # Generate the URL
        url = f"{CLOUDFLARE_ENDPOINT_URL}/{file_name}"
        return url
    except Exception as e:
        print(f"Error generating S3 URL: {e}")
        raise e
