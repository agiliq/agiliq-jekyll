---
layout: post
comments: true
title:  "Upgrading django apps from older versions to latest Django version"
date:   2018-04-12
categories: [python, django, version-upgrade]
author: Anjaneyulu
---
### Why to upgrade Django to a newer version ?

We can get several benefits from the newer version of the django. Upgrading to the newer version might be a complex process. But, It's always recommended to upgrade the Django applications to newer versions.

I recently upgraded a Django app we had on Django 1.6 to Django 1.11. We coudn't upgrade to Django 2.0, as there some dependencies with Python 2.7. Here are the things I found.

### Benefits with Django version upgrade
* Bugs are fixed
* Newer features are added
* Provided latest security measures
* Will get better community support. Most of the developers are upgrading their applications to newer versions. 

### Checklist to follow for django version upgrade
* Read every release note of django version which is greater than the current django version.
* Understand the changes of version release notes. You will get some idea about the features that will be deprecated and new features willl be added.
* After, upgrade the django to the next major release of version. Now, run the application and check for errors.
* If django application contains unit test cases then first run the tests to see if the version upgrade had any errors. In most of the cases unit tests will be failed due to version upgrade.
* If django application do not contain the unit tests then we need to manually check the each and every functionality to find the errors.
* In most of the cases python packages that we use may not support the new release.
* Upgrade all the python packages to the newer versions.
* If it doesn't have next release then we need to download it and upgrade the package to use it with our application or we need to look for other packages that can replace it.
* Fix the errors that you find while testing the django application.
* To get help search for the error on sites like Google, Stackoverflow and Github.
* After fixing the errors of the current version upgrade the django to next major version release and repeat the above process until the latest release of the django.


### Database changes and django migrations
* If we upgrade the django applications from versions before django==1.8 we might be using south package to manage the database related changes.
* In django==1.8 and later versions south is upgraded and included as a part of the django package to manage the database related changes effectively.
* "south" package creates database table "south_migrationhistory". we do not need it anymore we can drop the table.
* Delete all the migrations that were created by "south" in all applications and create new migrations with command
```python
python manage.py makemigrations <app_name>
```
* After creating the migrations when we try to apply with below command we get error like table already exists.
```python
python manage.py migrate <app_name>
```

* We get error because migration will tries to apply the database  operations like create table update table, etc. We already have the database schema with all the tables so, it raises the error.

* If we do not apply the migrations then it will be difficult for us to make database related changes in the future. So, to make it work we fake the migrations with below command.
```python
python manage.py migrate <app_name>  --fake
``` 

* Above command will create an entry in the "django_migrations" table. Next time when we make changes to django models(app tables) then it will lookup the "django_migrations" table and creates next migration based on the existed migration entries. So, the new migrations can be applied easily.


>Note: After upgrading the django application to the newer version. Do not directly deploy it on live server. Perform the regression testing on staging server and then deploy it on live server.
