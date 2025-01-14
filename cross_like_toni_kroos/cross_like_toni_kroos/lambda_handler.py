import json
import boto3
import os
import random

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

    cred = get_cro.assume_role(target_account_id, target_role_name)

    ssm_client = boto3.client(
        'ssm',
        aws_access_key_id=cred['Credentials']['AccessKeyId'],
        aws_secret_access_key=cred['Credentials']['SecretAccessKey'],
        aws_session_token=cred['Credentials']['SessionToken'],
        config=cross_config
    )

    try:
        db_host = str(get_parameter(ssm_client, ssm_host_param))
        print(f"Database host: {db_host}")

        db_port = int(ssm_port_param)
        db_name = ssm_name_param
        db_user = get_parameter(ssm_client, ssm_user_param)
        db_password = get_parameter(ssm_client, ssm_password_param)

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
        cursor.execute("SELECT * FROM ")
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


def get_parameter(client, name):
    try:
        response = client.get_parameter(Name=name, WithDecryption=True)
        return response['Parameter']['Value']
    except client.exceptions.ParameterNotFound:
        raise ValueError(f"SSM Parameter '{name}' not found.")
    except Exception as e:
        raise RuntimeError(f"Failed to fetch parameter '{name}': {str(e)}")


class get_cro:
    @staticmethod
    def assume_role(account_id, role_name, *, session_name=None, transient_role_credentials=None):
        """
        Assume role in an account and return credentials

        Args:
            account_id (str): ID of the account to assume role in
            role_name (str): Name of the role to assume
            session_name (str): optional name for the assume_role session
            transient role (dict): result of a different assume_role call with credentials of the transient role

        Returns:
            dict: Credentials for the assumed role
        """
        # set up boto3 client to assume role adding transient role credentials if provided
        if not transient_role_credentials:
            sts_client = boto3.client('sts')
        else:
            sts_client = boto3.client('sts', **transient_role_credentials)

        # generate random session name if not provided
        if not session_name:
            session_name = f'AssumeRoleSession{random.randint(1, 1000)}'

        response = sts_client.assume_role(
            RoleArn=f'arn:aws:iam::{account_id}:role/{role_name}',
            RoleSessionName=session_name,
        )

        # creds = {
        #     'aws_access_key_id': response['Credentials']['AccessKeyId'],
        #     'aws_secret_access_key': response['Credentials']['SecretAccessKey'],
        #     'aws_session_token': response['Credentials']['SessionToken']
        # }

        return response
