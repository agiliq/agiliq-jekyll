---
layout: post
comments: true
title:  "Modelling sorting and ordering in Redis"
description: "How to store sortable data in Redis"
keywords: "Redis"
date: 2019-12-17
categories: [Redis]
author: Akshar
---

## Agenda

In this post we will see how to model our data in such a way that it could be sorted.

This post assumes that you have Redis installed and you can run `redis-cli`.

Assume we are storing a list of `Person` in Redis. We use Redis list datastructure to store Person. Each `Person` has a `name` `id` and `age`. You want an ability to sort by `id` or sort by `age`. We will discuss how we can achieve it.

## Basics

The underlying data type we would use is a Redis `Sorted set`. A `Sorted set` allows assigning score to each member of the set.

Let's create a `Sorted set` called `names_and_ages`. We will add `members` ned, bran, rickon and catelyn to the sorted set. We will assign members' respective ages as their score.

    127.0.0.1:6379> ZADD names_and_ages 35 ned
    (integer) 1
    127.0.0.1:6379> ZADD names_and_ages 7 bran
    (integer) 1
    127.0.0.1:6379> ZADD names_and_ages 4 rickon
    (integer) 1
    127.0.0.1:6379> ZADD names_and_ages 33 catelyn
    (integer) 1

We didn't see any error, which indicates that the members and their corresponding scores were added to the sorted set.

Notice that rickon is the youngest and ned is the oldest.

Let's get all the members of this sorted set.

    127.0.0.1:6379> zrange names_and_ages 0 -1
    1) "rickon"
    2) "bran"
    3) "catelyn"
    4) "ned"

The output confirms that the sorted set kept the data sorted based on the age/scores.

## Sorting on entities

We will use a Redis hash to store `Person` entities and a Redis list to store the keys of all people.

Let's add few `Person`.

    127.0.0.1:6379> HMSET person-1 id 1 name ned age 35
    OK
    127.0.0.1:6379> RPUSH people person-1
    (integer) 1

    127.0.0.1:6379> HMSET person-2 id 2 name catelyn age 33
    OK
    127.0.0.1:6379> RPUSH people person-2
    (integer) 2

We can use `LRANGE` on people to find the keys of all person added to Redis.

    127.0.0.1:6379> LRANGE people 0 -1
    1) "person-1"
    2) "person-2"

We can loop over these keys and get details for Person.

### Problem

What if we want to get the Person list sorted by their age? Redis doesn't have a query language where we can say that we want our results sorted.

### Solution

Let's introduce a sorted set. We will use the `Person` key as member and person's age as score. Let's flush everything and start afresh.

    127.0.0.1:6379> HMSET person-1 id 1 name ned age 35
    OK
    127.0.0.1:6379> rpush people person-1
    (integer) 1
    127.0.0.1:6379> ZADD people-age-sorted 35 person-1
    (integer) 1

    127.0.0.1:6379> HMSET person-2 id 2 name bran age 7
    OK
    127.0.0.1:6379> rpush people person-2
    (integer) 2
    127.0.0.1:6379> ZADD people-age-sorted 7 person-2
    (integer) 1

    127.0.0.1:6379> HMSET person-3 id 3 name rickon age 4
    OK
    127.0.0.1:6379> rpush people person-3
    (integer) 3
    127.0.0.1:6379> ZADD people-age-sorted 4 person-3
    (integer) 1

    127.0.0.1:6379> HMSET person-4 id 4 name catelyn age 33
    OK
    127.0.0.1:6379> rpush people person-4
    (integer) 4
    127.0.0.1:6379> ZADD people-age-sorted 33 person-4
    (integer) 1

Let's get people keys sorted by their age:

    127.0.0.1:6379> zrange people-age-sorted 0 -1
    1) "person-3"
    2) "person-2"
    3) "person-4"
    4) "person-1"

`person-3` is the key for rickon and `person-1` is the key for ned.

And then we can loop over these keys to get full representation of these people.

    127.0.0.1:6379> HGETALL person-3
    1) "id"
    2) "3"
    3) "name"
    4) "rickon"
    5) "age"
    6) "4"

Similarly we can get all attributes of other people.

In case we want the age sorted by descending, we can use Redis `ZREVRANGE`.

    127.0.0.1:6379> ZREVRANGE people-age-sorted 0 -1
    1) "person-1"
    2) "person-4"
    3) "person-2"
    4) "person-3"

This example can be easily tailored to work with any programming language client. See our <a href="https://www.agiliq.com/blog/2019/11/writing-an-orm-for-redis/" target="_blank">last post</a> on how we did it with Python.
