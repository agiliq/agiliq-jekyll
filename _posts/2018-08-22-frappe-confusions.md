---
layout: post
comments: true
title:  "Frequent confusions of new Frappe/ERPNext developers"
description: "Answering confusions of beginner Frappe developers"
keywords: "Frappe, ERPNext, Python"
date:   2018-08-22
categories: [python, frappe, erpnext]
author: Akshar
---

I recently started with Frappe/ERPNext and initially struggled in few areas. Now I have a better grasp of things and I am putting my understanding of Frappe and related terminologies here:

I could categorize the confusion for a new developer into following questions:

* How is Frappe different from Erpnext.

* What is the difference between bench and frappe.

* What goes under the hood on bench init.

* How the virtual environment is managed.

* What happens when we do bench new-site.

* When frappe says it is multi-tenant, what does it mean.

* How routing works in Frappe/Erpnext.

* How /desk is rendered.

* How tables and columns are created and tracked without the end user writing any Python code.

### How is Frappe different from Erpnext?

Frappe is the framework using which Erpnext is built. You can think of Frappe as a framework and Erpnext is an application built using Frappe.

You could build another application called Erpnext-advanced using Frappe.

Erpnext is a set of modules. Different modules in erpnext are stock, crm, restaurant, healthcare, education and several others.

You could quickly build another application called Erpnext-advanced using Frappe. This app could have modules library, grocery, bag etc

### How is Frappe synonymous to other frameworks

Frappe is synonymous to Django while ERPNext is synonymous to Django admin.

Frappe is synonymous to Flask. ERPNext is synonymous to an app built using Flask. This app could have several routes where forms are rendered. These forms could allow doing CRUD.

### What is the difference between bench and frappe

Bench is a command line tool. It can be thought of as similar to ls, cp, mkdir etc.

Bench is used to initialize a Frappe project. It sets up different directories needed in a Frappe project. It enables interacting with a Frappe project once a project is initialized.

### What goes on under the hood on `bench init`?

`bench init <project-name>` initializes a Frappe project. bench init makes extensive use of Python's os module. bench init creates a lot of folders and files. It specifically does the following:

* Creates a directory/folder called `<project-name>`. Let's assume project-name is trpnext, so a folder called trpnext is created.
* Hereafter every folder or file is created under trpnext.
* Creates folders `apps`, `sites` etc.
* Creates a virtualenv directory called `env`.
* Installs needed packages in virtualenv. eg: `python-pdfkit` is intalled.
* Creates `trpnext/sites/common_site_config.json`
* Fetches `frappe` framework from github using `git clone` and installs it in virtualenv.
* Installs front-end packages using npm or yarn.
* Creates other needed files and folders for smooth functioning of project.

### How virtual environment is managed

I came to Frappe after using Django and Flask.

In Django and Flask projects, you are supposed to create a virtual environment, activate the virtual environments and then install Django or Flask inside that virtual environment. Essentially the project must be initialized inside a virtual environment to avoid polluting the global site packages.

Initialization of Frappe project doesn't expect you to create a virtualenv. So I was sceptical that it might be polluting my global site-packages. I was wrong!

`bench init` creates a virtual environment as written above. After running `bench init`, you should be able to find a directory called `env` inside your project root. This is your virtual environment.

Any packages installed for Frappe project goes under this virtual environment.

### What goes on under the hood on `bench new-site`

Any frappe project can have multiple sites. More on that later.

Every site of a frappe project has a database where tables and data for that particular site are stored.

`bench new-site` command does the following:

* Creates a database user and a database.
* Creates some tables needed for smooth operation of Frappe project. eg: It creates tables tabDocField, tabDocPerm, tabDocType etc.
* Other tables provided by Frappe framework, like user, blog_post, web_page, web_form, roles etc are created in the database.
* Some rows are inserted in user and roles table.

`bench new-site` essentially bootstraps a site. After this you would be able to add a doctype to this site which will create a database table under the hood.

### How installation of a package is different from installation of app on a site

In Frappe terminology, installation of app has a different meaning that conventional Python installation.

Conventional Python installation means `pip install` which installs the app in virtualenv.

Frappe installation means creation of an app's tables in the site's database.

`bench init` does `pip install frappe`. It installs frappe framework in project in conventional Python installation sense. But it hasn't yet installed frappe framework on a site in Frappe installation sense.

`bench new-site` creates a site and then installs frappe framework in this site in Frappe installation sense. This means that frappe tables are created in this site's database.

This will become more clear as we talk about `bench get-app`.

----

Answers for more questions are under progress and I will add them here soon. Please feel free to add more questions and I can answer them.
