import boto3
import time

s3_client = boto3.client('s3', region_name='us-west-2')
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

def lambda_handler(event, context):
    bucket_name = 'a2testbucket123' 
    table_name = 'S3-object-size-history'
    
    # Fetch all objects
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    total_size = 0
    total_objects = 0
    
    if 'Contents' in response:
        for obj in response['Contents']:
            total_size += obj['Size']
            total_objects += 1
    
    timestamp = str(int(time.time()))
    
    table = dynamodb.Table(table_name)
    table.put_item(
        Item={
            'BucketName': bucket_name,
            'Timestamp': timestamp,
            'TotalSize': total_size,
            'ObjectCount': total_objects,
            'RecordedAt': timestamp
        }
    )
    
    return {
        'statusCode': 200,
        'body': 'Bucket size recorded successfully.'
    }