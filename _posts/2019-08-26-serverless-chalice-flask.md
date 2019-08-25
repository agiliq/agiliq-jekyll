---
layout: post
comments: true
title:  "Building Serverless Python applications with AWS-Chalice"
description: "Deploying serverless python applications using aws-chalice"
keywords: "serverless, chalice, python, aws"
date:   2019-07-25
categories: [serverless, chalice, python]
author: Anmol
---

<!-- Building and Deploying Serverless Python applications with Chalice -->

## Building Serverless Python with aws-chalice

**[Chalice](https://github.com/aws/chalice)** is a Python Serverless Microframework for writing serverless apps in python. It allows you to quickly create and deploy applications that use AWS Lambda. 

Chalice is a decorator-based API to write python applications that run on Amazon API Gateway and AWS Lambda. It is highly inspired by Flask.


<!-- Chalice is its own framework it doesn't have any compatibility with flask, they both are simple and used for similar things so there may be some superficial similarities. So, you should not be able to simply make a few changes to a Flask app and turn it into a Chalice app. -->


Chalice includes:
* A command line tool for creating, deploying, and managing your app
* A decorator based API for integrating with Amazon API Gateway, Amazon S3, Amazon SNS, Amazon SQS, and other AWS services.
* Automatic IAM policy generation




#### Prerequisites 
**Configure AWS Credentials** 
First, before using AWS, we have to make sure we have a valid AWS account and have the aws environment variables(access-keys).

then, create a folder at the root level

```sh
 $ mkdir .aws
```

Now, create a file called credentials and store the `aws_access_key_id` and `aws_secret_access_key`. To find these access credentials

- Go to IAM dashboard in AWS console
- Click on Users
- Click on your User name
- Then, go to Security credentials tab
- Go down to Access keys
- Note down the `access_key_id`. `secret_access_key` is only visible when you are creating new user or when creating a new access key, so you need to note down both the access_key_id and secret_access_key at the time of user creation only or create a new access key so that we can get both the keys.

```sh
  ###~/.aws/credentials
  [default]
  aws_access_key_id= XXXXXXXXXXXXXXXXXXXX
  aws_secret_access_key=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

#### Create a Chalice App

Let us install `chalice` in our virtual-env

```sh
$ pip install chalice
```

let us create a new-project in chalice

```sh
$ chalice new-project agiliqblog
$ cd agiliqblog

```

Now when we go to the folder we will see the files `app.py`, `requirement.txt` 
along with `.gitignore` .

when we open `app.py` we can see 

```py
from chalice import Chalice

app = Chalice(app_name='agiliqblog')

@app.route('/')
def index():
    return {'hello': 'world'}
```

The new-project command created a sample app that defines a single view, /, that when called will return the JSON body `{"hello": "world"}`.

Now let us run the app locally to see it 

```sh
$ chalice local
Restarting local dev server.
Serving on http://127.0.0.1:8000
```

![](/assets/images/chalice/localhost-1.png)

The `@app.route()` decorator is the Chalice view function (similar to a django view function), which takes a URL as its first parameter.

Now let us add another view function


```py
...
...

@app.route('/profile/{name}', methods=['GET'])
def index(name):
    return {'Hello': name}

```

This new view function will only accept `GET` requests, and return json - `{"Hello":"agiliq"}` when hitting this route. 
If we want to return an HTTP Response with a status code and response headers

```py
from chalice import Chalice, Response

app = Chalice(app_name='agiliqblog')

@app.route('/profile/{name}', methods=['GET'])
def index(president):
    return Response(template, status_code=200, headers={"Content-Type": "text/html", "Access-Control-Allow-Origin": "*"})

```
To render html templates we have to install `Jinja2` and add it to `requirements.txt` file.


#### Database
For the database layer of our application, let us create an AWS DynamoDB as it is a NoSQL DB 
by following the instructions in [https://www.agiliq.com/blog/2019/01/complete-serverless-django/#setup-serverless-mysql-database](https://www.agiliq.com/blog/2019/01/complete-serverless-django/#setup-serverless-mysql-database)

After creating the db, now let us link it to our chalice project

<!-- As we are using MySQL for the database, we have to install python MySQL client `PyMySQL`

```sh
$ pip install PyMySQL
```
let us create a folder named agiliqblog and in this folder create a file named `connectdb.py` 

```sh

agiliqblog/
  - chalicelib/
    - __init__.py
    - connectdb.py
  - app.py

``` -->

```py
# app.py
import MySQLdb

rds_host = 'blog-cluster.cluster-kpa234yjp247g.us-east-2.rds.amazonaws.com'
db_name = 'blogdb'
user_name = 'blog_admin'
password = 'blogadmin'
port = 3306
...
...

conn = None

def get_conn():
    global conn
    if conn is None:
        conn = Db.conn()
    return conn

```

