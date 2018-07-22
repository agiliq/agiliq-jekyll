---
layout: post
comments: true
title:  "Advanced Database queries in Frappe"
description: "Frappe queries involving joins, group by and order"
keywords: "Frappe, ERPNext, Python"
date:   2018-07-22
categories: [python, frappe]
author: Akshar
---

#### Goal

In this post we will see how we can accomplish `join` and `group by` using Frappe database api.

#### Setup

We have an app which has categories, items and reviews. There are multiple categories and each item will be of a particular category. Every item can have multiple reviews.

We will use doctypes `Hub Item` and `Hub Category` and `Hub Item Review` in our examples.

`Hub Item` has a `Link` field which points to `Hub Category`. `Hub Item` has a `Table` field which points to `Hub Item Review`.

Assuming `Hub Category` looks like the following:

    {
        "name": "Hub Category",
        "fields": [
            {
                "fieldname": "description",
                "fieldtype": "Text Editor"
            },
        ]
    }

Assuming `Hub Item` looks like the following:

    {
        "name": "Hub Item",
        "fields": [
            {
                "fieldname": "hub_category",
                "fieldtype": "Link",
                "options": "Hub Category"
            },
            {
                "fieldname": "reviews",
                "fieldtype": "Table",
                "options": "Hub Item Review"
            },
        ]
    }


We want to accomplish the followings:

#### Get **child table** rows for `Hub Item`s using single query

Assuming we have an index page in our website where we want to show 20 Hub Items.

The query for that would be:

    In [1]: items = frappe.get_all("Hub Item", start=0, page_length=20, fields="name, hub_category", order_by='creation desc')

Suppose we also want to show several reviews for each of the twenty items. Making a db call for each `Hub Item` to get its reviews would lead to 20 db calls which would be highly inefficient.

The performant and efficient way would be to **join** `Hub Item` and `Hub Item Review`. `frappe.get_all()` is capable of performing `join` provided we satisfy some conditions.

We need to ask for child table attributes in the `fields` kwarg of `get_all()`.

    In [2]: items_with_reviews = frappe.get_all("Hub Item", fields="`tabHub Item`.name, `tabHub Item`.hub_category, `tabHub Item Review`.content")

Doctype `Hub Item Review` is stored in table `tabHub Item Review` under the hood. In above query, we have mentioned `tabHub Item Review` in fields. This gives a cue to `frappe.get_all()` that join is needed here between parent doctype `Hub item` and child doctype `Hub Item Review`.

The rows of items_with_reviews would look like:

    In [3]: items_with_reviews[1]
    Out[3]:
    {u'content': u'Now username attribute would be set on reviews.',
     u'hub_category': 'Bags',
     u'name': u'002-002-08778'}

    In [4]: items_with_reviews[2]
    Out[4]: {u'content': u'This is an awesome product too.', u'hub_category': 'Bags', u'name': u'002-002-08778'}

    In [5]: items_with_reviews[3]
    Out[5]: {u'content': u'This is a good product too.', u'hub_category': 'Bags', u'name': u'002-002-08778'}

It is your responsibility to group all reviews for a particular item into say a single list and assign it to item.

You can see the query which is executed if you pass `debug=True` to `get_all()`.

    In [6]: items_with_reviews = frappe.get_all("Hub Item", fields="`tabHub Item`.name, `tabHub Item Review`.content", debug=True)

The logged query would look like:

    select `tabHub Item`.name, `tabHub Item Review`.content from `tabHub Item` left join `tabHub Item Review` on (`tabHub Item Review`.parent = `tabHub Item`.name) order by `tabHub Item`.`modified` DESC

We can get reviews for most recent 20 items by executing:

    In [7]: items = frappe.get_all("Hub Item", fields="`tabHub Item`.name, `tabHub Item`.hub_category", start=0, page_length=20)
    In [8]: item_names = [item['name'] for item in items]
    In [9]: item_with_reviews = frappe.get_all("Hub Item", fields="`tabHub Item`.name, `tabHub Item Review`.content", filters={"name": ("IN", item_names)})

#### Get count of **child table** rows for each Document

Suppose we want to get count of reviews for each `Hub Item` in a single query.

At database level we want to work with Item table as well as Review table. So we need to give a cue to `get_list()` to perform a join. The following query would do the trick:

    In [10]: items_with_reviews_count = frappe.get_list("Hub Item", fields="`tabHub Item`.name, `tabHub Item Review`.parent, count(`tabHub Item Review`.content) as cnt", group_by="`tabHub Item`.name")

    In [10]: items_with_reviews_count[0]
    Out[10]: {u'cnt': 4, u'name': u'iPhone', u'parent': u'iPhone'}

We can find items annotated with number of reviews in descending order by doing:

    In [11]: items_with_reviews_count = frappe.get_list("Hub Item", fields="`tabHub Item`.name, `tabHub Item Review`.parent, count(`tabHub Item Review`.content) as cnt", group_by="`tabHub Item`.name", order_by="cnt desc")

    In [12]: items_with_reviews_count[0]
    Out[12]: {u'cnt': 6, u'name': u'002-002-08778', u'parent': u'002-002-08778'}


#### Getting an attribute of Link field

By default, our queries only give us the `name` field of the `Link` Document.

Assuming we have an index page in our website where we want to show 20 Hub Items.

The query for that would be:

    items = frappe.get_all("Hub Item", start=0, page_length=20, fields="name, hub_category", order_by='creation desc')

You can get the hub_category for an item by doing:

    print(items[0].hub_category)

Suppose we wanted to show description of each associated category along with the item too. Something like `items[0].hub_category_description`. In such case we need a join between Hub Item and Hub Category.

Frappe database api doesn't provide a straightforward method for this. You need to write raw sql query to achieve this.

    items = frappe.db.sql("select i.name, i.hub_category, c.description as hub_category_description from `tabHub Item` as i left join `tabHub Category` as c on i.hub_category=c.name order by i.creation desc limit 0, 20", as_dict=True)
