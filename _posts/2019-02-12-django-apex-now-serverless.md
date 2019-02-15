---
layout: post
comments: true
title: "Adventures in Deploying Django with Apex Up"
description: "Adventures in Deploying Django serverless with Apex Up"
keywords: "serverless, django, lambda, Apex-Up, aws, rds, Aurora"
date: 2019-02-12 15:35:27+05:30
categories: [Serverless Django, Apex, Lambda, AWS RDS, Aurora ]
author: anmol akhilesh
---

## Adventures in Deploying Django with Apex Up


We will try to deploy a basic django app onto  **_AWS Lambda_** using **_Apex Up_**.

**[AWS Lambda](https://aws.amazon.com/lambda/)** is a serverless computing platform by amazon, which is completely event driven and it automatically manages the computing resources. It scales automatically when needed, depending upon the requests the application gets.

**[Apex Up](https://up.docs.apex.sh/)** is a framework used for deploying serverless applications onto AWS-Lambda. Up currently supports Node.js, Golang, Python, Java, Crystal, and static sites out of the box. Up is platform-agnostic, supporting AWS Lambda and API Gateway.


### Install and Configure the Environment

First configure the AWS credentials [https://www.agiliq.com/blog/2019/01/complete-serverless-django/#configure-aws-credentials](https://www.agiliq.com/blog/2019/01/complete-serverless-django/#configure-aws-credentials)


#### Install Apex Up

Currently _Up_ has only [binary form releases](https://github.com/apex/up/releases) and can be installed by

```sh
$ curl -sf https://up.apex.sh/install | sh
```
this installs _Up_ in `/usr/local/bin` by default.


We can verify the installation by 

```sh
$ up version

# or 

$ up --help
```

#### Go to Django app

**First we have to note that _Apex-UP_ currently supports only Node.js lambda environment**, but we can use python 2.7 and 3.4 in it.

So we will use python34 and Django==2.0.13 for the app. We will create a basic django app for the deployment.

Next create a virtualenv with python34 and install Django==2.0.3

```sh
$ django-admin --version        # check the django version
2.0.3
```

Create a project 

```sh
$ django-admin startproject polls
```

Now go inside the _polls_ folder and  **rename the `manage.py` to `app.py`** for _apex-up_ to work.

```sh
$ python  app.py runserver
```

which will show us 

![](/assets/images/apex-up/django.png)


create a `requirements.txt` file and mention the Django version in it

```sh
$ echo "Django>2.0.13"> requirements.txt
```

and in `polls/settings.py` comment the databases part

```py
...
...

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

...
...
```

Now create a file in the same level as the `app.py` file named **`up.json`** and add the following lines


```json
{
  "name": "pollsapi",
  "profile": "default",
  "regions": [
    "us-east-2"
  ],
  "proxy": {
    "command": "python3 app.py runserver 0.0.0.0:$PORT"
  }
}
```

here **`name`** is the name of the project to be deployed

**`profile`** is the aws credentials profile name

**`region`** is the region of the lambda function

**`proxy`**  acts as a reverse proxy in front of your server, which provides features like CORS, redirection, script injection and middleware style features.

  We have to include the following configuration to our proxy object

  Add **`command`**  Command run through the shell to start your server (Default ./server)

  In the proxy command we have to give the command to start the django server ie _runserver_ .

  As presently _Up_ supports only Node.js lambda runtime environment, but we can use python 2.7 and 3.4 in it.
  So we can use python3 by mentioning the command as `python3 app.py runserver 0.0.0.0:$PORT` where the `$PORT` is the port where our app runs(which is generated dynamically).




Now let us test the app by deploying it,


```sh
$ up
# or
$ up deploy
# or
$ up -v         # verbose
```

```sh
$ up

     build: 4,752 files, 16 MB (9.463s)
     deploy: staging (version 3) (17.103s)
     stack: complete (26.324s)
     endpoint: https://Xpiix0c1.execute-api.us-east-2.amazonaws.com/staging/

     Please consider subscribing to Up Pro for additional features and to help keep the project alive!
     Visit https://github.com/apex/up#pro-features for details.
```

to get the url of the application


```sh

$ up url
# or
$ up url --open
```

Now when we open the url, we got

![](/assets/images/apex-up/error-internal.png)

The logs can be checked by these commands

```sh
$ up logs
# or
$ up logs -f            # for live logs
```

Let us check the logs,

```sh
 $ up logs
  Feb 12th 15:48:54am FATA staging 2 error creating handler: waiting for http://127.0.0.1:43435 to be in listening state: timed out after 15s: name=polls-final type=server
  Feb 12th 15:48:54am INFO 2019-02-14T05:18:54.122Z     dfb02a38-d65e-43b5-b7ad-d27e46bf384d    Error: read ECONNRESET
    at _errnoException (util.js:1022:11)
    at Pipe.onread (net.js:628:25)
  Feb 12th 15:48:54am INFO REPORT RequestId: dfb02a38-d65e-43b5-b7ad-d27e46bf384d       Duration: 15388.17 ms   Billed Duration: 15400 ms  Memory Size: 512 MB     Max Memory Used: 100 MB
  Feb 12th 15:48:54am INFO RequestId: dfb02a38-d65e-43b5-b7ad-d27e46bf384d Process exited before completing request
```

we are getting the above error.



Now let us try the same deployment with `Django==1.11`

first let us delete the previous deployment 

```sh
$ up stack delete   # delete the previous deployment
```

And change the Django version in the `requirements.txt` file  to 

```
# requirements.txt
Django==1.11
```

now create another virtualenv and install this version of Django, And let us run it

```sh
$ python  app.py runserver
```

we get django 1.11 page.

![](/assets/images/apex-up/django-1.11.png)



Now let us  deploy again

```sh
$ up

     build: 4,752 files, 16 MB (9.463s)
     deploy: staging (version 3) (17.103s)
     stack: complete (26.324s)
     endpoint: https://0giix0cq21.execute-api.us-east-2.amazonaws.com/staging/

     Please consider subscribing to Up Pro for additional features and to help keep the project alive!
     Visit https://github.com/apex/up#pro-features for details.

```
when we checked the url, we got

![](/assets/images/apex-up/up-server-error.png)

We got a different error!, this time the error message is from _Up_

let us check the logs again 


```sh
$ up logs
  Feb 13th 17:25:49am INFO staging 4 initializing
  Feb 13th 17:25:49am INFO staging 4 starting app: PORT=43007 command=python3 app.py runserver 0.0.0.0:$PORT
  Feb 13th 17:25:49am INFO staging 4 started app
  Feb 13th 17:25:49am INFO staging 4 waiting for app to listen on PORT
  Feb 13th 17:25:55am INFO staging 4 app listening: duration=6.137s
  Feb 13th 17:25:55am INFO staging 4 initialized: duration=6.138s
  Feb 13th 17:25:55am INFO staging 4 request: id=2dcd88a2-301d-11e9-99a9-6d964888c7f6 ip=124.123.105.73 method=GET path=/
  Feb 13th 17:25:55am ERRO staging 4 Invalid HTTP_HOST header: '0giix0cq21.execute-api.us-east-2.amazonaws.com'. You may need to add '0giix0cq21.execute-api.us-east-2.amazonaws.com' to ALLOWED_HOSTS.
  Feb 13th 17:25:56am ERRO staging 4 [14/Feb/2019 05:55:56] "GET / HTTP/1.1" 400 64942
  Feb 13th 17:25:56am WARN staging 4 response: duration=262ms id=2dcd88a2-301d-11e9-99a9-6d964888c7f6 ip=124.123.105.73 method=GET path=/ size=652 B status=400
  Feb 13th 17:25:56am INFO REPORT RequestId: 8c1735ae-4684-4d5b-a0b8-9c4f437c91c1       Duration: 6643.21 ms    Billed Duration: 6700 ms Memory Size: 512 MB      Max Memory Used: 99 MB

```

Now the error is stating that the app could not listen to the port!

  We tried to take the help of Apex-Up Slack group and they were really helpfull, _TJ Holowaychuk(founder of apex)_ reproduced the problem and the tried to look into the error.

  But at present the Apex-up is still not ready for Django-apps. But in future updates there will be more for the django python community.




_Up_ also sends our logs to AWS cloudwatch, so we can search for them there also.


##### Troubleshooting

We can check for the errors by

```sh

$ up logs error               # Shows error logs.

$ up logs 'error or fatal'    # Shows error and fatal logs.

$ up logs 'status >= 400'     # Shows 4xx and 5xx responses.

```

**We have to note that we have only python 2.7 and python 3.4 versions available**



