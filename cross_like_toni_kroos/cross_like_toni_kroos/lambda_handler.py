import json
import boto3
import os
import get_crossaccount
from botocore.config import Config
import mysql.connector


def lambda_handler(event, context):
    # Get environment variables
    json_region = os.environ['AWS_REGION']
    ssm_host_param = os.environ['SSM_HOST_PARAM']
    ssm_port_param = os.environ['SSM_PORT_PARAM']
    ssm_name_param = os.environ['SSM_DB_NAME_PARAM']
    ssm_user_param = os.environ['SSM_USERNAME_PARAM']
    ssm_password_param = os.environ['SSM_PASSWORD_PARAM']
    target_account_id = os.environ['TARGET_ACCOUNT_ID']
    target_role_name = os.environ['TARGET_ROLE_NAME']

    cross_config = Config(
        region_name=json_region
    )

    cred = get_crossaccount.get_cro.assume_role(target_account_id, target_role_name)

    ssm_client = boto3.client(
        'ssm',
        aws_access_key_id=cred['Credentials']['AccessKeyId'],
        aws_secret_access_key=cred['Credentials']['SecretAccessKey'],
        aws_session_token=cred['Credentials']['SessionToken'],
        config=cross_config
    )

    try:
        db_host = ssm_client.get_parameter(Name=ssm_host_param, WithDecryption=True)['Parameter']['Value']
        db_port = int(ssm_client.get_parameter(Name=ssm_port_param, WithDecryption=True)['Parameter']['Value'])
        db_name = ssm_client.get_parameter(Name=ssm_name_param, WithDecryption=True)['Parameter']['Value']
        db_user = ssm_client.get_parameter(Name=ssm_user_param, WithDecryption=True)['Parameter']['Value']
        db_password = ssm_client.get_parameter(Name=ssm_password_param, WithDecryption=True)['Parameter']['Value']

        conn = mysql.connector.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password,
            connect_timeout=5,
            connection_timeout=5,
            use_pure=True
        )

        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "MySQL connection successful"
            })
        }

    except mysql.connector.Error as db_err:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "error": f"Database error: {str(db_err)}"
            })
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "error": str(e)
            })
        }
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()
