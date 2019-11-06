---
layout: post
comments: true
title:  "Understanding Django transactions"
description: "Writing concurrency safe Django code"
keywords: "Django REST Framework, DRF, Django, Python, API"
date: 2019-11-05
categories: [django, transactions]
author: Akshar
---

## Agenda

This post assumes that you understand transactions at database level. Also this post has been written considering PostgreSQL as database.

To recap, every SQL statement in psql implicitly executes inside a transaction without user/client having to explicitly use transaction constructs like `BEGIN` and `COMMIT`.

We will write a view which leads to a race condition and will then fix it using Django's F expressions and later using Django transaction decorator.

## View

Let's assume we have the following view.

    from rest_framework.views import APIView
    from rest_framework.responses import Response

    class LikeView(APIView):

        def patch(self, request, *args, **kwargs):
            post = get_object_or_404(Post, pk=kwargs['pk'])
            post.likes += 1
            post.save()
            return Response("Voted")

Assume this api is exposed at `http://localhost:8000/api/post/<pk>/like`.

Let's assume the correct `likes` is 0 for post with id 1.

If you make 50 concurrent calls to `http://localhost:8000/api/post/1/like`, you will notice that the likes might not have increased to 50. It might show 47 or 48 or some other number less than 50.

This happened because there is a race condition in the code. One process/thread might have read a value for `likes` and before it could save(), another process/thread would have read the same value. So even though `save()` executed from both processes, still the value would have been incremented only once.

The fix for this is to handle increment of `likes` using a database call without reading it in memory.

Modify the above code to following:

    from django.db.models import F

    class LikeView(APIView):

        def patch(self, request, *args, **kwargs):
            Post.objects.filter(pk=kwargs['pk']).update(votes=F('votes') + 1)

We used ORM `update()` which runs underlying database's `update`. As the db update runs in a transaction so each process/thread would correctly increment the value of `likes`.
