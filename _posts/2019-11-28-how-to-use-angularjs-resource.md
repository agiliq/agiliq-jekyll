---
layout: post
comments: true
title:  "How to use AngularJS $resource"
description: "Using $resource to make api calls"
keywords: "Angularjs"
date: 2019-11-28
categories: [AngularJS, api, $resource]
author: Akshar
---

## Agenda

We will see how to use AngularJS `$resource` to make api calls.

`$resource` documentation describes it as:

    A factory which creates a resource object that lets you interact with RESTful server-side data sources.

`$resource` is most powerful when it's configured with a classic RESTful backend.

## Backend setup

Let's assume we are working with a polls application. This application allows people to create poll questions along with associated choices. Poeple can vote on any of the choices.

There are two database entities in our application, namely `Question` and `Choice`. A `Question` can have multiple `Choice`.

A Question has fields `id` and `question_text`. A Choice has fields `id`, `choice_text` and `question_id`.

Let's assume that the backend exposes the following api endpoints.

- GET /api/polls/questions/ - This returns a list of questions
- GET /api/polls/questions/:id/ - This returns details of a question
- POST /api/polls/questions/ - This creates a question
- PATCH /api/polls/questions/:id/ - This edits a question
- DELETE /api/polls/questions/:id/ - This deletes a question
- GET /api/polls/questions/:id/choices/ - This returns choices for a question

### GET /api/polls/questions/

This returns the following structure:

    [{'id': 71, 'question_text': 'Is Vue.js better than AngularJS'},
     {'id': 72, 'question_text': 'Is Go faster than Python'}]

It's a list of objects.

### GET /api/polls/questions/:id/

This returns the following structure:

    {'id': 71, 'question_text': 'Is Vue.js better than AngularJS'}

Notice it's an object and not a list.

### POST /api/polls/questions/

This needs the following payload to create a question:

    {'question_text': 'Is TravisCI cheaper than CircleCI'}

We need to post an object with key `question_text`.

This should have given you sufficient idea on the backend setup and api structure.

## AngularJS setup

Let's create a module called `myApp` and mark `ngResource` as a dependency module.

    var myApp = angular.module("myApp", ['ngResource']);

    myApp.config(['$resourceProvider', function($resourceProvider){
        $resourceProvider.defaults.stripTrailingSlashes = false;
    }]);

Ensure that `angular-resource` script is included in your index.html.

## Creating $resource

You would usually create a resource in the controller or a service.

Generally we need to pass a `url` and a `paramDefaults` when defining a resource. Let's create a resource called `Questions`.

    var Questions = $resource('http://localhost:8000/api/polls/questions/:id/',
        {'id': '@id'}
    )

The `url` we used is `http://localhost:8000/api/polls/questions/:id/` and `paramDefaults` we used is `{'id': '@id'}`.

We provided a parametrized `url` to `$resource` and `:id` is a parameter in our case.

`Questions` is a Resource instance with the following methods:

- query()
- get()
- save()
- delete()

GET /api/polls/questions/ call can be made in the following way:

    Questions.query().$promise.then(function (response) {
        console.log(response)
    }, function(error) {
        console.log(error);
    });

Notice how we skipped the value for parameter `id` in `Questions.query()`. Actual network call would have been `/api/polls/questions/`.

`response` is a list of `Resource`. Each Resource will represent a question with fields `id` and `question_text`.

GET /api/polls/questions/:id call can be made in the following way:

    Questions.get({'id': 71}).$promise.then(function (response) {
        console.log(response);
    }, function (error) {
    });

Notice how we provided a value for parameter `id` in `Questions.get()`. Actual network call would have been `/api/polls/questions/71/`.

`response` is a `Resource` having keys `id` and `question_text`.

POST /api/polls/questions/ can be made in the following way:

    Questions.save({'question_text': 'Tea or Coffee or Milk'}).$promise.then(function (response) {
        console.log(response);
    });

`response` is a `Resource` having keys `id` and `question_text`. This assumes that the backend returns the created Question.

DELETE /api/polls/questions/:id/ can be made in the following way:

    Questions.delete({'id': '74'}).$promise.then(function (response) {console.log(response);})

AngularJS `$resource` by default doesn't provide support for `PATCH`. We will have to add a custom action for it.

We will need to add a third argument in `$resource` call and it should be `{'patch': {method: 'patch'}}`. `$resource` call would look like:

    var Questions = $resource('http://localhost:8000/api/polls/questions/:id/',
        {'id': '@id'},
        {'patch': {method: 'patch'}}
    )

PATCH /api/polls/questions/:id/ can be made in the following way:

    Questions.patch({'id': '71', 'question_text': 'Amazon or Flipkart'}).$promise.then(function(response) {
        console.log(response);
    }, function (response) {
        console.log(response);
    });

This would make a network call to PATCH `/api/polls/questions/71/` and send payload as `{'question_text': 'Amazon or Flipkart'}`.

Hope this post helped in reducing some confusion around `$resource`.
