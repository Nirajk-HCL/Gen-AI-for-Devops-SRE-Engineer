import boto3
import os
from dotenv import load_dotenv

load_dotenv()

def create_lambda_function():
    lambda_client = boto3.client('lambda', region_name=os.getenv('AWS_REGION'))

    function_name = os.getenv('LAMBDA_FUNCTION_NAME')
    role_arn = os.getenv('LAMBDA_ROLE_ARN')
    handler = os.getenv('LAMBDA_HANDLER', 'lambda_function.lambda_handler')
    runtime = os.getenv('LAMBDA_RUNTIME', 'python3.12')
    zip_path = os.getenv('LAMBDA_ZIP_PATH', 'function.zip')

    try:
        with open(zip_path, 'rb') as f:
            zipped_code = f.read()

        response = lambda_client.create_function(
            FunctionName=function_name,
            Runtime=runtime,
            Role=role_arn,
            Handler=handler,
            Code={'ZipFile': zipped_code},
            Publish=True,
            Timeout=15,
            MemorySize=128,
        )
        return f"Lambda function '{function_name}' created successfully."
    except Exception as e:
        return f"Error creating Lambda function: {e}"

def delete_lambda_function():
    lambda_client = boto3.client('lambda', region_name=os.getenv('AWS_REGION'))
    function_name = os.getenv('LAMBDA_FUNCTION_NAME')

    try:
        lambda_client.delete_function(FunctionName=function_name)
        return f"Lambda function '{function_name}' deleted successfully."
    except Exception as e:
        return f"Error deleting Lambda function: {e}" 
