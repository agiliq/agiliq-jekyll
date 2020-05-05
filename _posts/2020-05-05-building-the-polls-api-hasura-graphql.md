---
layout: post
comments: true
title:  "building the polls API with Hasura GraphQL Engine"
description: "Let's quickly build the polls api with Hasura GraphQL Engine"
keywords: "Hasura GraphQL Engine"
date: 2020-05-04
categories: [GraphQL, PostgreSQL]
author: Anjaneyulu Batta
---

we already know the concept of polls app(i.e It consists of questions and choices and people choses the choice for a specific question). Let's build an api for polls app using **Hasura GraphQL Engine**

We have already seen how to setup the *Hasura GraphQL Engine*. If you do not know how to set it up the read our article "[Instant GraphQL API for Postgres with Hasura](/blog/2020/05/instant-graphql-api-for-postgres-with-hasura/)" and get back here.

## What api's we will be building ?

- An api to create a poll question.
- Api to list questions.
- Api to get question detail.
- Api to edit a question.
- Api to delete a question.
- Api to create choice for a particular question.
- Api to see question detail along with available choices.
- Api to vote for a particular choice of a question.


## Database Schema

Let's create the database schema for polls api. We have two tables 1. `Question` 2. `Choice`

### Table: Question

Question table has the fields `id`, `question_text`, `pub_date`.

![Hasura GraphQL Polls API](/assets/images/graphql/hasura-polls-api-question-tbl.png)

### Table: Choice

Choice table has the fields `id`, `question_id`, `choice_text`, `votes`.

![Hasura GraphQL Polls API](/assets/images/graphql/hasura-polls-api-choice-tbl.png)


## Create a poll question

### GraphQL mutation to insert the data

```
mutation CreateQuestion{
  insert_question_one(object: {
    question_text: "What is python?", pub_date: "2020-05-05"
  }){
    id
    question_text
    pub_date
  }
}
```

> cURL:

```
curl 'http://localhost:4400/v1/graphql' -H 'x-hasura-admin-secret: hasurasecret' --data '{"query":"mutation CreateQuestion{\n  insert_question_one(object: {\n    question_text: \"What is python?\", pub_date: \"2020-05-05\"\n  }){\n    id\n    question_text\n    pub_date\n  }\n}","variables":null,"operationName":"CreateQuestion"}'
```

Output: 

```json
{
  "data": {
    "insert_question_one": {
      "id": 1,
      "question_text": "What is python?",
      "pub_date": "2020-05-05"
    }
  }
}
```

## List all poll questions

### Graphql query to retrieve all questions

```graphql
query AllQuestions {
  question{
    id
    question_text
    pub_date
  }
}
```

> cURL:

```
curl 'http://localhost:4400/v1/graphql' -H 'Referer: http://localhost:4400/console/api-explorer' -H 'content-type: application/json' -H 'x-hasura-admin-secret: hasurasecret' -H 'Origin: http://localhost:4400' --data '{"query":"query AllQuestions {\n  question{\n    id\n    question_text\n    pub_date\n  }\n}","variables":null,"operationName":"AllQuestions"}'
```

Output: 

```json
{
  "data": {
    "question": [
      {
        "id": 1,
        "question_text": "What is python?",
        "pub_date": "2020-05-05"
      }
    ]
  }
}
```

## Retrieve a specific poll question

### Graphql query to retrieve a specific question with `pk`

```graphql
query RetrieveQuestionWithPK {
  question_by_pk(id: 1) {
    id
    question_text
    pub_date
  }
}
```

> cURL:

```bash
curl 'http://localhost:4400/v1/graphql' -H 'content-type: application/json' -H 'x-hasura-admin-secret: hasurasecret' -H 'Origin: http://localhost:4400' -H 'Connection: keep-alive' --data '{"query":"query RetrieveQuestionWithPK {\n  question_by_pk(id: 1) {\n    id\n    question_text\n    pub_date\n  }\n}\n","variables":null,"operationName":"RetrieveQuestionWithPK"}'
```

Output: 

```json
{
  "data": {
    "question_by_pk": {
      "id": 1,
      "question_text": "What is python?",
      "pub_date": "2020-05-05"
    }
  }
}
```

## Edit a poll question

### Graphql `mutation` to update a specific question

```graphql
mutation UpdateQuestionWithPK {
  update_question_by_pk(pk_columns: {id: 1}, _set: {question_text: "Who invented python?"}) {
    id
    pub_date
    question_text
  }
}
```

> cURL:

```bash
curl 'http://localhost:4400/v1/graphql' -H 'content-type: application/json' -H 'x-hasura-admin-secret: hasurasecret' -H 'Origin: http://localhost:4400' -H 'Connection: keep-alive' --data '{"query":"mutation UpdateQuestionWithPK {\n  update_question_by_pk(pk_columns: {id: 1}, _set: {question_text: \"Who invented python?\"}) {\n    id\n    pub_date\n    question_text\n  }\n}\n","variables":null,"operationName":"UpdateQuestionWithPK"}'
```

Output:

```json
{
  "data": {
    "update_question_by_pk": {
      "id": 1,
      "pub_date": "2020-05-05",
      "question_text": "Who invented python?"
    }
  }
}
```

If you see that we have updated the question text from `What is python?` to `Who invented python?`.

## Delete a poll question

### GraphQL mutation to query to delete the question with pk

```graphql
mutation DeleteQuestionByPK{
  delete_question_by_pk(id: 1) {
    id
  }
}
```

cURL:

