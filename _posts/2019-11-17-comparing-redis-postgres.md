---
layout: post
comments: true
title:  "Comparing Redis and PostgreSQL"
description: "How Redis can make your websites insanely fast"
keywords: "Django, Python, Redis, Caching"
date: 2019-11-17
categories: [Redis, django]
author: Akshar
---

## Agenda

Redis is an in-memory caching tool which can supplement your database.

I always wondered how fast can my website become if I add a caching layer. That's the motivation behind this blog post. I saw an improvement of 10x when I started fetching things from Redis instead of the database.

## Setup

We will use a Python/Django project to test things out but the solution can be easily adapted for any other language/framework.

Let's assume we have the following model.

    # customers/models.py

    class Customer(BaseModel):
        customer_id = models.CharField(max_length=10)
        address = models.TextField()

Assume we have an api which returns the details for a customer. The api is built using Django REST Framework and look like:

    # customers/views.py

    class CustomersAPIView(APIView):

        def post(self, request, *args, **kwargs):
            pass

        def get(self, request, *args, **kwargs):
            if 'pk' in kwargs:
                # TODO: Use get_object_or_404()
                customer = Customer.objects.get(pk=kwargs['pk'])
                data = CustomerSerializer(customer).data
                return Response(data)
            # TODO: Implement returning list of customers
            return Response([])

Let's move the logic to get customer to a service called `get_customer_db`.

    # customers/services.py

    def get_customer_db(pk):
        customer = Customer.objects.get(pk=pk)
        return CustomerSerializer(customer).data

Modify the view to use `get_customer_db`.

    from .services import get_customer_db

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            data = get_customer_db(kwargs['pk'])
            return Response(data)
        # TODO: Implement returning list of customers
        return Response([])

We expect that this api would be called very frequently from our UI/client. It would be sub-optimal to fetch the same customer details every single time from the database.

This is an ideal scenario to add caching. Let's add a service called `get_customer_redis`.

    import redis

    from .serializers import CustomerSerializer
    from .models import Customer

    r = redis.Redis(host='localhost', port=6379, db=0, charset='utf-8', decode_responses=True)

    def get_customer_redis(pk):
        key = 'customer-%d' % (pk,)
        customer_representation = r.hgetall(key)
        if not customer_representation:
            customer_representation = set_customer_redis(pk)
        return customer_representation


    def set_customer_redis(pk):
        key = 'customer-%d' % (pk,)
        customer_representation = get_customer_db(pk)
        r.hmset(key, customer_representation)
        return customer_representation

In get_customer_redis, we search for key `customer-<pk>`. If this key isn't found in redis, we get the customer's details from the db and set it the redis cache. This ensures that any subsequent calls to `get_customer_redis` gets us the data from redis instead of hitting the db.

## Redis vs Postgres

Let's compare `get_customer_db` and `get_customer_redis` now. We will run 1000 executions for both of these functions to get details for customer with pk 3.

Let's write a helper function which lets us execute these functions n number of times.


    In [1]: import time

    In [2]: def fun(f, iteration, pk):
        ...:     st = time.time()
        ...:     for each in range(iteration):
        ...:         f(pk)
        ...:     print(time.time() - st)

    In [3]: from customers.services import get_customer_redis, get_customer_db

    In [4]: fun(get_customer_db, 1000, 3)
    1.3029980659484863

We fetched details from the db 1000 times. It took 1.302 seconds.

Let's fetch details from the cache 1000 times.

    In [20]: fun(get_customer_redis, 1000, 3)
    0.12113094329833984

It took 0.12 seconds to fetch details 1000 times from the cache.

## Conclusion

Redis gave us an improvement of 10 times. This value might differ in your case depending on how big your dataset is but Redis will definitely perform better than postgres.
