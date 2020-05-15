---
title: Python Basics - Functions
keywords: git
summary: "Leverage the power of code recycling with functions."
sidebar: mydoc_sidebar
permalink: hypy_pyfun.html
folder: python-basics
---

## What are functions?

Functions are a convenient way to divide code into handy, reusable and better readable blocks, which help structuring code. Blocks can accept parametric arguments and can be reused. Thus, functions are a key element for sharing code.
	
* The `def` keyword followed by a function name with *arguments* in parentheses and a code block is what defines a function.
* The type of *arguments* that a functions can receive are:
    - Required arguments: `argument_name`
    - Optional arguments: `*args`
    - Optional keyword arguments: `**kwargs`

Using optional (keyword) arguments makes functions more robust and flexible. The code block of a function is indented, similar to loops: 


```python
def my_function(argument1, *args, **kwargs):
    something = f(arguments)
    return something
```

## A basic example
Three countries on earth use imperial units, while most other countries use the *Système International* (*French: International System*) of units (SI units). Let's write a simple function to help imperial unit users converting *feet* (imperial) to *meter* (SI).

In the following example, the function name is `feet_to_meter` and the function accepts one argument, which is `feet`. The function returns the `feet` argument multiplied with 0.3048, which corresponds to the conversion factor from feet to meters.



```python
def feet_to_meter(feet):
    return 0.3048 * feet
```

## Function calls

In order to call a function, it must be defined before the call. The function may be defined in the same script or in another script, which can than be imported as module ([read more about modules and packages in the next section](hypy_pckg.html)). Then we can call, for example, the above-defined `feet_to_meter` function as follows:


```python
feet_value = 10
print("{0} feet are {1} meters.".format(feet_value, feet_to_meter(feet_value)))
```

    10 feet are 3.048 meters.
    

## Extended functionality
Let's extend the above function.
The variable will not be available outside of the function.


```python
def feet_to_meter(feet, *args):
    conv = 0.3048
    return conv * feet
```
