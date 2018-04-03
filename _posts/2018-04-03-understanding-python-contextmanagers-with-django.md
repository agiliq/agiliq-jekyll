---
layout: default
comments: true
title:  "Understanding Python contextmanagers by reading Django source code"
date:   2018-04-03
categories: [python, django, tutorial, django-internals]
author: shabda
---

Django comes with a bunch of useful context managers. The three I use most

- `transactions.atomic` - To get a atomic transaction block
- `TestCase.settings` - To change settings during a test run
- `connection.cursor` - TO get a raw cursor

`connection.cursor` Is gereally implemnted in the actual DB backends such a psycopg2, so we will focus on `transactions.atomic`, `TestCase.settings` and a few other contextmanagers.

### So what are context managers?

Context managers are a code patterns for

- Step 1: Do something
- Step 2: Do something else
- Step 3: Final step, *this step must be guaranteed to run*.








