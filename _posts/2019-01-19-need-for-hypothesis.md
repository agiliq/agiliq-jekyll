---
layout: post
comments: true
title:  "Need for Hypothesis"
description: "Why is there a need for hypothesis in python application development?"
keywords: "Python, Hypothesis, Testing"
date:   2019-01-19
categories: [python, hypothesis, testing]
author: Santosh
---

### What is hypothesis?

Hypothesis is family of testing libraries which let you write tests parametrized by a source of examples. A Hypothesis implementation then generates simple and comprehensible examples that make your tests fail. This simplifies writing your tests and makes them more powerful at the same time, by letting software automate the boring bits and do them to a higher standard than a human would, freeing you to focus on the higher level test logic.

It is in short the testing tool. Tests in hypothesis are to make our lives easier in writing tests and also to write better tests.

As quoted by the author himself, "The purpose of hypothesis is to drag the world kicking and screaming into a new and terrifying age of high quality software"

### How to use hypothesis?

Hypothesis integrates into your normal testing workflow. Getting started is as simple as installing a library and writing some code using it - no new services to run, no new test runners to learn.

We can install it by,
```sh
pip install hypothesis
```

The main thing about hypothesis is *Strategy*. A strategy is a recipe for describing the sort of data you want to generate. Rather than having to hand-write generators for the data needed, we can just compose the ones hypothesis provides us with, to get the data in the required format

Ex: If we need a list of floats which are definitely a number and not infinite, we can use the strategy

```py
lists(floats(allow_nan=False, allow_infinity=False))
```

As well as it is easier to write, the resultant data will ususally have a distribution that is much better at finding edge cases than most of the heavily tuned maual implementations

Once we understand data generation for tests, the main entrypoint to Hypothesis is the `@given` decorator. It takes a function with some arguments as input & turns it into a normal test function.

This helps us to realize that hypothesis is not itself a test runner, but it runs alongside our testing framework and all it does is to expose a function of the appropriate name which the test runner picks up.

A simple example illustrating `@given` decorator (taken from hypothesis docs), 

```py
from hypothesis import given
from hypothesis.strategies import text

def encode(input_string):
    count = 1
    prev = ''
    lst = []
    for character in input_string:
        if character != prev:
            if prev:
                entry = (prev, count)
                lst.append(entry)
            count = 1
            prev = character
        else:
            count += 1
    entry = (character, count)
    lst.append(entry)
    return lst


def decode(lst):
    q = ''
    for character, count in lst:
        q += character * count
    return q

@given(text())
def test_decode_inverts_encode(s):
    assert decode(encode(s)) == s
```

In the function above we are trying to encode something and then decode it to get the same value back. We find a bug immediately,

![](/assets/images/hypothesis/test.png)

Hypothesis correctly points out that this code is simply wrong if called on an empty string.

If we wanted to make sure this example was always checked we could add it in explicitly by using the `@example` decorator i.e.

```py
@given(text())
@example('')
def test_decode_inverts_encode(s):
    assert decode(encode(s)) == s
```

This ensures to show what kinds of inputs are valid or to ensure that particular edge cases such as `""` are tested everytime.
Note that both `@example` and `@given` support keyword arguments as well as positional i.e.

```py
@given(s=text())
@example(s='')
def test_decode_inverts_encode(s):
    assert decode(encode(s)) == s
```

Once hypothesis finds an error with respect to a test after multiple test runs, it will continue to fail with the same example everytime. This is because Hypothesis has a local test database where it saves all the examples which failed. When we rerun the test, it will first try the previous failure. This is important because, even if at heart hypothesis is random testing, it is repeatable random testing, i.e. a bug will never go away by chance, because further tests will run only, if the previous failure no longer failed.


Ultimately hypothesis provides repeatability, reporting and simplification for randomized tests, and it provides a large library of generators to make it easier to write them.