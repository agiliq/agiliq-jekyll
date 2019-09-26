---
layout: post
comments: true
title:  "A serverless web application using Python, API Gateway and Lambda function"
description: "Creating a REST application using AWS Chalice and Peewee"
keywords: "AWS, Chalice, Peewee, Serverless"
date: 2019-09-22
categories: [Serverless, AWS, Lambda]
author: Akshar
---

## Agenda

This post is inspired by Django polls app. We will build RESTful endpoints for a polls app using AWS Chalice.

We will use a Postgres database. We want to avoid raw sql queries and hence will use peewee as our ORM.

We will be creating the following apis in this post.

- An api to create a poll question.
- Api to list questions.
- Api to get question detail.
- Api to edit a question.
- Api to delete a question.

## Setup

Let's create a virtualenv.

    mkvirtualenv --python=/usr/local/bin/python3 use-chalice

We are using Python 3.7 through this post.

Install chalice

    pip install chalice

Create a chalice project.

    chalice new-project polls

We are assuming that your AWS credentials are properly configured in ~/.aws/config.

`chalice new-project` would create the following files:

    drwxr-xr-x   .chalice
    -rw-r--r--   app.py
    -rw-r--r--   requirements.txt

Ignore `.chalice` and `requirements.txt` for now.

Issue following command to run the chalice server locally

    chalice local

Navigate to http://localhost:8000/. You should see `{"hello": "world"}` on the page.

This confirms our setup is working properly. Let's deploy our app using API Gateway and Lamda function. Run the following command
    
    chalice deploy

The output would look similar to:

![](/assets/images/aws/chalice-deploy.png)

This assumes that the AWS credentials configured in ~/.aws/config has proper IAM policies assigned. The user should have the following policies assigned:

- AWSLambdaFullAccess
- AmazonAPIGatewayAdministrator
- IAMFullAccess

Navigate to `Rest API URL`. The api url I got is `https://baxnta8me9.execute-api.ap-south-1.amazonaws.com/api/`

![](/assets/images/aws/rest-api-url-index.png)

## Polls apis

Our codebase isn't going to have a single `index` route anymore. It will be a full-fledged web application having database connection code, an ORM, and several routes, and associated views for the routes.

We should be splitting this logic across multiple modules instead of keeping everything in `app.py`.

If we want any other file apart from `app.py` to be packaged by chalice during deployment, it needs to be in a `chalicelib` directory. Let's create this directory.

    mkdir chalicelib

We will keep four files in `chalicelib` namely `__init__.py`, `settings.py`, `db.py` and `models.py`.

    touch chalicelib/__init__.py
    touch chalicelib/settings.py
    touch chalicelib/db.py
    touch chalicelib/models.py

We don't want to keep database credentials in code and hence will keep them in environment variables. We will read the environment variables in `settings.py`.

Add following code to `settings.py`.

    # chalicelib/settings.py
    import os

    DATABASE = {
        'HOST': os.environ['DB_HOST'],
        'PORT': os.environ['DB_PORT'],
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
    }

Let's use `db.py` for handling database connection. Add following code to `db.py`.

    # chalicelib/db.py
    from chalicelib import settings
    from peewee import PostgresqlDatabase


    db = PostgresqlDatabase(
        settings.DATABASE['NAME'], user=settings.DATABASE['USER'], password=settings.DATABASE['PASSWORD'], host=settings.DATABASE['HOST'], port=settings.DATABASE['PORT']
    )

We are relying on `peewee` library to connect to the database. Also `peewee` will need `psycopg2` since we are connecting to a PostgreSQL database.

    pip install peewee
    pip install psycopg2

Let's define our Peewee model in `models.py`

    # chalicelib/models.py
    from peewee import Model, CharField, DateField

    from chalicelib.db import db

    class Question(Model):
        question_text = CharField()
        pub_date = DateField()

        class Meta:
            database = db


    if db.table_exists('question') is False:
        db.create_tables([Question])

In `models.py` we have also written code to create the `question` table if it doesn't exist. We will take a different approach in production environment but for demonstration purpose, this will do.

