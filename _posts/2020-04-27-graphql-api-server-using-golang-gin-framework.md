---
layout: post
comments: true
title:  "GraphQL api server using golang Gin framework"
description: "GraphQL api server using golang Gin framework"
keywords: "GraphQL"
date: 2020-04-27
categories: [Golang]
author: Anjaneyulu Batta
---

## Why GraphQL ?

* To avoid multiple versioning of your rest API.
* Ask for what you need: Client has a provision to ask only those fields which they needs. There would be no handling on server side specific to the platform.
* Avoid multiple API calls to get the related data. GraphQL allows us to get the related data in a single request.
* Speed up the application performance.

## GraphQL Architecture
![GraphQL Architecture](/assets/images/graphql/graphql-architecture.png)

### Schema

* Schema is the way to provide structure of the object or resource. Based on the schema we can query or mutate the data/resource on the GraphqL server.

### Queries

* Queries are used to retrieve the data from the GraphQL server.

### Mutations

* Mutations are used to update/modify the resource on the server.

### Resolvers

* Resolvers are used to create the data structure that matches with the provided resource schema.

## Creating GraphQL api server using golang Gin framework

Case: We are creating a question and choice model. A question can have multiple choices and a choice can have only one question.

Let's build a **GraphQL** api server for above scenario using golang packages <a href="https://gqlgen.com/getting-started/">gqlgen</a>, <a href="https://gorm.io/">gorm</a> and <a href="https://godoc.org/github.com/gin-gonic/gin">gin-gonic</a>

### Setup the project

```sh
$ mkdir gin-graphql-postgres
$ cd gin-graphql-postgres
$ go mod init github.com/anjaneyulubatta505/gin-graphql-postgres
$ go get github.com/99designs/gqlgen
$ go get -u github.com/gin-gonic/gin
$ go get -u github.com/jinzhu/gorm
```

### Building the server

Let's create the project skeliton with below command

```sh
$ go run github.com/99designs/gqlgen init
```

It will create a project structure like below

```
├── go.mod
├── go.sum
├── gqlgen.yml               - The gqlgen config file, knobs for controlling the generated code.
├── graph
│   ├── generated            - A package that only contains the generated runtime
│   │   └── generated.go
│   ├── model                - A package for all your graph models, generated or otherwise
│   │   └── models_gen.go
│   ├── resolver.go          - The root graph resolver type. This file wont get regenerated
│   ├── schema.graphqls      - Some schema. You can split the schema into as many graphql files as you like
│   └── schema.resolvers.go  - the resolver implementation for schema.graphql
└── server.go                - The entry point to your app. Customize it however you see fit
```

If you see the above generated files you can find the `schema.graphqls` and `schema.resolvers.go`.

`schema.graphqls` comes with the `ToDO` models by default. We have to update the schema as per our requirement.

### Write GraphQL Schema

> file: graph/schema.graphqls

```graphql
type Question{
  id: String!
  question_text: String!
  pub_date: String!
  choices: [Choice]
}

type Choice{
  id: String!
  question: Question!
  question_id: String!
  choice_text: String!
}

type Query {
  questions: [Question]!
  choices: [Choice]!
}

input QuestionInput {
  question_text: String!
  pub_date: String!
}

input ChoiceInput {
  question_id: String!
  choice_text: String!
}

type Mutation {
  createQuestion(input: QuestionInput!): Question!
  createChoice(input: ChoiceInput): Choice!
}
````

Now, let's run the below command to update the resolvers implementation (i.e By default it comes with TODO app).

```sh
$ rm graph/schema.resolvers.go && gqlgen generate
```

Now, open the file `graph/schema.resolvers.go` you can find the resolvers for the above schema.

```go
package graph

// This file will be automatically regenerated based on the schema, any resolver implementations
// will be copied through when generating and any unknown code will be moved to the end.

import (
        "context"
        "fmt"

        "github.com/anjaneyulubatta505/gin-graphql-postgres/graph/generated"
        "github.com/anjaneyulubatta505/gin-graphql-postgres/graph/model"
)

func (r *mutationResolver) CreateQuestion(ctx context.Context, input model.QuestionInput) (*model.Question, error) {
        panic(fmt.Errorf("not implemented"))
}

func (r *mutationResolver) CreateChoice(ctx context.Context, input *model.ChoiceInput) (*model.Choice, error) {
        panic(fmt.Errorf("not implemented"))
}

func (r *queryResolver) Questions(ctx context.Context) ([]*model.Question, error) {
        panic(fmt.Errorf("not implemented"))
}

func (r *queryResolver) Choices(ctx context.Context) ([]*model.Choice, error) {
        panic(fmt.Errorf("not implemented"))
}

