---
layout: post
comments: true
title:  "Adding an api layer to Django polls api"
description: "Polls api using api_view and ModelSerializer"
keywords: "Django REST Framework, DRF, Django, Python, API"
date: 2019-05-01
categories: [API, django, drf]
author: Akshar
---

## Agenda

This post assumes intermediate knowledge of Django and expects that you are familiar with Django ModelForm. It also assumes that you understand why DRF should be used for apis instead of using plain Django.

If you are an absolute beginner to Django, follow <a href="https://www.agiliq.com/blog/2019/04/drf-polls/" target="_blank">our introductory post</a> of this series. Our introductory post also explains why DRF should be used for apis instead of plain Django.

We will be creating the following apis in this post.

- An api to create a poll question.
- Api to list questions.
- Api to get question detail.
- Api to edit a question.
- Api to delete a question.
- Api to create choice for a particular question.
- Api to see question detail along with available choices.
- Api to vote for a particular choice of a question.
- Api to see result for a particular question.

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


### Create question

Let's write an api to create question.

This api should be available at POST /api/polls/questions/.

Side note: <a href="https://github.com/NationalBankBelgium/REST-API-Design-Guide/wiki/REST-Resources-Parameters" target="_blank">This.</a> is an informative resource to learn about REST api endpoints design best practices.

Create a module called polls/apiviews.py to keep polls apis.

    touch polls/apiviews.py

Add following code to polls/apiviews.py

    from django.http import HttpResponse
    from django.views.decorators.csrf import csrf_exempt

    from .models import Question

    @csrf_exempt
    def questions_view(request):
        if request.method == 'GET':
            return HttpResponse("Not Implemented")
        elif request.method == 'POST':
            return HttpResponse("Not Implemented")

Add following urlpattern to root URLconf file.

    # mysite/urls.py
    path('api/polls/', include('polls.urls'))

Add following urlpattern to polls/urls.py

    from . import apiviews

    path('questions/', apiviews.questions_view, name='questions_view'),

We will create a `ModelSerializer` subclass which will be used in the view. A ModelSerializer is a class provided by DRF which can handle data validation and provide primitive representation of model instances.

A DRF ModelSerializer is similar to a Django `ModelForm` and provides similar interface as a ModelForm. A ModelSerializer serves analogous pupose to that of a ModelForm.

A ModelForm is used to validate posted form data. Simiarly a ModelSerializer is used to validate posted data in an api request. A ModelForm can provide a form representation of a model instance for editing. Similarly a ModelSerializer can provide a representation of a model instance which is easily understandable.

Let's write our ModelSerializer in polls/serializers.py

    from rest_framework import serializers

    from polls.models import Question

    class QuestionSerializer(serializers.ModelSerializer):

        class Meta:
            model = Question
            exclude = ()

Hereafter I would be using ModelSerializer and ModelSerializer subclass interchangeably.

You should have noticed the interface similarity of the ModelSerializer we wrote above with a ModelForm. A ModelForm needs a `Meta`, similarly a ModelSerializer needs a Meta too. Meta of ModelForm expects a `model` attribute, similarly ModelSerializer.Meta expects a `model` too.

We want the serializer to enforce presence of all Question fields in POSTed data, so we have set `exclude` attribute to an empty tuple.

We could have used `fields` attribute instead of `exclude`.

    class QuestionSerializer(serializers.ModelSerializer):

        class Meta:
            model = Question
            fields = '__all__'

Let's use this serializer in the view.

    from rest_framework.decorators import api_view
    from rest_framework.response import Response
    from rest_framework import status

    from .models import Question
    from .serializers import QuestionSerializer


    @api_view(['GET', 'POST'])
    def questions_view(request):
        if request.method == 'GET':
            return Response("Not Implemented")
        elif request.method == 'POST':
            serializer = QuestionSerializer(data=request.data)
            if serializer.is_valid():
                question = serializer.save()
                return Response("Question created with id %s" % (question.id))
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

We wrote a regular Django view and decorated it with DRF decorator `api_view`. A regular Django view only handles form-data by default. api_view can handle form-data as well as application/json data.

We used a DRF specific `Response` object instead of Django `HttpResponse`. `Response` is a subclass of `HttpResponse` having additional functionality which comes in handy while working with apis.

A ModelSerializer provides a method called `is_valid()` similar to Django ModelForm `is_valid()`. ModelSerializer.is_valid does validation on POSTed data and can report on errors. ModelSerializer also provides a default implementation of save(). The default implementation of save() creates a model instance and returns the created instance.

Let's use Postman to make a POST call to this api endpoint. Postman is an extremely useful tool, start using it if you aren't already.

Let's make a POST request without pub_date.

![](/assets/images/drf/model-serializer-without-pub-date.png)

The response should look like:

![](/assets/images/drf/model-serializer-without-pub-date-response.png)

Our model serializer did the validation and provided a descriptive error message without us having to write any validation code.

