#!/usr/bin/env python

import boto3
import json

from datetime import datetime


def load_config():
    with open('config.json') as fp:
        content = fp.read()
        return json.loads(content)


def get_boto_client():
    return (boto3.client('sqs'), boto3.client('sns'))


def get_aws_account_id():
    return boto3.client('sts').get_caller_identity().get('Account')


def get_aws_region():
    return boto3.session.Session().region_name


def get_sns_arn(sns_name):
    return 'arn:aws:sns:%s:%s:%s' % (get_aws_region(), get_aws_account_id(), sns_name)


def fetch_queue_messages(sqs, config):
    messages = sqs.receive_message(
        QueueUrl = config['sqs']['queue_url'],
        MessageAttributeNames= ['timestamp'],
    )

    return [{'timestamp': message['MessageAttributes']['timestamp']['StringValue']}
            for message in messages.get('Messages', [])]


def send_sns_notification(sns, config):
    response = sns.publish(
        TopicArn = get_sns_arn(config['sns']['topic_name']),
        Subject = 'SQS Processes Complete',
        Message = 'The messages stored in SQS are processed',
    )

    print ('SQS Messages are processed and SNS Notification sent')


def get_utc_now():
    return datetime.utcnow().strftime("%b %d %Y %H:%M:%S")


def process_queue_messages(sqs, sns, config):
    while True:
        messages = fetch_queue_messages(sqs, config)
        
        if len(messages) == 0:
            send_sns_notification(sns, config)
            return

        for message in messages:
            utc_now = get_utc_now()

            with open('messages.txt', 'a') as fp:
                fp.write('%s - %s\n' % (utc_now, message['timestamp']))


if __name__ == "__main__":
    config = load_config()
    sqs, sns = get_boto_client()
    process_queue_messages(sqs, sns, config)
