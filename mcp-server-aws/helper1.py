import boto3
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def create_s3_bucket():
    bucket_name = os.getenv('S3_BUCKET_NAME', '')
    region = os.getenv('AWS_REGION', 'us-east-1')

    if not bucket_name:
        return "S3_BUCKET_NAME not set in environment."

    s3 = boto3.client('s3', region_name=region)

    try:
        if region == 'us-east-1':
            s3.create_bucket(Bucket=bucket_name)
        else:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        return f"S3 bucket '{bucket_name}' created successfully."
    except Exception as e:
        return f"Error creating S3 bucket: {e}"

def delete_s3_bucket():
    bucket_name = os.getenv('S3_BUCKET_NAME', '')
    region = os.getenv('AWS_REGION', 'us-east-1')

    if not bucket_name:
        return "S3_BUCKET_NAME not set in environment."

    s3 = boto3.client('s3', region_name=region)

    try:
        s3.delete_bucket(Bucket=bucket_name)
        return f"S3 bucket '{bucket_name}' deleted successfully."
    except Exception as e:
        return f"Error deleting S3 bucket: {e}"
