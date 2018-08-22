---
layout: post
comments: true
title:  "How web pages get styled in Frappe/ERPNext"
description: "Understanding what happens under the hood during webpage render"
keywords: "Frappe, ERPNext, Python"
date: 2018-08-21
categories: [python, erpnext, frappe]
author: Akshar
---

#### Goal

Any webpage added in Frappe or ERPNext gets a default bootstrap styling.

In this post we will understand what happens under the hood which styles this page without the desk user having to enter any style definition.

#### Setup

This post assumes that you have a frappe project initialized and you are able to add a site to your frappe installation.

Let's add a site

    $ bench new-site foo.bar


#### Create a web page

Let's create a `What we do` page.

If you want to understand creating webpages in detail and how to customise them, then read our [earlier post](https://www.agiliq.com/blog/2018/08/frappe-static-webpages/).

Navigate to the desk and under desk navigate to Tools > Website > Web Page > New.

![](/assets/images/frappe/add-static-webpage.png)

Let's add a 'What we do' page. Add the following things in the relevant fields.

![](/assets/images/frappe/static-what-we-do.png)

The fields we added are `Title`, `Route` and `Main Section`. We also checked `Published`.

Navigate to `/what-we-do` and you should be able to see the page.

![](/assets/images/frappe/what-we-do.png)

This page has a default bootstrap styling added without much effort from us.

##### Which style is applied to this page and where the stylesheets are

Any webpage that you add from desk gets it's html from `frappe/website/doctype/web_page/templates/web_page.html`.

There is a placeholder called `main_section` in web_page.html. Whatever `Main Section` we add for Web Page is inserted in the placeholder.

web_page.html ultimately extends from `frappe/templates/base.html`.

There are several templates included in base.html which work together to provide a particular layout for every webpage.

eg: base.html includes a template called `frappe/templates/includes/navbar/navbar.html`. This template uses a context variable called `top_bar_items` and renders the navbar.

Four stylesheets are added to base.html during rendering:

* assets/frappe/css/bootstrap.css
* Any theme specific bootstrap
* assets/css/frappe-web.css
* frappe/www/website_theme.css

Three among these stylesheets ensure that bootstrap styling is applied to the webpages.

The configurable stylesheet among the above 4 is `Any theme specific bootstrap`. This allows you to customise the look of your pages.

You can modify the styling of your webpages by adding a website theme or customizing the `Standard` theme which frappe provides by default.

##### Modifying `Standard` theme

Any Website theme has several fields which dictate how the webpage looks. eg: `Font Size`

You can set Font Size, Top Bar Color, Footer Text Color etc. from this page.

![](/assets/images/frappe/website-theme.png)

There is a field called `Style using CSS` in Website Theme form where you can add css rules which get applied throughout the site.

Let's set color #fafbfc for navbar and footer.

![](/assets/images/frappe/website-theme-style-using-css.png)

Refresh any webpage of your site to see the changes.
