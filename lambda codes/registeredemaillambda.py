import boto3
import requests
import json

dynamodb_table_name = "funtubeDB2"

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

def lambda_handler(event, context):
    # Retrieve artist and user details from event
    table = dynamodb.Table(dynamodb_table_name)
    response = table.scan()
    # Items : {data}, somethingelse: {someData}
    for item in response['Items']:
        show_id = item['id']
        email = item['email']

        # Set up the Ticketmaster API endpoint URL
        #url = f'https://app.ticketmaster.com/discovery/v2/events/G5vjZ9ISF_0vU.json?apikey=7kyWM9xf2TVWoiEpA7lEXDsAFLjvAGN1'
        url = f'https://app.ticketmaster.com/discovery/v2/events/{show_id}.json?apikey=7kyWM9xf2TVWoiEpA7lEXDsAFLjvAGN1'
        # Make the API request
        response = requests.get(url)
        # Check for a successful response
        if response.status_code == 200:
            # Parse the JSON response
            data = json.loads(response.text)
            # Extract the desired information from the response
            event_data = {
                'name' : data['name'],
                'location' : data['_embedded']['venues'][0]['city']['name'],
                'venue' : data['_embedded']['venues'][0]['name'],
                'date' : data['dates']['start']['localDate'],
                'time' : data['dates']['start']['localTime'],
                'id' : data['id'],
                'min' : str(data['priceRanges'][0]['min']),
                'max' : str(data['priceRanges'][0]['max'])
            }
            print(type(data['priceRanges'][0]['min']))
            # Update the item in DynamoDB
            update_dynamodb(table, email, show_id, event_data)
            #Notifying users of updated information
            sending_user_updated_info(email, event_data)
            
            

def update_dynamodb(table, email, show_id, event_data):
    dynamodb_client = boto3.client('dynamodb')
    # Update the item in DynamoDB
    response = dynamodb_client.update_item(
        TableName = 'funtubeDB2',
        Key={
            'id': {'S' : event_data['id']},
            'email': {'S' : email}
        },
        UpdateExpression='SET #min = :min, #max = :max',
        ExpressionAttributeNames={
            '#min': 'min',
            '#max': 'max'
            },
        ExpressionAttributeValues={
            ':min': {'S' : event_data['min']},
            ':max': {'S' : event_data['max']}
            }
    )
    
def sending_user_updated_info(email, event_data):
    sns = boto3.client('sns')
    sns_topic_arn = 'arn:aws:sns:us-east-1:035082996281:email'
    try:
        response = sns.publish(
            TopicArn=sns_topic_arn,
            # Protocol='email',
            Message=f"This is the updated information for {'name'}: The current lowest price is ${event_data['min']} and the highest price is ${event_data['max'].",
            Subject='Ticket Price Update',
            MessageAttributes={
                'Email': {
                    'DataType': 'String',
                    'StringValue': email
                }
            }
        )
        print("User has been updated successfully.")
    except Exception as e:
        print("Error sending email")

#Configure Test Event
# {
#   "id": "G5vjZ9ISF_0vU",
#   "email": "test2@gt.com"
# }