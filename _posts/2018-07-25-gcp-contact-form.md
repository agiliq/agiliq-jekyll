---
layout: post
comments: true
title:  "Contact Form for static sites using GCP"
description: "How to get emails when a user provides their details in a contact form in our website - Best Practices"
keywords: "Google Cloud Functions, Python, Mailgun API, Google Cloud Datastore"
date:   2018-07-25
categories: [python, google cloud functions, mailgun, google cloud datastore]
author: Santosh
---

If you run a static site, you probably want a contact form on it so people can contact you. 

Having a separate server just for handling contact forms sure is a headache. Why not just write a cloud function which will just do our small task without the pain of installing and maintaining servers? 

Then, let's get started.

In this tutorial we'll be setting up a simple contact form using Google Cloud Functions. 
Mailgun will be used to send mail. We will also write the data to Cloud Datastore so we can review the records if mail sending fails.

### Setup Backend

* First, navigate to <https://console.cloud.google.com/functions> to create a new cloud function. Create a new function using the following settings:

```
Name                    : CLOUD_FUNCTION_NAME
Memory Allocated        : As per requirement
Source Code             : Inline editor
Runtime                 : Python 3.7
main.py                 : Code in ./scripts/send_email.py
requirements.txt        : Code in ./scripts/requirements.txt
Function to execute     : Name of the function to be executed first
Region                  : As per requirement
Timeout                 : 60

Environment Variables   : TO_ADDRESS, MAILGUN_API_KEY, MAILGUN_DOMAIN_NAME, 
                          REDIRECT_SUCCESS_URL, REDIRECT_FAILURE_URL, PROJECT_ID
                          CONFIRMATION_EMAIL_BODY, CONFIRMATION_EMAIL_FROM_NAME
```

`Note:` If the environment variables are not configured properly, the code will not run and give errors.

Let's have a look at our sample python script used to send email i.e. `./scripts/send_email.py`

```py
import os
import datetime
import requests
from flask import redirect
from google.cloud import datastore


def start(request):
    """
    Google cloud platform internally uses flask to run cloud functions.
    So here `request` is Flask.request
    """
    # Initializing Redirect URLs
    REDIRECT_SUCCESS_URL = os.environ.get('REDIRECT_SUCCESS_URL', None)
    REDIRECT_FAILURE_URL = os.environ.get('REDIRECT_FAILURE_URL', None)
    TO_ADDRESS = str(os.environ.get('TO_ADDRESS', None))

    # Consuming input variables required from form
    FROM_EMAIL = request.form['email']
    FROM_NAME = request.form['name']
    body = request.form['body']

    # Before sending the email, keep track of users who are mailing us
    client_key = save_user_data(FROM_NAME, FROM_EMAIL, body)

    # Send an email using MAILGUN API
    # Decoupled send_email() in order to make it easily usable
    response = send_email(FROM_EMAIL, FROM_NAME, 'Contacted at Agiliq form', body +
                          "\n\nRegards,\n{}\n{}".format(FROM_NAME, FROM_EMAIL), TO_ADDRESS)

    # Send confirmation email to the user, as we've got the email
    send_confirmation_email(FROM_EMAIL, TO_ADDRESS)

    # Redirect to success page if 200 else redirect to error page
    if response == 200:
        return redirect(REDIRECT_SUCCESS_URL, code=302)
    return redirect(REDIRECT_FAILURE_URL, code=302)


def save_user_data(FROM_NAME, FROM_EMAIL, body):
    """
    Save the data in our DB as user has not got the email
    """
    # Initializing the data where PROJECT_ID = GCP Project ID
    PROJECT_ID = os.environ.get('PROJECT_ID', None)
    client = datastore.Client(PROJECT_ID)

    key = client.key('Task')

    # Create a new entity
    task = datastore.Entity(key, exclude_from_indexes=['message'])
    task.update({
        'created': datetime.datetime.now(),
        'name': FROM_NAME,
        'email': FROM_EMAIL,
        'message': body
    })

    # Upload the data
    client.put(task)

    return client.key


def send_confirmation_email(FROM_EMAIL, TO_ADDRESS):
    """
    Send a confirmation email to the user saying we're received their email.
    """
    CONFIRMATION_EMAIL_TO_ADDRESS = FROM_EMAIL
    CONFIRMATION_EMAIL_FROM_ADDRESS = TO_ADDRESS
    CONFIRMATION_SUBJECT = 'Thank you for contacting us!'
    CONFIRMATION_EMAIL_BODY = os.environ.get('CONFIRMATION_EMAIL_BODY', None)
    CONFIRMATION_EMAIL_FROM_NAME = os.environ.get(
        'CONFIRMATION_EMAIL_FROM_NAME', None)

    send_email(CONFIRMATION_EMAIL_FROM_ADDRESS, CONFIRMATION_EMAIL_FROM_NAME,
               CONFIRMATION_SUBJECT, CONFIRMATION_EMAIL_BODY, CONFIRMATION_EMAIL_TO_ADDRESS)


def send_email(FROM_EMAIL, FROM_NAME, SUBJECT, BODY, TO_ADDRESS):
    """
    Send an email using MailGUN API Client
    """

    # Initializing important data from environment
    MAILGUN_DOMAIN_NAME = os.environ.get('MAILGUN_DOMAIN_NAME', None)
    MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY', None)

    # Preparing the data to be sent as email
    url = 'https://api.mailgun.net/v3/{}/messages'.format(MAILGUN_DOMAIN_NAME)
    auth = ('api', MAILGUN_API_KEY)
    data = {
        'from': '{} <{}>'.format(FROM_NAME, FROM_EMAIL),
        'to': TO_ADDRESS,
        'subject': SUBJECT,
        'text': BODY
    }

    # Sending the email
    response = requests.post(url, auth=auth, data=data)
    return response.status_code
```

* The script is fairly self explanatory where we're writing a google cloud function, and calling `send_email()` method which takes in params FROM_EMAIL, FROM_NAME, SUBJECT, BODY, TO_ADDRESS. This will send the email to the Organization where a user has submitted the contact form.

* Also, if a user contacts an organization, a good practice would be sending a confirmation email to the user. This is handled by the method `send_confirmation_email()` where we'll be sending the variables FROM_EMAIL and TO_ADDRESS and load the remaining constants from environment.

* Another good practice would be to keep track of all the users contacting the organization. The simplest way would be to store the data in `Cloud Datastore` as it supports SQL Querying and very simple to perform CRUD operations over. Here data is to be saved which is seen in the method `save_user_data()`

### Setup FrontEnd

`Note:` As we're using [Jekyll](https://jekyllrb.com/) to run our website it's better to have a basic understanding before seeing this documentation.

At the frontend side, i.e. our Jekyll Application, create a file with type `markdown` as Jekyll internally converts the code written into HTML

```html
---
layout: default
title: "TITLE_OF_PAGE"
permalink: "PERMANENT_URL_IN_PROJECT"
redirect_from: "REDIRECT_FROM_URL"
---
<form action="YOUR_GOOGLE_CLOUD_FUNCTION_URL" method="POST">
    Name:       <input type="text" id="name" name="name" placeholder="Name">
    Email:      <input type="email" id="email" name="email" placeholder="email">
    Message:    <textarea rows="6" cols="30" id="body" name="body" placeholder="Message"></textarea>
            
            <input type="submit" name="Submit"/>
</form>
```