// Mutation returns generated.MutationResolver implementation.
func (r *Resolver) Mutation() generated.MutationResolver { return &mutationResolver{r} }

// Query returns generated.QueryResolver implementation.
func (r *Resolver) Query() generated.QueryResolver { return &queryResolver{r} }

type mutationResolver struct{ *Resolver }
type queryResolver struct{ *Resolver }
```

In the above code you can find the functions to implement the **queries** `func (r *queryResolver) Questions`, `func (r *queryResolver) Choices` and mutations `func (r *mutationResolver) CreateQuestion`, `func (r *mutationResolver) CreateChoice`.

Now, we are ready to implement the queries and mutations in GraphQL api.

### Database orm setup with "gorm"

Let's add batteries to communicate with postgres database. Now, create file `db/main.go` and the below code.

> file: db/main.go

```go
package database

import (
	"fmt"

	"github.com/AnjaneyuluBatta505/gin-graphql-postgres/graph/model"
	"github.com/jinzhu/gorm"
	_ "github.com/jinzhu/gorm/dialects/postgres"
)

type dbConfig struct {
	host     string
	port     int
	user     string
	dbname   string
	password string
}

var config = dbConfig{"localhost", 5432, "postgres", "test", "root"}

func getDatabaseUrl() string {
	return fmt.Sprintf(
		"host=%s port=%d user=%s dbname=%s password=%s",
		config.host, config.port, config.user, config.dbname, config.password)
}

func GetDatabase() (*gorm.DB, error) {
	db, err := gorm.Open("postgres", getDatabaseUrl())
	return db, err
}

func RunMigrations(db *gorm.DB) {
	if !db.HasTable(&model.Question{}) {
		db.CreateTable(&model.Question{})
	}
	if !db.HasTable(&model.Choice{}) {
		db.CreateTable(&model.Choice{})
		db.Model(&model.Choice{}).AddForeignKey("question_id", "questions(id)", "CASCADE", "CASCADE")
	}
}
```
Now, we are ready to communicate with the database. It's time to implement the resolvers to return the data that matches with our GraphQL schema.

### Implement the GraphQL resolvers

Let's open the file `graph/schema.resolvers.go` and implement the resolvers like below

> file: graph/schema.resolvers.go

```go
package graph

// This file will be automatically regenerated based on the schema, any resolver implementations
// will be copied through when generating and any unknown code will be moved to the end.

import (
	"context"
	"fmt"
	"log"

	database "github.com/AnjaneyuluBatta505/gin-graphql-postgres/db"
	"github.com/AnjaneyuluBatta505/gin-graphql-postgres/graph/generated"
	"github.com/AnjaneyuluBatta505/gin-graphql-postgres/graph/model"
)

func (r *mutationResolver) CreateQuestion(ctx context.Context, input model.QuestionInput) (*model.Question, error) {
	db, err := database.GetDatabase()
	if err != nil {
		log.Println("Unable to connect to database", err)
		return nil, err
	}
	defer db.Close()
	fmt.Println("input", input.QuestionText, input.PubDate)
	question := model.Question{}
	question.QuestionText = input.QuestionText
	question.PubDate = input.PubDate
	db.Create(&question)
	return &question, nil
}

func (r *mutationResolver) CreateChoice(ctx context.Context, input *model.ChoiceInput) (*model.Choice, error) {
	db, err := database.GetDatabase()
	if err != nil {
		log.Println("Unable to connect to database", err)
		return nil, err
	}
	defer db.Close()
	choice := model.Choice{}
	question := model.Question{}
	choice.QuestionID = input.QuestionID
	choice.ChoiceText = input.ChoiceText
	db.First(&question, choice.QuestionID)
	choice.Question = &question
	db.Create(&choice)
	return &choice, nil
}

func (r *queryResolver) Questions(ctx context.Context) ([]*model.Question, error) {
	db, err := database.GetDatabase()
	if err != nil {
		log.Println("Unable to connect to database", err)
		return nil, err
	}
	defer db.Close()
	db.Find(&r.questions)
	for _, question := range r.questions {
		var choices []*model.Choice
		db.Where(&model.Choice{QuestionID: question.ID}).Find(&choices)
		question.Choices = choices
	}
	return r.questions, nil
}

func (r *queryResolver) Choices(ctx context.Context) ([]*model.Choice, error) {
	db, err := database.GetDatabase()
	if err != nil {
		log.Println("Unable to connect to database", err)
		return nil, err
	}
	defer db.Close()
	db.Find(&r.choices)
	return r.choices, nil
}

// Mutation returns generated.MutationResolver implementation.
func (r *Resolver) Mutation() generated.MutationResolver { return &mutationResolver{r} }

