---
layout: post
comments: true
title:  "Getting started with Python graphene"
description: "How to write GraphQL compliant apis with Python"
keywords: "GraphQL, Graphene, Python, API"
date: 2019-08-28
categories: [GraphQL, API, python, graphene]
author: Akshar
---

## Agenda

We will write an api endpoint which will respond to graphql queries.

- We will use `graphene` library to create our GraphQL service.
- We will expose this GraphQL endpoint using Flask.
- We will consume the api from a browser or angular/react client.

This post assumes that you have basic familiarity with <a href="https://graphql.org/" target="_blank">graphql</a>.

## Setup

Let's assume our application works with `Person` entities. A Person has a `first_name`, `last_name` and `age`. The api will allow querying on `Person`.

Our queries would look like:

    http://localhost:5000/?search={ person {firstName lastName age}} # Return all attributes of a single person.
    http://localhost:5000/?search={ person {firstName lastName}} # Return firstName and lastName of a single person.
    http://localhost:5000/?search={ people {firstName lastName}} # Return firstName and lastName of all people in our system.
    http://localhost:5000/?search={ person(key: 1) {firstName lastName age}} # Return all attributes of a person identified by key 1.

In a real world scenario, you would fetch `Person`s from a database table and would use an ORM to convert the database rows to Python classes. We want to focus on GraphQL in this post and avoid database operations. So let's create a `Person` `namedtuple` and create few instances of `Person`.

Let's write our code in a file called `hello_graphene.py`.

    import collections

    Person = collections.namedtuple("Person", ['first_name', 'last_name', 'age'])

    data = {
        1: Person("steve", "jobs", 56),
        2: Person("bill", "gates", 63),
        3: Person("ken", "thompson", 76),
        4: Person("guido", "rossum", 63)
    }

After this you should be able to do `person.first_name`, `person.last_name` and `person.age`. Let's verify it from an ipython shell.

    In [2]: from hello_graphene import data

    In [3]: data
    Out[3]:
    {1: Person(first_name='steve', last_name='jobs', age=56),
     2: Person(first_name='bill', last_name='gates', age=63),
     3: Person(first_name='ken', last_name='thompson', age=76),
     4: Person(first_name='guido', last_name='rossum', age=63)}

    In [4]: person = data[1]

    In [5]: person.first_name
    Out[5]: 'steve'

    In [6]: person.last_name
    Out[6]: 'jobs'

## Creating schema

Ensure that you have `graphene` installed.

    pip install graphene

GraphQL expects a root type. And we want to make `person` field available on root type. That's why we will have to write a `Person` type and the root type. This should be in `hello_graphene.py`.

    from graphene import ObjectType, String, Schema, Int, Field, List

    class PersonType(ObjectType):
        first_name = String()
        last_name = String()
        age = Int()

        def resolve_first_name(person, info):
            return person.first_name

        def resolve_last_name(person, info):
            return person.last_name

        def resolve_age(person, info):
            return person.age    

    class Query(ObjectType):
        person = Field(PersonType)

        def resolve_person(root, info):
            return data[1]

Convention suggests that we call the root type as `Query`. Any GraphQL `type` we create must extend from `ObjectType`. <a href="https://graphql.org/learn/" target="_blank">GraphQL dictates</a> that there must be resolver function for each field on each type. That's whey we have `resolve_person` for `person`, `resolve_first_name` for `first_name` and so on.

For now we have hardcode the resolver for person to always return details for person with key 1 which in our case is `steve jobs`. We are fixing it soon, hang on.

We need to tell to our GraphQL service that the root type is `Query`. The mechanism for doing that is to add a `Schema` instance.

    schema = Schema(query=Query)

Our full `hello_graphene.py` looks like:

    import collections
    from graphene import ObjectType, String, Schema, Int, Field, List

    Person = collections.namedtuple("Person", ['first_name', 'last_name', 'age'])

    data = {
        1: Person("steve", "jobs", 56),
        2: Person("bill", "gates", 63),
        3: Person("ken", "thompson", 76),
        4: Person("guido", "rossum", 63)
    }

    class PersonType(ObjectType):
        first_name = String()
        last_name = String()
        age = Int()

        def resolve_first_name(person, info):
            return person.first_name

        def resolve_last_name(person, info):
            return person.last_name

        def resolve_age(person, info):
            return person.age    

    class Query(ObjectType):
        person = Field(PersonType)

        def resolve_person(root, info):
            return data[1]

    schema = Schema(query=Query)

Our GraphQL service is ready now.

## Executing queries

Let's execute a GraphQL query from the shell.

    In [3]: from hello_graphene import schema

    In [7]: query = '{person {firstName lastName age} }'

    In [8]: result = schema.execute(query)

    In [9]: result.data
    Out[9]:
    OrderedDict([('person',
                  OrderedDict([('firstName', 'steve'),
                               ('lastName', 'jobs'),
                               ('age', 56)]))])

