import os
import json
import boto3
import get_crossaccount


def lambda_handler(event, context):
    json_region = os.environ['AWS_REGION']
    cred = get_crossaccount.get_cro.assume_role("account_id", "role_name")
    b3client = boto3.session(
        aws_access_key_id=cred.aws_access_key,
        aws_secret_access_key=cred.aws_secret_access_key,
        aws_session_token=cred.aws_session_token

    )
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "Region ": json_region
        })
    }