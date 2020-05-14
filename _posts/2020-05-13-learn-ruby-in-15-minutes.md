---
layout: post
comments: true
title:  "Learn ruby in 15 minutes"
description: "A quick way to learn the ruby programming language with examples"
keywords: "ruby, programming"
date: 2020-05-13
categories: [Ruby, Programming]
author: Anjaneyulu Batta
---

## Introduction to Ruby

* Ruby is popular
* Ruby is an object oriented programming language
* Ruby was created by Yukihiro Matsumoto, or "Matz", in Japan in the mid 1990's.
* Ruby has good community support

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

```ruby
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

## Array data structure in Ruby

* Array are containers which holds the ruby objects which includes numbers, strings, booleans, etc.
* It holds the objects in an order
* We can access array elements with indexes and index always starts with `0`
* We can also access array elements with negative indexes and negative index starts with `-1`
* Negative indexes works in reverse order. `-1` index returns the last value of the array.

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

### How to update an element in a Hash ?

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

Example2: string comparison with if else

```ruby
def str_cmp(s1, s2)
  if s1 > s2
    return 1
  elsif s1 == s2
    return 0
  else
    return -1
  end
end

s1 = "hi"
s2 = "hello"

out = str_cmp(s1, s2)
puts out
```

Output: 

```
1
```

## Building Calculator with If/Else

Let's implement the basic calulator with if else conditions.

```ruby
def calculate(a, op, b)
  if op == "+"
    return a + b
  elsif op == "-"
    return a - b
  elsif op == "/"
    return a / b
  elsif op == "*"
    return a * b
  else
    return "Invalid operator"
  end
end


puts "Enter num1: "
num1 = gets.chomp().to_f
puts "Enter operator one of + - * /  : "
op = gets.chomp()
puts "Enter num2: "
num2 = gets.chomp().to_f

out = calculate(num1, op, num2)

puts out
```

Output:

```
Enter num1:
10
Enter operator one of + - * /  : 
+
Enter num2: 
20

30.0
```

## Case Expressions in Ruby

Case expression are shorter forms of the `if/else` conditions.

Let's re-modify the above calculator with the case expressions

```ruby
def calculate(a, op, b)
  case op
  when "+"
    return a + b
  when "-"
    return a - b
  when "/"
    return a / b
  when "*"
    return a * b
  else
    return "Invalid operator"
  end
end

puts "Enter num1: "
num1 = gets.chomp().to_f
puts "Enter operator one of + - * /  : "
op = gets.chomp()
puts "Enter num2: "
num2 = gets.chomp().to_f

out = calculate(num1, op, num2)

puts out
```

In the above code we have replaced the if/else conditions with the `case`. We can see that it's shorter than the if/else statements.

## While Loop in Ruby

while loop is used to iterate the a block of statements until some condition is met. Let's write a simple while loop that can print the numbers from `1` to `10`.


```ruby
num = 1

while num <= 10
  puts num
  num += 1
end
```

Output:

```
1
2
3
4
5
6
7
8
9
10
```

## Building a Guessing Game

Let's build a guessing game with the `while` loop. User has to guess the number within 3 attempts. Let's code it

```ruby
guess = 3
attempts = 3

success = fase
while !success and attempts > 0
  num = gets.chomp().to_i
  if num == guess
    sucess = true
  end
end

if success:
  puts "You guessed correctly within 3 attempts"
else
  puts "Invalid guess"
```

Output:

```
Enter your guess number:
10
Enter your guess number:
20
Enter your guess number:
3
You guessed correctly within 3 attempts
```

## For Loop in Ruby

For loop is mostly used to iterate elements in arrays or hashes.

Example1:

```ruby
names = ["David", "Anna", "Shera", "John"]

for name in names
  puts name
end
```

Example2:

```ruby
names = ["David", "Anna", "Shera", "John"]

names.each do |name|
  puts name
end
```

## How to write Comments in Ruby ?

We can write comments in two ways

### Single line comment

```ruby
# this is single line comment
```

### Multiline comment

```ruby
=begin
this
is
multiline
comment
=>
```

## Reading Files in Ruby

While reading and writing files we have to provide the file full path or realative path and the file mode. We have the following file modes.

* reading : `r`
* write : `w`
* append : `a`

Example1:

```ruby
File.open("test.txt", "r") do |file|
  puts file.read()
end
```

Example2:

```ruby
file = File.open("test.txt", "r")
for line in file.readlines()
  puts line
end
file.close()
```

## Writing data to Files in Ruby

We can write to files using the write mode `w`. If we open file with `a` then we can read from the file and write to the file.

```ruby
File.open("test.txt", "w") do |file|
  file.write("line1\n")
  file.write("line2\n")
  file.write("line3\n")
