import boto3
import matplotlib.pyplot as plt
from boto3.dynamodb.conditions import Key
import time
import io

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
s3 = boto3.client('s3', region_name='us-west-2')

def lambda_handler(event, context):
    bucket_name = 'a2testbucket123'
    table_name = 'S3-object-size-history'

    table = dynamodb.Table(table_name)
    current_time = int(time.time())
    start_time = current_time - 2500

    response = table.query(
        KeyConditionExpression=Key('BucketName').eq(bucket_name) &
                               Key('Timestamp').between(str(start_time), str(current_time))
    )

    print(f"DynamoDB query result: {response['Items']}")

    timestamps = []
    sizes = []
    max_size = 0
    
    for item in response['Items']:
        timestamps.append(int(item['Timestamp']))
        sizes.append(item['TotalSize'])
        max_size = max(max_size, item['TotalSize'])

    print(f"Plot data - sizes: {sizes}, timestamps: {timestamps}")

    if not timestamps:
        print("No data retrieved from DynamoDB.")
        return {
            'statusCode': 400,
            'body': 'No data to plot.'
        }

    plt.figure()
    plt.plot(timestamps, sizes, label='Bucket Size',color='blue', linewidth=2, marker='o', markersize=8)
    
    plt.axhline(y=max_size, color='r', linestyle='--', label='Max Size')

    plt.ylim(0, max_size + 5000)

    plt.xlabel('Timestamp')
    plt.ylabel('Bucket Size (Bytes)')
    plt.xticks(rotation=45)
    plt.legend()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
    print("Saving plot to S3...")
    s3.put_object(Bucket=bucket_name, Key='plot.png', Body=buffer, ContentType='image/png')
#    s3_client.put_object(Bucket=bucket_name, Key='plot/plot.png', Body=buffer, ContentType='image/png')
    print("Plot saved to S3.")
    
    return {
        'statusCode': 200,
        'body': 'Plot saved to S3.'
    }
