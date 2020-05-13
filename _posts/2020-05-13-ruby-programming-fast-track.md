---
layout: post
comments: true
title:  "Learn Ruby Programming Fast Track"
description: "A quick way to learn the ruby programming language with examples"
keywords: "ruby, programming"
date: 2020-05-13
categories: [Ruby, Programming]
author: Anjaneyulu Batta
---

## Introduction to Ruby

* Ruby is an object oriented programming language
* Ruby was created by Yukihiro Matsumoto, or "Matz", in Japan in the mid 1990's.
* 

## Ruby Installation in Ubuntu

Let's install the **ruby** on ubuntu with the below command

```
sudo apt-get install ruby-full
```

Let's confirm the ruby installation with command `ruby -v`

```
$ ruby -v
ruby 2.7.0p0 (2019-12-25 revision 647ee6f091) [x86_64-linux-gnu]
```

## Ruby "Hello World" Program

Let's print the `Hello World` with ruby

**file: hello_world.rb**

```ruby
puts "Hello World"
```

**.rb** is file extension for the ruby program files.

Let's run the above program on terminal with command `ruby hello_world.rb` and we will get the output like below

```ruby
Hello World
```

## Declaring Variables in Ruby

As ruby is dynamic programming language, we don't need to specify the types while declaring the variables.
Variables can hold the data types like string, boolean, integers, floating point numbers, arrays, objects, etc.

Let's declare declare the variables in the below code.

```
number = 150
pi = 3.141
name = "Agiliq info solutions"
student_names = ["John", "David", "Shera", "Anna"]
is_ruby_awesome = true
```

## Data Types in Ruby
In ruby we have below data types

* Numbers
  * Integers
  * Floating point numbers

Example:

```ruby
num1 = 456
num2 = 1235.56
```
We also have numbers like complex numbers but we use them rarely.

* Strings: Collection of characters. Most of the data is represented in the strings

Example:

```ruby
name = "Roman Reigns"
```

* Symbols: Symbols are light-weight strings. A symbol is preceded by a colon (`:`)

Example:

```ruby
name = :Michael
country = :India
```

* Hashes: Used to represent the key value pairs

Example:

```ruby
country_name_codes = {"India" => "IN", "America": "USA", "Bangladesh": "BD", "Srilanka": "SL"}
```
We can also use data like integers, symbols and other data types in **Hashes**

* Arrays: Used to store the collection of non-homogenious data elements

Example: 

```ruby
collection = ["Google", 250.5, true]
```

* Booleans: Used represent the truth values

```ruby
valid = true
invalid = false
```

## Working With Strings in Ruby

### string contactenation

```ruby
first_name = "John"
last_name = 'Hendry'

puts ("Full Name is " + first_name + " " + last_name)
```

### convert string to upper case

```ruby
name = "John Hendry"
upper_case = name.upcase
puts (upper_case)
```

### convert string to lower case

```ruby
name = "John Hendry"
down_case = name.downcase
puts (down_case)
```

### String interpolation in ruby

```ruby
first_name = "John"
last_name = "Hendry"
full_name = "#{first_name} #{last_name}"
puts full_name
```

## Getting User Input

In ruby we can get the input from the user with keyword `gets`. It also includes the new line when we hit the `enter` key.
To avoid it we use `gets.chomp()` which will remove the new line. Let's see an example

```ruby
print "Enter your name: "
name = gets.chomp()
print("Hello #{name}: ")
```
Output:

```
Enter your name: Google                                                                                                                                                     
Hello Google
```

## print vs puts in Ruby

`print` doesn't include the new line character but `puts` does. It's the only difference.

## Arrays in Ruby

* Array are containers which holds the ruby objects which includes numbers, strings, booleans, etc.
* It holds the objects in an order
* We can access array elements with indexes and index always starts with `0`
* We can also access array elements with negative indexes and negative index starts with `-1`

### How to create array ?

We can create array in two ways in ruby

```ruby
empty_array1 = Arra.new()
empty_array2 = []

puts empty_array1
puts empty_array2
```

We will get empty output because we didn't have any elements in the array.

let's create array with initial elements

```ruby
array1 = Array.new([1,2,3])
array2 = ["one", "two", "three"]

puts array1
puts array2
```

Output:

```
1
2
3                                        
one
two
three 
```

### How to insert elements into an array ?

We can insert elements into an array with square bracket notation. Let's see an example

