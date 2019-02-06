---
layout: post
comments: true
title:  "Updating Django from 1.x to 2.x"
description: "Updating the software application to latest releases is very important. Because latest releases always includes new features which boosts development process and resolves potential problems."
keywords: "Django version update, Django version upgrade"
date:   2019-02-04
categories: [django, version update, software update]
main_category: django
author: Anjaneyulu
---

Updating the software application to latest releases is very important. Because latest releases always includes new features which boosts development process and resolves potential problems.

### Why to update to from Django 1.x to 2.x ?
* <a href="https://docs.djangoproject.com/en/dev/releases/1.0/" target="__blank">Django 1.0</a> is first stable version so, it obvious that it contains less features.
* <a href="https://docs.djangoproject.com/en/dev/releases/1.1/" target="__blank">Django 1.1</a> ORM improvements
    * Aggregate support
        - It includes RDBMS agregate features `COUNT(), MAX(), MIN()`, etc 
    * Query expressions(i.e <a target="__blank" href="https://docs.djangoproject.com/en/dev/ref/models/expressions/#django.db.models.F">F object</a>)
        - `F` object is a new feature in ORM queries. By using `F` queries we can refer to another field on the query and can traverse relationships to refer to fields on related models.
    * Model Improvements
      * Added `managed` option in django model `Meta` class. if `managed=True` then ORM can make database changes like dropping, creating and updating the table structure/data.
      * Default value of `managed` is `True`
* <a href="https://docs.djangoproject.com/en/dev/releases/1.2/" target="__blank">Django 1.2</a> new features
    * Support for multiple database connections in a single Django instance.
    * Model validation before saving the data into the database(i.e data type, uniqueness of database table record, etc)
    * Improved protection against <a href="https://docs.djangoproject.com/en/dev/ref/csrf/" target="__blank">CSRF</a> attacks.
* <a href="https://docs.djangoproject.com/en/dev/releases/1.3/" target="__blank">Django 1.3</a> new features
    * Built-in support for writing class-based views using <a href="https://docs.djangoproject.com/en/dev/topics/class-based-views/generic-display/" target="__blank">generic views</a>.
    * Built-in support for python logging.
    * In previous versions of django it was common to place static assets in `MEDIA_ROOT` along with user-uploaded files, and serve them both at `MEDIA_URL`.
    * Static assets should now go in `static/` subdirectories of our apps or in other static assets directories listed in `STATICFILES_DIRS`, and will be served at `STATIC_URL`.
* <a href="https://docs.djangoproject.com/en/dev/releases/1.4/" target="__blank">Django 1.4</a> features & deprecations
    * Django 1.4 has dropped support for Python 2.4. Python 2.5 is the minimum required Python version.
    * The Biggest feature added in this version is support for timezones. Based on the <a href="https://docs.djangoproject.com/en/dev/topics/i18n/timezones/" target="__blank">timezones</a> datetime/date objects will be handled.
    * It supports integration with in-browser testing frameworks like <a href="https://selenium-python.readthedocs.io/" target="__blank">Selenium</a>.
    * <a href="https://docs.djangoproject.com/en/dev/topics/testing/tools/#django.test.LiveServerTestCase" target="__blank">`django.test.LiveServerTestCase`</a> base class allows us to test the interactions with front-end and back-end.
    * ORM improvements includes <a href="https://docs.djangoproject.com/en/dev/releases/1.4/#model-objects-bulk-create-in-the-orm" target="__blank">`bulk_create`</a> and <a href="https://docs.djangoproject.com/en/dev/releases/1.4/#queryset-prefetch-related" target="__blank">`prefetch_related`</a>(i.e batch-load related objects).

* <a href="https://docs.djangoproject.com/en/dev/releases/1.5/" target="__blank">Django 1.5</a> features
    * This release blasted with new feature <a href="https://docs.djangoproject.com/en/dev/topics/auth/customizing/#auth-custom-user" target="__blank">Configurable User model</a> where we can use our own user model.
    * It's also the first release that supports <a href="https://docs.python.org/3/" target="__blank">Python3</a>.
    * <a href="https://docs.djangoproject.com/en/dev/ref/contrib/gis/" target="__blank">GeoDjango</a> now supports <a href="https://postgis.net/docs/manual-2.0/" target="__blank">PostGIS 2.0</a>.
    * It provides better support for streaming responses with class `django.http.StreamingHttpResponse`.
* <a href="https://docs.djangoproject.com/en/dev/releases/1.6/" target="__blank">Django 1.6</a> features
    * It supports persistent database connections. This avoids the overhead of re-establishing a connection at the beginning of each request.
    * Database transaction management improved. Database-level autocommit is now turned on by default. This makes transaction handling more explicit and should improve performance.
    * It introduced a new test runner suit that allows more flexibility in the location of tests(i.e `django.test.runner.DiscoverRunner`). With test discovery, tests can be located in any module whose name matches the pattern `test*.py`.
    * A new `django.db.models.BinaryField` model field allows storage of raw binary data in the database.

