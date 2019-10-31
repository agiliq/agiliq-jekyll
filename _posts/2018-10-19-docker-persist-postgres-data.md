---
layout: post
comments: true
title:  "Using Docker postgres image with flask app"
description: "Persist docker postgres data"
keywords: "Flask, Python, API, Peewee"
date: 2018-10-18
categories: [Flask, Docker]
author: Akshar
---

## Agenda

This is a follow up from our <a href="https://www.agiliq.com/blog/2018/10/flask-docker/" target="_blank">last post</a> which created a Flask polls app.

In last post, the flask app connected to a postgres server running on the host. In this post we will use a postgres docker image. This has an advantage that you don't need to have postgres setup on the host machine. At the same time we want the postgres data to persist even after the containers are destroyed.

Our code would remain unchanged in this post. Check the <a href="https://www.agiliq.com/blog/2018/10/flask-docker/" target="_blank">last post</a> to get code familiarity.

## Docker services

In last post we had a single service called `flask`. In this post we will add an additional service called `db`. Also we will rename `flask` to `web`.

Your directory structure would look like:

    ├── Dockerfile
    ├── README.md
    ├── __init__.py
    ├── app.py
    ├── db.py
    ├── docker-compose.yml
    ├── env.list
    ├── models.py
    ├── requirements.txt
    ├── settings.py
    └── tox.ini

docker-compose.yml should look like:

    version: '3'
    services:
        web:
            build: .
            command: flask run --host=0.0.0.0 --port=8000
            ports:
                - 8000:8000
            environment:
                - FLASK_APP=app.py
            env_file:
                - env.list
            depends_on:
                - db
        db:
            image: postgres
            environment:
                - POSTGRES_USER=polls
                - POSTGRES_PASSWORD=hearmeroar
                - POSTGRES_DB=polls_db
            volumes:
                - flask_polls_data:/var/lib/postgresql/data

    volumes:
        flask_polls_data:

Service `web` is largely unchanged from last post.

We used official `postgres` image provided by Docker. We set some environment variables to set database name and credentials.

Flask app would be connecting to this database now so we need to edit env.list file to make it look like:

    DB_HOST=db
    DB_PORT=5432
    DB_NAME=polls_db
    DB_USER=polls
    DB_PASSWORD=hearmeroar

We used `volumes` to persist our data.
