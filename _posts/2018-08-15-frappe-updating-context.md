---
layout: post
comments: true
title:  "Updating Frappe webpage context"
description: "Different hookpoints to modify context"
keywords: "Frappe, Erpnext, Python"
date: 2018-08-15
categories: [python, frappe, erpnext]
author: Akshar
---

#### Goal

Any webpage served from an erpnext/frappe installation has an associated context which is used when the webpage is rendered.

This post explains how we can modify context available to webpages.

#### Setup

This post assumes that you have bench initialized and you are able to add a site to your frappe installation.

Let's add a site

    $ bench new-site foo.bar

Let's create an app so that we have a hooks.py where we can do any needed modify.

    $ bench new-app meeting # You could use any app name
    $ bench --site foo.bar install-app meeting

Let's add a web view which should respond at "/custom-homepage" and ensure that the web view is browsable. Refer to our [earlier post](https://www.agiliq.com/blog/2018/07/frappe-web-pages/) to understand web views in detail.

Content of meeting/www/custom-homepage.html:

    {% raw %}
    {{body}}
    {% endraw %}

Content of meeting/www/custom_homepage.py:

    def get_context(context):
        context['body'] = 'This is a custom homepage'

Ensure that you are able to navigate to '/custom-homepage'.

#### Hookpoints

You can add extra context apart from the default ones and controller addes ones by using the ollowing hook points:

* site_config.website_context
* hooks.website_context
* hooks.update_website_context

##### site_config website_context

Add a dictionary `website_context` to your site's site_config.json. Example

    {
     "db_name": "<db-name>",
     "db_password": "<db-password>",
     "developer_mode": 1,
     "dormant": true,
     "limits": {
      "space_usage": {
       "backup_size": 1.0,
       "database_size": 4.51,
       "files_size": 0.0,
       "total": 5.51
      }
     },
     "website_context": {
         "site_config_context_variable": "This is foo.bar!"
     }
    }

You should be able to use any key of dictionary website_context in your webpages after this. Modify custom_homepage.html to:

    {% raw %}
    Adding some site_config context variable too.<br/>
    {{body}}<br/>
    {{site_config_context_variable}}<br/>
    {% endraw %}

Refresh your page and it should look like:

![](/assets/images/frappe/site-config-website-context.png)

site_config website_context is the correct place to add context variables which cannot be added through website settings and which is needed on most of the pages. Good candidates for this could be, say, a tagline for the site which you want to show on all pages.

##### hooks website_context

Any app specific context should be added using hooks.website_context. Assume you write an erpnext app and want your name to appear in every webpage of this app in any erpnext instalation.

Add a dictionary `website_context` to meeting's hooks.py. Example

    website_context = {
      'footer': 'Agiliq Info Solutions'
    }

You don't need to make any change to custom-homepage.html because by default it extends from templates/base.html provided by Frappe. And base.html takes care of using footer context variable if present.

Clear cache and reload the page.

![](/assets/images/frappe/hooks-website-context.png)

hooks.website_context is the correct place to add any app specific context. Example: You want to show something on all the pages of your particular app.

##### hooks update_website_context

site_config.website_context and hooks.website_context come handy when you want to add a static value to the context. You cannot add dynamic values, say something read from db, using site_config.website_context and hooks.website_context.

Suppose you want the list of users to be available to all the webpages. Or you want to run some python function which generates a dynamic value, eg: current datetime, and want this dynamic value to be available in the context. You can achieve it using update_website_context.

update_website_context should be a list and each element of list should be the dotted notation of function.

Add the following to meeting/hooks.py

    update_website_context = [
      'meeting.www.custom_homepage.add_users_to_context'
    ]

Add a function called add_users_to_context() in meeting/www/custom_homepage.py

    def add_users_to_context(context):
        context['users'] = frappe.db.get_all('User')

Modify custom-homepage.html to have following 

    {% raw %}
    {{body}}<br/>
    {% for user in users %}
          <p>{{user.name}}</p>
    {% endfor %}
    {% endraw %}

Clear cache and reload the page.

![](/assets/images/frappe/hooks-update-website-context.png)

It should look like the image above.
