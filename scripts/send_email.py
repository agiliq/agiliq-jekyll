import os
import requests
from flask import redirect


def start(request):
    """
    Google cloud platform internally uses flask to run cloud functions.
    So here `request` is Flask.request
    """

    # Consuming input variables required from form
    from_email = request.form['email']
    from_name = request.form['name']
    body = request.form['body']

    # Send an email using MAILGUN API
    # Decoupled send_email() in order to make it easily usable
    response = send_email(from_email, from_name, body +
                          "\n\nRegards,\n{}\n{}".format(from_name, from_email))
    if response == 200:
        return redirect('https://www.agiliq.com/thanks/', code=response)
    return redirect('https://www.agiliq.com/sorry/', code=500)


def send_email(from_email, from_name, body):
    """
    Send an email using MailGUN API Client
    """

    # Initializing important data from environment
    MAILGUN_DOMAIN_NAME = os.environ.get('MAILGUN_DOMAIN_NAME', None)
    MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY', None)
    TO_ADDRESS = str(os.environ.get('TO_ADDRESS', None))

    # Preparing the data to be sent as email
    url = 'https://api.mailgun.net/v3/{}/messages'.format(MAILGUN_DOMAIN_NAME)
    auth = ('api', MAILGUN_API_KEY)
    data = {
        'from': '{} <{}>'.format(from_name, from_email),
        'to': TO_ADDRESS,
        'subject': 'Contacted at Agiliq form',
        'text': body
    }

    # Sending the email
    response = requests.post(url, auth=auth, data=data)
    return response.status_code
