---
layout: post
comments: true
title:  "Input and Output properties in Angular 9"
description: "Passing data between parent and child components"
keywords: "Angular, Angular9, JS, Javascript"
date: 2020-05-09
categories: [Angular, Angular9, JS, Javascript]
author: Manjunath Hugar
---


### @Input
We can pass data from parent component to child component and vice versa. Angular provides two powerful features to accomplish this - @Input and @Ouput.

This post assumes that you have setup your angular project, if you are new to Angular and want to get started, please go through this [Official documentation](https://angular.io/tutorial/toh-pt0).

Let's quickly create two components, we will use the default `app-root` component as the parent component and create a child component called `app-recipe`.

This is how our parent component `app.component.ts` would look like - 
```
import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  item = 'Tacos';
}
```
here, we have a defined a property called `item` containing value `Tacos` and we want to pass this property to our child component `app-recipe`.

To receive the property `item` from the parent component, we need to let Angular know that it can receive the property from the parent component in to the child component.

For this, we need to bind the property in the child component to the @input decorator.
Our child component `recipe.component.ts` would look like this - 
```
import { Component, Input } from '@angular/core'

@Component({
    selector: 'app-recipe',
    templateUrl: './recipe.component.html'
})
export class RecipeComponent {
    @Input() recipeItem: string;
}
```
We told Angular that we want to receive data from the parent component of type `string`, we can also use other types like `number`, `boolean` or `object`.
Our child component is ready to receive the data from the parent component.

and now the last thing required is to pass the data from parent to child component using the custom property binding, our parent component html `app.component.html` would look like this - 
```
<app-recipe [recipeItem]="item"></app-recipe>
```
In the child selector `app-recipe` we need to bind the parent property `item` to the child property `recipeItem` by making use of the custom property binding feature of the Angular.

We are now ready to render the data in our child component html `recipe.component.html` and this is how it looks - 

```
{% raw %}<h1>I love {{ recipeItem }}</h1>{% endraw %}
```

### @Output

We saw how can we can pass data from parent component to child component, let's do the other way now.

We want the following to happen - 
- Child component contains a text box to enter a new recipe and a button to add that recipe.
- When a button to `Add Recipe` is clicked, we want to relay the data to the parent component.
- Parent component receives the data emitted from the child component and adds that value to the array and display them.

replace the child component `recipe.component.ts` with the following - 
```
import { Component, Output, EventEmitter } from '@angular/core'

@Component({
    selector: 'app-recipe',
    templateUrl: './recipe.component.html'
})
export class RecipeComponent {
    @Output() recipeItemEvent = new EventEmitter<string>();

    addRecipe(value: string) {
        this.recipeItemEvent.emit(value);
    }
}
```

- `@Output() newItemEvent = new EventEmitter<string>();` - this line creates a new event emitter and emits the data of type string which will be available to the parent component, again the type could be of any type.
- `addRecipe` emits the value submitted by the user.
- Make sure to import `Output` and `EventEmitter` from `@angular/core`.

now add the following to the child component template `recipe.component.html` - 
```
<input type="text" #recipeItem>
<button (click)="addRecipe(recipeItem.value)">
    Add Recipe
</button>
```

in the child template, we have an input text box with a local reference `#recipeItem` and a button to add a recipe. When a button is clicked, it invokes the method `addRecipe` and passes whatever data is entered in the text box.

Now we have let Angular know that we want to pass data from child component to parent component by using the @Output decorator which basically sends the data to the parent component and also raises a custom event.

Our next step is bind the method in the parent component to the custom event raised by the child component.

Add the following to the parent component `app.component.ts` - 
```
import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  recipes = [];
  addNewRecipe(item: string) {
    this.recipes.push(item);
  }
}
```
this looks simple and straightforward, we have an empty array called `recipes` and a method `addNewRecipe` to add item to an array.


and now the last thing remaining is to make use of the custom event binding, replace the parent component template `app.component.html` with the following

```
{% raw %}
<ul>
  <li *ngFor="let recipe of recipes">
    {{ recipe }}
  </li>
</ul>
{% endraw %}
<app-recipe (recipeItemEvent)="addNewRecipe($event)">
</app-recipe>
```

What does this template contain - 

- An unordered list to list down the recipes.
- `(recipeItemEvent)="addNewRecipe($event)"` - binds the custom event of the child component `recipeItemEvent` to the parent component method `addNewRecipe`.
- $event contains the data emitted from the child component.

I hope you found this post useful, in case if you have any queries or suggestions, please feel free to comment down below.

Thanks for reading this post, see you in the next blog.
