Notice how our result datastructure has the same structure as the query.

Let's execute one more query to ensure that the service only returns the requested fields.

    In [10]: query = '{person {firstName} }'

    In [11]: result = schema.execute(query)

    In [12]: result.data
    Out[12]: OrderedDict([('person', OrderedDict([('firstName', 'steve')]))])

We want to expose the service on any endpoint now so that browser or any client can consume the api. Let's expose a Flask endpoint.

Add the following code to a file flask_graphql.py

    import json
    from flask import Flask, request

    from hello_graphene import schema

    app = Flask(__name__)

    @app.route('/graphql')
    def graphql():
        query = request.args.get('query')
        result = schema.execute(query)
        d = json.dumps(result.data)
        return '{}'.format(d)

Start the flask server.

    $ export FLASK_APP=flask_graphql.py
    $ flask run

Let's make a request to flask app with a GraphQL query.

![](/assets/images/graphql/person-first-name.png)

Let's modify the GraphQL service to allow getting details of any person. Essentially we want to use <a href="https://graphql.org/learn/queries/#arguments" target="_blank">arguments</a> with our GraphQL api.

We need to allow arguments on `person` field. Modify `person` to look like:

    person = Field(PersonType, key=Int())

We will have to modify resolver for person to accomodate the argument too.

    def resolve_person(root, info, key):
        return data[key]

Restart the shell and get data for `steve` and `bill`.

    In [1]: from hello_graphene import schema

    In [2]: query = '{person(key: 1) {firstName} }'

    In [3]: schema.execute(query).data
    Out[3]: OrderedDict([('person', OrderedDict([('firstName', 'steve')]))])

    In [4]: query = '{person(key: 2) {firstName} }'

    In [5]: schema.execute(query).data
    Out[5]: OrderedDict([('person', OrderedDict([('firstName', 'bill')]))])

Let's hit the api from browser and get data for `bill`.

![](/assets/images/graphql/person-detail-details.png)

Ideally you would use the api endpoint from an angular or react client or from a mobile app.

If you are getting person from a database using SQLAlchemy, then the argument would probably be named `id` and the resolver would look something like:

    person = Field(PersonType, id=Int())

    def resolve_person(root, info, id):
        return Person.query.get(id)

We want our service to return details of all people in our system. Let's add a field called `people` on the root type.

    class Query(ObjectType):
        person = Field(PersonType, key=Int())
        people = List(PersonType)

        def resolve_person(root, info, key):
            return data[key]

        def resolve_people(root, info):
            return data.values()

Since `people` would be returning a list of people, so we set it's type as `graphene.List`. Each entry of the list would be a `PersonType`.

    In [1]: from hello_graphene import schema

    In [2]: query = '{people {firstName age} }'

    In [3]: schema.execute(query).data
    Out[3]:
    OrderedDict([('people',
                  [OrderedDict([('firstName', 'steve'), ('age', 56)]),
                   OrderedDict([('firstName', 'bill'), ('age', 63)]),
                   OrderedDict([('firstName', 'ken'), ('age', 76)]),
                   OrderedDict([('firstName', 'guido'), ('age', 63)])])])

## Supporting defaults

Currently you wouldn't be able to query on `person` without `key`. Let's try a query which would cause an exception.

    In [6]: query = '{person {firstName} }'

    In [7]: schema.execute(query).data
    TypeError: resolve_person() missing 1 required positional argument: 'key'
    Traceback (most recent call last):
      File "/Users/akshar/Envs/gryffindor/lib/python3.6/site-packages/graphql/execution/executor.py", line 450, in resolve_or_error
        return executor.execute(resolve_fn, source, info, **args)
      File "/Users/akshar/Envs/gryffindor/lib/python3.6/site-packages/graphql/execution/executors/sync.py", line 16, in execute
        return fn(*args, **kwargs)
    graphql.error.located_error.GraphQLLocatedError: resolve_person() missing 1 required positional argument: 'key'

If person's key isn't provided, then we want to respond with `steve`'s details. We can accomplish this by setting a `default_value` on `people` and this default_value should contain `steve`'s key.

    person = Field(PersonType, key=Int(default_value=1))

Restart the shell and try the query once more.

    In [4]: query = '{person {firstName} }'

    In [5]: schema.execute(query).data
    Out[5]: OrderedDict([('person', OrderedDict([('firstName', 'steve')]))])

If we pass a `key` though, then corresponding person's details would be fetched.

    In [6]: query = '{person(key: 2) {firstName} }'

    In [7]: schema.execute(query).data
    Out[7]: OrderedDict([('person', OrderedDict([('firstName', 'bill')]))])


Hope this post was helpful. Stay tuned for more GraphQL posts.
