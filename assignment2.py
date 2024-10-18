import boto3
import botocore

s3_client = boto3.client('s3', region_name='us-west-2')
dynamodb_client = boto3.client('dynamodb', region_name='us-west-2')


def create_s3_bucket(bucket_name):
    try:
        location = {'LocationConstraint': 'us-west-2'}

        s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
        print(f"Bucket {bucket_name} created.")
    except botocore.exceptions.ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'BucketAlreadyExists':
            print(f"Bucket {bucket_name} already exists. Please choose a different name.")
        elif error_code == 'InvalidBucketName':
            print(f"Invalid bucket name: {bucket_name}. Please make sure it follows S3 naming rules.")
        else:
            print(f"Error creating bucket: {e}")


def create_dynamodb_table(table_name):
    try:
        dynamodb_client.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'BucketName',
                    'KeyType': 'HASH'  
                },
                {
                    'AttributeName': 'Timestamp',
                    'KeyType': 'RANGE'  
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'BucketName',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'Timestamp',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print(f"DynamoDB table {table_name} created.")
    except botocore.exceptions.ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'ResourceInUseException':
            print(f"DynamoDB table {table_name} already exists. No need to create it again.")
        else:
            print(f"Error creating table: {e}")

create_s3_bucket('a2testbucket123') 
create_dynamodb_table('S3-object-size-history')