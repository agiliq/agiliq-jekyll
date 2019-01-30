---
layout: post
comments: true
title: "Using npm to manage frontend dependencies"
date: 2019-01-29 11:30:27+05:30
categories: npm, frontend
author: akshar
---

### Agenda

There are several ways to manage frontend dependencies. Few worth mentioning are npm, bower and yarn. This post specifically talks about using npm to manage dependencies.

Traditionally, dependency managers weren't used for managing client side libraries. Client side libraries used to be part of version control. This post talks about how using a dependency manager is advantegous over not using a dependency manager.

### Confusion which we will address

One frequently ocurring confusion is how npm which is a package manager for Node.js can be used for managing client side libraries.

npm makes sense in context of Node.js. Node.js is a server development environment. How could a package manager for server environment manage dependencies for frontend.

We will address this confusion.

### Setup

The traditional approach to frontend development involved keeping the dependencies in version control along with the source code.

Assume we have a very basic application which is dependent on jquery.

In such cases, jquery.js would be kept as part of version control.

Create a directory called 'jquery-example'.

    mkdir jquery-exaple
    cd jquery-example

Create a directory called `libs` and add `jquery.js` to it.

    mkdir libs
    # Download jquery from internet and add it to libs/

Create an index.html which looks like:

    <!DOCTYPE html>
    <html>
        <body>
            <p id="para">Hello World!</p>
            <input type="button" id="german-button" value="Switch to German"></input>
            <script src="libs/jquery.js"></script>
            <script>
                $(document).ready(function () {
                    $("#german-button").click(function () {
                        $("#para").text("Hallo Welt");
                    });
                })
            </script>
        </body>
    </html>

Open this page in a browser, clicking on the button would change the paragraph text. This verifies that jquery is working properly.

### Problem with this approach

This approach requires that dependency jquery be kept as part of the code repository.

We want to add bootstrap to our project now, we will have to download bootstrap and add it to version control too. Gradually our repository will fill with third party libraries. This approach looks incorrect.

If you have worked with any backend programming language, you must be knowing that dependencies shouldn't be kept as part of version control.

Python projects have a requirements.txt to track dependencies and has `pip` to install these requirements. Ruby projects have `gem` to install dependencies. Java has jar files and so on.

Frontend dependency management shouldn't be any different. There should be a file which lists the dependencies of the project along with version numbers.

When a developer starts on the project, he should install the listed dependencies before running the project.

A very frequently used approach is to use `npm` to track and install dependencies.

### How a Node.js package manager be used with frontend

Traditionally `npm` was used to manage node dependencies. But gradually people started using it to manage frontend dependencies too.

Even `pip`, a Python package manager could have been used to manage frontend dependencies, had PyPi allowed listing frontend libraries in its registry.

### Using npm to install dependencies

Create a file called package.json in current directory with following content.

    {
        "dependencies": {
            "jquery": "3.3.1",
            "bootstrap": "4.2.1"
        }
    }

Execute command `npm install`.

    npm install

This command would read package.json and install dependencies jquery and bootstrap.

A new directory called `node_modules` should have been created and directories `jquery` and `bootstrap` should have been created inside `node_modules`. Check that `node_modules` was created with these two directories.

    ╰─$ ls node_modules
    bootstrap jquery

Modify `index.html`, so that `link` and `script` look like:

    <link href="node_modules/bootstrap/dist/css/bootstrap.css" type="text/css" rel="stylesheet">
    <script src="node_modules/jquery/dist/jquery.js"></script>

Full `index.html` file would look like:

    <!DOCTYPE html>
    <html>
        <head>
            <link href="node_modules/bootstrap/dist/css/bootstrap.css" type="text/css" rel="stylesheet">
        </head>
        <body>
            <p id="para">Hello World!</p>
            <button type="button" id="german-button" value="Switch to German" class="btn-primary">Switch to German</button>
            <script src="node_modules/jquery/dist/jquery.js"></script>
            <script>
                $(document).ready(function () {
                    $("#german-button").click(function () {
                        $("#para").text("Hallo Welt");
                    });
                })
            </script>
        </body>
    </html>

Notice that we waren't using lib/ directory anymore. Remove lib/ and page should still function properly.

This approach doesn't need dependencies to be part of version control. The directory `node_modules` shouldn't be part of version control. If you are using Git, then you would add `node_modules` to .gitignore.

Only `index.html` and `package.json` would be part of version control.

When a new developer clones the repository, he/she would run `npm install`. This would ensure that a `node_modules` is created and bootstrap and jquery are installed inside node_modules.
