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

def read_file_from_s3(bucket_name: str, file_name: str) -> BytesIO:
    """
    Read a file from S3 bucket and return its content as a BytesIO object.

    Args:
        bucket_name (str): Имя S3 бакета
        file_name (str): Имя файла в S3

    Returns:
        BytesIO: File content as a BytesIO object that can be read based on file type
    """
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
        file_content = response['Body'].read()
        return BytesIO(file_content)
    except Exception as e:
        print(f"Error reading file from S3: {e}")
        raise e

def upload_audio_to_s3(object_name: BytesIO, bucket_name: str, file_name_in_s3: str, ) -> str:
    """
    Upload an audio buffer to S3 bucket and return its URL
    
    Args:
        file_obj (BytesIO): Аудио буфер для загрузки
        file_name_in_s3 (str): Имя файла в S3
        bucket_name (str): Имя S3 бакета
        
    Returns:
        str: URL загруженного файла
    """
    try:
        # Загружаем файл в S3
        s3_client.upload_fileobj(
            object_name,
            bucket_name,
            file_name_in_s3
        )
        
        print(f"Uploading file to S3 key: {file_name_in_s3}")

        return True
    except Exception as e:
        print(f"Error uploading file to S3: {e}")
        raise e

# if __name__ == "__main__":
#     # Test configuration
#     bucket_name = os.getenv('CLOUDFLARE_TTS_BUCKET_NAME')
#     file_name_in_s3 = "subway_surfers.mp4"
#     file_path = "/Users/timur/Downloads/brain_rot_production_v2/subway_surfers.mp4"
#     with open(file_path, 'rb') as f:
#         upload_audio_to_s3(object_name=f, bucket_name=bucket_name, file_name_in_s3=file_name_in_s3)
#     # obj = read_file_from_s3(bucket_name=bucket_name, file_name="test.mp3")
#     # with open("test.mp3", "wb") as f:
#     #     f.write(obj.getbuffer())