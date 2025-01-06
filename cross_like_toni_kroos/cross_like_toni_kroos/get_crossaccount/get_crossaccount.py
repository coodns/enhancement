import boto3
import random

class get_cro:

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

        creds = {
            'aws_access_key_id': response['Credentials']['AccessKeyId'],
            'aws_secret_access_key': response['Credentials']['SecretAccessKey'],
            'aws_session_token': response['Credentials']['SessionToken']
        }

        return creds

