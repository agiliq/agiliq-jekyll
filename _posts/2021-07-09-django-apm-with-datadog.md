---
layout: post
comments: true
title:  "Django application monitoring with datadog"
description: "Django application monitoring allows us to analyze the pitfalls of the application so that we can fix it and improve the application."
keywords: "django, performance, datadog"
date: 2021-07-09
categories: [Django, Performance, Monitoring]
author: Anjaneyulu Batta
---

## Application performance monitoring

Application performance monitoring (i.e APM) is a way to analyze the each transaction of an application and find the pitfalls of it.

APM allow us to find

- Whether the app is behaving as expected or not?
- What parts of the application is using more resources like Memory, CPU, etc.?
- What queries are taking more time in database?
- How frequently an url is being requested?
- Application availability

With the above information, we can fix the issues and improve the application before it affects the business.

## Datadog and it's features

Datadog is a monitoring service for cloud-scale applications, providing monitoring of servers, databases, tools, and services, through a SaaS-based data analytics platform.

Features

- Allows developer to analyze each request in depth, so that developer can see what part of the application is taking more time.
- It gives the insights on how frequently an API or web page is failing or accessing
- It allows to set the *alerts* so that developers can be notified if anything goes wrong.
- It allows clear insights on database queries so that dev's can analyze the issue and fix/improve the DB/Query performance.
- It allows to create the dashboards for different application events and create alerts based on the events. so that people will know before it impact the business.
- It supports different languages and their frameworks also.


## Integrating Datadog with django app

Get the API key and install the datadog agent with below command

```bash
DD_API_KEY=<API_KEY> DD_AGENT_MAJOR_VERSION=7 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```


To use the datadog with django we need to install the python package `ddtrace` with below command.

```python
pip install ddtrace

```


Now, run the `ddtrace-run` wrapper with your `gunicorn` command, keeping all the arguments intact:

```bash
ddtrace-run gunicorn [...] myapp.wsgi:application [...]
```

Update the `settings.py` file by adding `'ddtrace.contrib.django'` to installed apps.

```python
INSTALLED_APPS = [
  # your Django apps...
  'ddtrace.contrib.django',
]
```

Restart the application and send few requests to the app, we should be able to see the metrics of django application.


## Integrating datadog with PostgreSQL

SSH into PostgreSQL server and install the datadog agent with below command. You will need to get the API Key

```bash
DD_API_KEY=<API_KEY> DD_AGENT_MAJOR_VERSION=7 bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"
```

Now, create a postgres user `datadog` with read-only access.

```sql
create user datadog with password '<PASSWORD>';
grant pg_monitor to datadog;
grant SELECT ON pg_stat_database to datadog;
```

Verify connection using below command

```sql
psql -h localhost -U datadog postgres -c \
"select * from pg_stat_database LIMIT(1);" \
&& echo -e "\e[0;32mPostgres connection - OK\e[0m" \
|| echo -e "\e[0;31mCannot connect to Postgres\e[0m"
```

To configure the Agent to collect PostgreSQL metrics, create a `conf.yaml` file from the provided template.

```bash
sudo cp /etc/datadog-agent/conf.d/postgres.d/conf.yaml.example /etc/datadog-agent/conf.d/postgres.d/conf.yaml
```

Add the following to config file:

```yaml
init_config:

instances:
  - host: localhost
    port: 5432
    username: datadog
    password: <PASSWORD>
```

> Note: replace the localhost with actual host name or IP

Restart the agent with below command

```
sudo service datadog-agent restart
```

Wait for 5 min, We should be able to see PostgreSQL performance metrics in datadog dashboard.

That's it folks. You can check their official docs at https://docs.datadoghq.com/
