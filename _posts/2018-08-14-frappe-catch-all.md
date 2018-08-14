---
layout: post
comments: true
title:  "Frappe website catch all"
description: "Adding fallback page in frappe"
keywords: "Frappe, Erpnext, Python"
date: 2018-08-14
categories: [python, frappe, erpnext]
author: Akshar
---

#### Goal

This post explains how we can serve a fallback page instead of serving the default 404 when path can't be resolved.

Frappe installation provides several routes by default. Some of them are `/about` `/contact`, `/newsletters` etc.

You might want your about page to be served when path provided by user cannot be resolved.

#### Setup

This post assumes that you have bench initialized and you are able to add a site to your frappe installation.

Let's add a site

    $ bench new-site foo.bar

#### Default behaviour

If you access `foo.bar:8000/some-random-url`, you would see a 404 page.

![](/assets/images/frappe-website-route-rules/website-catch-all-404.png)

#### Adding rules

There is a hookpoint called `website_catch_all` in hooks.py which allows setting a fallback path.

Create an app so that we have a hooks.py where we can add route.

    $ bench new-app meeting # You could use any app name
    $ bench --site foo.bar install-app meeting

Add a module level attribute `website_catch_all` in meeting/meeting/hooks.py

    website_catch_all = ['about']

This would ensure that the About page is served in case the url cannot be resolved to a valid path.

![](/assets/images/frappe-website-route-rules/website-catch-all.png)
![](/assets/images/frappe-website-route-rules/website-catch-all-2.png)
