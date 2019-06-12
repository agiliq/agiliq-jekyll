---
layout: post
comments: true
title: "Do npm packages work in browser or only in Node.js"
date: 2019-01-29 13:30:27+05:30
categories: npm, frontend, nodejs
author: Akshar
---

Some npm packages work in browser environment while others don't. It depends on how the package is written.

There are several npm packages which only work in browser context and don't work in Node.js environment.

While some other npm packages are written targetting Node.js and only work in Node.js environment. They do not work in browser context.

And there are several npm packages which work in both Node.js and browser context.

It all depends on how the package is written and what it's trying to achieve.

Let's see an example for each one of these.

### Only works with Node.js

There is an npm package called `colors`.

Install it:

    npm install colors

It is meant for Node.js environment. Try using it on Node.js repl.

    ╰─$ node
    > var colors = require('colors');
    undefined
    > console.log('hello'.green);
    hello
    undefined
    > console.log('i like cake and pies'.underline.red)
    i like cake and pies

This package's intention is to allow different colored logging for server environments. That's why it targets Node.js environment.

Trying to use it in an html file would fail with an **Uncaught ReferenceError**.

Use it in an index.html file.

    <script src="node_modules/colors/lib/colors.js"></script>

You would see a **colors.js:32 Uncaught ReferenceError: module is not defined at colors.js:32** on the browser console. npm package `colors` works with Node.js but not in browser.

### Works with browser as well as Node.js

npm `jquery` works with browser as well as Node.js.

Install it:

    npm install jquery

jQuery can now be used in any webpage, say index.html, by including it:

    <script src="node_modules/jquery/dist/jquery.js"></script>

You should be able to do DOM manipulation using $.

It can be used in Node.js environment too. Try using it on Node.js repl.

    ╰─$ node
    > var jQ = require('jQuery')

No error was raised in repl which confirms that it can be used in Node.js too.

### Only works in browser

npm `angular` package targets browser environment and isn't meant for Node.js environment.

Install it:

    npm install angular

AngularJS can now be used in any webpage, say index.html, by including it:

    <script src="node_modules/angular/angular.js"></script>

But trying to use it in a Node.js environment will raise an error. Start a node repl:

    ╰─$ node
    > require('angular')
    ReferenceError: window is not defined
        at Object.<anonymous> (/Users/akshar/Play/Vue/jquery-example/node_modules/angular/angular.js:36403:4)
        at Module._compile (internal/modules/cjs/loader.js:721:30)
        at Object.Module._extensions..js (internal/modules/cjs/loader.js:732:10)
        at Module.load (internal/modules/cjs/loader.js:620:32)
        at tryModuleLoad (internal/modules/cjs/loader.js:560:12)
        at Function.Module._load (internal/modules/cjs/loader.js:552:3)
        at Module.require (internal/modules/cjs/loader.js:657:17)
        at require (internal/modules/cjs/helpers.js:22:18)
    >

This package intention's is to make frontend development, DOM manipulation, data binding etc. easier. This package doesn't make sense in server environment. That's why it's written in such a way as to support only browser environment and not Node.js.
