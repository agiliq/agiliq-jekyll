---
layout: post
comments: true
title:  "Using python graphene with Django"
description: "How to write GraphQL compliant apis with Django"
keywords: "GraphQL, Graphene, Python, API, Django"
date: 2019-09-14
categories: [GraphQL, API, python, django]
author: Akshar
---

## Agenda

We will write a GraphQL compliant api for a Django project.

We will use two models through this post and expose the data for those models using GraphQL api.

- We will use `graphene` library to create our GraphQL service.
- The GraphQL service will interact with Django models.
- We will expose this GraphQL service using Django.

This post builds on our <a href="https://www.agiliq.com/blog/2019/08/getting-started-with-python-graphene/" target="_blank">last post</a>which gives an introduction to Python graphene.

## Setup

This post assumes that you have the project setup as described at https://docs.djangoproject.com/en/2.2/intro/tutorial01/.

You must have a `polls` app in your project and the models `Question` and `Choice`.

    # polls/models.py
    class Question(models.Model):
        question_text = models.CharField(max_length=200)
        pub_date = models.DateTimeField('date published')

        def __str__(self):
            return self.question_text

        def was_published_recently(self):
            now = timezone.now()
            return now - datetime.timedelta(days=1) <= self.pub_date <= now


    class Choice(models.Model):
        question = models.ForeignKey(Question, on_delete=models.CASCADE)
        choice_text = models.CharField(max_length=200)
        votes = models.IntegerField(default=0)

        def __str__(self):
            return self.choice_text

## Schema

Create a file called `mysite/graphql.py`. This assumes that your project name is `mysite` created using `django-admin startproject mysite`.

    # mysite/graphql.py

    from graphene import Schema, ObjectType, Field, String, List, Int

    from polls.models import Question


    class QuestionType(ObjectType):

        question_text = String()
        pub_date = String()

        def resolve_question_text(question, info):
            return question.question_text

        def resolve_pub_date(question, info):
            return question.pub_date.strftime('%Y-%m-%d')


    class Query(ObjectType):
        questions = List(QuestionType)
        question = Field(QuestionType, id=Int())

        def resolve_questions(root, info):
            return Question.objects.all()

        def resolve_question(root, info, id):
            return Question.objects.get(id=id)

    schema = Schema(query=Query)

We have named our root object type as `Query`. It has two fields called `questions` and `question`.

We will use `questions` to get list of all questions. We will use `question` to get detail of a particular question.

## Queries

Let's make some queries from `manage.py shell`.

Get `question_text` and `id` of all questions.

    In [5]: schema.execute('{ questions{ID questionText} }').data
    Out[5]:
    OrderedDict([('questions',
                  [OrderedDict([('ID', 56),
                                ('questionText', 'Is the color of sky blue')]),
                   OrderedDict([('ID', 57),
                                ('questionText',
                                 'Is Samsung more reliable than iPhone?')]),
                   OrderedDict([('ID', 61),
                                ('questionText',
                                 'Is the color of sky yellow')])])])

Get `question_text` and `pub_date` of all questions.

    In [6]: schema.execute('{ questions{questionText pubDate} }').data
    Out[6]:
    OrderedDict([('questions',
                  [OrderedDict([('questionText', 'Is the color of sky blue'),
                                ('pubDate', '2019-05-15')]),
                   OrderedDict([('questionText',
                                 'Is Samsung more reliable than iPhone?'),
                                ('pubDate', '2019-07-03')]),
                   OrderedDict([('questionText', 'Is the color of sky yellow'),
                                ('pubDate', '2019-08-13')])])])

Get `question_text` and `pub_date` of question with id 56.

    In [7]: schema.execute('{ question(id:56){questionText pubDate} }').data
    Out[7]:
    OrderedDict([('question',
                  OrderedDict([('questionText', 'Is the color of sky blue'),
                               ('pubDate', '2019-05-15')]))])

## Api

Let's setup the api endpoint `/graphql`. Create a view and a urlpattern.

    # mysite/views.py
    from django.views import View
    from django.http import JsonResponse

    from .graphql import schema


    class GraphQLView(View):

        def get(self, request, *args, **kwargs):
            search = request.GET.get('search')
            result = schema.execute(search)
            return JsonResponse(result.data, safe=False)

Urlpattern would look like:

    # mysite/urls.py

    from . import views

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('graphql/', views.GraphQLView.as_view()),
    ]

Start the server

    python manage.py runserver

With this setup, the following queries, which we tried on shell, should work.

    http://localhost:8000/graphql/?search={ questions{ID questionText} }
    http://localhost:8000/graphql/?search={ questions{questionText pubDate} }
    http://localhost:8000/graphql/?search={ question(id:56){questionText pubDate} }

## Aliasing

We can use Graphql aliases and get question detail for two different questions in a single api call.

    http://localhost:8000/graphql/?search={second: question(id:57){questionText pubDate} first: question(id:56){questionText pubDate}}

This would have required two api calls in a classic REST architecture.

## Nested fields