```ruby
array = []
array[0] = 1
array[1] = 2
array[2] = "hello"

puts array
```

Output:

```
1
2
hello
```

### How to get element from an array ?

We can get an element from an array using the indexes. Let's see an example

```ruby
planets = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus"]
earth = planets[2]
puts ("Our Planet is #{earth}")
```

Output:

```
Our planet is Earth
```

### How to delete element form an array ?

We can delete an element in array with it's index by using the method `delete_at`. Let's see an example.

```ruby
numbers = [1,2,3,4,5]
numbers.delete_at(1)
puts numbers
```
Above code will remove the element `2` whose index is `1`

Output:

```
1
3
4
5
```

We can also delete the last element in an array using method `pop`

```ruby
numbers = [1,2,3,4,5]
numbers.pop()
puts numbers
```

Output:

```
1
2
3
4
```

### How to get slice of an array ?

We can also get a slice of a given array with **start** and **end** indexes. Let's see an example

```ruby
a = [1,2,3,4,5,6,7,8,9]
slice = a[0, 5]

puts slice
```

Output: 

```
1
2
3
4
5
```

We can also do it with **slice** method of an array like below

```ruby
a = [1,2,3,4,5,6,7,8,9]
slice = a.slice(0, 5)
puts slice
```
It will also give the output same as above.


### How to get index of an element in an array?

We can use the `find_index` method of array to get the index. Let's see an example below

```ruby
a = [1,2,3,4,5,6,7,8,9]
index = a.find_index(9)
puts index
```

Output

```
8
```

## Hash data structure in Ruby

Hash is data structure in ruby it stores the data in the form of key and value.

### Creating Hash in Ruby

```ruby
empty_hash = Hash.new
empty_hash1 = {}
student = {"name" => "David", "age": 20}
```

### How to add element to Hash ?

```ruby
numbers = {}
numbers[1] = "one"
numbers[2] = "two"
numbers[3] = "three"

puts numbers
```

Output:

```
{1=>"one", 2=>"two", 3=>"three"}
```
We can add elements to the hases like above.

### How to access an element in a Hash ?

We can access the element in a has using square bracket like below

```ruby
numbers = {1 => "one", 2 => "two"}

num_one = numbers[1]

puts num_one
```

Output:

```
one
```

### How delete a element in a Hash ?

We have `delete` method on Hash to do it.

```ruby
numbers = {1 => "one", 2 => "two"}
numbers.delete(2)

puts numbers
```

Output:

```
{1 => "one"}
```

### How to update an eement in a Hash ?

We can do that like below

```ruby
numbers = {1 => "one"}
numbers[1] = "two"

puts numbers
```

Output:

```
{1 => "two"}
```

## Methods or Functions

A method or a function is a block of that can perform a specific task. In ruby we define method with keyword "def".

Let's see an example function that prints "hello".

```ruby
def say_hello
  puts "hello"
end
```

### Function or Method with return type

Let's write a math funtion that return cube for a given number

```ruby
def cube(num)
  return num * num * num
end

# call the function

output = cube(3)
puts output
```

Output: 

```
27
```

A method always have scope within `def` and `end` keywords. Unless we call the function it won't execute.

## If/Else Statements in Ruby

If and else statements are used to decide the conitional functionality. Let's take a simple scenario of university grades.

> "If student gets a cgpa > 8.5 out of 10 then he/she can get a gift"

Let's write the code for that scenario

```ruby
puts "Enter student cgpa: "
cgpa = gets.chomp().to_f

if cgpa > 8.5
  puts "Eligible for gift"
else
  puts "Not eligible for Gift"
end
```

Output:

```
Enter student cgpa:
7.2

Not eligible for Gift
```



## Building a Better Calculator with If/Else

## Case Expressions

## While Loops

## Building a Guessing Game

## For Loops

## Comments

## Reading Files

## Writing Files

## Handling Errors / Exceptions

## Classes & Objects

## Initialize Method

## Object Methods

## Building a Quiz

## Inheritance

## Ruby Modules

## Interactive Ruby (irb)

Ruby comes with the program called `irb` which allows us to instatly write and execute the `ruby` code. Let's do that by using the command `irb` in the terminal it will bring the interactive console like below

```ruby
rb(main):001:0> puts "Hello"
Hello
=> nil
irb(main):002:0> 

```

That's it folks. Let's learn more about **ruby** and it's framework **rails** in coming up articles.
