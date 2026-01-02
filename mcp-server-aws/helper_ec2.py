import boto3

import os

import sys

from botocore.exceptions import ClientError

from dotenv import load_dotenv
 
# Load environment variables from .env if available

load_dotenv()
 
# Initialize AWS clients dynamically (can expand for other services)

aws_clients = {

    "ec2": boto3.client(

        "ec2", region_name=os.getenv("AWS_REGION", "us-east-1")

    ),

    "s3": boto3.client(

        "s3", region_name=os.getenv("AWS_REGION", "us-east-1")

    ),

    "lambda": boto3.client(

        "lambda", region_name=os.getenv("AWS_REGION", "us-east-1")

    ),

}
 
 
def create_ec2_instance(**kwargs):

    """Create an EC2 instance with dynamic parameters or defaults from env."""

    ec2 = aws_clients["ec2"]
 
    ami_id = kwargs.get("ImageId", os.getenv("AMI_ID"))

    instance_type = kwargs.get("InstanceType", os.getenv("INSTANCE_TYPE", "t2.micro"))

    key_name = kwargs.get("KeyName", os.getenv("KEY_NAME"))

    security_group_ids = kwargs.get(

        "SecurityGroupIds", os.getenv("SECURITY_GROUP_IDS", "").split(",")

    )
 
    if not ami_id or not key_name or not security_group_ids:

        print("Missing required EC2 parameters (AMI_ID, KEY_NAME, SECURITY_GROUP_IDS).")

        return None
 
    try:

        response = ec2.run_instances(

            ImageId=ami_id,

            InstanceType=instance_type,

            MinCount=1,

            MaxCount=1,

            KeyName=key_name,

            SecurityGroupIds=list(security_group_ids),

            TagSpecifications=[

                {

                    "ResourceType": "instance",

                    "Tags": [

                        {"Key": "Name", "Value": kwargs.get("Name", "MyPyEc2Instance-mcp")},

                        {"Key": "Environment", "Value": kwargs.get("Environment", "Staging")},

                    ],

                }

            ],

        )

        instance_id = response["Instances"][0]["InstanceId"]

        print(f"EC2 instance created with ID: {instance_id}")

        return instance_id

    except ClientError as e:

        print(f"Error creating EC2 instance: {e}")

        return None
 
 
def terminate_ec2_instance(instance_id: str):

    """Terminate an EC2 instance by ID."""

    ec2 = aws_clients["ec2"]
 
    try:

        response = ec2.terminate_instances(InstanceIds=[instance_id])

        print(f"Terminating instance: {instance_id}")

        for instance in response["TerminatingInstances"]:

            print(f"  Instance ID: {instance['InstanceId']}")

            print(f"  Previous State: {instance['PreviousState']['Name']}")

            print(f"  Current State: {instance['CurrentState']['Name']}")

        return True

    except ClientError as e:

        print(f"Error terminating instance {instance_id}: {e}")

        return False
 

def stop_ec2_instance(instance_id: str):
    """Stop an EC2 instance by ID."""
    ec2 = aws_clients["ec2"]
    try:
        response = ec2.stop_instances(InstanceIds=[instance_id])
        print(f"Stopping instance: {instance_id}")
        for instance in response["StoppingInstances"]:
            print(f"  Instance ID: {instance['InstanceId']}")
            print(f"  Previous State: {instance['PreviousState']['Name']}")
            print(f"  Current State: {instance['CurrentState']['Name']}")
        return True
    except ClientError as e:
        print(f"Error stopping instance {instance_id}: {e}")
        return False


def start_ec2_instance(instance_id: str):
    """Start an EC2 instance by ID."""
    ec2 = aws_clients["ec2"]
    try:
        response = ec2.start_instances(InstanceIds=[instance_id])
        print(f"Starting instance: {instance_id}")
        for instance in response["StartingInstances"]:
            print(f"  Instance ID: {instance['InstanceId']}")
            print(f"  Previous State: {instance['PreviousState']['Name']}")
            print(f"  Current State: {instance['CurrentState']['Name']}")
        return True
    except ClientError as e:
        print(f"Error starting instance {instance_id}: {e}")
        return False


def perform_aws_action(service: str, action: str, **kwargs):

    """

    Generic AWS action handler for EC2, S3, Lambda, etc.

    :param service: AWS service (ec2, s3, lambda)

    :param action: Action to perform (create, terminate, deploy, etc.)

    :param kwargs: Service-specific parameters

    :return: Result or error message

    """

    client = aws_clients.get(service.lower())

    if not client:

        return f"Service '{service}' is not supported."
 
    try:

        if service.lower() == "ec2":

            if action.lower() == "create":

                return create_ec2_instance(**kwargs)

            elif action.lower() == "terminate":

                instance_id = kwargs.get("InstanceId")

                if not instance_id:

                    return "InstanceId is required to terminate EC2 instance."

                return terminate_ec2_instance(instance_id)
 
        elif service.lower() == "s3":

            if action.lower() == "create":

                bucket_name = kwargs.get("BucketName")

                if not bucket_name:

                    return "BucketName is required to create S3 bucket."

                client.create_bucket(Bucket=bucket_name)

                return f"S3 bucket '{bucket_name}' created successfully."
 
        elif service.lower() == "lambda":

            if action.lower() == "deploy":

                function_name = kwargs.get("FunctionName")

                runtime = kwargs.get("Runtime", "python3.9")

                role = kwargs.get("Role")

                handler = kwargs.get("Handler", "lambda_function.lambda_handler")

                code = kwargs.get("Code")

                if not all([function_name, role, code]):

                    return "FunctionName, Role, and Code are required to deploy Lambda."

                client.create_function(

                    FunctionName=function_name,

                    Runtime=runtime,

                    Role=role,

                    Handler=handler,

                    Code=code,

                )

                return f"Lambda function '{function_name}' deployed successfully."
 
        return f"Action '{action}' not supported for service '{service}'."
 
    except ClientError as e:

        return f"AWS ClientError: {e}"
 
 
if __name__ == "__main__":

    # Test example for EC2

    instance_id = create_ec2_instance()

    if instance_id:

        terminate_ec2_instance(instance_id)

    else:

        print("No instance created; cannot terminate.")
