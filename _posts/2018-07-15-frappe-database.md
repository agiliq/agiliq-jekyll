---
layout: post
comments: true
title:  "Frappe Database api"
description: "How to use Frappe database api"
keywords: "Frappe, ERPNext, Python"
date:   2018-07-15
categories: [python, django, frappe]
author: Akshar
---

Frappe provides a database api using which you can communicate with the underlying database of your site. In this post we will try different frappe database methods from the python shell.

### Start shell

You can start a python shell by issuing the following command:

    bench --site <site_name> console

My site name is my.second. I issued the following command

    bench --site my.second console

Import the global `frappe` variable.

    In [1]: import frappe

`frappe` has several attributes. The attribute which encapsulates database connection and is used to communicate with the database is `frappe.db`.

Any default installation of frappe has a doctype called `User` which stores user details like username, first_name, email etc. This is the table which stores `Administrator` detail which is created when you run `frappe init <site_name>`.

### Count

Let's get a count of `User` in the database.

    In [2]: frappe.db.count('User')
    Out[2]: 3

Add few Users using `/desk#List/User/List` and get the count again.

    In [3]: frappe.db.count('User')
    Out[3]: 5

You can add filter conditions too in `count`.

    In [4]: frappe.db.count('User', filters={'email': 'david.beckham@gmail.com'})
    Out[4]: 1

    In [7]: frappe.db.count('User', filters={'email': ('like', 'david%')})
    Out[7]: 2

    In [8]: frappe.db.count('User', filters={'email': ('in', ['david.beckham@gmail.com', 'david.guetta@gmail.com'])})
    Out[8]: 2


### get_values()

You can get all users using following query.

    In [39]: users = frappe.db.get_values("User", filters={})

    In [40]: users
    Out[40]:
    ((u'Administrator',),
     (u'david.guetta@gmail.com',),
     (u'david.beckham@gmail.com',),
     (u'Guest',),
     (u'raaj.akshar+mysecond@gmail.com',))

You can get name and email for all users using following query.

    In [41]: users = frappe.db.get_values("User", filters={}, fieldname=["name", "email"])

    In [42]: users
    Out[42]:
    ((u'Administrator', u'admin@example.com'),
     (u'raaj.akshar+mysecond@gmail.com', u'raaj.akshar+mysecond@gmail.com'))

Get it as a dict using:

    In [43]: users = frappe.db.get_values("User", filters={}, fieldname=["name", "email"], as_dict=True)

    In [44]: users
    Out[44]:
    [{u'email': u'admin@example.com', u'name': u'Administrator'},
     {u'email': u'raaj.akshar+mysecond@gmail.com',
      u'name': u'raaj.akshar+mysecond@gmail.com'}]


### Ordering

You can order the results by passing kwarg `order_by` to `get_values()`.

    In [45]: users = frappe.db.get_values("User", filters={}, fieldname=["name", "email"], as_dict=True, order_by='creation')

    In [46]: users
    Out[46]:
    [{u'email': u'raaj.akshar+mysecond@gmail.com',
      u'name': u'raaj.akshar+mysecond@gmail.com'},
     {u'email': u'admin@example.com', u'name': u'Administrator'}]

You can order in descending order using `<column_name> desc`.

    In [47]: users = frappe.db.get_values("User", filters={}, fieldname=["name", "email"], as_dict=True, order_by='creation desc')

    In [48]: users
    Out[48]:
     [{u'email': u'admin@example.com', u'name': u'Administrator'},
     {u'email': u'raaj.akshar+mysecond@gmail.com',
      u'name': u'raaj.akshar+mysecond@gmail.com'}]

### Getting a single row

You can retrieve a single row from db using method `get_value()`.

    In [61]: user = frappe.db.get_value("User", filters={"name": "Administrator"}, fieldname="*")

    In [62]: user
    Out[62]:
    {u'_assign': None,
     u'_comments': None,
     u'_liked_by': None,
     u'_user_tags': None,
     u'background_image': None,
     u'background_style': u'Fill Screen',
     .....
     .....
     u'email': u'admin@example.com',
     u'email_signature': None,
     u'enabled': 1,
     u'first_name': u'Administrator',
     u'full_name': u'Administrator'}

If there is no row which matches the filter criteria then `get_value()` would return None.

    user = frappe.db.get_value("User", filters={"name": "jhhooreqereee"}, fieldname="*")
    In [65]: print(user)
    None

If you are filtering by `name` column, then you can send `filters` kwarg as a string instead of as a dictionary.

    In [66]: user = frappe.db.get_value("User", filters="Administrator")

Infact you can send it as an arg and not as a kwarg.

    In [66]: user = frappe.db.get_value("User", "Administrator")

There is even a shorter way of achieving the above result. If you want all the fields of the document and are filtering by name, then you don't need to use `get_value()`. You can use `get()` in such cases.

    In [67]: user = frappe.db.get("User", "Administrator")

### Raw query

You can run raw sql queries too with frappe.

Get username for all users.

    In [9]: users = frappe.db.sql("select name from tabUser");

    In [10]: users
    Out[10]:
    ((u'raaj.akshar+mysecond@gmail.com',),
     (u'Guest',),
     (u'Administrator',),
     (u'david.beckham@gmail.com',),
     (u'david.guetta@gmail.com',))

You can get the results as a dictionary where each table column would be mapped to the corresponding value.

    In [13]: users = frappe.db.sql("select name, email from tabUser", as_dict=True);

    In [14]: users
    Out[14]:
    [{u'email': u'admin@example.com', u'name': u'Administrator'},
     {u'email': u'raaj.akshar+mysecond@gmail.com',
      u'name': u'raaj.akshar+mysecond@gmail.com'}]

Or you can get the results as a list and not as a dict. In this case every db row would be returned as a list.

    In [15]: users = frappe.db.sql("select name, email from tabUser", as_list=True);

    In [16]: users
    Out[16]:
    [[u'Administrator', u'admin@example.com'],
     [u'raaj.akshar+mysecond@gmail.com', u'raaj.akshar+mysecond@gmail.com']]

You can do joins in frappe.db.sql(). Default Frappe installation creates a User table called `tabUser` and Language table called `tabLanguage`. User has a link field to Language. If we want to find language_code for language associated with each user we can do in following way.

    In [35]: users = frappe.db.sql("select u.name, l.language_code from tabUser as u inner join tabLanguage as l on u.language=l.name", as_dict=True);

    In [36]: users
    Out[36]:
    [{u'language_code': u'en', u'name': u'david.beckham@gmail.com'},
     {u'language_code': u'en', u'name': u'david.guetta@gmail.com'},
     {u'language_code': u'en', u'name': u'raaj.akshar+mysecond@gmail.com'}]

With frappe.db.sql you can essentially do anything you are allowed to do with plain sql.
