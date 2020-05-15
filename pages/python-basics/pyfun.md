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
    - Required arguments: `arg`
    - Default keyword arguments (with default values): `arg=value`
    - Optional arguments: `*args`
    - Optional keyword arguments: `**kwargs`

Using optional (keyword) arguments makes functions more robust and flexible. The code block of a function is indented, similar to loops: 


```python
def my_function(argument1, *args, **kwargs):
    something = f(arguments)
    return something
```

## A basic example
Three countries on earth use imperial units, while most other countries use the *Système International* (*French: International System*) of units (SI units). Let's write a simple function to help imperial unit users converting *feet* (imperial) to *meters* (SI).

In the following example, the function name is `feet_to_meter` and the function accepts one argument, which is `feet`. The function returns the `feet` argument multiplied with a `conversion_factor` of 0.3048, which corresponds to the conversion factor from feet to meters. In this simple example the definition of the `conversion_factor` variable is not explicitly required.

{% include note.html content ="Internal variables (i.e., variables defined within a function), such as `conversion_factor`, are not accessible outside of the function." %}



```python
def feet_to_meter(feet):
    conversion_factor = 0.3048
    return conversion_factor * feet
```

## Function calls

In order to call a function, it must be defined before the call. The function may be defined in the same script or in another script, which can than be imported as module ([read more about modules and packages in the next section](hypy_pckg.html)). Then we can call, for example, the above-defined `feet_to_meter` function as follows:


```python
feet_value = 10
print("{0} feet are {1} meters.".format(feet_value, feet_to_meter(feet_value)))
```

    10 feet are 3.048 meters.
    

## Optional arguments *args
Let's replace the non-optional `feet` argument in the above function with an optional argument `*args` to enable the conversion of as many length values as the function receives. The following lines explain step by step how that works.

1. We want to ensure that anyone understands the input and output parameters of the function. This is why we defined within a pair of triple double-apostrophes (`"""`) input parameters (`:params parameter_name: definition`) and the function return (`:output: definition`).
1. By default, we will assume that multiple values are provided. Therefore, a list called `value_list` in intantiated at the beginning of the function, while `conversion_factor` remains the same as before.
1. A for-loop over `*args` identifies and processes the arguments provided. Why a for-loop? Well, *Python* recognizes `*args` automatically as a list, and therefore, we can iterate over `*args`, even though the provided range of values was not a list type.
1. The for-loop in the `try` code block includes a `try` - `except` statement in order to verify if the provided values (arguments) are numeric and can be converted to meters. If the `try` block runs successfully, the expression `arg * conversion_factor` appends the converted argument `arg` to `value_list`.
1. Eventually, the `return` keyword returns the value list.


```python
def feet_to_meter(*args):
    """ 
    :param *args: numeric values in feet
    :output: returns list of values in meter
    """
    value_list = []
    conversion_factor = 0.3048
    for arg in args:
        try:
            value_list.append(arg * conversion_factor)
        except TypeError:
            print(str(arg) + " is not a number.")
    return value_list
```

With the newly defined and more flexible function, we can now call `feet_to_meter` with as many arguments as needed:


```python
print("Function call with 3 values: ")
print(feet_to_meter(3, 1, 10))

print("Function call with no value: ")
print(feet_to_meter())

print("Function call with non-numeric values:")
print(feet_to_meter("just", "words"))

print("Function call with mixed numeric and non-numeric values:")
print(feet_to_meter("just", "words", 2))
```

    Function call with 3 values: 
    [0.9144000000000001, 0.3048, 3.048]
    Function call with no value: 
    []
    Function call with non-numeric values:
    just is not a number.
    words is not a number.
    []
    Function call with mixed numeric and non-numeric values:
    just is not a number.
    words is not a number.
    [0.6096]
    

## Keyword arguments **kwargs
In the last section, we made the `feet_to_meter` more flexible so that it can now receive as many arguments as needed. Since the first definition of the function, there is this internal `conversion_factor` variable, which was essentially useless because we could have directly used the value 0.3048 instead. Until now.
Imagine we are writing this function for a historian. So in the past imperial units were wide spread in many cultures (e.g., Greek, Roman or Chinese) with varying length definitions between 0.250 m and 0.335 m. That means our historian will need flexibility regarding the conversion factor, while we still want to use 0.3048 m as default value. This job can be done with optional keyword arguments `**kwargs` an this is how we implement them:

1. Add `**kwargs` after `*args` in the function `def` parentheses (the order of `*args, **kwargs` is important).
1. Keep `conversion_factor = 0.3048` as default value (we want the function to be functional also without any keyword argument provided).
1. Similar to the `*args` statement, *Python* automatically identifies variables beginning with `**` as optional keyword arguments (actually, the name *args* and *kwargs* does not matter - the `*` sign are important). The difference to `*args` is that *Python* identifies `**kwargs` as a dictionary.
1. A for-loop iterates over the *kwargs*-dictionary and the `if` statement will identify any keyword argument that contains the string `"conv"` as conversion_factor.
1. A `try`- `except` statement tests if the provided value for the keyword argument is numeric by attempting a conversion to `float()`.

The remaining function is unchanged from above.


```python
def feet_to_meter(*args, **kwargs):
    """ 
    :param *args: numeric values in feet
    :output: returns list of values in meter
    """
    value_list = []
    conversion_factor = 0.3048
    for k in kwargs.items():
            if "conv" in k[0]:
                try:
                    conversion_factor = float(k[1])
                    print("Using conversion factor = " + str(k[1]))
                except:
                    print(str(k[1]) + " is not a number (using default value 0.3048).")  
    
    for arg in args:
        try:
            value_list.append(arg * conversion_factor)
        except TypeError:
            print(str(arg) + " is not a number.")
    return value_list
```

With the newly defined flexibility of the `feet_to_meter` let's test some different conversion factors:


```python
print("Function call with 3 values and a conversion factor of 0.25: ")
print(feet_to_meter(3, 1, 10, conv_factor=0.25))

print("Function call with 3 values and a conversion factor of 1/7 with slightly different name: ")
print(feet_to_meter(3, 1, 10, conversion_factor=1/7))


```

    Function call with 3 values and a conversion factor of 0.25: 
    Using conversion factor = 0.25
    [0.75, 0.25, 2.5]
    Function call with 3 values and a conversion factor of 1/7 with slightly different name: 
    Using conversion factor = 0.14285714285714285
    [0.42857142857142855, 0.14285714285714285, 1.4285714285714284]
    

## Default keyword arguments

Keyword arguments can also be defined by default.