```bash
curl 'http://localhost:4400/v1/graphql' -H 'content-type: application/json' -H 'x-hasura-admin-secret: hasurasecret' --data '{"query":"mutation DeleteQuestionByPK{\n  delete_question_by_pk(id: 1) {\n    id\n  }\n}\n","variables":null,"operationName":"DeleteQuestionByPK"}'
```

Output:

```json
{
  "data": {
    "delete_question_by_pk": {
      "id": 1
    }
  }
}
```

Let's insert the question back again with the query

```graphql
mutation CreateQuestion{
  insert_question_one(object: {
    question_text: "What is python?", pub_date: "2020-05-05"
  }){
    id
    question_text
    pub_date
  }
}
```

Output:

```json
{
  "data": {
    "insert_question_one": {
      "id": 2,
      "question_text": "What is python?",
      "pub_date": "2020-05-05"
    }
  }
}
```

## Create choices for the question

### Graphql mutation query to create question choices in bulk

```graphql
mutation CreateChoices {
  insert_choice(objects: [
    {choice_text: "snake", question_id: 2, votes: 0},
    {choice_text: "programming language", question_id: 2, votes: 0},
    {choice_text: "both", question_id: 2, votes: 0},
    {choice_text: "I don't know", question_id: 2, votes: 0}]) {
    returning {
      choice_text
      id
      question_id
      votes
    }
  }
}
```

cURL:

```bash
curl 'http://localhost:4400/v1/graphql' -H 'content-type: application/json' -H 'x-hasura-admin-secret: hasurasecret' --data $'{"query":"mutation CreateChoices {\\n  insert_choice(objects: [\\n    {choice_text: \\"snake\\", question_id: 2, votes: 0},\\n    {choice_text: \\"programming language\\", question_id: 2, votes: 0},\\n    {choice_text: \\"both\\", question_id: 2, votes: 0},\\n    {choice_text: \\"I don\'t know\\", question_id: 2, votes: 0}]) {\\n    returning {\\n      choice_text\\n      id\\n      question_id\\n      votes\\n    }\\n  }\\n}\\n","variables":null,"operationName":"CreateChoices"}'
```

Output:

```json
{
  "data": {
    "insert_choice": {
      "returning": [
        {
          "choice_text": "snake",
          "id": 2,
          "question_id": 2,
          "votes": 0
        },
        {
          "choice_text": "programming language",
          "id": 3,
          "question_id": 2,
          "votes": 0
        },
        {
          "choice_text": "both",
          "id": 4,
          "question_id": 2,
          "votes": 0
        },
        {
          "choice_text": "I don't know",
          "id": 5,
          "question_id": 2,
          "votes": 0
        }
      ]
    }
  }
}
```

## Question detail with choices

Before getting the question detail with choices we need to configure the Relationships like below as show in the image.

![Hasura GraphQL relationships](/assets/images/graphql/hasura-graphql-relations.png)

Now, we are ready to query the GraphQL. Let's do that

### GraphQL query

```graphql
query GetQuestion {
  question{
    id
    question_text
    pub_date
    choices{
      id
      choice_text
      votes
    }
  }
}
```

Output:

```json
{
  "data": {
    "question": [
      {
        "id": 2,
        "question_text": "What is python?",
        "pub_date": "2020-05-05",
        "choices": [
          {
            "id": 2,
            "choice_text": "snake",
            "votes": 0
          },
          {
            "id": 3,
            "choice_text": "programming language",
            "votes": 0
          },
          {
            "id": 4,
            "choice_text": "both",
            "votes": 0
          },
          {
            "id": 5,
            "choice_text": "I don't know",
            "votes": 0
          }
        ]
      }
    ]
  }
}
```

Whoa! Yes, we got the question details with all of the choices.


## Vote a for a choice

### Graphql mutation query to update the choice

```graphql
mutation {
  update_choice(_inc: {votes: 1}, where: {id: {_eq: 2}}) {
    returning {
      choice_text
      id
      question_id
      votes
    }
  }
}
```

I'm sure you are now comfortable with cURL so, I'm just skipping the cURL. Try it out on your own this time.

Output:

```json
{
  "data": {
    "update_choice": {
      "returning": [
        {
          "choice_text": "snake",
          "id": 2,
          "question_id": 2,
          "votes": 1
        }
      ]
    }
  }
}
```

We have upvoted the choice with id `2`. If you observe we have created the choice with votes `0`. After the above query it incremented it by `1`. Because we have sent `_inc: {votes: 1}` in the query.


Let's do the question detail query again to see if the votes updated or not.

```graphql
query GetQuestion {
  question{
    id
    question_text
    pub_date
    choices{
      id
      choice_text
      votes
    }
  }
}
```

Output:

```json
{
  "data": {
    "question": [
      {
        "id": 2,
        "question_text": "What is python?",
        "pub_date": "2020-05-05",
        "choices": [
          {
            "id": 3,
            "choice_text": "programming language",
            "votes": 0
          },
          {
            "id": 4,
            "choice_text": "both",
            "votes": 0
          },
          {
            "id": 5,
            "choice_text": "I don't know",
            "votes": 0
          },
          {
            "id": 2,
            "choice_text": "snake",
            "votes": 1
          }
        ]
      }
    ]
  }
}
```

If we see the above output the choice with id `2` has votes `1` and other choices votes are `0`. So, we have completed the apis for the polls app using Hasura GraphQL Engine.

It's that simple to create the GraphQL api's using Hasura. That's it folks. Let's do more in the coming articles!
