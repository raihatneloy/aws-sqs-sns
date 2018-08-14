# aws-sqs-sns

## Requirements
Python: 3.6

### Pip package requirements
From the root directory of the repository, run the following command:<br/>
`pip install -r requirements.txt`

## Running the script
`config.json` file should contain information in the following format:
```
{
    "sqs": {
        "queue_name": "<your sqs queue name>"
    },
    "sns": {
        "topic_name": "<your sns topic name for notification>"
    }
}
```
From the root directory of the repository, run the following command:<br/>
`./aws-sqs-sns-check.py`<br/>
After the command completes, there will be a file on the root directory of the repository names `messages.txt` where the outputs should be written