---
layout: post
comments: true
title:  "Javascript pass by value and pass by reference"
description: ""
keywords: "JS, Javascript"
date: 2020-05-18
categories: [JS, Javascript]
author: Manjunath Hugar
---

In this blog post, we are going to understand pass by value and pass by reference in Javascript.

It is important to understand this, in order to improve the javascript development and debugging skills.

### Pass by value
In javascript, all primitive types are passed by value, to understand this let's take a look at the following example - 
```js
myNumber = 10;
```
here, the value `10` is stored somewhere in the memory and the variable `myNumber` has the address location of the memory where the value `10` is stored.

and now lets suppose if we setup a new variable `otherNumber` which is equal to `myNumber`
```js
otherNumber = myNumber
```
since `myNumber` points to a memory location containing primitive type value `10`, `otherNumber` points to a new memory location and the copy of primitive value is stored in that memory location. That means the variables `myNumber` and `otherNumber` are pointing to two different memory locations but the same value `10` is stored in those two memory locations.

This process is called `Pass by value`.

That means, if we change `myNumber` then it should not affect `otherNumber` because they are pointing to two different locations in memory.

Let's try changing the value of `myNumber` to 20
```js
myNumber = 20
console.log(myNumber)
console.log(otherNumber)
```
when you run this, you should see the following output as expected -
```
20
10
```

same approach is followed when a primitive type value is passed to the function as a parameter.

### Pass by reference
All objects in Javascript
(including functions, remember functions are first class objects) are passed by reference.
consider an example
```js
var person = {"name": "Sachin"};
```
as usual, JS allocates memory to store an object `{"name": "Sachin"}` and the variable `person` points to that memory location.
but what happens when we assign `person` to new variable let's say `person1` is interesting
```js
var person1 = person;
```
now in this case, instead of creating a new memory space for `person1` and copying the object in to that memory, JS simply makes `person1` point to the same memory location where the var `person` is pointing to.

that means if we mutate (to change something) `person` like below
```js
person.name = "Vijay";
```
and log both `person` and `person1`, what do you think will happen?
```js
console.log(person);
console.log(person1);
```
remember that when it comes to objects, the variables which are set equal to each other simply points to the same memory location. So in this case changing `person` will change `person1` as well.
Think of it like a person having an alias name but his address remains the same.
We should see the following output

```js
{name: "Vijay"}
{name: "Vijay"}
```
and again, you should see the same behavior when objects are passed to the functions as parameters.
```js
function changePerson(pObj) {
    pObj.name = "Ramesh";
}
```
when we pass the object `person` to the function, it is passed by reference, let's log `person` and `person1` now and we should see that the property `name` of object `person` and `person1` set to the value `Ramesh`.
```js
changePerson(person);
console.log(person);
console.log(person1);
```
This is known as `pass by reference`.
