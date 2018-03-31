---
layout: default
comments: true
title:  "Understanding python magic methods by reading Django queryset source code."
date:   2018-01-21 19:41:32+05:30
categories: [python, django, tutorial]
author: shabda
---

Django querysets are amazing. We use them everyday, but rarely think about the wonderful APIs they give us. Just some of the amazing properties which queysets have

- You can get a slice `queryset[i:j]` out of them, only the needed objects are pulled from DB.
- You can lookup a specifc object `queryset[i]`, only the required object is pulled from DB.
- You can iterate over them, `for user in users_queryset`, as if they were a list.
- You can `AND` or `OR` them and they apply the criteria at the SQL level.
- You can use them like a boolean, `if users_queryset: users_queryset.update(first_name="Batman")`
- You can pickle and unpickle them, even when the indivdual istances may not be.
- You can get a useful representation of the queryset in python cli, or ipython. Even if the queryset consists of 1000s of records, only first 20 records will be printed and shown.

Querysets get all of these properties by implemnting the Python magic methods, aka the dunder methods. So why do you need these magic, dunder methods? **Because they make the api much cleaned to use.**

It is much more intutive to say, `if users_queryset: users_queryset.do_something()` than `if users_queryset.as_boolean: users_queryset.do_something()`. It is more intutive to say `queryset_1 & queryset_2` rather than `queryse_1.do_and(queryset_2)`

Magic methods are metods implemented by classes which have a special meaning to the Python interpretor. They always start with a `__` and are sometimes called *dunder* method. (Dunder == double underscore).

Query and related classes implement the following methods to get the properies we listed above.

- `__getitem__`: For `queryset[i:j]` and `queryset[i]`
- `__iter__` for `for user in users_queryset`
- `__and__` and `__or__` for `queryset_1 & queryset_2` and `queryset_1 | queryset_2`
- `__bool__` to use them like a boolean
- `__getstate__` and `__setstate__` to pickle and unpickle them
- `__repr__` to get a useful representation and to limit the DB hit

We will look at how Django 2.0 does it.

### Implemnting `__getitem__`

The code looks like this:

``` python
    def __getitem__(self, k):
        """Retrieve an item or slice from the set of results."""
        if not isinstance(k, (int, slice)):
            raise TypeError
        assert ((not isinstance(k, slice) and (k >= 0)) or
                (isinstance(k, slice) and (k.start is None or k.start >= 0) and
                 (k.stop is None or k.stop >= 0))), \
            "Negative indexing is not supported."

        if self._result_cache is not None:
            return self._result_cache[k]

        if isinstance(k, slice):
            qs = self._chain()
            if k.start is not None:
                start = int(k.start)
            else:
                start = None
            if k.stop is not None:
                stop = int(k.stop)
            else:
                stop = None
            qs.query.set_limits(start, stop)
            return list(qs)[::k.step] if k.step else qs
```

There is a lot going on here, but each `if` block is straightforward.

- In the first of block, we ensure slice has reaonable value.
- In second block, if `_result_cache` is filled, aka the queryset has been evaluated, we return the slice from the cache and skip hitting the db again.
- If the  `_result_cache` is not filled, we `qs.query.set_limits(start, stop)` which sets the limit and offset in sql.

### Implemnting `__iter__`

### Implemnting `__and__` and `__or__`
### Implemnting `__bool__`
### Implemnting `__getstate__` and `__setstate__`
### Implemnting `__repr__`
