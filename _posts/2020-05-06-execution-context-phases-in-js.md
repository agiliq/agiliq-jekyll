---
layout: post
comments: true
title:  "Understanding the Execution Context phases in Javascript"
description: "Creation and Execution phase"
keywords: "JS, Javascript"
date: 2020-05-06
categories: [JS, Javascript]
author: Manjunath Hugar
---

Let's take a look at the code below - 

```
var a = 10;

function foo() {
  console.log("function foo is called!")
}

foo();
console.log(a);
```

when we execute this code, we see the output as expected

```
function foo is called!
10
```

but what will happen if we move the last 2 lines of code in the beginning like this?

```
foo();
console.log(a);

var a = 10;

function foo() {
  console.log("function foo is called!")
}
```
we get the following output when we run this - 
```
function foo is called!
undefined
```
Ideally we would expect the JS to raise an exception because the function `foo` is called before it is declared and the variable `a` is referenced before it is declared. In fact this is how most of the programming language works.

But in this case, the `function foo` is properly executed even though we called it before its declaration and the variable `a` is set to undefined. That means the JS has access to the `function foo` and the `var a` which is stored somewhere.
In order to understand this, we need to understand the execution context phases in JS.

Let's understand how JS is working under the hood - 

Execution context consists of two phases - `Creation Phase` and the `Execution Phase`.

### Creation Phase
During the creation phase of the execution context, JS allocates memory space for the functions and variables. In case of functions, the whole function body is stored but in case of the variables, it is declared and assigned a default value `undefined`. This phenomena is called `Hoisting`. 

An important thing to understand is, the value of `a` is set to `undefined` during this phase because the JS found a `var a` defined somewhere in our code above. If we remove the line `var a = 10` then it will result in an error `Uncaught ReferenceError: a is not defined`.

So in the above when JS ran `console.log(a)`, the `var a` is not assigned any value at that point so it picked up the value from the memory space which is set to undefined during the creation phase and printed that value.

*Note: It is recommended not to rely on hoisting, that means it is a good practice to declare and define the variables and the functions before they are referred.*


### Execution Phase
 In this phase, JS executes our code line by line and assigns the value to the variables. In our example above, the value `10` to the variable `a` is set.
 
 ------------------------------------------------------------
 To summarize this, lets take a look at the code below - 
 
 ```
function foo() {
  console.log("function foo is called!")
}
foo()
console.log(a);
var a = 10;
console.log(a)
 ```
 
since we now understand the phases in execution context, we can confidently say by looking at the code above that the output of the code is - 
 
 ```
function foo is called!
undefined
10
 ```
 
- function foo is called and it prints the `function foo is called!`.
- On the next line as we know that during the creation phase, JS assigned a default value to the `var a` to `undefined` so it printed undefined and 
- The last line prints 10 because during the execution phase, JS assigned the value 10 to the `var a`.
 
 
