# FunTube
## Table of Contents
1. Introduction
2. Features
3. Technologies Used
4. Usage
5. Deployment
6. Contributing
7. License
## 1. Introduction
FunTube is a web application that provides daily updates on selected ticket prices from Ticketmaster. It allows users to fill out a form and select their preferred concert information. The application uses AWS Amplify to host the website, AWS Gateway as the API gateway, AWS Lambda to store information into DynamoDB, and CloudWatch to trigger another Lambda function. The triggered Lambda function retrieves updated information, stores it into DynamoDB, and sends daily notifications to users about updated pricing information.

## 2. Features
User-friendly web interface to select concert information. Automated daily updates on selected ticket prices. Storing and retrieving data using DynamoDB. Notification system to inform users about updated pricing information

## 3. Technologies Used
AWS Amplify, AWS Gateway, AWS Lambda, DynamoDB, CloudWatch, AWS SNS, Jenkins, Docker, and GitHub

## 4. Usage
1. Open the FunTube website in your preferred web browser.

2. Fill out the form and select your preferred concert information.

3. Submit the form to store the information in DynamoDB.

4. The CloudWatch rule triggers the Lambda function daily at 10:00 AM EST to retrieve updated pricing information.

5. The Lambda function stores the updated information in DynamoDB.

6. Users receive daily notifications about updated pricing information.

## 5. Deployment
To deploy FunTube to a production environment, you can follow the steps below:

1. Set up an AWS account if you haven't already.

2. Set up the required AWS services, such as Amplify, DynamoDB, AWS Gateway, AWS SNS and CloudWatch.

3. Configure the necessary environment variables and permissions for the Lambda functions.

4. Push the updated code to the remote repository.

5. Configure the production environment in the AWS Amplify console.

6. Trigger the initial deployment using the AWS Amplify console.

7. Monitor the deployment process and ensure all resources are provisioned successfully.

8. Once the deployment is complete, FunTube will be accessible to users through the Amplify-provided URL.

## 6. Contributing
Contributions are welcome! If you find any issues or would like to suggest improvements, please create a new issue or submit a pull request.

Before contributing, please review our Contributing Guidelines.

## 7. License
The FunTube project is licensed under the MIT License.
