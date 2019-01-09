---
layout: post
comments: true
title:  "Tracking creator of Django objects"
description: "Using middleware and threading.local to track Django model object creator"
keywords: "Django, Python"
date: 2019-01-09
categories: [python, django]
author: akshar
---

#### Agenda

We have a Django project with multiple models. We want to add auditing to all/several of our models. Our auditing involves tracking the user who created a particular model instance.

A naive way to achieve it would be to set `creator=request.user` during instance initialization or during manager's `.create()` call. This requires passing `request.user` to __init__() or manager's create() from every view which saves a model instance. This approach would be ugly and make code unmaintainable.

There is a better way using which we can avoid passing `request.user` from every view during instance creation. This way involves creating a middleware and thread local object and using the thread local object in `save()`.

#### Ugly way

We want to audit every model and track creator of every model instance. Let's create a BaseModel with a single field `creator` and make all other models extend from it.

    # base/models.py
    from django.contrib.auth import User

    NULL_AND_BLANK = {'null': True, 'blank': True}

    class BaseModel(models.Model):
        creator = models.ForeignKey(User, **NULL_AND_BLANK)

        class Meta:
            abstract = True

Make model `Name` extend from `BaseModel`.

    # names/models.py
    class Name(BaseModel):
        english_representation = models.CharField(max_length=100)
        vernacular_representation = models.CharField(max_length=100)

        def __unicode__(self):
            return self.english_representation

Assume there is a view which processes a form and creates a Name instance in the database. We want to audit `Name` and track the user who created this name.

    # names/views.py
    @login_required
    def create_name(self, request):
        form = NameForm(data=request.POST or None)
        if form.is_valid():
            Name.objects.create(english_representation=form.cleaned_data['english_representation'], vernacular_representation=form.cleaned_data['vernacular_representation'], creator=request.user)
        return render(request, 'names/name-create.html', {'form': form})

Or your view code could look like:

    # names/views.py
    @login_required
    def create_name(request):
        form = NameForm(data=request.POST or None)
        if form.is_valid():
            name = Name(english_representation=form.cleaned_data['english_representation'], vernacular_representation=form.cleaned_data['vernacular_representation'], creator=request.user)
            name.save()
        return render(request, 'names/name-create.html', {'form': form})

Notice that we had to pass `creator=request.user`.

You could have multiple views in your project which deal with object creation. You will have to pass `request.user` from every view where you want to audit the instance.

This approach is ugly.

#### Better way

We could add a middleware which sets `request.user` in a thread local object. We can override `save()` of base model and use the thread local object to set creator.

Let's add a middleware.

    # base/middleware.py
    import threading

    local = threading.local()

    class BaseMiddleware(object):

        def __init__(self, get_response):
            self.get_response = get_response

        def __call__(self, request):
            local.user = request.user
            response = self.get_response(request)
            return response

This middleware would ensure that `local.user` is set for every request which hits the server.

We must add `base.middleware.BaseMiddleware` after `SessionMiddleware` and `AuthenticationMiddleware` to ensure that `request.user` is correctly populated by the time our custom middleware, i.e BaseMiddleware is executed.

    # settings.py
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',

        'base.middleware.BaseMiddleware',
    ]

Next we need to override BaseModel.save().

    # base/models.py
    from .middleware import local

    class BaseModel(models.Model):
        created = models.DateTimeField(auto_now_add=True)
        modified = models.DateTimeField(auto_now=True)
        creator = models.ForeignKey(User, **NULL_AND_BLANK)

        def save(self, *args, **kwargs):
            if self.pk is None and hasattr(local, 'user'):
                self.creator = local.user
            return super(BaseModel, self).save(*args, **kwargs)

        class Meta:
            abstract = True

We can then modify view code to remove `request.user` from manager's `.create()` calls.

    @login_required
    def create_name(request):
        form = NameForm(data=request.POST or None)
        if form.is_valid():
            name = Name.objects.create(english_representation=form.cleaned_data['english_representation'], vernacular_representation=form.cleaned_data['vernacular_representation'])
        return render(request, 'names/name-create.html', {'form': form})

Now `creator` would be set to `request.user` when a valid form is submitted, even though we didn't pass `creator` from view.

Views which create an instance don't need to pass `creator` anymore and still all models which extend from BaseModel would be audited.

If we create an instance from shell, then `creator` would be set to null because shell commands don't invoke middleware code.

    In [4]: Name.objects.create(english_representation='will', vernacular_representation='विल')
    Out[4]: <Name: will>

    In [5]: n = Name.objects.latest('pk')

    In [6]: n.english_representation
    Out[6]: u'will'

    In [8]: n.creator is None
    Out[8]: True

This approach looks much cleaner than passing `creator` from every instance creation view.
