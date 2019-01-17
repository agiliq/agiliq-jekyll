---
layout: post
comments: true
title:  "Basics of Node.js"
date:   2019-01-18 11:30:27+05:30
categories: django
author: akshar
---

### Basics

This post assumes a proper installation of Node.js.

Node.js is essentially JavaScript execution environment with some added features.

Any JavaScript which executes properly in Chrome would execute in Node.js environment too. In addition, Node.js provides ways to do I/O, connect to database, manage processes etc.

Browser JavaScript has limitations like not being able to do I/O, interface with databases etc. Node.js essentially provides a general purpose programming environment which works outside of browser and which can overcome the browser limitations.

#### Basic Node.js setup

This post assumes that you have Node.js and npm installed.

Create a directory named `getting-started` and `cd` to it.

    mkdir getting-started
    cd getting-started

Create a file index.js with following content:

    console.log('In index');

Run this file with Node.

    node index.js

You should see the output:

    In index

Any valid JavaScript can be put in index.js. Let's say:

    var fruits = ['Apple', 'Banana', 'Orange'];

    for (var i=0; i<fruits.length; i++) {
        console.log(fruits[i]);
    }

Execute this file with Node again.

    node index.js

You should see the fruits printed.

Node.js also provides a repl. Just type `node` in your terminal and try some valid JavaScript statements. eg: Adding two numbers.

    ╰─$ node
    > 1 + 2
    3
    > var a = 3;
    undefined
    > a = 5;
    5
    > console.log(a)
    5
    undefined
    > const c = 7;
    undefined
    > console.log(7)
    7

### Difference from JavaScript

Node.js has some additional things from JavaScript. Let's see some valid Node.js which wouldn't execute in a browserr, and hence is invalid in a browser context.

Node.js provides a special attribute called `exports`.

Similarly, Node.js provides a special function called `require`. `require` provides same feature as `Python import` or `Ruby require` or `Java import`. Let's see `exports` and `require` in action.

Add a file called `lib/util.js`. Directory `lib` should be created in your working directory, i.e `getting-started`. Add following content to `lib/util.js`

    exports.name = 'John Doe';

Start interactive `node` on console and do the following:

    ╰─$ node
    > const UTIL = require('./lib/util.js')
    undefined
    > console.log(UTIL)
    { name: 'John Doe' }

`exports` can be used in any .js file which would be used in Node.js context. It is used to expose **objects** or **functions** which can be imported by other Node.js files.

We started an interactive node repl and imported `lib/util.js` exposed attributes using `require`.

Try to use `exports` or `require` in a Chrome console and you would see a `ReferenceError`.

This example shows that Node.js provides features extra from a traditional browser context JavaScript features.

You can also import, or more correctly `require`, util.js in index.js instead of trying things on repl. Modify content of index.js to:

    const UTIL = require('./lib/util.js')
    console.log(UTIL['name']);

Run index.js

    node index.js
