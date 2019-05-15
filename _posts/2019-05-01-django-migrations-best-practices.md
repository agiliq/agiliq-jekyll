---
layout: post
comments: true
title:  "Opinionated guide to Django Migrations"
description: "Opinionated guide to Django Migrations"
keywords: "DB, Migration, Django, Python, API"
date: 2019-05-01
categories: [API, django, drf]
author: Shabda
---


## Opinionated guide to Django Migrations

Django migrations are a life saver. By automating Django schema management, they allow quick and explorative database engineering.

In long running Django projects, this can prove a double edged sword. 
Since migrations run as part of tests and old migrations stay in your repo as the schema evolves,
they can clutter your code base and make tests slow.

Below are my opioniated steps to keep your migrations managable in a long running Django project. 

- Use descriptive name for migration files
- Do not use Django migrations for data migrations
- A maximum of one migration per app per pull request
- Squash migrations aggressively
- Periodically reset migrations

Let's look at each of them.

### Always name migration files

When you run `python manage.py migrate`, 

Django will frequently give migrations names like `0028_auto_20170313_1712.py`. Always rename this to something like `0028_added_is_bear_flag.py`.
A descriptive name name for migration file is as important as descriptive name for variables. 

### Do not use Django migrations for data migrations

Django migrations allows creating data migrations. A one time data migration stays until squashed or removed. 
It is much easier to create a data migration as a django custom command, apply it using `manage.py command`. 
After the data migration is not needed, delete the command file.

### A maximum of one migration per app per pull request

If you use a git based, branch -> pull review -> merge based workflow, you might create multiple migrations for an app in a single PR.
They should be squashed before the pull request is merged to master, so that every app has at max one new migration.

It is easier to squash the latest migration on the branch than when they have been merged and there are migrations after this.

### Squash migrations aggressively

You should squash your migrations to reduce the number of new migration. 
The periodicty of squashing would depend on the team, but we have found good results with once every two sprints.

### Reset migrations periodically

Even with the steps identified above, sometimes the number of your migration files grow to be too unwieldy a number.
In such cases, it is advisable to delete all your migrations and create a new migrations with `manage.py migrate`.

Ideally this would lead to only one migration per app, 
but if you have circular dependecy, with a app A and app B both having `ForeignKey` to each other, you will get `CircularDependencyError`.

To fix, this comment out the `ForeignKey`s to break the cycle, then add them back one by one until every FK is added back.
With this done, you would have only a few migrations per app.
