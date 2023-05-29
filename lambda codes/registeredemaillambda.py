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
                'min' : data['priceRanges']['min'],
                'max' : data['priceRanges']['max']
                }
            # Update the item in DynamoDB
            update_dynamodb(table, show_id, event_data)

def update_dynamodb(table, show_id, event_data):
    # Update the item in DynamoDB
    table.update_item(
        Key={
            'id': show_id
        },
        UpdateExpression='SET #name = :name, #location = :location, #venue = :venue, #date = :date, #time = :time, #min = :min, #max = :max',
        ExpressionAttributeNames={
            '#name': 'name',
            '#location': 'location',
            '#venue': 'venue',
            '#date': 'date',
            '#time': 'time',
            '#min': 'min',
            '#max': 'max'
            },
        ExpressionAttributeValues={
            ':name': event_data['name'],
            ':location': event_data['location'],
            ':venue': event_data['venue'],
            ':date': event_data['date'],
            ':time': event_data['time'],
            ':min': event_data['min'],
            ':max': event_data['max']
            }
    )
 # Subscribe the user's email to an SNS topic
    sns = boto3.client('sns')
    sns_topic_arn = 'arn:aws:sns:us-east-1:035082996281:funtuberegisteredemail'
    try:
        response = sns.subscribe(
            TopicArn=sns_topic_arn,
            Protocol='email',
            Subject='Ticket Price Update'
        )
        # Customize the notification message here
        notification_message = f"This is the updated information for {artist_name} :\n{json.dumps(ticket_prices)}"
        # Send the customized notification to the user
        response = sns.publish(
            TopicArn=sns_topic_arn,
            Message=notification_message
        )

  

#Configure Test Event
# {
#   "id": "G5vjZ9ISF_0vU",
#   "email": "test2@gt.com"
# }