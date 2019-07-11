---
layout: post
comments: true
title:  "Angular template syntax"
description: "A quick introduction to angular template syntax and component's data & event binding"
keywords: "angular template, angular template syntax, template syntax"
date:   2019-07-09
categories: [angular, templates, components]
author: Anjaneyulu
---
Angular provides a simplified approach to work with templates. It got a super cool syntax to speed-up the development.

In our <a href="/blog/2019/07/understanding-basic-folder-structure-angular-webapp/" target="__target">previous article</a> we have seen the folder structure of angular app. Angular starts it's execution from `src/main.ts` file where it bootstraps the application’s root module (`AppModule`) to run in the browser. In this article we work with angular component and it's template syntax.

# Example Angular Component
```ts
import { Component } from '@angular/core';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
})
export class AppComponent {
  title = 'my-app';
}
```

# Angular Inline String Template
  - It's string representation of the `HTML` instead a `HTML` file.
  - If you check the above example component it's using a template path with for component property `templateUrl`. we can use a string `HTML` syntax like below.
```ts
import { Component } from '@angular/core';
@Component({
  selector: 'app-root',
  template: '<h1>Welcome to Angular App</h1>',
  styleUrls: ['./app.component.css']
})
export class AppComponent {}
```
  - In the above code we have used sting template `<h1>Welcome to Angular App</h1>` with attribute `template`.
  - It's always recommended to use the file template instead of a string template for better code readability and maintainability.

# Angular File based Template
  - In above <a href="#example-angular-component">Example Angular Component</a> we have used a HTML template `templateUrl: './app.component.html'`.
  - Coponent `AppComponent` user the template `app.component.html` to render the component in the app.

# Passing Data from Component to Template
  - It's pretty simple in angular. All properties of component are available on the template.
  - Let's see a simple example to pass a username to the template from component.
  - template: **app.component.html**

```ts
{% raw %}<h1> Hello {{username}}! </h1>{% endraw %}
```

  - component: **app.component.ts**

```ts
  import { Component } from '@angular/core';
  @Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
  })
  export class AppComponent {
    username = 'John Doe';
  }
```

  - If you update component, template code as above you can see text `Hello John Doe!` in the app.

# Interpolation (i.e `{% raw %}{{ }}{% endraw %}`)
  - Interpolation is a double braced syntax to render data in the template.
  - It can also evalute the basic javascript/typescript expressions like `+`, `>`, etc.
  - Let's see some code to see how to use interpolation
{% raw %}
```ts
<h1> Welcome {{username}}! </h1>
<p>The sum of 1 + 1 is {{1 + 1}}.</p>
<p>1 > 1 is {{1 > 1}}.</p>
<p>1 == 1 is {{1 == 1}}.</p>
<p>1 > 5 is {{1 > 5}}.</p>
<p>"hello" && "world" is "{{ "hello" && "world" }}"</p>
<span>
  Hello {{ 1 + 1 === 3 ? 'me' : 'you' }}
</span>
<p>{{ user?.preferences?.avatar }}</p>
<p>{{ user?.name | uppercase }}</p>
```
{% endraw %}
  - The safe navigation operator, `?.`, prevents the JavaScript engine from complaining if you try to access values on objects that are null or undefined.
  - The pipe operator, `|`, allows to pass-in the interpolated value to a <a href="https://angular.io/api?type=pipe" target="__blank" nofollow>pipe</a>
  - Note: we can only do basic operations using interpolation syntax. We are not allowed to do complex operations like bitwise `OR` i.e `{% raw %}{{ 20 | 5 }}{% endraw %}`

# Property binding
  - It's the way to sync the property values of template HTML elements in sync with components attributes/properties.
  - Let's take an example for property binding
  - **app.component.html**
{% raw %}
```html
  <div>
    <label> is superuser ? <input type="checkbox" [checked]="status"/></label>
  </div>
```
{% endraw %}

  - **app.component.ts**

{% raw %}
```ts
import { Component } from '@angular/core';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  status = ''
  constructor(){
    setTimeout(()=>{this.status = 'checked'}, 500)
    setTimeout(()=>{this.status = ''}, 2500)
  }
}
```
{% endraw %}
  - In above example we have a property binding on checkbox that can be checked/un-checked dynamically based on the value of components property `status`.
  - If test the above code you can find that the checkbox initially un checked and after 500 milli seconds it will be checked and again after 2 seconds it will again unchecked because we are updating the component property dynamically using `setTimeout` function. 

# One-Way event binding

# Two-Way event binding