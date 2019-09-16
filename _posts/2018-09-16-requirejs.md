---
layout: post
comments: true
title: "Getting started with require.js"
keywords: "requirejs, amd, javascript"
date: 2018-09-16 12:30:27+05:30
categories: frontend, javascript
author: Akshar
---

## Agenda

This post discusses why traditonal approach of having all scripts in index.html is substandard and how it should be addressed using require.js

Traditionally all the needed scripts were part of index.html. Developers manually ensured that the script ordering is maintained in such a way that a needed script is loaded before a dependent script.

## Setup

Let's first setup a project which follows the traditional approach.

We have an index.html file which uses four scripts. Let's define the scripts first.

scripts/app/one.js

    const sayOne = function () {
        console.log("saying one");
    };

scripts/app/two.js

    sayOne();
    const sayTwo = function () {
        console.log("saying two");
    };

As can be seen above, two.js uses a function defined in one.js. two.js is thus dependent on one.js

scripts/app/three.js

    sayTwo();
    const sayThree = function () {
        console.log("saying three");
    };

three.js is dependent on two.js

We have a main script file called scripts/main.js which calls sayThree().

scripts/main.js

    sayThree();

Our index.html look like:

    <html>
        <head>
        </head>
        <body>
            <script src="scripts/app/one.js"></script>
            <script src="scripts/app/two.js"></script>
            <script src="scripts/app/three.js"></script>
            <script src="scripts/main.js"></script>
        </body>
    </html>

With this setup we should be able to see the following output on the console.

    saying one
    saying two
    saying three

If we mess the script loading order, say place two.js before one.js then our entire system breaks and expected output wouldn't be printed on console. We will see error in such case.

We have to be extremely cautious and careful to maintain order while adding all scripts to index file. This is prone to breaking.

### require.js to rescue

Require.js way of doing it would be:

scripts/app/one.js

    define(function(){
        var sayOne = function () {
            console.log("saying one");
        };
        return {
            'sayOne': sayOne
        }
    });

script/app/two.js

    define(['app/one'], function(one){
        one.sayOne();
        var sayTwo = function () {
            console.log("saying two");
        };
        return {
            'sayTwo': sayTwo
        }
    });

script/app/three.js

    define(['app/two'], function(two){
        two.sayTwo();
        var sayThree = function () {
            console.log("saying three");
        };
        return {
            'sayThree': sayThree
        }
    });

scripts/main.js

    define(['app/three'], function(three) {
        three.sayThree();
    })

index.html

    <html>
        <head>
        </head>
        <body>
            <script data-main="scripts/main.js" src="scripts/require.js"></script>
        </body>
    </html>

Notice how we only have one script tag in index. require.js takes care of loading the proper scripts.

## Takeaway

* Requirejs enables modular javascript code. Codebase stays maintainable.
* Requirejs ensures that global namespace remains unpolluted.
