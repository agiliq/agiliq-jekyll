---
layout: post
comments: true
title:  "TypeScript in 10 minutes"
description: "A quick introduction to typescript and it's usage"
keywords: "A quick introduction to typescript and it's usage"
date:   2019-07-09
categories: [typescript, microsoft, javascript]
author: Anjaneyulu Batta
---
`TypeScript` is object oriented programming language developed by `MicroSoft`. We can say that `TypeScript` is a superset of `javascript` because it supports all of it's functionality and provides more efficient ways to write less code to implement complex functionality.
File extension for `TypeScript` is `.ts`. We need a `TypeScript` compiler to convert the `.ts` files into a `JavaScript` code.

# Why TypeScript ?
  - TypeScript is opensource.
  - It simplifies the `javascript` code and speed-up the development and debugging.
  - TypeScript gives us all the benefits of ES6 (ECMAScript 6), plus more productivity.
  - TypeScript helps us to avoid painful bugs that developers commonly run into when writing JavaScript by type checking the code.
  - TypeScript is a superset of ES3, ES5, and ES6. Hence, it supports all ES3, ES5, and ES6 features.
  - Supports object-oriented programming.
  - It has features like Interfaces, Generics, Inheritance, and Method Access Modifiers
  - It needs to be compiled to javascript before releasing it into production so, it throws syntatical errors if any which makes bug fixing easier.

# Installing TypeScript
We can install `TypeScript` with node package manager `npm` using below command.
```sh
sudo npm install -g typescript
# check installation
tsc --version
```
# Writing first TypeScript program
Let's write our very first `TypeScript` program (File: `helloUser.js`)
```ts
function helloUser(user: string){
  return `Hello ${user}`
}
let msg = helloUser('Agiliq');
console.log(msg);
```
  - **Compiling the TypeScript to JavaScript**

    - Let's compile the above code `helloUser.js` with command `tsc`
```ts
  tsc helloUser.ts
```
    - Above command generates a javascript file `helloUser.js` and the compiled code looks like below.
```javascript
function helloUser(user) {
    return "Hello " + user;
}
var msg = helloUser('Agiliq');
console.log(msg);
```

  - **Executing javascript with node**
    - Let's run compiled javascript code with command `node` in terminal.
    ```sh
    node helloUser.js
    # Output: Hello Agiliq
    ```

# A note about `let`
  - The let keyword is a newer JavaScript construct that `TypeScript` makes available. `let` an alternative for javascript keyword `var`. In future releases of javascript `var` may completely replaced with `let`. So, it's recommended to use the keyword `let` instead `var`. 