end
```

## Raising Exception in Ruby

We can raise exceptions using the keyword `raise`.

Example:

```ruby
def div(n1, n2)
  if n2 == 0
    raise ZeroDevisionError
  end
  return n1/n2
end
```

## Handling Exception in Ruby

We may get errors on run time then we can handle it with `rescue` keyword.

Example:

```ruby
def div(n1, n2)
  if n2 == 0
    raise ZeroDevisionError
  end
  return n1/n2
end


begin
  puts div(10, 0)
rescue ZeroDevisionError
  puts "Error occured"
end
```

* We can use multiple rescue statements based on the error type

## Classes & Objects in Ruby

Everything is an object in ruby. A class is a blue print for an object. A class can have attributes or methods or both.s

### Class Example

```ruby
class Book
  attr_accessor :title, :author, :pages
end

obj = Book.new()

obj.title = "Harry Potter"
obj.author = "J. K. Rowling"
obj.pages = 223

puts obj.title
```

### Variables in Ruby Class

* **Local Variables**: Local variables are the variables that are defined in a method. Local variables are not available outside the method. 
* **Instance Variables**: instance varialbes availabe to use once the object is created. These always starts with `@`
* **Class variables**: Can be accessable across different objects. These always starts with `@@`.
* **Global Variables**: These varibles available across the classes and always start with `$`

## Initialize Method

It will difficult for us to update the data for an object every time when we create an object. So, to make it simplify we use a method `initialize`. It always called when an object is created. Let's re-write the above book class with `initialize method`.

```ruby
class Book
  attr_accessor :title, :author, :pages

  def initialize(title, author, pages)
    @title = title
    @author = author
    @pages = pages
  end
end

obj = Book.new("Harry Potter", "J. K. Rowling", 223)

puts obj.title
```

We can see that it's very easy compare to the above approach

## Class & Methods in Ruby 

We can have multiple methods on a class. Let's see an example for Circle

```ruby
class Circle
  attr_accessor :radius

  def initialize(radius)
    @radius = radius
  end

  def area
    return 3.14 * @radius * @radius
  end

  def perimeter
    return 2 * 3.14 * @radius
  end
end

obj = Circle.new(5)

puts obj.area # output: 78.5
puts obj.perimeter  # output: 31.400000000000002
```
In above code, we have written a class for `Circe`. Circle takes radius and creates an object and calculates it's perimeter, area.
We can have multiple objects for the same class.

## Inheritance in Ruby 

We use the inheritance oncept in Ruby. But we can only have single parent. Ruby doesn't allow multiple inheritance(i.e class A cannot have both parent classes B, C). But we can achieve that kind of functionality with modules.
Let's see an example for the class.

```ruby
class Animal
  attr_accessor :name, :color

  def initialize(name, color)
    @name = name
    @color = color
  end

  def speak
    puts "Huuuu"
  end

end

class Cat < Animal

  def walk
    puts "I can walk with my four legs"
  end

end

obj = Cat.new("Sammy", "white")

puts obj.name  # Out: Sammy
puts obj.speak # Out: Huuuu
puts obj.walk  # I can walk with my four legs
```

We use `<` symbol to inherit the class. We can implement the additional methods and can override the existing methods of parent classs by re-defining the method in the child class.

## working with Ruby Modules

By usng modules we can group the methods, classes and constants. It will allow us to group the related functionality into a single unit. We can import and use the module in other ruby programs

### Module Usage

file: math.rb

```ruby
module MyMath
  PI = 3.14

  def Circle_area(r)
    return PI * r * r
  end
end
```

file: util.rb

```ruby
require "./math.rb"
include MyMath

puts MyMath::PI               # Out: 3.14
puts MyMath.circle_area(5)    # Out: 78.5
```

### Using modules as mixins in Ruby classes

```ruby
module Introspect
  def kind
    puts "This object is a #{self.class.name}"
  end
end

class Animal
  include Introspect
  def initialize(name)
    @name = name
  end
end

class Car
  include Introspect
  def initialize(model)
    @model = model
  end
end

c = Car.new("Ferrari")
d = Animal.new("Cat")

c.kind  # Out: This object is a Car
d.kind  # Out: This object is a Animal
```

We can make use of mixins like above in ruby programming. Modules are one of the finest features in ruby.

## Interactive Ruby (irb)

Ruby comes with the program called `irb` which allows us to instatly write and execute the `ruby` code. Let's do that by using the command `irb` in the terminal it will bring the interactive console like below

```ruby
rb(main):001:0> puts "Hello"
Hello
=> nil
irb(main):002:0> 

```

That's it folks. Let's learn more about **ruby** and it's framework **rails** in coming up articles.
