import json
import boto3

def lambda_handler(event, context):
    if 'queryStringParameters' in event and 'email' in event['queryStringParameters']:
        email = event['queryStringParameters']['email']
        
        # publish message to SNS topic
        sns = boto3.client('sns')
        topic_arn = 'arn:aws:sns:us-east-1:748795926248:testfuntube'
        message = {
            'email': email
        }
        response = sns.publish(
            TopicArn=topic_arn,
            Message=json.dumps({'default': json.dumps(message)}),
            MessageStructure='json'
        )
        
        return {
            'statusCode': 200,
            'body': 'Email received'
        }
    else:
        return {
            'statusCode': 400,
            'body': 'Bad Request: Email parameter missing'
        }
#json {
 # "queryStringParameters": {
   # "email": "user4@example.com"
  #}
#}
