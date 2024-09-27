import boto3
import json

session = boto3.Session()
iam_client = session.client('iam')

# Create the Dev role
dev_role = iam_client.create_role(
    RoleName='Dev',
    AssumeRolePolicyDocument=json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "ec2.amazonaws.com"},
                "Action": "sts:AssumeRole"
            }
        ]
    })
)

# Attach full access to S3
iam_client.attach_role_policy(
    RoleName='Dev',
    PolicyArn='arn:aws:iam::aws:policy/AmazonS3FullAccess'
)

# Create the User role
user_role = iam_client.create_role(
    RoleName='User',
    AssumeRolePolicyDocument=json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "ec2.amazonaws.com"},
                "Action": "sts:AssumeRole"
            }
        ]
    })
)

# User role - list and get
iam_client.put_role_policy(
    RoleName='User',
    PolicyName='UserS3Access',
    PolicyDocument=json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": ["s3:ListBucket", "s3:GetObject"],
                "Resource": "*"
            }
        ]
    })
)

# Create a user
user_response = iam_client.create_user(UserName='MyIAMUser')

# access keys
access_key_response = iam_client.create_access_key(UserName='MyIAMUser')

# Print details
print("Access Key ID:", access_key_response['AccessKey']['AccessKeyId'])
print("Secret Access Key:", access_key_response['AccessKey']['SecretAccessKey'])

# Assume the Dev role using STS
sts_client = session.client('sts')
assume_dev_role = sts_client.assume_role(
    RoleArn='arn:aws:iam::515966507643:role/Dev',
    RoleSessionName='DevSession'
)

# Temporary credentials
dev_credentials = assume_dev_role['Credentials']

# Create an S3 client with temporary Dev role credentials
s3_client = boto3.client(
    's3',
    aws_access_key_id=dev_credentials['AccessKeyId'],
    aws_secret_access_key=dev_credentials['SecretAccessKey'],
    aws_session_token=dev_credentials['SessionToken']
)

# lecture1 bucket
s3_client.create_bucket(Bucket='lecture1')
s3_client.put_object(Bucket='lecture1', Key='assignment1.txt', Body='Empty Assignment 1')
s3_client.put_object(Bucket='lecture1', Key='assignment2.txt', Body='Empty Assignment 2')

with open('/Users/kaysmacpro/Downloads/111.jpg', 'rb') as f:
    s3_client.upload_fileobj(f, 'lecture1', 'recording1.jpg')


# Assume the User role
assume_user_role = sts_client.assume_role(
    RoleArn='arn:aws:iam::515966507643:role/User',
    RoleSessionName='UserSession'
)

user_credentials = assume_user_role['Credentials']
# Create an S3 client using the temporary credentials
s3_user_client = boto3.client(
    's3',
    aws_access_key_id=user_credentials['AccessKeyId'],
    aws_secret_access_key=user_credentials['SecretAccessKey'],
    aws_session_token=user_credentials['SessionToken']
)

# List objects in the 'lecture1' bucket with prefix 'assignment'
response = s3_user_client.list_objects_v2(Bucket='lecture1', Prefix='assignment')

# total size
total_size = sum(obj['Size'] for obj in response.get('Contents', []))

print(f"Total size of objects with prefix 'assignment': {total_size} bytes")

# Assume the Dev role
assume_dev_role = sts_client.assume_role(
    RoleArn='arn:aws:iam::515966507643:role/Dev',  # Replace with your account ID and role ARN
    RoleSessionName='DevSession'
)

dev_credentials = assume_dev_role['Credentials']

# Create an S3 client using the Dev role's temporary credentials
s3_dev_client = boto3.client(
    's3',
    aws_access_key_id=dev_credentials['AccessKeyId'],
    aws_secret_access_key=dev_credentials['SecretAccessKey'],
    aws_session_token=dev_credentials['SessionToken']
)

# Delete all objects from the 'lecture1' bucket
s3_dev_client.delete_objects(
    Bucket='lecture1',
    Delete={
        'Objects': [
            {'Key': 'assignment1.txt'},
            {'Key': 'assignment2.txt'},
            {'Key': 'recording1.jpg'}
        ]
    }
)

# Delete the 'lecture1' bucket
s3_dev_client.delete_bucket(Bucket='lecture1')
