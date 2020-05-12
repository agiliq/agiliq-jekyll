---
layout: post
comments: true
title:  "How to seup Google Stackdriver Logging for Django App with Gunicorn"
description: "Setting up google stackdriver logging with django + gunicorn is simple. though google official documentation doesn't explained it."
date:   2018-09-06
categories: [google-cloud, stackdriver, logging]
author: Anjaneyulu Batta
---

Setting up google stackdriver logging with django + gunicorn is simple. Google's stackdriver logging official documentation only explained about python. It did not explain about how to setup the stackdriver logging for Django Application.

When deploying the django applications on production environment most of the developers uses Nginx as reverse proxy server and Gunicorn as WSGI server. So, we will configure the google stackdriver logging with gunicorn and django.
x
### Create a Service Account with scopes ("logging.write", "logging.admin")
Login to your google cloud console and create a Service account. While creating the service account select the below roles
* **Logging > Logs Writer.** This authorizes the Stackdriver Logging agent.
* **Monitoring > Monitoring Metric Writer.** This authorizes the Stackdriver Monitoring agent. Adding this role lets you use this service account to run both Stackdriver agents.

After creating the service account with above two roles a JSON file will be downloaded. It'll be in the below format.

```sh
[PROJECT-NAME]-[KEY-ID].json
``` 

Now, copy the service account file to the below location with below commands in linux.

```sh
sudo mkdir -p "/etc/google/auth/"
sudo cp "path/to/[PROJECT-NAME]-[KEY-ID].json" "/etc/google/auth/"
```
### Setting the environment variable

Provide authentication credentials to your application code by setting the environment variable GOOGLE_APPLICATION_CREDENTIALS. Open the `~/.bashrc` file and add the below line of code at the end of the file.

```
export GOOGLE_APPLICATION_CREDENTIALS="/etc/google/auth/[PROJECT-NAME]-[KEY-ID].json"
```

### Configure Django `settings.py` file
* Activate the virtual environment and install python package `google-cloud-logging` using pip.
* Let's configure google stackdriver logging in django application.

```python
import sys
from google.cloud import logging as google_cloud_logging

log_client = google_cloud_logging.Client()

LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'handlers': {
	    'console': {
	        'level': 'INFO',
	        'class': 'logging.StreamHandler',
	        'stream': sys.stdout,
	    },
	    'mail_admins': {
	        'level': 'ERROR',
	        'class': 'django.utils.log.AdminEmailHandler'
	    },
	    'stackdriver_logging': {
	        'class': 'google.cloud.logging.handlers.CloudLoggingHandler',
	        'client': log_client
	    },
	    'stackdriver_error_reporting': {
	        'level': 'ERROR',
	        'class': 'gcp_utils.stackdriver_logging.StackdriverErrorHandler',
	    }
	},
	'loggers': {
	    'django': {
	        'handlers': ['console', 'stackdriver_logging'],
	        'level': 'DEBUG',
	        'propagate': True,
	    },
	    'django.request': {
	        'handlers': [
	            'stackdriver_logging',
	            'mail_admins'
	        ],
	        'level': 'ERROR',
	    }
	},
}
```

* Now, run the development server using `python manage.py runserver` and browse some pages to check whether google stackdrver is logging the access log or not. 
* Go to google cloud console and click on stackdriver logging to see the logs.

### Configure the Gunicorn for stackdriver logging
* If above django congifuration didn't work with Gunicorn then follow the below configuration.
* Open file `gunicorn.conf.py` and configure it as below

```python
from google.cloud import logging as google_cloud_logging

log_client = google_cloud_logging.Client()
log_client.setup_logging()

bind = "127.0.0.1:8000"
workers = 3
loglevel = "debug"
proc_name = "django_app"
daemon = False
pythonpath = "/path/to/python/"
timeout = 90
accesslog = '/home/user/logs/debug.log'
logconfig_dict = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'stackdriver_logging': {
            'class': 'google.cloud.logging.handlers.CloudLoggingHandler',
            'client': log_client
        },
    },
    'loggers': {
        'gunicorn.access': {
            'handlers': ['stackdriver_logging'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': [
                'stackdriver_logging',
                'mail_admins'
            ],
            'level': 'ERROR',
        }
    },
}
```

Now, run the Gunicorn process as `$ gunicorn -c gunicorn.conf.py wsgi:application`

* Check the logs in the google cloud console under stackdriver logging.

We have successfully configured our django application with google cloud stackdriver logging.