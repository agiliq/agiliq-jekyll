---
layout: post
comments: true
title: "Using bower to manage frontend dependencies"
date: 2019-01-29 12:30:27+05:30
categories: bower, frontend
author: akshar
---

### Agenda

There are several ways to manage frontend dependencies. Few worth mentioning are npm, bower and yarn. This post specifically talks about using bower to manage dependencies.

Traditionally, dependency managers weren't used for managing client side libraries. Client side libraries used to be part of version control. This post talks about how using a dependency manager is advantegous over not using a dependency manager.

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

A very frequently used approach is to use `bower` to track and install dependencies.

### Using bower to install dependencies

Before bower can be used properly, there is a need for a bower.json file.

Create a bower.json file by running `bower init`.

    bower init

It would ask you some questions, you can skip answering the questions and in such case sensible defaults would be used.

    ╰─$ bower init
    ? name jquery-example
    ? description A test project to understand bower
    ? main file
    ? keywords
    ? authors Akshar Raaj <akshar@agiliq.com>
    ? license MIT
    ? homepage
    ? set currently installed components as dependencies? No
    ? add commonly ignored files to ignore list? Yes
    ? would you like to mark this package as private which prevents it from being accidentally published to the registry? Yes

    {
      name: 'another-test',
      authors: [
        'Akshar Raaj <akshar@agiliq.com>'
      ],
      description: 'A test project to understand bower',
      main: '',
      license: 'MIT',
      homepage: '',
      private: true,
      ignore: [
        '**/.*',
        'node_modules',
        'bower_components',
        'test',
        'tests'
      ]
    }

    ? Looks good? Yes

A bower.json file should have been created in your current directory.

Install jquery using bower now.

    bower install jquery --save

You would find that a `dependencies` key is added to bower.json.

    "dependencies": {
        "jquery": "^3.3.1"
    }

A new directory called `bower_components` should have been created and directory `jquery` should have been created inside `bower_components`. Check that these directories were created.

    ╰─$ ls bower_components
    jquery

Modify `index.html`, so that `script` looks like:

    <script src="bower_components/jquery/dist/jquery.js"></script>

Full `index.html` file would look like:

    <!DOCTYPE html>
    <html>
        <body>
            <p id="para">Hello World!</p>
            <button type="button" id="german-button" value="Switch to German" class="btn-primary">Switch to German</button>
            <script src="bower_components/jquery/dist/jquery.js"></script>
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

This approach doesn't need dependencies to be part of version control. The directory `bower_components` shouldn't be part of version control. If you are using Git, then you would add `bower_components` to .gitignore.

Only `index.html` and `bower.json` would be part of version control.

When a new developer clones the repository, he/she would run `bower install`. This would ensure that a `bower_components` is created and jquery is installed inside bower_components.
