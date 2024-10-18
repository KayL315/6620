import boto3
import time

s3_client = boto3.client('s3', region_name='us-west-2')
lambda_client = boto3.client('lambda', region_name='us-west-2')

def lambda_handler(event, context):
    bucket_name = 'a2testbucket123'

    s3_client.put_object(Bucket=bucket_name, Key='assignment1.txt', Body='Empty Assignment 1')
    time.sleep(5)
    s3_client.put_object(Bucket=bucket_name, Key='assignment1.txt', Body='Empty Assignment 2222222222')
    time.sleep(5)
    
    s3_client.delete_object(Bucket=bucket_name, Key='assignment1.txt')
    time.sleep(5)
    
    s3_client.put_object(Bucket=bucket_name, Key='assignment2.txt', Body='33')
    

    lambda_client.invoke(FunctionName='plottingLambda')
    
    return {
        'statusCode': 200,
        'body': 'Operations completed.'
    }