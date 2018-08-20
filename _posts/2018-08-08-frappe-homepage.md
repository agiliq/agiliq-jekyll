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

This post explains how we can set homepage in a erpnext/frappe installation.

Default frappe installation doesn't provide a homepage. You can create and set a homepage in several ways as described below:

#### Setup

This post assumes that you have a Frappe project initialized and you are able to add a site to your frappe installation.

Let's add a site

    $ bench new-site foo.bar

Let's create an app and install it in the site foo.bar.

    $ bench new-app meeting
    $ bench --site foo.bar install-app meeting

#### Default behaviour

If you are logged in as an administrator and access the homepage i.e `foo.bar:8002`, you would be redirected to the desk environment.

![](/assets/images/frappe-homepage/admin-homepage.png)

If you aren't logged in as administrator, i.e for a Guest visitor, accessing homepage redirects to login page.

![](/assets/images/frappe-homepage/guest-login.png)

We want to change this behaviour and instead of redirecting to login page we want to show some content.

There are several alternatives provided by frappe to add a homepage. They are:

* Using `Website Settings`
* Using `home_page` attribute of hooks.py
* Using `get_website_user_home_page` attribute of hooks.py
* Using `role_home_page` attribute of hooks.py

#### Using **Website Settings**

Homepage can be set using `Home Page` field of `Website Settings`.

You can set it to any valid route of your project. There are some routes provided by default in any Frappe installation. eg: `about` and `contact`.

Access path `/about` and you should be able to see a page.

![](/assets/images/frappe/default-about.png)

You can set `about` as homepage of your application in the following way:

![](/assets/images/frappe/set-about-as-homepage.png)

Clear cache and reload the homepage, and your about page content should show on homepage.

![](/assets/images/frappe/about-as-homepage.png)

You can create a Web Page from the desk and set it as the homepage instead. You can learn about creating Web Pages from our [other post](https://www.agiliq.com/blog/2018/08/frappe-static-webpages/).

Assuming you have created a Webpage with route `what-we-do` which looks like:

![](/assets/images/frappe/webpage-what-we-do.png)

You can set `what-we-do` as homepage of your application in the following way:

![](/assets/images/frappe/set-what-we-do-as-homepage.png)

Clear cache and reload the homepage, and your about page content should show on homepage.

![](/assets/images/frappe/what-we-do-as-homepage.png)

You can set a custom webview added in www/ as your homepage too.

Assume we have a web view at `meeting/www/custom-homepage.html` with associated controller at `meeting/www/custom_homepage.py`. Read our [last post](https://www.agiliq.com/blog/2018/07/frappe-web-pages/) to understand web view in detail.

Content of meeting/www/custom-homepage.html could be:

    {% raw %}
    {{body}}
    {% endraw %}

Content of meeting/www/custom_homepage.py could be:

    def get_context(context):
        context['body'] = 'This is a custom homepage'

Set `Home Page` of `Website Settings` to `custom-homepage`.

Clear cache and reload the homepage. It should show content of web view `custom-homepage`.

![](/assets/images/frappe-homepage/custom-homepage.png)

#### Using **home_page** attribute

You can set homepage using `home_page` variable of hooks. This takes precedence over Website Settings homepage.

Edit `meeting/hooks.py` and add module level attribute `home_page`.

    home_page = "about"

Clear cache and load the homepage. It should show content of about page on homepage now.

![](/assets/images/frappe-homepage/guest-homepage.png)

As with `Website Settings` `Home Page`, you can point `home_page` hook to a www/ webview too.

Edit `home_page` attribute of `meeting/hooks.py` to point to this web view route.

    home_page = "custom-homepage"

Clear cache and load the homepage. It should show content of web view `custom-homepage`.

![](/assets/images/frappe-homepage/custom-homepage.png)

