import boto3
import matplotlib.pyplot as plt
import time
import io

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
s3 = boto3.client('s3', region_name='us-west-2')

def lambda_handler(event, context):
    bucket_name = 'a2testbucket123' 
    table_name = 'S3-object-size-history'

    table = dynamodb.Table(table_name)
    current_time = int(time.time())
    start_time = current_time - 10
    response = table.query(
    KeyConditionExpression=boto3.dynamodb.conditions.Key('BucketName').eq('a2testbucket123') &
                           boto3.dynamodb.conditions.Key('Timestamp').between(str(start_time), str(current_time))
)
    
    timestamps = []
    sizes = []
    max_size = 0
    
    for item in response['Items']:
        timestamps.append(int(item['Timestamp']))
        sizes.append(item['TotalSize'])
        max_size = max(max_size, item['TotalSize'])
    
    # Plotting
    plt.figure()
    plt.plot(timestamps, sizes, label='Bucket Size')
    plt.axhline(y=max_size, color='r', linestyle='--', label='Max Size')
    plt.xlabel('Timestamp')
    plt.ylabel('Bucket Size (Bytes)')
    plt.legend()
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    s3.put_object(Bucket='a2testbucket123', Key='plot.png', Body=buffer)
    
    return {
        'statusCode': 200,
        'body': 'Plot saved to S3.'
    }  