// Query returns generated.QueryResolver implementation.
func (r *Resolver) Query() generated.QueryResolver { return &queryResolver{r} }

type mutationResolver struct{ *Resolver }
type queryResolver struct{ *Resolver }
```

If you see the above code, we have implemented the `mutations` and `queries` that returns the data matches with our schema.
In the **`mutations`** implementation we are writing the data to the `postgres` database and in the **`queries`** implementation we are retriving the data from the database.

### Final touch with **Gin-Gonic**

We are good to go but we are missing the speed of **Gin-Gonic**. Let's do that. Open the file `server.go` and update it like below.

> file: server.go

```go
package main

import (
	"github.com/99designs/gqlgen/graphql/handler"
	"github.com/99designs/gqlgen/graphql/playground"
	"github.com/AnjaneyuluBatta505/gin-graphql-postgres/graph"
	"github.com/AnjaneyuluBatta505/gin-graphql-postgres/graph/generated"
	"github.com/gin-gonic/gin"
)

const defaultPort = ":8080"

// Defining the Graphql handler
func graphqlHandler() gin.HandlerFunc {
	// NewExecutableSchema and Config are in the generated.go file
	// Resolver is in the resolver.go file
	h := handler.NewDefaultServer(generated.NewExecutableSchema(generated.Config{Resolvers: &graph.Resolver{}}))

	return func(c *gin.Context) {
		h.ServeHTTP(c.Writer, c.Request)
	}
}

// Defining the Playground handler
func playgroundHandler() gin.HandlerFunc {
	h := playground.Handler("GraphQL", "/query")

	return func(c *gin.Context) {
		h.ServeHTTP(c.Writer, c.Request)
	}
}

func main() {
	r := gin.Default()
	r.POST("/query", graphqlHandler())
	r.GET("/", playgroundHandler())
	r.Run(defaultPort)
}
```

Yeah! We are ready to test *GraphQL* api server. Let's launch it with below command.

```sh
$ go run server.go
```

It will run the server on "`localhost:8080`". Let's open that url to see the **GraphQL** playground.

![GraphQL Playground](/assets/images/graphql/graphql-playground.png)


## GraphQL query to mutate the data

Let's write the GraphQL query to create the data in the database through playground

```graphql
mutation {
  createQuestion(input: {question_text: "What is your name ?", pub_date: "2020-04-27"}){
    id
    question_text
  }
}
```

After executing the above query we will get the JSON data like below (i.e not exactly same  :P)

```
{
  "data": {
    "createQuestion": {
      "id": "3",
      "question_text": "What is your name ?"
    }
  }
}
```

In the above we are creating the question with data `{question_text: "What is your name ?", pub_date: "2020-04-27"}` and after creating we are asking it to return `id`, `question_text`. If we want only id then we can remove `question_text` from the query.

Find the equivalent `cURL` request below

```
curl 'http://localhost:8080/query' \
  -H 'Connection: keep-alive' \
  -H 'accept: */*' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36' \
  -H 'content-type: application/json' \
  -H 'Origin: http://localhost:8080' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Referer: http://localhost:8080/' \
  -H 'Accept-Language: en-GB,en-US;q=0.9,en;q=0.8'\
  --data-binary '{"operationName":null,"variables":{},"query":"mutation {\n  createQuestion(input: {question_text: \"What is your name ?\", pub_date: \"2020-04-27\"}) {\n    id\n    question_text\n  }\n}\n"}' \
  --compressed
```

You can import the above cURL into postman to test it.

In the same way we can wtite the query to insert the choices. Let's an example GraphQL query.

```graphql
mutation {
  createChoice(input: {question_id: "3", choice_text: "Agiliq"}){
    id
    question{
      id
      question_text
    }
    choice_text
  }
}
```

Till now, we have seen how to mutate the data. Let's see how to retrieve the data from *GraphQL* api server.


## GraphQL query to query/retrieve the data

Let's write a graphql query to retrieve all the questions with their options.

```graphql
query{
  questions{
    id
    question_text
    choices{
      id
      choice_text
    }
  }
}
```

It will give us the JSON response like below.

```json
{
  "data": {
    "questions": [
      {
        "id": "3",
        "question_text": "What is your name ?",
        "choices": [
          {
            "id": "31",
            "choice_text": "Agiliq"
          }
        ]
      }
    ]
  }
}
```

You can check-out the source code at <a href="https://github.com/AnjaneyuluBatta505/gin-graphql-postgres/"> Github - gin-graphql-postgres</a>

That's it folks, we can do more with **GraphQL**. Let's do that in the up coming articles. Have a good day!!
