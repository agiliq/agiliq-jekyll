---
layout: post
comments: true
title:  "Docker setup for a Flask polls app"
description: "Create a dockerfile for a flask REST application"
keywords: "Flask, Python, API, Peewee"
date: 2018-10-18
categories: [Flask, Docker]
author: Akshar
---

## Agenda

We will write a Flask REST application and create a Docker setup for it. This Flask application communicates with a PostgreSQL database on the host.

## Application

Create a directory for the project.

    mkdir flask_polls
    cd flask_polls

We have a PostgreSQL database running on the host machine. The database name is `peewee_polls`. We will use `peewee` as ORM to connect to this database. You could use SQLAlchemy or any other replacement for peewee.

We will keep database configuration in environment variable.

Let's create a settings.py which will read the environment variables.

    # settings.py

    import os

    DATABASE = {
        'HOST': os.environ['DB_HOST'],
        'PORT': os.environ['DB_PORT'],
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
    }

Let's create db.py which will connect to the database.

    # db.py
    from peewee import PostgresqlDatabase

    from . import settings


    db = PostgresqlDatabase(
        settings.DATABASE['NAME'], user=settings.DATABASE['USER'], password=settings.DATABASE['PASSWORD'], host=settings.DATABASE['HOST'], port=settings.DATABASE['PORT']
    )

Let's add the ORM for `question` table.

    # models.py
    from peewee import Model, CharField, DateField

    from .db import db


    class Question(Model):
        question_text = CharField()
        pub_date = DateField()

        class Meta:
            database = db


    if db.table_exists('question') is False:
        db.create_tables([Question])

Let's write the Flask application now:

    import json
    from datetime import datetime
    from flask import Flask, request

    from .models import Question

    app = Flask(__name__)


    @app.route('/polls/questions/', methods=['GET', 'POST'])
    def questions():
        if request.method == 'POST':
            question_text = request.form['question_text']
            pub_date = datetime.strptime(request.form['pub_date'], '%Y-%m-%d')
            question = Question(question_text=question_text, pub_date=pub_date)
            question.save()
            rep = {'question_text': question.question_text, 'id': question.id, 'pub_date': question.pub_date.strftime('%Y-%m-%d')}
            return rep
        elif request.method == 'GET':
            questions = Question.select()
            l = []
            for question in questions:
                l.append({'question_text': question.question_text, 'id': question.id, 'pub_date': question.pub_date.strftime('%Y-%m-%d')})
            return json.dumps(l)

Since we are treating this directory as a package, so ensure there is ` `__init__.py` file too.

    touch __init__.py

Let's create a `requirements.txt` using which Docker will install the needed libraries:

    Flask
    peewee
    psycopg2

Let's add the Dockerfile for this setup:

    FROM python:3

    WORKDIR /srv

    ADD ./requirements.txt /srv/requirements.txt

    RUN pip install -r requirements.txt

    ADD . /srv

    RUN export FLASK_APP=app.py
    CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]

We can build the image using:

    docker build -t flask-polls .

We want to run a container using this image now. Since our database configuration is in environment variable, so we will have to create an env.list which holds env variables.

    ╰─$ cat env.list
    DB_HOST=host.docker.internal
    DB_PORT=5432
    DB_NAME=peewee_polls
    DB_USER=akshar
    DB_PASSWORD=akshar

In our setup, we want Docker to connect to a db running on host, that's why we have setup `DB_HOST` as `host.docker.internal`.

Let' run the container:

    docker run -p 8000:8000 --env-file env.list flask-polls

We have mappend port 8000 of docker container with port 8000 on localhost. We also passed the env.list file which running the container, this ensures that `DB_HOST`, `DB_PORT` etc. are available on the container.

Navigate to `http://localhost:8000/polls/questions/` and you should be able to see the questions. As you haven't created any question yet, so you would probably see it empty.

Let's create a question using `requests`.

    In [1]: import requests

    In [2]: data = {'question_text': 'Ba ba blue sheep?', 'pub_date': '2019-10-20'}

    In [12]: resp = requests.post('http://localhost:8000/polls/questions/', data=data)

    In [13]: resp.status_code
    Out[13]: 200

    In [14]: resp.content
    Out[14]: b'{"id":4,"pub_date":"2019-10-20","question_text":"Ba ba blue sheep?"}\n'

Making a GET request to http://localhost:8000/polls/questions/ should show this question.
