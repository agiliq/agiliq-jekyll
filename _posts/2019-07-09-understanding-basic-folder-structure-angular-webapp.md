---
layout: post
comments: true
title:  "Understanding basic folder structure of Angular Webapp"
description: "Angular creates a bunch of files when we create a new angular webapp. Let's understand the important files and folders that we should aware of."
keywords: "angular folder structure, angular first webapp, first angular app"
date:   2019-07-09
categories: [angular, basic folder structure]
author: Anjaneyulu
---
When we create the Angular webapp it will create a bunch of files and folders. We need to have a basic understanding of what these files and folders do. So, why to wait, let's jump in.

# Workspace configuration files
  * `.editorconfig`
    - Configuration for code editors
  * `.gitignore`
    - It contains list of patterns to ignore while pushing/uploading the code to git repository.
  * `README.md`
    - It contains information about the project.
  * `angular.json`
    - It contains default configurations for command line interface(CLI). It includes configuration for build, serve, and test tools.
  * `package.json`
    - It contains configuratios for `npm` package dependencies that used in the appliaction/project.
  * `package-lock.json`
    - It provides version information for all packages installed into node_modules by `npm`.
  * `src/`
    - It holds the development code for the application.  
  * `node_modules/`
    - It holds all packages installed by `npm`. Do not modify it's contents unless you are sure about the change.
  * `tsconfig.json`
    - Default TypeScript configuration for projects in the workspace.
  * `tslint.json`
    - Default TSLint configuration for projects in the workspace.

# Application source files
  * All files at top level of `src/` support testing and running your application
  * All it's sub-folders contains application source code and specific configurations.
  * `src/app/`
    - It contains the component files.
    - `src/app/app.component.ts`: Defines the logic for the app's root component, named `AppComponent`. 
    - `src/app/app.component.html`: It's a html template used by the root component.
    - `src/app/app.component.css`: It's a stylesheet for the root component.
    - `src/app/app.component.spec.ts`: Defines a unit test for the root AppComponent.
    - `src/app/app.module.ts`: Defines the root module, named AppModule, that tells Angular how to assemble the application. Initially declares only the AppComponent. As you add more components to the app, they must be declared here.

# Application configuration files
  * `browserslist`: Configures sharing of target browsers and Node.js versions among various front-end tools.
  * `karma.conf.js`: Application-specific Karma configuration. Karma  is a task runner for application tests.
  * `tsconfig.spec.json`: TypeScript configuration for the application tests.
  * `tslint.json`: Application-specific TSLint configuration.

# End-to-end test files
  * An `e2e/` folder at the top level contains source files for a set of end-to-end tests that correspond to the root-level application, along with test-specific configuration files.

We have seen the basic angular application structure above. Let's change the contents of a root component that we have created in the last blog post(<a target="__blank" href="/blog/2019/07/getting-started-with-angular-webapp/">"**Getting Started with Angular WebApp**"</a>).

Now, open terminal and go to project directory and run the development server

```sh
cd my-app && ng serve --open
```
It will open the browser with url "http://localhost:4200" and you can see our app. Let's modify contents of root applications template(i.e `my-app/src/app/app.component.html`) and style sheet(i.e `my-app/src/app/app.component.css`) like below.

`my-app/src/app/app.component.html`

```html
<div>
  <h1>
    Welcome to Agiliq <span>Angular Webapp!</span>
  </h1>
  <img src="https://www.agiliq.com/assets/images/logo.png" />
</div>
```

`my-app/src/app/app.component.css`

```css
h1{
  font-style: oblique;
  color: green;
}
h1 span{
  color: orange;
}
img{
  height: 300px;
  width: 500px;
}
```

After making above changes you can see the below page.
!["agiliq-angular-app"](/assets/images/angular/agiliq-angular-app.png)

That's it folks! Stay tuned for more updates on Angular!
