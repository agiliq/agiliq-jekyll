---
layout: post
comments: true
title:  "Getting started with AWS Lambda using Python"
description: "Writing a Hello World Python web application using lambda"
keywords: "Serverless, Python, AWS, Lambda"
date: 2019-09-20
categories: [Serverless, AWS]
author: Akshar
---

## Agenda

We will create our first serverless web application using bare Python, API Gateway and AWS Lambda.

## Setup

I like to work with IAM users having limited permissions.

### IAM user setup

You can continue working as root user if you want to avoid IAM hassle. Skip to next section in such case.

Let's create an IAM user who has Lambda and API Gateway permissions. This step will have to be done while logged in as a root user or someone who has IAM permissions.

![](/assets/images/aws/add-user.png)

On next screen, select `Create group`. Enter `Group name` and enable following policies:

- AmazonAPIGatewayAdministrator
- AWSLambdaFullAccess
- IAMFullAccess

Associate the user with group.

![](/assets/images/aws/associate-user-group.png)

Skip `Tags` and go to Review screen. Create the user.

![](/assets/images/aws/create-user.png)

Logout as root user and login as this user.

### Writing a lambda function

Navigate to `Lambda` service in the AWS console. It would look similar to:

![](/assets/images/aws/lambda-screen.png)

Click `Create function`. Choose `Author from scratch`.

Enter `Function name` as `hello-world`. `Runtime` as `Python 3.7`. `Execution role` as `Create a new role with basic Lambda permissions`. Click on `Create function`.

A lambda function would be created.

You will notice two tabs. `Configuration` and `Monitoring`. By default `Configuration` would be selected. `Configuration` has following sections.

- Designer
- Function code
- Environment variables

And few more sections.

You should see a code editor under `Function code`. It should have some code written by default. Change the code to following:

    def lambda_handler(event, context):
        return {
            'statusCode': 200,
            'body': 'Hello World!'
        }

And `Save`, you will find `Save` button on top right corner.

The lambda function is ready. Let's setup API Gateway now.

### API Gateway setup

Navigate to `API Gateway` service in the AWS console. Click `Create API`.

![](/assets/images/aws/gateway-screen.png)

Give `API name` as `hello-world`. Let `Endpoint Type` stay as `Regional`. Click `Create API`.

Choose `Create Method` from `Actions`.

![](/assets/images/aws/gateway-create-method.png)

In the dropdown, select `GET` and tick.

In `GET - Setup`, choose Integration Type as `Lambda Function`. In `Lambda Function` field, start typing name of your lambda function. In our case it is `hello-world`.

![](/assets/images/aws/gateway-get-setup.png)

Do `Save`.

From left panel, select `Stages`. Click on `Create`

Follow following 7 steps.o

You will get a url similar to https://do80fzbglf.execute-api.ap-south-1.amazonaws.com/prod.

Navigating to this url should give you the following response.

    {"statusCode": 200, "body": "Hello World!"}
