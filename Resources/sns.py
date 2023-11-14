import boto3
import json
from Resources.aws import env

def aws_sns(message, subject):
    topic_arn = env.arn
    try:
        # Set up access to sns client
        sns_client = boto3.client('sns',
                                 aws_access_key_id=env.aws_user_access_key,
                                 aws_secret_access_key=env.aws_secret_access_key,
                                 region_name='us-east-2')

        # Example message and subject
        # message = {"member_id": 123,
        #            "member_name": "Test Trader",
        #            "portfolio_value": 1000000,
        #            "age": 23}
        # subject = "ADD_MEMBER"

        # publish notification and retrieve response
        response = sns_client.publish(TopicArn=topic_arn,
                                     Message=json.dumps(message),
                                     Subject=subject)

        # Print response if notification sent successfully
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            print(response)
            print("Notification sent successfully.")
    # Return error if response fails
    except Exception as e:
        print("Error while publishing notification:", e)
