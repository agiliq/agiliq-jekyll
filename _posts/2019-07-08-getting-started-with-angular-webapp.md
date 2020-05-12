---
layout: post
comments: true
title:  "Getting Started with Angular WebApp"
description: "Basic environment setup for first angular web applcation"
keywords: "angular first app, angularjs webapp, first angular app"
date:   2019-07-08
categories: [angular, typescript]
author: Anjaneyulu Batta
---
Angular is a type script based web/mobile application framework. It is an opensource web/mobile framework developed by Google. It has a great community support.

# Why to use angular ?
 - It follows MVC(Model-View-Controller) approach.
 - It follows modular structure(i.e components, directives, pipes, or services)
 - Re-Usability of code
 - It supports Unit testing
 - It uses type script so we write less code and do more.
 - Due to it's modularity it can be maintained easily.

# Install pre-requisites for angular
 * Install `Node.js` and `npm`
 ```sh
sudo apt-get install curl python-software-properties
curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
sudo apt-get install nodejs
# check version
node -v
# Also, check the npm version
npm -v 
 ```
 * Install Angluar CLI Globally
  ```
  sudo npm install -g @angular/cli
  ```

# Create first application("my-app") with Angular-CLI 
  ```
  ng new my-app
  ```
  It will ask some questions read it and answer accordingly.
  * Now, It's time to run the application. To do it just execute the below commands in terminal

```sh
  cd my-app && ng serve --open
  ```
  ![Angular first app](/assets/images/angular/angular-first-app.png)  
  * It open's a screen like above in the web browser. Angular dev server runs on a port 4200. Hurray! Congrat's you have created your first app.

Stay tuned for agiliq blog more tutorials on angular.