Let's post with wrong format of pub_date.

![](/assets/images/drf/question-post-pub-date-wrong-format.png)

As you should have noticed, the descriptive error messages were provided to us by the serializer for free.

![](/assets/images/drf/model-serializer-post.png)

The POST call should have created a Question instance.

    In [5]: Question.objects.all()
    Out[5]: <QuerySet [<Question: Is Adidas better than Reebok?>]>

POST one more question

![](/assets/images/drf/model-serializer-another-post.png)

### List questions

The api should be available at `GET /api/polls/questions/`.

We want the api response to provide the `id`, `question_text` and `pub_date` for all questions.

Modify questions_view so it looks like the following:

    @api_view(['GET', 'POST'])
    def questions_view(request):
        if request.method == 'GET':
            questions = Question.objects.all()
            serializer = QuestionSerializer(questions, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = QuestionSerializer(data=request.data)
            if serializer.is_valid():
                question = serializer.save()
                return Response("Question created with id %s" % (question.id))
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

Notice how concise our GET handler code is:

    questions = Question.objects.all()
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)

Try GET /api/polls/questions/

![](/assets/images/drf/model-serializer-get.png)

A ModelSerializer provides an attribute called `data` using which you can get the representation of model instance.

Let's use QuestionSerializer in the POST too to get the entire representation of Question instance once it is created. Modify the POST handler part to look like:

    if serializer.is_valid():
        question = serializer.save()
        serializer = QuestionSerializer(question)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

### List with derived fields

Question has a method called `was_published_recently` which returns a boolean. We also want to send `was_published_recently` for all Questions in GET call.

This will need adding the following line to QuestionSerializer.

    was_published_recently = serializers.BooleanField(read_only=True)

We made it `read_only` because it's not a model field and so serializer should not be expecting it in POST calls.

Serializer is smart enough to infer that `was_published_recently` is not a model field on Question but is instead a method. Serializer uses Question.was_published_recently() to get a boolean value and add it in the serializer representation for Question.

![](/assets/images/drf/model-serializer-get-derived-field.png)

Say you want to add one more model method called `Question.verbose_question_text`  and want it in the GET response. You would do the following:

    # polls/models.py
    # Add this method to model Question
    def verbose_question_text(self):
        return "Question : %s" % (self.question_text)

    # polls/serializers.py
    # Add following to QuestionSerializer
    verbose_question_text = serializers.CharField(read_only=True)

### Detail of a question

The api should be available at `GET /api/polls/questions/<question_id>/`.

Add the following view to polls/apiviews.py

    from django.shortcuts import get_object_or_404


    @api_view(['GET', 'PATCH', 'DELETE'])
    def question_detail_view(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        if request.method == 'GET':
            serializer = QuestionSerializer(question)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            raise NotImplementedError("PATCH currently not supported")
        elif request.method == 'DELETE':
            raise NotImplementedError("DELETE currently not supported")

Currently PATCH and DELETE are not implemented.

Add a urlpattern to polls/urls.py

    path('questions/<int:question_id>/', apiviews.question_detail_view, name='question_detail_view'),

Make a GET request to /api/polls/questions/31/

![](/assets/images/drf/model-serializer-get-derived-field-2.png)

We have introduced a Django shortcut `get_object_or_404()`. DRF is smart enough to deal with this Django shortcut and return a 404 response when a question with id doesn't exist.

![](/assets/images/drf/404.png)

### Edit a poll question

The api should be available at `PATCH /api/polls/questions/<question_id>`.

We want to send a partial represention of a question in the api request and want an attribute of question to be changed accordingly. eg: We might want to change `question_text` of a Question instance. PATCH is the recommended HTTP method for such cases.

Modify question_detail_view PATCH handler code.

    @api_view(['GET', 'PATCH', 'DELETE'])
    def question_detail_view(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        if request.method == 'GET':
            serializer = QuestionSerializer(question)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = QuestionSerializer(question, data=request.data, partial=True)
            if serializer.is_valid():
                question = serializer.save()
                serializer = QuestionSerializer(question)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            raise NotImplementedError("DELETE currently not supported")

When we want to edit an instance, we need to pass the instance as first argument to ModelSerializer and the posted data as second argument. That's why we passed `question` as first argument and `request.data` as second argument.

DRF provides a keyword argument called `partial` on ModelSerializer and that's what we used here.

question_text of Question id 32 is "What is the color of sky?". Let's change it to "What is the color of sky? Is it blue?" by making a PATCH request to /api/polls/questions/32/.

![](/assets/images/drf/model-serializer-patch.png)

### Delete a poll question

The api should be available at `DELETE /api/polls/questions/<question_id>`.

Modify DELETE handler code to look like:

    elif request.method == 'DELETE':
        question.delete()
        return Response("Question deleted", status=status.HTTP_204_NO_CONTENT)

Let's delete the question with id 32.

![](/assets/images/drf/model-serializer-delete.png)
