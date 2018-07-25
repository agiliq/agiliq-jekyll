---
layout: post
comments: true
title:  "Web pages using Frappe"
description: "How to add a web page in a Frappe or Erpnext project"
keywords: "Frappe, Erpnext, Python"
date:   2018-07-25
categories: [python, django, frappe, erpnext]
author: Akshar
---

#### A little background

This post assumes that you have **bench** initialized and you are able to add a site to it.

Any erpnext installation has two user environments. They are:

* Desk View
* Web View

Quoting [Frappe docs](https://frappe.io/docs/user/en/tutorial/web-views)

    Frappe has two main user environments, the Desk and Web. Desk is a controlled UI environment with a rich AJAX application and the web is more traditional HTML templates served for public consumption. Web views can also be generated to create more controlled views for users who may login but still do not have access to the Desk.

Desk is only accessible to "System User". This is the environment used by System users to do CRUD, run reports and analyse data. This is not a customer facing part.

You might need customer facing views in your erpnext installation. This is where web views come handy.

Web views provide extreme flexibility and extensibility. You have unlimited control on the theme and layout of your web views. You can mix data from different database tables and show it in a single web view. You can restrict who has access to which web view and lots more.

Landing pages, homepages, and featured pages are good candidates for web view.

There are several ways in which web views can be created.

* Adding code in an app's www/ or templates/ folder.
* Using `hooks.website_route_rules`.
* Setting `Has web view` as True for a doctype.
* Using Printview and Listview for a doctype.

In this post we will discuss the first alternative which is "adding code in an app's www/ folder". We will discuss the other alternatives in our later posts.

#### Setup

Let's add a site

    $ bench new-site my.fourth

There is an app called `hub` on github. You can `get-app` and `install-app` on your site.

    $ bench get-app hub
    $ bench --site my.fourth install-app hub

#### Create a webpage

After installing `hub` you should be able to see directory `hub/hub/www/` in your `apps` folder.

Try to access url `/featured`(http://my.fourth:8003/featured), you would get a 404.

Add a file called featured.html in `hub/hub/www` with following content.

    Hub featured page

Navigate to `http://my.fourth:8003/featured`. You should see a page which looks like:

![](/assets/images/frappe-web-pages/basic-page.png)

As you should be able to figure out, basic bootstrap styling was added to your page. Frappe takes care of adding basic bootstrap styling if your html file only contains content and if it doesn't have `<body>` tag. Details on exact logic followed by Frappe templates later.

If you don't want any default frappe styling, then you can add your html content to have `<body>` tag.

    <html>
          <body>
              Hub featured page
          </body>
    <html>

Let's just keep the html content and let Frappe provide basic styling. Change content of featured.html back to:

    Hub featured page

You can provide `context` for this template by writing a file called `featured.py` in `hub/hub/www/`.

Add the following content in `featured.py`

    def get_context(context):
        context['custom_content'] = 'Hub featured page custom content'

Modify `featured.html` to look like:

    Hub featured page<br/>
    {{custom_content}}

Clear cache(cache can be cleared using `bench --site my.fourth clear-cache`) and reload your page. It should start looking like:

![](/assets/images/frappe-web-pages/page-with-context.png)

As you would have realised, `featured.html` is a Jinja template.

Every html template can have a corresponding controller which would provide the context for the template. In our last example, featured.py is the controller for featured.html.

If you want to have a route `/item-listing`, you should create a template called `item-listing.html` and a controller called `item_listing.py`. Frappe is smart enough to match the hyphen in template name with underscore in controller name.

Let's show name for all users on featured.html. Modify featured.py to look like:

    import frappe

    def get_context(context):
        context['users'] = frappe.get_all('User')

Modify featured.html to look like:

    <h2>Users<h2/>
    {% for user in users %}
        {{user.name}}<br/>
    {% endfor %}

Clear cache and reload your page and you should be able to see name of users.

You would have realized the extensibility of frappe templates by now. You can do anything allowed in Python in your `get_context()` and that would be available in your corresponding template.

If you also wanted to show names of all `Hub Item` in your featured page, you could change featured.py to:

    def get_context(context):
        context['users'] = frappe.get_all('User')
        context['hub_items'] = frappe.get_all('Hub Item')

Frappe web template use a look of hooks which you can use.
