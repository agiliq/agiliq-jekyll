---
layout: post
comments: true
title:  "Frappe website route rules"
description: "Adding website routes in frappe"
keywords: "Frappe, Erpnext, Python"
date: 2018-08-08
categories: [python, frappe, erpnext]
author: Akshar
---

#### Goal

This post explains how we can add routes which resolve to a webpage.

Frappe installation provides several routes by default. Some of them are `/about` `/contact`, `/newsletters` etc.

You might want your about page to be served from `/about-us` and not only from `/about`. Similarly you might want your contact page to be served fromm `/contact-us` and not only from `/contact`.

#### Setup

This post assumes that you have bench initialized and you are able to add a site to your frappe installation.

Let's add a site

    $ bench new-site foo.bar

#### Default behaviour

If you access `foo.bar:8000/contact-us`, you would see a 404 page.

![](/assets/images/frappe-website-route-rules/404.png)

#### Adding rules

There is a hookpoint called `website_route_rules` in hooks.py which allows adding route rules.

Create an app so that we have a hooks.py where we can add route.

    $ bench new-app meeting # You could use any app name
    $ bench --site foo.bar install-app meeting

Add a module level attribute `website_route_rules` in meeting/meeting/hooks.py

    website_route_rules = [
      {'from_route': '/about-us', 'to_route': 'about'},
      {'from_route': '/contact-us', 'to_route': 'contact'},
    ]

This would ensure that the About page which is otherwise only accessible from `/about` is not also accessible from `/about-us`. Similarly Contact page is served from both `/contact` and `/contact-us`.

![](/assets/images/frappe-website-route-rules/about-us.png)
![](/assets/images/frappe-website-route-rules/contact-us.png)