# Data Types in TypeScript
  * **Boolean**: Used for boolean values like `true` or `false`
    ```ts
    let isReady: boolean = false;
    let isDone: boolean;
    ```
  * **Number**: User for numeric data types.
    ```ts
    let decimal: number = 6;
    let hex: number = 0xf00d;
    let binary: number = 0b1010;
    let octal: number = 0o744;
    ```
  * **String**: Used to represent the text data.
    ```ts
    let title: string = 'Hello Agiliq';
    let location: string = "Hyderabad";
    let concat: string;
    concat = `${title} , ${location}`;
    console.log(concat);
    // output: Hello Agiliq , Hyderabad
    ```
    - Note: use backtick (&nbsp;`&nbsp;&nbsp;) for string formatting only.
  * **Array**: TypeScript, like JavaScript, allows you to work with arrays of values.
    - Homogeneous elements of array
    ```ts
    let list: Array<number> = [1, 2, 3];
    // valid re-assignment
    list = [5, 6, 7];
    // invalid
    // list = ["hi", "hello"];
    ```
      - It will throw an error if you try to assign a non-numeric element because of it's type definition.
    - Non-Homogeneous elements of array;
     ```ts
    let list: Array<any> ;
    // valid re-assignment
    list = [5, 6, 7];
    // valid re-assignment
    list = ["hi", "hello"];
    ```
  * **Tuple**: Tuple types allow you to express an array with a fixed number of elements whose types are known, but need not be the same.
    ```ts
    // Declare a tuple type
    let x: [string, number];
    // Initialize it
    x = ["hello", 10]; // OK
    // Initialize it incorrectly
    x = [10, "hello"]; // Error
    ```
  * **Enum**: As in languages like C#, an enum is a way of giving more friendly names to sets of numeric values.
  ```ts
  enum Color {Red, Green, Blue}
  // Red = 0, Green = 1, Blue = 2 
  let c: Color = Color.Green;
  console.log(c)
  // output: 1
  ```
  * **Any**: It can be used for un-know datatype. So, supports all data types.
  ```ts
  let notSure: any = 4;
  notSure = "maybe a string instead";
  notSure = false; // okay, definitely a boolean
  ```
  * **Void**: void is a little like the opposite of any: the absence of having any type at all.
  ```ts
  function warnUser(): void {
    console.log("This is my warning message");
  }
  ```
    - Note: `void` data type allows only `undefined` or `null` values for assignment.

  * **Never**: The never type represents the type of values that never occur.
    ```ts
    // Function returning never must have unreachable end point
    function error(message: string): never {
        throw new Error(message);
    }

    // Inferred return type is never
    function fail() {
        return error("Something failed");
    }
    ```
    - It can be used for cases like above code.

  * **Object**: object is a type that represents the non-primitive type.
    ```ts
    let employee: Object = {name: "John", designation: "Developer"};
    ```

# using Classes
  - Class allows developers to use object oriented concepts like inheritance, encapsulation, abstraction and polymorphism.
  - keyword `extends` used to implement the inheritance concept in TypeScript.
  - Let's take a look at a simple class
  ```ts
    class Person{
        firstName = "";
        lastName = "";
        constructor(firstName: string, lastName: string){
          this.firstName = firstName;
          this.lastName = lastName;
        }
        fullName(){
          return `${this.firstName} ${this.lastName}`
        }
    }
    let p = new Person("John", "Snow");
    console.log("Name: ", p.fullName());
    // output: Name:  John Snow
  ```
  - **Inheritance**:
    - Let’s take a look at an example:
    ```ts
      class Animal {
          move(distanceInMeters: number = 0) {
              console.log(`Animal moved ${distanceInMeters}m.`);
          }
      }

      class Dog extends Animal {
          bark() {
              console.log('Woof! Woof!');
          }
      }

      class Human extends Animal {
          talk() {
              console.log('Hello World! I\'m Chitti!');
          }
      }

      const dog = new Dog();
      dog.move(10);
      dog.bark();

      const human = new Human();
      human.move(100)
      human.talk()
    ```

# using Interfaces
  - An `interface` is a specification that defines a related set of methods and properties to be implemented by a class/function.
  - Keyword `interface` to define an interface.
  - Let’s take a look at simple examples:
    ```ts
    // class using an interface
    interface ClockInterface {
      currentTime: Date;
      setTime(d: Date): void;
    }
    class Clock implements ClockInterface {
      currentTime: Date = new Date();
      setTime(d: Date) {
          this.currentTime = d;
      }
      constructor(h: number, m: number) { }
    }
    // function using an interface
    interface LabeledValue {
      label: string;
    }

    function printLabel(labeledObj: LabeledValue) {
        console.log(labeledObj.label);
    }

    let myObj = {size: 10, label: "Size 10 Object"};
    printLabel(myObj);
    ```

# using Decorators
  - A Decorator is a special kind of declaration that can be attached to a class declaration, method, accessor, property, or parameter.
  - A Decorators may or may not receive arguments based it's declaration.
  - Example:
  ```ts
    function course(target) {
      Object.defineProperty(target.prototype, 'course', {value: () => "Angular"})
    }

    @course
    class Person {
        firstName;
        lastName;

        constructor(firstName, lastName) {
            this.firstName = firstName;
            this.lastName = lastName;
        }
    }
    let asim = new Person("Alex", "W");
    console.log(asim.course());
    //output: Angular
  ```
  - In above code `course` is a decorator which sets property `course` to the decorated class `Person` when it is initialized.

We have covered basic concepts of `TypeScript`. You can refer below link for more information.

*Reference: <a href="https://www.typescriptlang.org/docs/home.html" __target="blank">https://www.typescriptlang.org/docs/home.html</a>*