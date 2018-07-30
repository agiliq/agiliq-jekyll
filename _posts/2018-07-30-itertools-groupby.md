---
layout: post
comments: true
title:  "Python itertools groupby"
description: "When and How to use Python itertools.groupby"
keywords: "Python, Itertools"
date:   2018-07-30
categories: [python, django]
author: Akshar
---

One of the most useful Python builtin module is **itertools**. It provides several methods which allow manipulation of data structures in a concise way.

Here we will talk about `itertools.groupby`.

### When to use `groupby`

It comes into picture when there is a sequence and several elements of the sequence are related. If we want to group all the related elements of the sequence under a group then groupby becomes handy.

Suppose we have a list of dictionaries, which looks like:

    In [6]: companies = [{'country': 'India', 'company': 'Flipkart'}, {'country': 'India', 'company': 'Myntra'}, {'country': 'India', 'company': 'Paytm'}, {'
       ...: country': 'USA', 'company': 'Apple'}, {'country': 'USA', 'company': 'Facebook'}, {'country': 'Japan', 'company': 'Canon'}, {'country': 'Japan', '
       ...: company': 'Pixela'}]

Each element of the list contains detail of a company which includes the name of the company and the country of the company. We have a web page where we want to show the country name in heading followed by all the companies of that country. Then heading of another country with all companies of that country and so on. This can be achieved with `groupby`.

### How to use `groupby`

`groupby` works with a sequence or an iterable. Let's use the same datastructure as defined above.

    In [13]: import itertools

    In [22]: companies_grouped_by_country = itertools.groupby(companies, key=lambda each: each['country'])

`groupby` returns an iterator. companies_grouped_by_country is an iterator here.

**key** argument to groupby tells the criteria using which elements of sequence should be grouped. We want to group elements of the sequence based on each country's country key.

Looping through companies_grouped_by_country yields tuples where first element of the tuple is the key which was used to group and second element of tuple is another iterator.

Let's first consider the first element of tuple. Let's loop through companies_grouped_by_country.

    In [26]: for country_name, _ in companies_grouped_by_country:
        ...:     print country_name
        ...:
    India
    USA
    Japan

Since each element yielded by companies_grouped_by_country is a tuple, so we unpacked it into two variables, i.e country_name and `_`. The first element of tuples are country names in our case as it was the criteria used to group.

We want to see related company details along with the country for each country.

    In [22]: companies_grouped_by_country = itertools.groupby(companies, key=lambda each: each['country'])
    In [33]: for country_name, country_companies in companies_grouped_by_country:
        ...:     print "----"
        ...:     print country_name
        ...:     for company_detail in country_companies:
        ...:         print company_detail 
        ...:     print "----"
        ...:
        ...:
    ----
    India
    {'country': 'India', 'company': 'Flipkart'}
    {'country': 'India', 'company': 'Myntra'}
    {'country': 'India', 'company': 'Paytm'}
    ----
    ----
    USA
    {'country': 'USA', 'company': 'Apple'}
    {'country': 'USA', 'company': 'Facebook'}
    ----
    ----
    Japan
    {'country': 'Japan', 'company': 'Canon'}
    {'country': 'Japan', 'company': 'Pixela'}
    ----

If we only want to print company names, then we could do:

    In [22]: companies_grouped_by_country = itertools.groupby(companies, key=lambda each: each['country'])
    In [38]: for country_name, country_companies in companies_grouped_by_country:
        ...:     print "----"
        ...:     print country_name
        ...:     for company_detail in country_companies:
        ...:         print "--", company_detail['company']
        ...:     print "----"
        ...:
        ...:
    ----
    India
    -- Flipkart
    -- Myntra
    -- Paytm
    ----
    ----
    USA
    -- Apple
    -- Facebook
    ----
    ----
    Japan
    -- Canon
    -- Pixela

If you want to understand iterators in detail you should read our [previous post] on iterators (https://www.agiliq.com/blog/2017/10/iterators-and-iterables/).
