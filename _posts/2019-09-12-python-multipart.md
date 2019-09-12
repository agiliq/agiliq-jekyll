---
layout: post
comments: true
title:  "Handling multipart form upload with vanilla Python"
description: "Using python-multipart library to handle multipart/form-upload data"
keywords: "Python, Multipart, Form-upload, python-multipart"
date: 2019-09-12
categories: [python]
author: Akshar
---

## Agenda

We will see how to parse multipart/form-data with a tiny Python library. We want to avoid frameworks like Django or Flask.

We will use <a href="https://github.com/andrew-d/python-multipart" target="_blank">python-multipart</a> to handle a multipart form upload.

## Use case

Why would someone do it is arguable. Why not use Django or Flask which transparently does the parsing.

My web application is extermely small and basic. It has only two routes.

First route is the index page which displays a form. Form has a file field. The uploaded file would be sent to a server where some metadata would be extracted out of this image.

Second route handles the POSTed form data.

Django or Flask would be an overkill for such a tiny application.

python-multipart can come extremely useful while writing lambda functions. My lambda functions are usually small and I prefer to keep my zip files tiny. Django or Flask makes the zip files huge. Ignore this paragraph if you aren't familiar with AWS Lambda.

## Application

Create a virtualenv or virtualenvwrapper and install `python-multipart`.

    pip install python-multipart

Let's write the wsgi application.

    import multipart
    from wsgiref.simple_server import make_server

    def simple_app(environ, start_response):
        fields = {}
        files = {}
        def on_field(field):
            fields[field.field_name] = field.value
        def on_file(file):
            files[file.field_name] = {'name': file.file_name, 'file_object': file.file_object}

        if environ['PATH_INFO'] != '/upload':
            with open('index.html') as f:
                content = f.read()
        else:
            multipart_headers = {'Content-Type': environ['CONTENT_TYPE']}
            multipart_headers['Content-Length'] = environ['CONTENT_LENGTH']
            multipart.parse_form(multipart_headers, environ['wsgi.input'], on_field, on_file)
            print(fields)
            print(files)
            content = "Hello world"
        content = [content.encode('utf-8')]
        status = '200 OK'
        headers = [('Content-type', 'text/html; charset=utf-8')]
        start_response(status, headers)
        return content

    with make_server('', 8051, simple_app) as httpd:
        print("Serving on port 8051...")
        httpd.serve_forever()

Let's create index.html file in the same folder

    <html>
        <head>
            <form enctype="multipart/form-data" method="POST" action="/upload">
                <input type="text" name="name"></input>
                <input type="file" name="foo"></input>
                <input type="submit"></input>
            </form>
        </head>
        <body>
        </body>
    </html>

Start the web application

    python web_application.py

Navigate to `localhost:8051`. You should see a form.

![](/assets/images/multipart/index.png)

Enter a name in text field and choose a file. Submit the form. You should see the name and filename printed on the shell.

    127.0.0.1 - - [12/Sep/2019 18:50:11] "GET /favicon.ico HTTP/1.1" 200 298
    {b'name': b'akshar'}
    {b'foo': {'name': b'crown.jpeg', 'file_object': <_io.BytesIO object at 0x10eaa8518>}}

### Code step through

- We created a basic wsgi application.
- We defined two variables. One variable for non binary data. Other variable for files.
- We added two callbacks named `on_field` and `on_file`. python-multipart calls these callbacks while parsing multipart data.
- Added if/else condition to handle our two routes.
- Call `multipart.parse_form` with needed arguments.
- python-multipart calls `on_field` once it's done parsing a non binary field.
- python-multipart calls `on_file` once it's done parsing a file field.

## Doing more
Instead of printing we could have used boto and uploaded the file to S3. Or we could have analysed the image. For now we will just write the uploaded image on the filesystem.

Remove the two print statements and replace them with following lines:

    for each_file, each_file_details in files.items():
        with open(each_file_details['name'], 'wb') as f:
            uploaded_file = each_file_details['file_object']
            uploaded_file.seek(0)
            f.write(uploaded_file.read())

Full `simple_app` looks like:

    def simple_app(environ, start_response):
        fields = {}
        files = {}
        def on_field(field):
            fields[field.field_name] = field.value
        def on_file(file):
            files[file.field_name] = {'name': file.file_name, 'file_object': file.file_object}

        if environ['PATH_INFO'] != '/upload':
            with open('index.html') as f:
                content = f.read()
        else:
            multipart_headers = {'Content-Type': environ['CONTENT_TYPE']}
            multipart_headers['Content-Length'] = environ['CONTENT_LENGTH']
            multipart.parse_form(multipart_headers, environ['wsgi.input'], on_field, on_file)
            for each_file, each_file_details in files.items():
                with open(each_file_details['name'], 'wb') as f:
                    uploaded_file = each_file_details['file_object']
                    uploaded_file.seek(0)
                    f.write(uploaded_file.read())
            content = "Hello world"
        content = [content.encode('utf-8')]
        status = '200 OK'
        headers = [('Content-type', 'text/html; charset=utf-8')]
        start_response(status, headers)
        return content

Navigate to index page again and upload a text file. This file should have been written in the current directory. Navigate again to index and upload an image or a video file. This should have been written to the current folder too.

This code is capable to handle multiple file fields in the form.
