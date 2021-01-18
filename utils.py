import boto3
import os
import sys
import json
import logging
import uuid

from botocore.exceptions import ClientError

log = logging.getLogger()
log.setLevel(logging.INFO)
logging.getLogger('botocore').setLevel(logging.WARNING)


LOG_SHIPPER_FUNCTION = os.environ.get('TARGET_FUNCTION') or None

session = boto3.Session(
    aws_access_key_id=os.environ.get('AUTOMATION_ACCESS_KEY'),
    aws_secret_access_key=os.environ.get('AUTOMATION_SECRET_KEY'),
    region_name=os.environ.get('AWS_REGION') or 'us-east-1'
)
cloud_watch = session.client('logs')

lambda_func = session.client('lambda')


def get_lambda_policy():
    try:
        lambda_policy = lambda_func.get_policy(FunctionName=LOG_SHIPPER_FUNCTION).get("Policy")
        return json.loads(lambda_policy)

    except ClientError as error:
        raise error


def remove_lambda_permissions(sid):
    try:
        remove_permission = lambda_func.remove_permission(FunctionName=LOG_SHIPPER_FUNCTION, StatementId=sid)
        return remove_permission
    except ClientError as error:
        raise error

