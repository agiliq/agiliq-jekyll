---
layout: post
comments: true
title:  "Writing a Python ORM for redis"
description: "An elegant way to store instances in Redis"
keywords: "Redis, Python, ORM, Redis relational data"
date: 2019-11-30
categories: [Redis, Python]
author: Akshar
---

## Agenda

I always wondered how to store relational data in redis. Once I figured it, I though it would be fun to write an ORM which can store this data in redis and retrieve from redis.

The inspiration for this post is Django ORM.

This post assumes that you have a basic understanding of Redis and the redis python library `redis-py`.

## Entities

Let's assume we are working on a polls application. The application has `Question` and `Choice`. Each question can have multiple choice. Users have the ability to vote on any of the choices for a particular question.

We want the following abilities in our application.

- Store list of questions and retrieve them
- Retreive a question based on the id
- Store choices
- Associate list of choices with a question
- Disassociate a choice with a question
- Retrieve all choices for a question
- Track vote count on choice

## Models

Our models are `Question` and `Choice`. Since these two and any additional model will share some functionality, so let's create a base class called `Model`. `Question` and `Choice` would extend from `Model`.

### Base model

`Model` would look like:

    # models.py

    class Model(object):

        @classmethod
        def latest_instance_id_key(cls):
            """
            `key` which tracks id of the latest instance of this model.
            Because Redis doesn't have auto incrementing field so we need a counter using which
            we can assign an `id` to a new instance.

            Example:
            Consider model `Question`, this method will return `question-latest-id`.
            """
            pass

        @classmethod
        def list_key(cls):
            """
            `key` for the list which will contain `ids` of all model instances.

            Example:
            Consider model `Question`, this method will return `questions`.
            """
            pass

        def add_to_list(self):
            """
            Example:
            Consider model `Question`, this method will add `question.id` to `questions`.
            """
            pass

        @classmethod
        def latest_instance_id(cls):
            """
            This will use `latest_instance_id_key` and will return the value stored at this key.

            Example:
            Consider model `Question`, this method will return value of key `question-latest-id`.
            """
            pass

        def increment_latest_instance_id(self):
            """
            Once an instance is added to redis, this method will increase the counter by 1.

            Example:
            Consider model `Question`, this method will increment value of key `question-latest-id`.
            """
            pass

        @classmethod
        def cache_key(cls):
            """
            This generates a `key` for a new instance being added.

            Example:
            Consider model `Question`, if 5 instances of questions are already in Redis and a new instance is being added, then this would return `question-6`.
            """
            pass

        def save(self):
            """
            This inserts a new instance to redis.
            """
            pass

Class `Question` would look like:

    class Question(Model):

        def __init__(self, id=None, question_text=None):
            pass

Let's add implementation for different methods of `Model`.

`latest_instance_id_key` would look like:

    @classmethod
    def latest_instance_id_key(cls):
        class_name = cls.__name__.lower() # Convert class `Question` to string `question`
        return '%s-latest-id' % (class_name,)

`list_key` would look like:

    @classmethod
    def list_key(cls):
        class_name = cls.__name__.lower()
        return '%ss' % (class_name,) # Convert class `Question` to `questions`

`add_to_list` would look like:

    def add_to_list(self):
        list_key = self.list_key()
        connection.lpush(list_key, self.id)

`add_to_list` uses a Redis list to store keys of all instances inserted into redis. We used `redis-py` `lpush` method which translates to redis' `LPUSH` operation.

We will add code to generate `self.id` soon.

Make sure to define the `connection` as a module variable in `models.py`.

    connection = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

`latest_instance_id` would look like:

    @classmethod
    def latest_instance_id(cls):
        return int(connection.get(cls.latest_instance_id_key()))

`increment_latest_instance_id` would look like:

    def increment_latest_instance_id(self):
        connection.incr(self.latest_instance_id_key())

