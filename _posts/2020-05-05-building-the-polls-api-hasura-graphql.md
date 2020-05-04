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
- Api to see result for a particular question.


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