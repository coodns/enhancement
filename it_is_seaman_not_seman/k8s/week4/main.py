import boto3

sts_client = boto3.client('sts')

assumed_role = sts_client.assume_role(
    RoleArn="<target account arn>",
    RoleSessionName="crossAccountSession"
)

credentials = assumed_role['Credentials']

s3_client = boto3.client(
    's3',
    aws_access_key_id=credentials['AccessKeyId'],
    aws_secret_access_key=credentials['SecretAccessKey'],
    aws_session_token=credentials['SessionToken']
)

local_path = '/aws/answer.txt'
s3_client.download_file('<s3 bucket name>', '<key>', local_path)

print("File downloaded to", local_path)

try:
    with open(local_path, 'r') as file:
        content = file.read()
        print("File content:")
        print(content)

except Exception as e:
    print(f"Failed to read file: {e}")