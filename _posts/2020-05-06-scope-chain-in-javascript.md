---
layout: post
comments: true
title:  "Scope Chain in javascript"
description: "Understanding scope chain in javascript"
keywords: "JS, Javascript"
date: 2020-05-06
categories: [JS, Javascript]
author: Manjunath Hugar
---

Let's take a look at the following code:
```
function bar() {
    console.log(someVar);
}
function foo() {
    var someVar = 10;
    bar()
}
var someVar = 20;
foo()
```
What do you think will be printed? some of you may say it will print `undefined` because `someVar` is not defined inside the function `bar` or some of you may also say that it should print 10 because the function `bar` is called from inside the function `foo` and if some of you have guessed it right! the answer is `20`!.


Let's see what exactly is happening behind the scenes -

![](/assets/images/scope-chain/execution-context.png) 

Javascript maintains a stack of *Execution Context*, when the JS engine runs the above code, it creates a *Global Execution Context* and stores the function declarations and variables inside that (we will discuss about hoisting in another blog).
So in this case, variable `someVar` and the functions `foo` and `bar` are stored in the global execution context and wherever it encounters the function invocation (foo() in the above example), it creates a new execution context and this new execution context is placed above the global context.

Execution context for `foo()` will contain the `var someVar = 10` and also creates the execution context for `bar()` when the function bar is invoked and since no variables are declared inside the bar function, bar's execution context do not contain any variables.

Another important thing JS engine does is, it also stores the reference to its outer environment, so in our example the outer environment for `function bar` is the global execution context and as mentioned above, the global execution context has variable `someVar = 20` stored inside it.

When JS runs `console.log(someVar)`, it first checks the bar's execution context to see if someVar is stored in it, since someVar is not available in the bar's execution context it then checks its outer environment which is global execution context in our example, so it gets the value 20 from its outer environment and prints the value 20.

So lets now make some changes in our code and declare the function bar inside the function foo - 

```
function foo() {
    function bar() {
        console.log(someVar);
    }
    var someVar = 10;
    bar()
}

var someVar = 20;
foo()
```

As usual, JS engine creates the global execution context and stores the `function foo` and the `var someVar = 20` but doesn't store the `function bar`.

![](/assets/images/scope-chain/execution-context-2.png) 

How can we verify this? well, try calling the `function bar` from outside the `function foo` and the javascript will throw an error `Uncaught ReferenceError: bar is not defined`.

This is because in the execution stack, the outer environment for the `function bar` is now the `function foo`, because the function bar is now physically inside the function foo.

When the function foo is invoked, JS creates an execution context for function foo() and stores the variable someVar = 10, similarly another execution context for function bar is created and it doesn't contain any variables inside it since no variables are declared in function bar.

But now the outer environment for function bar is the function foo, that means the function bar holds the reference to foo()'s execution context and the outer environment to function foo is still the global context.


So now when JS runs `console.log(myVar)`, the following happens - 
* It looks for someVar in bar's execution context which is not available in our case.
* Then traverses down to its outer environment(foo()'s execution context) and finds the var someVar = 20 and prints that. 

If in our example if `someVar` is not defined in the function foo(), then it goes one level down and looks for the variable `someVar` in the global execution context. The variable look up the JS engine does from the top of the stack to all the way down at the global execution context is called the `Scope Chain`. 










