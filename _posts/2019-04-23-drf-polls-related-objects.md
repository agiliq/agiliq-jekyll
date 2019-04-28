---
layout: post
comments: true
title:  "Creating related objects in Django REST Framework"
description: "Polls apis to create related objects"
keywords: "Django REST Framework, DRF, Django, Python, API"
date: 2019-04-23
categories: [API, django, drf]
author: Akshar
---

## Agenda

This post assumes that you have followed our <a href="https://www.agiliq.com/blog/2019/04/drf-polls/" target="_blank">first post</a> of this series.

We will be creating the following apis in this post.

- An api to create an associated choice along with a Question
- An api to create multiple associated choices along with a Question
- Api to create multiple questions, each question with multiple choices

## Apis

Let's start writing our apis.

### Create a choice along with creating a question

The api for creating question is `POST /api/polls/questions/`.

Till now we used QuestionListPageSerializer for creating question, seralizer looked like:

    class QuestionListPageSerializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        question_text = serializers.CharField(max_length=200)
        pub_date = serializers.DateTimeField()
        was_published_recently = serializers.BooleanField(read_only=True) # Serializer is smart enough to understand that was_published_recently is a method on Question

        def create(self, validated_data):
            return Question.objects.create(**validated_data)

POST handler for view looked like.

    elif request.method == 'POST':
        serializer = QuestionListPageSerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.save()
            return Response(QuestionDetailPageSerializer(question).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

You can see full code <a href="here" target="_blank">https://www.agiliq.com/blog/2019/04/drf-polls/#final-code</a>

We now want to create a choice along with question. Add following attribute to QuestionListPageSerializer:

    choice = ChoiceSerializer(write_only=True)

A DRF `Serializer` is a subclass of DRF `Field`. Similar to how a serializer can have a `Field` as an attribute, it can also have another `Serializer` as an attribute.

Modify `create()` of QuestionListPageSerializer to following:

    def create(self, validated_data):
        choice_dict = validated_data['choice']
        question = Question.objects.create(**validated_data)
        choice_dict['question'] = question
        Choice.objects.create(**choice_dict)
        return question

Try to POST a question without a choice and the code would raise a 400 Bad Request.

![](/assets/images/drf/question-without-choice.png)

POST a question with valid choice data and the api call would succeed.

![](/assets/images/drf/question-with-choice.png)

Since QuestionListPageSerializer has a field ChoiceSerializer so a ChoiceSerializer representation needs to be sent as `choice` key in the POSTed data. Remember how we POSTed choice in the <a href="https://www.agiliq.com/blog/2019/04/drf-polls/#post-a-question-choice">last post.</a> We used a similar datastructure, i.e a dictionary containing `choice_text`.

Verify that the correct question and choice were created. Also verify that the choice was associated with the question.

    In [2]: question = Question.objects.latest('pk')

    In [3]: question.choice_set.all()
    Out[3]: <QuerySet [<Choice: Fossil>]>

    In [5]: choice = Choice.objects.latest('pk')

    In [6]: choice
    Out[6]: <Choice: Fossil>

    In [7]: choice.question
    Out[7]: <Question: Which company makes the most durable wallets?>

    In [8]: choice.question == question
    Out[8]: True

Try to post with invalid choice data, say without choice_text and api will respond with descriptive message.

![](/assets/images/drf/question-with-invalid-choice.png)

The message is:

    {
        "choice": {
            "choice_text": [
                "This field is required."
            ]
        }
    }

In case you want to make `choice` as an optional thing during question creation, add a `required=False` keyword argument.

    choice = ChoiceSerializer(write_only=True, required=False)

We will also need to adjust `create()` to deal with situation when `choice` isn't present in POSTed data.

    def create(self, validated_data):
        question = Question.objects.create(**validated_data)
        if 'choice' in validated_data:
            choice_dict = validated_data['choice']
            choice_dict['question'] = question
            Choice.objects.create(**choice_dict)
        return question

### Create multiple choices with question

We want the POST questions api to allow creation of multiple choices along with the question.

We will remove field `choice` from QuestionListPageSerializer and instead add a `choices` field which looks like:

    choices = ChoiceSerializer(many=True, write_only=True)

We will need to adjust `create()` code of QuestionListPageSerializer too.

    def create(self, validated_data):
        choices = validated_data.pop('choices', [])
        question = Question.objects.create(**validated_data)
        for choice_dict in choices:
            choice_dict['question'] = question
            Choice.objects.create(**choice_dict)
        return question

Entire serializer would look like:

    class QuestionListPageSerializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        question_text = serializers.CharField(max_length=200)
        pub_date = serializers.DateTimeField()
        was_published_recently = serializers.BooleanField(read_only=True) # Serializer is smart enough to understand that was_published_recently is a method on Question
        choices = ChoiceSerializer(many=True, write_only=True)

        def create(self, validated_data):
            choices = validated_data.pop('choices', [])
            question = Question.objects.create(**validated_data)
            for choice_dict in choices:
                choice_dict['question'] = question
                Choice.objects.create(**choice_dict)
            return question

Let's try POSTing a Question with two choices.

![](/assets/images/drf/question-post-with-two-choices.png)

You should have noticed `Status: 201 Created` which suggests that the Question and Choices should have been created.

The response of this call should be looking like the following:

![](/assets/images/drf/question-post-with-two-choices-response.png)

A question with id 21 was created. You can verify that the POSTed choices, i.e Fossil and Burberry, were associated with this question.

    In [2]: q = Question.objects.get(id=21)

    In [3]: q.choice_set.all()
    Out[3]: <QuerySet [<Choice: Burberry>, <Choice: Fossil>]>

Let's try posting with one invalid choice and one valid choice:

![](/assets/images/drf/question-post-with-invalid-choice.png)

You should have noticed that the api gave a 400 Bad Request. The response content would look like:

![](/assets/images/drf/question-post-with-invalid-choice-response.png)

If you notice the response content, `choices` is a list and the first dictionary of `choices` is empty. This means that first choice data is valid. The second dictionary has a message telling that `choice_text` is required, which suggests that second choice data is invalid.

### Create multiple questions

We want to create multiple questions along with associated choices in a single api call.

We will need to create a urlpattern and an apiview to achieve this.

    @api_view(['POST'])
    def multiple_questions_view(request):
        serializer = QuestionListPageSerializer(many=True, data=request.data)
        if serializer.is_valid():
            questions = serializer.save()
            return Response(QuestionDetailPageSerializer(questions, many=True).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

Let's keep the urlpattern as:

    path('multiple-questions/', apiviews.multiple_questions_view, name='multiple_questions_view')

Let's make a POST request.

![](/assets/images/drf/questions-multiple.png)

The status code 201 suggests that our questions and choices were correctly created. You response should look like:

![](/assets/images/drf/questions-multiple-response.png)

Stay tuned for next post of the series.