* <a href="https://docs.djangoproject.com/en/dev/releases/1.7/" target="__blank">Django 1.7</a> features & deprecations
    * `syncdb` management command replaced with `migrate`
    * `django.db.models.signals.pre_syncdb` and `django.db.models.signals.post_syncdb` have been deprecated and replaced by `pre_migrate` and `post_migrate` respectively.
    * `django.utils.simplejson` is removed and we can use python's json module(i.e `import json`).
    * `HttpResponse`, `SimpleTemplateResponse`, `TemplateResponse`, `render_to_response()`, `index()`, and `sitemap()` no longer take a `mimetype` argument. It's been renamed to `content_type`.

* <a href="https://docs.djangoproject.com/en/dev/releases/1.8/" target="__blank">Django 1.8</a> features
    * It now supports multiple template engines like `Jinja2`, `django`, `Mako`, etc.
    * `django-secure` third-party library had been integrated into `Django` to improve the security.
    * `PostgreSQL` specific functionality like `ArrayField`, `HStoreField`, `IntegerRangeField`, `BigIntegerRangeField`, etc. fields support added.
    * Added ORM support for <a href="https://docs.djangoproject.com/en/dev/ref/models/expressions/" target="__blank">`Query Expressions`</a>, <a href="https://docs.djangoproject.com/en/dev/ref/models/conditional-expressions/" target="__blank">`Conditional Expressions`</a>, and <a href="https://docs.djangoproject.com/en/dev/ref/models/expressions/" target="__blank">`Database Functions`</a>.
    * Improved the unittest functionality.


* <a href="https://docs.djangoproject.com/en/dev/releases/1.9/" target="__blank">Django 1.9</a> features & deprecations
    * `AUTH_PASSWORD_VALIDATORS` setting added to help prevent the usage of weak passwords by users.
    * <a href="https://docs.djangoproject.com/en/2.1/topics/auth/default/#the-permissionrequiredmixin-mixin" target="__blank">Permission mixins</a> support added for generic class based views.
    * Implicit QuerySet `__in` lookup removed (i.e `Model.objects.filter(related_id__in=RelatedModel.objects.all())`)
    * Dropped support for PostgreSQL 9.0, Oracle 11.1

* <a href="https://docs.djangoproject.com/en/dev/releases/1.10/" target="__blank">Django 1.10</a> features
    * Enabled full text search for PostgreSQL database table columns
    * The User model in `django.contrib.auth` originally only accepted ASCII letters and numbers in usernames.

* <a href="https://docs.djangoproject.com/en/dev/releases/1.11/" target="__blank">Django 1.11</a> features & deprecations
    * The Django 1.11.x series is the last to support Python 2. The next major release, Django 2.0, will only support Python 3.4+
    * Database table indexes available in model meta class (i.e  `Meta.indexes`).
    * Template-based widget rendering support added.
    * Added support for Subquery expressions
```python
posts = Post.objects.filter(published_at__gte=one_day_ago)
Comment.objects.filter(post__in=Subquery(posts.values('pk')))
```
    * Dropped support for PostgreSQL 9.2 and PostGIS 2.0

* <a href="https://docs.djangoproject.com/en/dev/releases/2.0/" target="__blank">Django 2.0</a> features & deprecations
    * It only support's Python3.4+. It dropped support for Python<3.
    * It simplified the url routing syntax by introducing the <a href="https://docs.djangoproject.com/en/2.1/topics/http/urls/#registering-custom-path-converters" target="__blank">path converters</a>.
    * Responsive user interface feature for django admin.


### Check list to update projects from Django1.x to Django2.x?
* Check-out the version of the django on which the project is running.
* It's recommended to update the current version to it's next version (i.e django 1.x to django 1.x+1).
* Before updating the django version first we have to read it's release notes for what are the features deprecated and what are the features introduced.
* Find replacements for deprecated features.
* In most django projects we use many third party packages. So, we have to take care of them too.
* If any third party package is deprecated then first we have to check for alternatives to it. If any alternative is available then use it.
* If no alternative found then update the existing package and use it.
* Remove all unused third party packages.
* After satisfying the requirements(i.e system softwares and pip packages) run the tests.
* If any failures while running tests then fix them.
* Try to remove all unused code(i.e you can use <a href="https://pypi.org/project/coveralls/" target="__blank">test coverage</a>)
* Try to optimize the existing code by replacing it with new features wherever it's required to speedup the application.
* Try to optimize the existing ORM queries with new features of ORM to speedup the query execution.
* Try to use `path` and `path converters` to make urls more readable.