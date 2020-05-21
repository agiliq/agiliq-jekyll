---
layout: post
comments: true
title:  "Custom atttibute directives in Angular"
description: "Building a simple attribute directive"
keywords: "Angular, Angular9"
date: 2020-05-18
categories: [Angular, Angular9]
author: Manjunath Hugar
---

Angular has three kinds of directives
- `Components` - is a directive with a template. 
- `Structural directives` - controls the DOM elements, using which we can add or remove elements from DOM. For ex: *ngIf, *ngFor etc.
- `Attribute directives` - to change the behavior or apperance of an element, component or the directive. For ex: ngClass, ngStyle etc.

In this blog post, we are going to create a simple custom attribute directive, which is when placed on an element, it will change its appearance.

Creating a directive is very simple, you can either create it manually or using the CLI command as below
```
ng generate directive highlight
```
the above command will generate a file named `highlight.directive.ts` and a test file `src/app/highlight.directive.spec.ts` inside `src/app` folder and it will also register your directive in `app.module.ts`.

so your `hightlight.directive.ts` should contain the following code 
```js
import { Directive } from '@angular/core';

@Directive({
  selector: '[appHighlight]'
})
export class HighlightDirective {

  constructor() { }

}
```

creating a directive is similar to creating a component, the only difference is that in directives we decorate our class using `@Directive` imported from `@angular/core`.
@Directive decorator has a selector which is enclosed in `[]` because we want to use this custom directive as an attribute in our HTML element.

Ok, now lets add this directive to our HTML tag, add this line to your `app.component.html`
```html
<p>This is <span appHighlight>Angular9</span></p>
```
now in order to make an element on which we used our custom directive available to our directive class, we need to inject a reference to that element in directive's constructor.

Modify `hightlight.directive.ts` to look like this - 
```js
import { Directive, ElementRef } from '@angular/core';

@Directive({
  selector: '[appHighlight]'
})
export class HighlightDirective {

  constructor(el: ElementRef) {
    el.nativeElement.style.fontSize = "20px";  
  }

}
```
`ElementRef` lets us access DOM elements directly through its `nativeElement property.`

now run `ng serve` and you should see that the text `Angular9` is set to font size 20px.

Now this is all good, but how about changing the element style based on user driven events like say for example - onmouseover, onmouseout etc?
Yes it is possible to listen to an event and change the appearance of DOM elements using the `@HostListener`

Import `HostListener` from `@angular/core`
```js
import { Directive, ElementRef, HostListener } from '@angular/core';
```
then add the event handlers to responsd to the events - `mouseenter`, `mouseleave` as below
```js
import { Directive, ElementRef, HostListener } from '@angular/core';

@Directive({
  selector: '[appHighlight]'
})
export class HighlightDirective {

  constructor(private el: ElementRef) { }

  @HostListener('mouseenter') onMouseEnter() {
    this.highlight("20px");
  }

  @HostListener('mouseleave') onMouseLeave() {
    this.highlight("16px");
  }

  private highlight(fontSize: string) {
    this.el.nativeElement.style.fontSize = fontSize;
  }

}
```
`@HostListener` subscribes to the events of the DOM element on which we have placed our attribute directive, in our case we have applied custom directive to the `span` element.

Now run the app using `ng serve` and you should see that the font size of the text `Angular9` changes on mouse over and mouse leave.

It is also possible to send data to the directive, instead of defining the values inside the directive. We can achive this by using the `@Input` property, you can refer this [post](https://www.agiliq.com/blog/2020/05/input-and-output-properties-in-angular/) for details about the `@Input` and `@Output` properties.

Update the file `highlight.directive.ts` with the following code
```js
import { Directive, ElementRef, HostListener, Input } from '@angular/core';

@Directive({
  selector: '[appHighlight]'
})
export class HighlightDirective {
  @Input() highlightText: string;

  constructor(private el: ElementRef) { }

  @HostListener('mouseenter') onMouseEnter() {
    this.highlight(this.highlightText);
  }

  @HostListener('mouseleave') onMouseLeave() {
    this.highlight("16px");
  }

  private highlight(fontSize: string) {
    this.el.nativeElement.style.fontSize = fontSize;
  }

}
```
and our `app.component.html` will look like this
```html
<p>This is <span appHighlight [highlightText]="'30px'">Angular9</span></p>
```
notice the use singlequotes in `[highlightText]="'30px'"`, this can be replaced with `highlightText="30px"` if you want to avoid using single quotes.

Everything looks great but wouldn't it be nice if there is a way to apply the directive and apply the font in the same attribute instead of having two attributes? we can do that using `@Input` alias.

replace `app.component.html` with the following code - 
```html
<p>This is <span [appHighlight]="'30px'">Angular9</span></p>
```

and use @Input alias in `highlight.directive.ts` as
```js
@Input('appHighlight') highlightText: string;
```

so our final code for `highlight.directive.ts` will look like this
```js
import { Directive, ElementRef, HostListener, Input } from '@angular/core';

@Directive({
  selector: '[appHighlight]'
})
export class HighlightDirective {
  @Input('appHighlight') highlightText: string;

  constructor(private el: ElementRef) { }

  @HostListener('mouseenter') onMouseEnter() {
    this.highlight(this.highlightText);
  }

  @HostListener('mouseleave') onMouseLeave() {
    this.highlight("16px");
  }

  private highlight(fontSize: string) {
    this.el.nativeElement.style.fontSize = fontSize;
  }

}
```
and our `app.component.html` will look like this
```html
<p>This is <span [appHighlight]="'30px'">Angular9</span></p>
```



