---
layout: post
comments: true
title: "Rails + GraphQL and React"
description:  "Polls API with GraphQL and ReactJS"
keywords: "Rails, Ruby, PostgreSQL, GraphQL, ReactJS, Polls API"
date:   2020-05-28
categories: [ruby, rails, postgresql, graphql, graphiql, reactjs, polls, pollsapi]
author: yvsssantosh
---

`Note: Kindly note that a user is expected to have basic understanding of Rails, GraphQL and ReactJS before trying this project.`

You can look into my previous tutorial to [get started](https://www.agiliq.com/blog/2020/04/running-rails-server-with-graphql-and-graphiql/) with Rails and GraphQL. This tutorial will be more focusing on building the frontend.

The entire code for this tutorial can be found [here](https://github.com/yvsssantosh/posts_graphql). I recommend starting from the `init` branch and go though the tutorial

## Setup the backend
Before we get started with generating models, lets enable cors middleware on our project, because we need it to test the code locally.

Just navigate to `Gemfile` and uncomment `rack-cors`

```sh
...

# Use Rack CORS for handling Cross-Origin Resource Sharing (CORS), making cross-origin AJAX possible
gem 'rack-cors'

# The line above would be commented, just uncomment it
...
```
Once this is done, run `bundle install` in the root directory of this project so that a new file `config/initializers/cors.rb` will be generated. Update it with the following code below. 

`Note: This is FOR DEVELOPMENT PURPOSES ONLY`

```rb
# cors.rb
Rails.application.config.middleware.insert_before 0, Rack::Cors do
  allow do
    origins '*'

    resource '*',
      headers: :any,
      methods: [:get, :post, :put, :patch, :delete, :options, :head]
  end
end
```

Lets generate the models now that we're done with setting up the middleware which will help our frontend server to connect to backend server without blocking any insecure requests.

```sh
# Generating models
# Generating User model with fields
#    `name`         : datatype -> string
#    `email`        : datatype -> string
rails generate model User name:string email:string

# Generating Poll model with fields 
#    `created_by`   : datatype -> User
#    `question`     : datatype -> string
rails generate model Poll user:belongs_to question:string

# Generating Choice model with fields 
#    `choice_text`  : datatype -> string
#    `poll`         : datatype -> Poll (FK)
rails generate model Choice poll:belongs_to choice_text:string

# Generating Vote model with fields 
#    `choice`       : datatype -> Choice (FK)
#    `poll`         : datatype -> Poll (FK)
#    `user`         : datatype -> User (FK)
rails generate model Vote choice:belongs_to poll:belongs_to user:belongs_to

# Make sure to add the `has_many` relationship where
# each foreign key has been mentioned.
# Refer `user.rb`, `poll.rb` and `choice.rb` in `app/models/` directory for the same

# Unique Key Migration
rails generate migration VotesUniqueConstraint
```
The last line above generates a migration where we're going to specify unique together relationship for fields `user_id` and `poll_id` in `Vote` model. This is to make sure that a user can vote for a choice present in a poll i.e., without this, a user can vote to POLL_1 with a choice CH_1 even though CH_1 is not a choice in that poll.

```rb
# TIMESTAMP_votes_unique_constraint.rb
class VotesUniqueConstraint < ActiveRecord::Migration[6.0]
  def change
    add_index :votes, [:user_id, :poll_id], unique: true
  end
end
```

Subsequently updating the votes model (`votes.rb`) as well
```rb
class Vote < ApplicationRecord
  belongs_to :choice
  belongs_to :poll
  belongs_to :user

  # Unique together constraint
  validates :user_id, uniqueness: {scope: :poll}
end
```

Lets run a seed on the db to generate some data. For this tutorial, we'll be using `Faker`

```rb
# seeds.rb
# We're using Faker to generate random emails, for testing
50.times do
    User.create(name: Faker::Name.name, email: Faker::Internet.email)
end

5.times do
    poll = Poll.create(question: Faker::Lorem.question, user: User.find(rand 1..50))
    4.times do
        poll.choices.create(choice_text: Faker::Lorem.sentence(word_count: 3))
    end
end

100.times do
    poll = Poll.find(rand 1..5)
    Vote.create(user: User.find(rand 1..50), poll: poll, choice: poll.choices.sample)
end
```
Run the command to migrate and seed the db
```sh
rails db:migrate db:seed
```

### Installing GraphQL
Now that our initial models and code is ready on rails, we need to setup GraphQL on rails
```sh
# Setting up GraphQL code in our project
# Note: Only works if GraphQL gem is pre-installed
# Make sure `gem 'graphql'` is in the `Gemfile`
# Then, run `bundle install`
rails generate graphql:install
```
Note that this command is very handy and auto-generates a lot of code for us. After running this command, we can see a new folder `graphql` has been created in the `app` directory. Also, `config/routes.rb` has also been automatically updated with the default graphql endpoint, which we'll be using to mutate and list the data in our database.

Configuring rails models as GraphQL Objects
```sh
# We need to run the command for each model. So,
rails generate graphql:object user
rails generate graphql:object poll
rails generate graphql:object choice
rails generate graphql:object vote
```

### Building Query to respond with right data

If it were just a Rails application, we'd have added code to the `controller.rb` file. But remember that since this is a GraphQL project, we will have a single endpoint serving all over data. So lets start modifying the `_type.rb` files which were generated earlier.

```rb
# user_type.rb
module Types
  class UserType < Types::BaseObject
    field :id, ID, null: false
    field :name, String, null: true
    field :email, String, null: true
    field :posts, [Types::PollType], null: true
    field :posts_count, Integer, null: true

    # Typical rails querying
    def posts_count
      object.posts.size
    end

  end
end
```

Similarly we'll be defining `polls_type.rb`, `choice_type.rb` and `vote_type.rb` based on the models generated earlier.

If there are any mutations, you'll be able to find them in `app/graphql/types/mutation_type.rb`. We have not defined any mutations for this tutorial. They have been explained in the previous tutorial [here](https://www.agiliq.com/blog/2020/04/running-rails-server-with-graphql-and-graphiql/).

The final backend code can be seen if we can checkout to that commit
```sh
git checkout 6dfa3cd819ae6e37eeff3fad858e744e31f1bf5b
```

## Setting up frontend

Create a basic react application with some standard boilerplate. I like `yarn`, so I've used it thorughout the next steps. You can use `npm` as well

```sh
# Creating a basic frontend project with some sample boilerplate
# Ref: https://create-react-app.dev/docs/getting-started/
npx create-react-app frontend

# I like to put most of the code in components folder, having
# react-based files ending with `.jsx` extension and format the
# code using standard. Again, its just a matter of preference.

yarn add -D standard babel-eslint

# Lets make a components directory in frontend/src and create a file 
# Polls.jsx. Also we'll be moving App.js -> src/components/App.jsx &
# its appropriate code restructuring is to be done

# I've made some basic css changes, to view them, run
git checkout ead45a7a75dc4c64c5bd7aeab439ab25b36a71a9
# and see `src/App.css` and use it accordingly.

```

### Installing dependencies

In frontend, we'll be using the following modules

  1. graphql
  1. apollo-boost
  1. react-polls (For showing polls and pseudo voting :P)
  1. react-apollo

Just install the packages using the command below

```sh
yarn add graphql apollo-boost react-polls react-apollo --save
```

Lets go to our main file where code execution starts (index.js). Few changes to make,
  1. We need a link to connect our graphql server to frontend
  1. Do fetch calls/install axios to do complicated fetch calls
  1. Add some `sagas` maybe? To complicate things
  1. Add a state store, like `Redux` to complicate things even more :P ;)

Anyways, sorry for scaring you here, but we don't need all that. We'll just use apollo-client for this and it'll handle everything for us. That's a breather right!!

All we need to do is to link to our graphql server (running at http://localhost:5000) to ApolloProvider(as a prop) and make the `App` component a child for it. That's all! More on this can be found [here](https://www.apollographql.com/docs/react/get-started/)

```jsx
// Default imports
// Same as before
import { ApolloProvider } from 'react-apollo'
import { ApolloClient } from 'apollo-client'
import { createHttpLink } from 'apollo-link-http'
import { InMemoryCache } from 'apollo-cache-inmemory'

// Custom Imports
// Same as before

const link = createHttpLink({ uri: 'http://localhost:5000/graphql' })
const client = new ApolloClient({ link: link, cache: new InMemoryCache() })

// Making `App` as a child for ApolloProvider
// and passing client props to it
ReactDOM.render(
  <ApolloProvider client={client}>
    <App />
  </ApolloProvider>,
  document.getElementById('root')
)

// Some other code
```

Now that we have Apollo connected, lets write the polls get query and populate using `react-polls` which we installed earlier.
```js
{
  polls {
    id
    question
    choices {
      choiceText
      voteCount
    }
  }
}
```
We'll be using this query to fetch the results from our backend server. Now lets update `src/components/App.jsx` accordingly

```jsx
// Default imports
import React from 'react'
import { useQuery } from 'react-apollo'
import { gql } from 'apollo-boost'

// Custom imports
import '../App.css'
import Polls from './Polls'
import reactLogo from '../assets/react-logo.svg'

// GraphQL query to get polls, choices and the number of votes
const GET_POLLS = gql`
{
  polls {
    id
    question
    choices {
      choiceText
      voteCount
    }
  }
}
`

const App = () => {
  // Note: Anything starting with useXXX is always a hook

  // Calling the useQuery hook of react-apollo, and observe that
  // we have configured the graphql settings once in index,js.
  // We don't need to configure it again in the entire app
  const { loading, error, data } = useQuery(GET_POLLS)

  if (loading) return 'Loading...'
  if (error) return `Error :  ${error.message}`

  return (
    <div className='app'>
      <header className='header'>
        <img src={reactLogo} className='logo' alt='React Logo' />
        <h1 className='name'>Polls API</h1>
      </header>
      <main className='main'>
        {/*
          Here we are mapping the data as react-polls has different
          variable naming when compared to our Polls API

          To avoid this, we can use graphql aliases, which changes
          our query to the following below.

          This is done intentionally to explain this concept of aliasing
          as many developers think that they have to change the backend
          to fit accordingly, which actually we can just use alias.

          {
            polls {
              question: question
              answers: choices {
                option: choiceText
                vootes: voteCount
              }
            }
          }

         */}
        <Polls polls={data.polls.map(
          poll => {
            return {
              id: poll.id,
              question: poll.question,
              answers: poll.choices.map(choice => {
                return {
                  option: choice.choiceText,
                  votes: choice.voteCount,
                  id: choice.id
                }
              })
            }
          }
        )}
        />
      </main>
    </div>
  )
}

export default App
```

Now moving on to `src/components/Polls.jsx`. The code has been explained in detail in the snippet below

```jsx
import React, { useState, useEffect } from 'react'
import Poll from 'react-polls'

const Polls = ({ polls }) => {
  const [pollData, updatePollData] = useState([])

  // Some custom style for the polling box
  // More on this can be found here => https://github.com/viniciusmeneses/react-polls#customize
  const pollStyles = {
    questionSeparator: true,
    questionSeparatorWidth: 'question',
    questionBold: true,
    questionColor: '#303030',
    align: 'center',
    theme: 'cyan'
  }

  // Replacing ComponentDidMount, ComponentDidUpdate and ComponentDidUnmount
  // And runs only when the polls are updated (the array in the end with `polls`)

  // More on useEffect hook => https://reactjs.org/docs/hooks-effect.html
  useEffect(() => {
    updatePollData(polls)
  }, [polls])

  // Simple onClick method used to handle Voting
  // This is a pseudo method, i.e. it just updates the
  // state of pollData and not the actual data on server
  const handleVote = (voteAnswer, pollNumber) => {
    const newPollData = [...pollData]

    // Increment no. of votes on the choice clicked
    newPollData.map(poll => (
      poll.id === pollNumber ? poll.answers.map(answer => (answer.option === voteAnswer ? answer.votes++ : null)) : null
    ))

    // Here we can implement a mutation to update the vote
    // made by particular user

    // state hook to update pollData
    updatePollData(newPollData)
  }

  // Renders Poll which is from the package `react-polls`
  return (
    pollData.map(
      poll => (
        <div key={poll.id}>
          <div>
            <Poll
              question={poll.question}
              answers={poll.answers}
              onVote={voteAnswer => handleVote(voteAnswer, poll.id)}
              customStyles={pollStyles} noStorage
            />
          </div>
        </div>
      )
    )
  )
}

export default Polls
```

This concludes the tutorial where we have created a basic GraphQL Application (full-stack), with

Backend -> Rails, Frontend -> React + Apollo

Please feel free to create any issues on [my github](https://github.com/yvsssantosh/polls_graphql_react/issues)