Let's write the view to handle `POST` and `GET` for questions. Add following code in `app.py`

    @app.route('/polls/questions', methods=['GET', 'POST'])
    def questions():
        request = app.current_request
        if request.method == 'POST':
            question_text = request.json_body['question_text']
            pub_date = datetime.strptime(request.json_body['pub_date'], '%Y-%m-%d')
            question = Question(question_text=question_text, pub_date=pub_date)
            question.save()
            rep = {'question_text': question.question_text, 'id': question.id, 'pub_date': question.pub_date.strftime('%Y-%m-%d')}
            return rep
        elif request.method == 'GET':
            questions = Question.select()
            l = []
            for question in questions:
                l.append({'question_text': question.question_text, 'id': question.id, 'pub_date': question.pub_date.strftime('%Y-%m-%d')})
            return l

With a little knowledge of `peewee` the above code should be self explanatory.

To avoid hassle of writing `export DB_HOST=localhost` etc. while testing, I use a basic shell script. I have saved it in env.sh

    #!/bin/sh
    export DB_HOST=localhost
    export DB_PORT=5432
    export DB_NAME=peewee_polls
    export DB_USER=akshar
    export DB_PASSWORD=akshar

Change env.sh to populate it with your local postgres db credentials.

Execute this script.

    . ./env.sh

Run chalice local if it's not already running.

    chalice local

Navigate to http://localhost:8000/polls/questions. You will get an empty list in response.

Let's post a question. We will use `requests` to post a question. You could use curl or any other tool you prefer.

    In [1]: import requests

    In [2]: url = 'http://localhost:8000/polls/questions/'

    In [3]: data = {'question_text': 'What is the color of sky?', 'pub_date': '2019-09-22'}

    In [4]: resp = requests.post(url, json=data)

    In [5]: resp
    Out[5]: <Response [200]>

    In [7]: resp.json()
    Out[7]:
    {u'id': 2,
     u'pub_date': u'2019-09-22',
     u'question_text': u'What is the color of sky?'}

Navigate to http://localhost:8000/polls/questions again. You should be seeing this question's detail in response.

### Deploying

Our project relies on `peewee`, so add it to requirements.txt. requirements.txt will have following content.

    peewee

We cannot straightaway add psycopg2 to requirements because of reasons described <a href="https://github.com/jkehler/awslambda-psycopg2" target="_blank">here</a>. psycopg2 from this repository needs to be added to our project.

chalice has a requirement that vendor libraries be added to a directory called `vendor`. Take the following steps

    mkdir vendor
    git clone git@github.com:jkehler/awslambda-psycopg2.git /tmp/awslambda-psycopg2
    cp -r /tmp/awslambda-psycopg2/psycopg2-3.7 vendor/psycopg2

The environment variables need to be defined in config.json. You should have a .chalice/config.json. Edit it to add environment variables.

    {
      "version": "2.0",
      "app_name": "polls",
      "stages": {
        "dev": {
          "api_gateway_stage": "api",
          "environment_variables": {
            "DB_HOST": "yourdb.c7saowmwi1we.ap-south-1.rds.amazonaws.com",
            "DB_PORT": "5432",
            "DB_USER": "postgres",
            "DB_PASSWORD": "yourpassword",
            "DB_NAME": "yourdbname"
          }
        }
      }
    }

We are assuming that you have a publically available database. You lambda code would connect to this database.

Run chalice deploy

    chalice deploy

You will get an output which would look like:

    Creating deployment package.
    Updating policy for IAM role: polls-dev
    Updating lambda function: polls-dev
    Updating rest API
    Resources deployed:
      - Lambda ARN: arn:aws:lambda:ap-south-1:117635876922:function:polls-dev
      - Rest API URL: https://baxnta8me9.execute-api.ap-south-1.amazonaws.com/api/

Navigate to `https://baxnta8me9.execute-api.ap-south-1.amazonaws.com/api/polls/questions`. You will see an empty list because we haven't created any question yet.

Let's create a question now.

    In [2]: url = 'http://localhost:8000/polls/questions/'

    In [3]: data = {'question_text': 'What is the color of sky?', 'pub_date': '2019-09-22'}

    In [4]: resp = requests.post(url, json=data)

    In [5]: resp
    Out[5]: <Response [200]>

    In [7]: resp.json()
    Out[7]:
    {u'id': 2,
     u'pub_date': u'2019-09-22',
     u'question_text': u'What is the color of sky?'}

Navigate to `https://baxnta8me9.execute-api.ap-south-1.amazonaws.com/api/polls/questions` again. You will see the just created question in the response.

In a similar way, we could add view which handles editing and deleting a question.