`cache_key` would look like:

    @classmethod
    def cache_key(cls):
        identifier = cls.latest_instance_id() + 1
        class_name = cls.__name__.lower()
        return '%s-%d' % (class_name, int(identifier))

`save` would look like:

    # TODO: This should be in a transaction.
    def save(self):
        key = self.cache_key()
        self.id = self.latest_instance_id() + 1
        connection.hmset(key, self.repr())
        self.increment_latest_instance_id()
        self.add_to_list()
        return self

Notice that we are using `self.repr()` in `save()`. It would be the responsibility to subclasses to define a `repr()` which will return a dictionary of attributes we want to save. It will become clear soon.

You must have noticed how `save()` is calling `increment_latest_instance_id()` and `add_to_list()`.

Also `save()` uses `redis-py` `hmset` which translates to Redis' `HMSET` command. This way we store the desired attributes of an instance.

### Model subclass

Let's implement methods of class `Question`.

    class Question(Model):

        def __init__(self, id=None, question_text=None):
            if id is not None:
                id = int(id)
            self.id = id
            self.question_text = question_text

        def repr(self):
            return {
                'id': self.id,
                'question_text': self.question_text
            }

Since base class' `save()` is using `repr()`, so every subclass must implement `repr()`. `repr()` should return the dictionary representation which we want to persist in redis. We want `id` and `question_text` of a question to be persisted in redis, so `repr` returns a dictionay with these attributes.

When we try to `save()` the first instance, it will internally call `latest_instance_id_key()` which expects that a key called `question-latest-id` exist in redis.

Let's create a `migration` file and add this key to redis.

    # migrations.py
    from models import connection

    def first_migration():
        connection.set('question-latest-id', 0)

    first_migration()

Execute this file:

    python migrations.py

## Using the ORM

Time to try our setup from `ipython`.

    ╰─$ ipython
    Python 3.6.5 (default, Mar 30 2018, 06:41:53)
    Type 'copyright', 'credits' or 'license' for more information
    IPython 7.7.0 -- An enhanced Interactive Python. Type '?' for help.

    In [1]: from models import Question

    In [2]: q = Question(question_text='Nike or Adidas?')

    In [8]: q.save()
    Out[8]: <models.Question at 0x11134d1d0>

Ensure your redis server, `redis-server` is running.

Let's start a redis client, `redis-cli`, and verify that `question-1` was inserted in redis.

    127.0.0.1:6379> keys *
    1) "question-latest-id"
    2) "questions"
    3) "question-1"

This also verified that key `questions` was created. Let's verify that it stored the id of inserted question.

    127.0.0.1:6379> LRANGE questions 0 -1
    1) "1"

Let's verify that `id` and `question_text` for the question was inserted.

    127.0.0.1:6379> HGETALL question-1
    1) "id"
    2) "1"
    3) "question_text"
    4) "Nike or Adidas?"

Let's create one more question from ipython and save it into redis.

    In [9]: q = Question(question_text='Rowling or Tolkien?')

    In [10]: q.save()
    Out[10]: <models.Question at 0x111e37550>

Let's verify that desired keys and values have been saved into redis.

    127.0.0.1:6379> keys *
    1) "question-latest-id"
    2) "question-1"
    3) "question-2"
    4) "questions"

    127.0.0.1:6379> LRANGE questions 0 -1
    1) "2"
    2) "1"

    127.0.0.1:6379> HGETALL question-2
    1) "id"
    2) "2"
    3) "question_text"
    4) "Rowling or Tolkien?"

### Fetch question

Let's add a method on `Question` to fetch a question with a given id.

    class Question(Model):
        ...

    @classmethod
    def get_question(cls, id):
        key = cls.cache_key(id)
        d = connection.hgetall(key)
        return Question(**d)

Notice how we are passing `id` to `cache_key`. We need to change `cache_key` code accordingly. Modify it to look like:

    @classmethod
    def cache_key(cls, identifier=None):
        if identifier is None:
            identifier = cls.latest_instance_id() + 1
        class_name = cls.__name__.lower()
        return '%s-%d' % (class_name, int(identifier))

