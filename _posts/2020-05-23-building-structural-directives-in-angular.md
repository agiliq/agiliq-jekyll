---
layout: post
comments: true
title:  "Building a structural directive in Angular"
description: ""
keywords: "Angular, Angular9"
date: 2020-05-23
categories: [Angular, Angular9]
author: Manjunath Hugar
---

In this blog post, we will create a very simple structural directive, but before that we will take a look at the builtin structural directive **`ngIf`** and what Angular does behine the scenes on structural directive.

### *ngIf
When an Angular project is created, it creates a component named `app` and we are going to use this component in our example.

In your file `app.component.ts` add a property `isVisible` and set this to `true` as below
```js
import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
   isVisible = true;
}
```
and now in the template `app.component.html`, we will use `ngIf` to control the DOM element, add the following to `app.component.html`
```html
<p *ngIf="isVisible">
    When life gives you lemons, sell them and buy a pineapple.
</p>

<p *ngIf="!isVisible">
    Keep calm and eat an Apple.
</p>
```
now run the application using the command `ng serve` and you should see the following text displayed
```
When life gives you lemons, sell them and buy a pineapple.
```
this is because the boolean property `isVisible` is set to `true` and Angular rendered the first paragraph.

*Note: ngIf doesn't hide elements, it adds/removes the element from DOM on which it is placed.*

### Structural directives behind the scenes
Did you observe the use of asterix `*` in `*ngIf`? it is just a syntactic sugar, behind the scenes Angular translates `*ngIf` in to `<ng-template>` around which the host element (`<p>` in our example) is wrapped.

So this
```html
<p *ngIf="isVisible">
    When life gives you lemons, sell them and buy a pineapple.
</p>
```
is translated to
```html
<ng-template [ngIf]="isVisible">
    <p>When life gives you lemons, sell them and buy a pineapple.</p>
</ng-template>
```
### Creating structural directive
Now that we know how `ngIf` works, we will create a custom structural directive which will be opposite to `ngIf`. That means, this directive will remove the element from the DOM if the conditiion if true.

create a file named `customcondition.directive.ts` and add the following code
```js
import { Directive } from '@angular/core';

@Directive({
    selector: '[appCustomCondition]'
})
export class CustomCondition {

}
```
after this, to get access to the `<ng-template>` and to also get access to the place in the DOM where we want to render it, we need to inject couple of things namely `TemplateRef` and `ViewContainerRef` in directive constructor like this
```js
import { Directive, TemplateRef, ViewContainerRef } from '@angular/core';

@Directive({
    selector: '[appCustomCondition]'
})
export class CustomCondition {
    constructor(private tRef: TemplateRef<any>, private vcRef: ViewContainerRef) { }
}
```
and lastly, since we are going to bind true/false value to our custom directive, we need someway to relay this value from `app` component to our custom `directive`.
For this, we need to decorate the property with `@Input` decorator and then we will use the dependencies injected in our constructor to add/remove the element from DOM.

so the final code in `customcondition.directive.ts` will look like this
```js
import { Directive, Input, TemplateRef, ViewContainerRef } from '@angular/core';

@Directive({
    selector: '[appCustomCondition]'
})
export class CustomCondition {
    @Input() set appCustomCondition(value: boolean) {
        if (!value) {
            this.vcRef.createEmbeddedView(this.tRef);
        } else {
            this.vcRef.clear();
        }
    }

    constructor(private tRef: TemplateRef<any>, private vcRef: ViewContainerRef) { }

}
```

*Note: The name of the directive selector and the property decorated with @Input should be the same.*

and our template `app.component.html` will look like this
```html
<p *appCustomCondition="isVisible">
    When life gives you lemons, sell them and buy a pineapple
</p>

<p *appCustomCondition="!isVisible">
    Keep calm and eat an Apple.
</p>
```

now when you run this using `ng serve`, you should the output as below
```
Keep calm and eat an Apple.
```
this is because our custom structural directive `appCustomCondition` does just the opposite of `ngIf`.





