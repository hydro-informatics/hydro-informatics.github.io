---
title: Advanced Python - Object Orientation and Classes
keywords: python
summary: "Leverage the power of Python by writing new classes."
sidebar: mydoc_sidebar
permalink: hypy_classes.html
folder: python-advanced
---

## The class of classes

Python is an inherently object-oriented language and makes the deployment of classes and objects extremely easy. Let's start with essential definitions.

### What is object-oriented programming (OOP)?

Object-Oriented Programming (OOP) is a programming paradigm that aligns the architecture of software with reality. Object orientation starts with the design of software, where a structured model is established. The structured model contains information about objects and their abstractions. The development and implementation of object-oriented software requires a structured way of thinking and the conceptual understanding of classes, inheritance and polymorphism.


### Objects and classes
In computer language, an **object** is an instance that contains data in the shape of fields (called *attributes* or *properties*) and code in the shape of features (*functions* or *methods*). The features of an object enable access (read) and manipulation of its data fields. Objects have a concept of `self` regarding their attributes, methods and data fields. `self` internally references attributes, properties or methods belonging to an object.

In *Python*, an object is an instance of a class. Thus, a **class** represents a blueprint for many similar objects with the same attributes and methods. A class does not use system memory and only its instance (i.e., objects) will use memory.

{% include image.html file="classes_objects.png" caption="Illustration of an IceCream class and to instances (objects) of the IceCream class." %}

### Inheritance

### Polymorphism




## Decorators {#dec}
Ref. functions.


## Magic methods {#magic}

Did you already wonder why the same operator has different effects depending on the variable type?

For example:


```python
a_string = "vanilla"
b_string = "cream"
print("+ operator applied to strings: " + str(a_string + b_string))

a_number = 50
b_number = 30
print("+ operator applied to integers: " + str(a_number + b_number))
```

    + operator applied to strings: vanillacream
    + operator applied to integers: 80
    

This behavior is called operator (or function) overloading in *Python*. Overloading is possible because of pre-defined names of *magic methods* in *Python*.

Magic methods are one of the key elements that make *Python* easy and clear to use. Because of their declaration using double underscores (`__this_is_magic__`), magic methods are also called *dunder* (**d**ouble **under**score) methods. Magic methods are special methods with fixed names and their *magic* name is because they do not need to be directly invoked. Behind the scenes, *Python* constantly uses *magic* methods, for example when a new instance of a class is assigned: When you write `var = MyClass()`, *Python* automatically calls `MyClass`'es `__init__()` and `__new__()` *magic* methods. Magic methods also apply to any operator or (augmented) assignment. For example, the `+` binary operator makes *Python* look for the magic method `__add__`. Thus, when we type `a + b`, and both variables are instances of `MyClass`, *Python* will look for the `__add__` method of `MyClass` in order to apply `a.__add__(b)`. If *Python* cannot find the `__add__` method in `MyClass`, it returns a `TypeError: unsupported operand`.  

The following sections list some documented magic methods for use in classes and packages in tabular format. The tables provide the most common magic methods and more documented magic objects or attributes exist. 

### Operators (Binary)

| Operator | Method                                       |
|----------|----------------------------------------------|
| `+`        | `object.__add__(self, *args, **kwargs)`      |
| `-`        | `object.__sub__(self, *args, **kwargs)`      |
| `*`        | `object.__mul__(self, *args, **kwargs)`      |
| `//`       | `object.__floordiv__(self, *args, **kwargs)` |
| `/`        | `object.__truediv__(self, *args, **kwargs)`  |
| `%`        | `object.__mod__(self, *args, **kwargs)`      |
| `**`       | `object.__pow__(self, *args, **kwargs)`      |
| `<<`       | `object.__lshift__(self, *args, **kwargs)`   |
| `>>`       | `object.__rshift__(self, *args, **kwargs)`   |
| `&`        | `object.__and__(self, *args, **kwargs)`      |
| `^`       | `object.__xor__(self, *args, **kwargs)`      |
| `|`        | `object.__or__(self, *args, **kwargs)`       |

