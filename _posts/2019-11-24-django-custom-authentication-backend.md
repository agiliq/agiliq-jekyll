---
layout: post
comments: true
title:  "Adding a custom authentication backend in Django"
description: "How to authenticate Django users through non default mechanism"
keywords: "Django REST Framework, DRF, Django, Python, API"
date: 2019-11-24
categories: [django]
author: Akshar
---

## Agenda

We will add a custom authentication backend to our Django project.

The default authentication mechanism in Django requires a user to provide a username and password.

Consider a scenario where you are building a banking application. Each customer has a customer_id. You might want to support customer authentication through both username and customer_id.

## Basics

The most common flow in a Django app shows two fields, namely `username` and `password`  in the login form. These values are passed to Django `authenticate()` from the view.

`authenticate` executes the authentication classes specified in `settings.AUTHENTICATION_BACKENDS`.

Default `AUTHENTICATION_BACKENDS` look like:

    AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)

We want to allow authentication with `customer_id` while still supporting the default authentication mechanism where user can authenticate using the `username`.

## Setup

Assume we have a model called `Customer`.

    # customers/models.py

    class Customer(BaseModel):
        customer_id = models.CharField(max_length=10)
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        address = models.TextField()
        city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)

        objects = CustomerManager()

        def __str__(self):
            return self.customer_id

We will have to add an authentication class, let's call it `CustomerBackend`.

It would look like the following:

    # customers/backends.py

    from django.contrib.auth.backends import ModelBackend
    from django.contrib.auth.models import User

    from customers.models import Customer

    class CustomerBackend(ModelBackend):

        def authenticate(self, request, **kwargs):
            customer_id = kwargs['username']
            password = kwargs['password']
            try:
                customer = Customer.objects.get(customer_id=customer_id)
                if customer.user.check_password(password) is True:
                    return customer.user
            except Customer.DoesNotExist:
                pass

The form and view can remain unchanged and keep the fields name as `username` and `password`. We need to add `CustomerBackend` to `AUTHENTICATION_BACKENDS`.

    AUTHENTICATION_BACKENDS = [
        'django.contrib.auth.backends.ModelBackend',
        'customers.backends.CustomerBackend',
    ]

With this, a user would be able to login with either their username or with their customer_id.
