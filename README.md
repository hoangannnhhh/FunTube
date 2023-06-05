# FunTube
## Table of Contents
1. Introduction
2. Features
3. Technologies Used
4. Setup
5. Usage
6. Deployment
7. Contributing
8. License
## 1. Introduction
FunTube is a web application that provides daily updates on selected ticket prices from Ticketmaster. It allows users to fill out a form and select their preferred concert information. The application uses AWS Amplify to host the website, AWS Gateway as the API gateway, AWS Lambda to store information into DynamoDB, and CloudWatch to trigger another Lambda function. The triggered Lambda function retrieves updated information, stores it into DynamoDB, and sends daily notifications to users about updated pricing information.

## 2. Features
User-friendly web interface to select concert information
Automated daily updates on selected ticket prices
Storing and retrieving data using DynamoDB
Notification system to inform users about updated pricing information

## 3. Technologies Used
AWS Amplify
AWS Gateway
AWS Lambda
DynamoDB
CloudWatch

## 5. Usage
Open the FunTube website in your preferred web browser.

Fill out the form and select your preferred concert information.

Submit the form to store the information in DynamoDB.

The CloudWatch rule triggers the Lambda function daily to retrieve updated pricing information.

The Lambda function stores the updated information in DynamoDB.

Users receive daily notifications about updated pricing information.

## 6. Deployment
To deploy FunTube to a production environment, you can follow the steps below:

Set up an AWS account if you haven't already.

Set up the required AWS services, such as Amplify, DynamoDB, AWS Gateway, and CloudWatch, following the instructions in the Setup section.

Configure the necessary environment variables and permissions for the Lambda functions.

Push the updated code to the remote repository.

Configure the production environment in the AWS Amplify console.

Trigger the initial deployment using the AWS Amplify console.

Monitor the deployment process and ensure all resources are provisioned successfully.

Once the deployment is complete, FunTube will be accessible to users through the Amplify-provided URL.

## 7. Contributing
Contributions are welcome! If you find any issues or would like to suggest improvements, please create a new issue or submit a pull request.

Before contributing, please review our Contributing Guidelines.

## 8. License
The FunTube project is licensed under the MIT License.
