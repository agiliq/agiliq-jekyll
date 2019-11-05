---
layout: post
comments: true
title:  "Using Docker redis image with flask"
description: "Writing a docker-compose which uses Flask, Postgres and Redis"
keywords: "Flask, Python, Docker"
date: 2018-10-20
categories: [Flask, Docker]
author: Akshar
---

## Agenda

This is a follow up from our <a href="https://www.agiliq.com/blog/2018/10/docker-persist-postgres-data/" target="_blank">last post</a> which created a Flask polls app which communcated with a Postgres database.

We had two services namely `web` and `db`.

Let's add one more service called `redis` to the mix.

Our code would remain unchanged in this post. Check the <a href="https://www.agiliq.com/blog/2018/10/docker-persist-postgres-data/" target="_blank">last post</a> to get code familiarity.

## Docker services

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
            ports:
                - 5433:5432
            volumes:
                - flask_polls_data:/var/lib/postgresql/data
        cache:
            image: redis
            command: redis-server --appendonly yes
            volumes:
                - redis_data:/data

    volumes:
        flask_polls_data:
        redis_data:

Service `web` and `db` are largely unchanged from last post.

We added `redis` image provided by Docker. We added a volume so that data persist beyond the lifetime of container.

Modify app.py to make it look like:

    import json
    import redis
    from datetime import datetime
    from flask import Flask, request

    from .models import Question

    app = Flask(__name__)

    r = redis.Redis(host='cache', port=6379, db=0)


    @app.route('/polls/questions/', methods=['GET', 'POST'])
    def questions():
        r.incr('hits', amount=1)
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


    @app.route('/hits', methods=['GET'])
    def hits():
        hits = int(r.get('hits').decode('utf-8'))
        return json.dumps({'hits': hits})

We added an endpoint which tells how many times the api has been consumed.

Ensure that `redis` is added to requirements.txt

Build the services:

    docker-compose build

Start the services:

    docker-compose up

Navigate to http://localhost:8000/polls/questions/ multiple times. Check http://localhost:8000/hits and you should see it increasing with every hit to questions api.

Stop the services

    docker-compose down

This would destroy the containers. Start the services again

    docker-compose down

Navigating to http://localhost:8000/hits would still give the correct hits which confirms that data is being persisted.