***

### Operators (Unary)

Unary operators deal with only one input in contrast to the above listed binary operators. Unary operators is what we typically use to increment or decrement variables with for example `++x` or `--x`.

| Operator  | Method                     |
|-----------|----------------------------|
| `-`         | `object.__neg__(self)`     |
| `+`         | `object.__pos__(self)`     |
| `abs()`     | `object.__abs__(self)`     |
| `~`         | `object.__invert__(self)`  |
| `complex()` | `object.__complex__(self)` |
| `int()`     | `object.__int__(self)`     |
| `long()`    | `object.__long__(self)`    |
| `float()`   | `object.__float__(self)`   |

***

### Operators (Comparative)

| Operator | Method                                 |
|----------|----------------------------------------|
| `<`        | `object.__lt__(self, *args, **kwargs)` |
| `<=`       | `object.__le__(self, *args, **kwargs)` |
| `==`       | `object.__eq__(self, *args, **kwargs)` |
| `!=`       | `object.__ne__(self, *args, **kwargs)` |
| `>=`       | `object.__ge__(self, *args, **kwargs)` |
| `>`        | `object.__gt__(self, *args, **kwargs)` |

***

### Assignments 

| Operator | Method                                        |
|----------|-----------------------------------------------|
| `+=`       | `object.__iadd__(self, *args, **kwargs)`      |
| `-=`       | `object.__isub__(self, *args, **kwargs)`      |
| `*=`       | `object.__imul__(self, *args, **kwargs)`      |
| `/=`       | `object.__idiv__(self, *args, **kwargs)`      |
| `//=`      | `object.__ifloordiv__(self, *args, **kwargs)` |
| `%=`       | `object.__imod__(self, *args, **kwargs)`      |
| `**=`      | `object.__ipow__(self, *args, **kwargs)`      |
| `<<=`      | `object.__ilshift__(self, *args, **kwargs)`   |
| `>>=`      | `object.__irshift__(self, *args, **kwargs)`   |
| `&=`       | `object.__iand__(self, *args, **kwargs)`      |
| `^=`       | `object.__ixor__(self, *args, **kwargs)`      |
| `|=`       | `object.__ior__(self, *args, **kwargs)`       |

***

A rather old (*Python* 2-based), but comprehensive and inclusive summary of magic methods is provided by [Rafe Kettler](https://rszalski.github.io/magicmethods/).

### Overloading custom *Python* classes

In order to make your own custom functions capable of using operators, maybe in a slightly different way, magic methods need to be implemented. The standard magic methods that a custom class should have are:

* `__init__(self, [...)` is the class initializer, which is called when an instance of the class is created. More precisely, it is called along with the `__new__(cls, [...)` method, which is rarely used (read more at [python.org](https://docs.python.org/3/reference/datamodel.html?highlight=__new__%20method#object.__new__)). The initializer gets the arguments passed with which the object was called. For example when `var = MyClass(1, 'vanilla' )`, the `__init__(self, [...)` method gets `1` and `'vanilla'`.
* `__call__(self, [...)` enables to call a class instance directly, for example `var('cherry')` (corresponds to `var.__call__('cherry')`) may be used to change from `'vanilla'` to `'cherry'`.

As a result, a robust class skeleton looks like this:


```python
class NewClass:
    def __init__(self, *args, **kwargs):
        pass
    
    def __call__(self, *args, **kwargs):
        # example prints class structure information to console
        print("Class Info: <type> = NewClass (%s)" % os.path.dirname(__file__))
        print(dir(self))
```

## Public and non-public attributes

Public attributes are any attributes that you expect to be used by unrelated clients (variables) of your class. Such attributes can be changed externally.

Non-public attributes are not intended to be used by third parties. Although non-public attributes cannot usually be changed externally, there are no guarantees that non-public attributes will nevertheless be changed or even removed. Non-public attributes should be named with a leading underscore (e.g., `_non_public_method` - see the [style guide](hypy_pystyle.html#object-styles)) .