Let's modify our GraphQL service so clients can get question related choices too along with question. This would need created a `ChoiceType`.

    class ChoiceType(ObjectType):
        choice_text = String()
        votes = Int()

        def resolve_choice_text(choice, info):
            return choice.choice_text

        def resolve_votes(choice, info):
            return choice.votes

Let's add `ChoiceType` to `QuestionType`.

    class QuestionType(ObjectType):

        choices = List(ChoiceType)

        def resolve_choices(question, info):
            return question.choice_set.all()

I have skipped other fields `ID`, `pub_date` and `question_text` here for brevity sake. Do not remove those fields and their resolver functions. Just add a `choices` and `resolve_choices` as done above.

Let's restart the shell and query for a question detail and ask for `choice_text` of associated choices too.

    In [7]: search = '{question(id:56){questionText pubDate choices{choiceText}}}'

    In [8]: schema.execute(search).data
    Out[8]:
    OrderedDict([('question',
                  OrderedDict([('questionText', 'Is the color of sky blue'),
                               ('pubDate', '2019-05-15'),
                               ('choices',
                                [OrderedDict([('choiceText', 'maybe')]),
                                 OrderedDict([('choiceText', 'yes')]),
                                 OrderedDict([('choiceText', 'no')])])]))])

The api call would look like:

    http://localhost:8000/graphql/?search={question(id:56){questionText pubDate choices{choiceText}}}

## Mutations

We want to provide a way to create Question. The way to do that with GraphQL is mutations.

Let's write a mutation called `CreateQuestion`. Model Question has fields `question_text` and `pub_date`. So mutation will need arguments `question_text` and `pub_date`.

Any `Mutation` we write with python-graphene needs to have a method called `mutate`. This is synonymous to how resolver functions are needed for query objecttypes.

Basic strucutre of a `Mutation` looks like:

    class CreateQuestion(Mutation):
        class Arguments:
            pass

        def mutate(root, info, *args):
            pass

Let's write actual code of `CreateQuestion`.

    class CreateQuestion(Mutation):
        class Arguments:
            question_text = String()
            pub_date = String()

        question = Field(QuestionType)

        def mutate(root, info, question_text, pub_date):
            pub_date = datetime.datetime.strptime(pub_date, '%Y-%m-%d')
            question = Question.objects.create(question_text=question_text, pub_date=pub_date)
            return CreateQuestion(question=question)

We will have to add this mutation on `schema` so that our GraphQL service understands that this mutation is an entry point.

    class MyMutations(ObjectType):
        create_question = CreateQuestion.Field()

    schema = Schema(query=Query, mutation=MyMutations)

Mutation `CreateQuestion` needs arguments `question_text` and `pub_date` to create a Question. These arguments will be passed to the `mutate` function. That's why you can see `question_text` and `pub_date` in function signature too. `question` is the output field of our mutation. So the created Question instance is returned once the mutation resolves.

Let's create some questions:

    In [7]: from bombardill.graphql import schema

    In [8]: mutation = """
       ...: mutation {
       ...:     createQuestion(questionText: "Do you like rabbits?", pubDate: "2019-10-22") {
       ...:         question {
       ...:             questionText
       ...:             pubDate
       ...:         }
       ...:     }
       ...: }
       ...: """

    In [9]: schema.execute(mutation).data
    Out[9]:
    OrderedDict([('createQuestion',
                  OrderedDict([('question',
                                OrderedDict([('questionText',
                                              'Do you like rabbits?'),
                                             ('pubDate', '2019-10-22')]))]))])

We sent a mutation and asked for `questionText` and `pubDate` fields of created question.

Let's create one more question but only ask for `questionText` field once the mutation resolves.

    In [10]: mutation = """
        ...: mutation {
        ...:     createQuestion(questionText: "Do you like hobbits?", pubDate: "2019-10-22") {
        ...:         question {
        ...:             questionText
        ...:         }
        ...:     }
        ...: }
        ...: """

    In [11]: schema.execute(mutation).data
    Out[11]:
    OrderedDict([('createQuestion',
                  OrderedDict([('question',
                                OrderedDict([('questionText',
                                              'Do you like hobbits?')]))]))])

## Create choice

Let's similarly add one more `Mutation` called `CreateChoice` and it on `MyMutations`.

    class CreateChoice(Mutation):
        class Arguments:
            question_id = Int()
            choice_text = String()

        choice = Field(ChoiceType)

        def mutate(root, info, question_id, choice_text):
            question = Question.objects.get(id=question_id)
            choice = Choice.objects.create(question=question, choice_text=choice_text)
            return CreateChoice(choice)

    class MyMutations(ObjectType):
        create_question = CreateQuestion.Field()
        create_choice = CreateChoice.Field()

Let's execute a query to create choice.

    In [2]: from bombardill.graphql import schema

    In [3]: mutation = """
       ...: mutation {
       ...:     createChoice(choiceText: "yes", questionId: 56) {
       ...:         choice {
       ...:             choiceText
       ...:         }
       ...:     }
       ...: }
       ...: """

    In [4]: schema.execute(mutation).data
    Out[4]:
    OrderedDict([('createChoice',
                  OrderedDict([('choice',
                                OrderedDict([('choiceText', 'yes')]))]))])

Similarly we can write mutations to update a question or delete a question.
