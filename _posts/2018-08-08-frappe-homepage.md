---
layout: post
comments: true
title:  "Frappe and Erpnext homepage"
description: "Customizing frappe/erpnext homepage"
keywords: "Frappe, Erpnext, Python"
date: 2018-08-08
categories: [python, frappe, erpnext]
author: Akshar
---

#### Goal

This post explains how we can add and customize homepage for a erpnext/frappe installation. By homepage, I mean the page which shows up when "foo.bar/" is accessed.

Default frappe installation doesn't provide a homepage. You might want to show a homepage for visitors of your frappe powered website. You can achieve it in several ways as described below:

#### Setup

This post assumes that you have bench initialized and you are able to add a site to your frappe installation.

Let's add a site

    $ bench new-site foo.bar

Let's create an app and install it in the site foo.bar.

    $ bench new-app meeting
    $ bench --site foo.bar install-app meeting

#### Default behaviour

If you are logged in as an administrator and access `foo.bar:8002`, you would be redirected to the desk environment.

![](/assets/images/frappe-homepage/admin-homepage.png)

But if you aren't logged in as administrator, i.e for a Guest visitor, accessing `foo.bar` redirects to login page. We want to change this behaviour and instead of redirecting to login page we want to show some content.

![](/assets/images/frappe-homepage/guest-login.png)

There are several hook points provided by frappe to add a homepage. They are:

* Using `home_page` attribute of hooks.py
* Using `Website Settings`
* Using `get_website_user_home_page` attribute of hooks.py
* Using `role_home_page` attribute of hooks.py

#### Using **home_page** attribute

Frappe provides a basic `About Us` page by default which can be accessed at `/about`.

![](/assets/images/frappe-homepage/about.png)

Frappe allows customizing this page which we will see later. For now, this basic page would suffice.

Suppose you don't want to spend too much time setting up the homepage and just want to show the about page when someone accesses homepage.

Edit `meeting/hooks.py` and add module level attribute `home_page`.

    home_page = "about"

Clear cache and load the homepage, i.e `foo.bar:8002`. It should show content of about page on homepage now.

![](/assets/images/frappe-homepage/guest-homepage.png)

You can point `home_page` hook to a web view too. Assume we have a web view at `meeting/www/custom-homepage.html` with associated controller at `meeting/www/custom_homepage.py`. Read our [last post](https://www.agiliq.com/blog/2018/07/frappe-web-pages/) to understand web view in detail.

Content of meeting/www/custom-homepage.html could be:

    \{\{body\}\}

Content of meeting/www/custom_homepage.py could be:

    def get_context(context):
        context['body'] = 'This is a custom homepage'

Edit `home_page` attribute of `meeting/hooks.py` to point to this web view route.

    home_page = "custom-homepage"

Clear cache and load the homepage, i.e `foo.bar:8002`. It should show content of web view `custom-homepage`.

![](/assets/images/frappe-homepage/custom-homepage.png)

#### Using **Website Settings**

Homepage can be set using `Home Page` field of `Website Settings` too. Comment `home_page` of hooks.py so that it's not in effect anymore. Add Home Page in Website Settings.

![](/assets/images/frappe-homepage/website-settings.png)

Load the homepage.

Remove `custom-homepage` from website settings and instead use `about`.

![](/assets/images/frappe-homepage/website-settings-about.png)

Reload the homepage and content of about us page should show up on homepage.
