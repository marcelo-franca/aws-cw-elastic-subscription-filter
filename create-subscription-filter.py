import boto3
import os
import sys
import logging
import uuid


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


def get_shipper_arn():
    response_lambda = lambda_func.get_function(FunctionName=LOG_SHIPPER_FUNCTION)
    return response_lambda['Configuration']['FunctionArn']


def create_subscription(region_name, account_id, log_group_name):
    log.info('Configuring lambda permissions')

    lambda_func.add_permission(
        FunctionName=LOG_SHIPPER_FUNCTION,
        StatementId=str(uuid.uuid4()),
        Action='lambda:InvokeFunction',
        Principal='logs.amazonaws.com',
        SourceArn=f'arn:aws:logs:{region_name}:{account_id}:log-group:{log_group_name}:*',
        SourceAccount=account_id
    )

    subscription = cloud_watch.put_subscription_filter(
        logGroupName=f'{log_group_name}',
        filterName=f"{log_group_name.split('/')[-1]}",
        filterPattern='',
        destinationArn=get_shipper_arn()
    )
    return subscription


def main():
    region_name = os.environ.get('AWS_REGION') or 'us-east-1'
    account_id = os.environ.get('AWS_ACCOUNT_ID')
    try:
        if len(sys.argv) < 2:
            log.warning("Looks like you do not define the log group name that you should create an elastic "
                        "subscription.\nPlease, input it below or quit and try again.")
            while True:
                _input = input("Log Group Name: ")
                if _input == '':
                    break
                else:
                    log_group_name = _input
                    create_subscription(region_name, account_id, log_group_name)
                    return log_group_name

        log_group_name = sys.argv[1]
        create_subscription(region_name, account_id, log_group_name)
    except IndexError:
        log.error("You do not define a log group name.")
    except KeyboardInterrupt:
        log.info("Exiting")


if __name__ == '__main__':
    main()
