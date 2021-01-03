import boto3
import os

session = boto3.Session(
    aws_access_key_id=os.environ.get('WK_AUTOMATION_ACCESS_KEY'),
    aws_secret_access_key=os.environ.get('WK_AUTOMATION_SECRET_KEY'),
    region_name=os.environ.get('WK_AWS_REGION') or 'us-east-1'
)
client = session.client('logs')


paginator = client.get_paginator('describe_log_groups')
response_iterator = paginator.paginate(PaginationConfig={'MaxItems': 200})
for page in response_iterator:
    for i in page['logGroups']:
        print(i['logGroupName'])
