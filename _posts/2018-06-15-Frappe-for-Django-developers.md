---
layout: post
comments: true
title:  "Frappe for Django developers"
description: "Comparing Frappe commands to Django - A Frappe tutorial for Django devs"
keywords: "Frappe, Django, Python"
date:   2018-06-15
categories: [python, django, frappe]
author: Akshar
---


This post is part 1 of Frappe for Django developers tutorials. It compares various Frappe commands with Django commands.

### What is Frappe Web Framework

Frappe is a web framework similar to Django.

Frappe applications are managed by a tool called `bench`. This post assumes that bench is installed. You can install bench from <a href="https://github.com/frappe/frappe/wiki/The-Hitchhiker's-Guide-to-Installing-Frapp%C3%A9-on-Mac-OS-X" target="_blank">here</a>.

Bench is Frappe manager. It is analogous to django-admin and manage.py.


### Frappe vs Django commands


You can start a frappe `project` using:

    bench init frappe-bench

Similar behaviour in Django is achieved using:

    django-admin startproject django-project

The next step after `bench init` is adding a site to the `bench`. It can be done by issuing the following command:

    bench new-site my.first

You will be prompted for your mariadb password which would look like

    MySQL root password:.

Enter your mariadb password so that database for this site can be created. In frappe a new database is created for every site created using `bench new-site`.

`bench new-site` would also create an administrative user in the database. Username for this user would be `Administrator` and bench would prompt you to set a password. It would look like

    Set Administrator password:.

Django doesn't have an analogous command as `bench new-site` because by default each Django installation works with a single site. You are expected to put database configuration in Django settings.py

Edit your `/etc/hosts` and add the following line:

    127.0.0.1   my.first

Start bench using following command:

    bench start

This is similar to Django's `runserver`:

    python manage.py runserver

You should be able to access your site at `http://my.first:8002` after issuing `bench start`. Navigating to this url will take you through a setup wizard. Once you complete the setup wizard, you would be redirected to `/desk`.

It should show you 3 tabs namely 'Tools', 'Email Inbox' and 'Explore'.

You can create a new app using:

    bench new-app meeting

Corresponding Django command for creating an app in a Django project is:

    python manage.py startapp myapp

You can install app `meeting` on site `my.second` using:

    bench --site my.second install-app meeting
    bench --site my.third install-app library_management

Since Django is a single site setup, so we don't have to add the app to the site.

Our next post in this series would focus on creating the <a href="https://docs.djangoproject.com/en/2.0/intro/tutorial01/" target="_blank'>Django poll application</a> using Frappe.