Let's fetch the added questions using their ids.

    In [2]: q = Question.get_question(1)

    In [3]: q.id
    Out[3]: 1

    In [4]: q.question_text
    Out[4]: 'Nike or Adidas?'

    In [5]: q = Question.get_question(2)

    In [6]: q.question_text
    Out[6]: 'Rowling or Tolkien?'

Let's ensure that save functionality is still working.

    In [7]: q = Question(question_text='Android or iOS?')

    In [8]: q.save()
    Out[8]: <models.Question at 0x10f13ba20>

Cool!

### Fetch all questions

Let's add a method to fetch all questions.

    # TODO: Use redis pipeline here
    @classmethod
    def get_questions(cls):
        list_key = cls.list_key()
        instances = []
        for question_id in connection.lrange(list_key, 0, -1):
            question = cls.get_question(question_id)
            instances.append(question)
        return instances

Let's use this method to fetch questions.

    In [1]: from models import Question

    In [2]: qs = Question.get_questions()

    In [3]: qs
    Out[3]:
    [<models.Question at 0x109009240>,
     <models.Question at 0x109009080>,
     <models.Question at 0x1090090f0>]

    In [5]: [question.question_text for question in qs]
    Out[5]: ['Android or iOS?', 'Rowling or Tolkien?', 'Nike or Adidas?']

`get_question` and `get_questions` have generic functionality and can be used with any model we add in future. So, let's them move to the base class. Let's rename `get_question` to `get`. And rename `get_questions` to `list`.


    class Model(object):
        ....

        @classmethod
        def get(cls, id):
            key = cls.cache_key(id)
            d = connection.hgetall(key)
            return cls(**d)

        # TODO: Use redis pipeline here
        @classmethod
        def list(cls):
            list_key = cls.list_key()
            instances = []
            for instance_id in connection.lrange(list_key, 0, -1):
                instance = cls.get(instance_id)
                instances.append(instance)
            return instances

Let's use `get()` and `list()` and verify that they behave as expected.

    In [1]: from models import Question

    In [2]: q = Question.get(1)

    In [3]: questions = Question.list()

    In [4]: [question.question_text for question in questions]
    Out[4]: ['Android or iOS?', 'Rowling or Tolkien?', 'Nike or Adidas?']

## Another model subclass

Let's add model `Choice` now.

    class Choice(Model):

        def __init__(self, id=None, choice_text=None, question_id=None, votes=0):
            if id is not None:
                id = int(id)
            self.id = id
            self.choice_text = choice_text
            self.question_id = question_id
            self.votes = votes

        def repr(self):
            return {
                'id': self.id,
                'choice_text': self.choice_text,
                'question_id': self.question_id,
                'votes': self.votes
            }

Before we could save a choice, we need to add key `choice-latest-id`. Remember our migrations.py?

Execute the following from ipython.

    from models import connection
    connection.set('choice-latest-id', 0)

Let's perform ORM operations on Choice now.

    In [1]: from models import Question, Choice

    In [2]: from models import connection

    In [3]: connection.set('choice-latest-id', 0)
    Out[3]: True

    In [4]: c = Choice(choice_text='Nike', question_id=1)

    In [5]: c.save()
    Out[5]: <models.Choice at 0x10aae50f0>

    In [6]: c = Choice(choice_text='Adidas', question_id=1)

    In [7]: c.save()
    Out[7]: <models.Choice at 0x10ab72ba8>

    In [8]: c = Choice.get(1)

    In [9]: c.choice_text
    Out[9]: 'Nike'

You should appreciate the usefulness of our base class. We get `save()`, `get()`, `list()` etc. for free in model `Choice`.

In the next post of this series, we will see how choices can be associated with a question and how to retrieve question's choices.
