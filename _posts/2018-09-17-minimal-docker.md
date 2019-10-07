---
layout: post
comments: true
title: "Getting started with docker"
keywords: "docker"
date: 2018-09-17 12:30:27+05:30
categories: docker
author: Akshar
---
## Assumption

This post assumes that you have installed docker.

## Why use docker

One primary reason to use Docker is to gain the portability provided by Docker. New developers starting on a project have to spend hours and days in getting their development environment ready. Docker can bring the development setup time down to minutes.

There are multiple other reasons too but this single reason alone is sufficient to entice me to use Docker.

## Minimal docker setup

Let's write a docker setup to just echo `Hello World`.

Create a directory

    mkdir echo-hello-world

Cd

    cd echo-hello-world

Create a Dockerfile

    touch Dockerfile

Add following entry to Dockerfile

    FROM alpine:latest

    CMD ["echo", "hello world"]

Every Dockerfile's first instruction must be `FROM <something>`. We need to provide a `base image` to  `FROM` instruction.

Here base image is `alpine:latest`. Alpine is a simple and lightweight Linux distro.

Once Dockerfile is added, we need to create an `image` using this Dockerfile.

Issue following command

    docker build -t echo-hello-world .

You should see following output:

    ╰─$ docker build -t echo-hello-world .
    Sending build context to Docker daemon  2.048kB
    Step 1/2 : FROM alpine:latest
     ---> 961769676411
    Step 2/2 : CMD ["echo", "hello world"]
     ---> Running in 0b6d6f2043be
    Removing intermediate container 0b6d6f2043be
     ---> 04ed766ba81d
    Successfully built 04ed766ba81d
    Successfully tagged echo-hello-world:latest

Run the image using following command:

    docker run echo-hello-world

You should see `hello world` echoed on the console.

    ╰─$ docker run echo-hello-world
    hello world

In subsequent posts we will create a Dockerfile to run a Django application.
