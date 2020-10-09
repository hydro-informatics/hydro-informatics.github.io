---
title: Python - Functions
tags: [python, object_orientation]
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

print("Function call with 2 values with default conversion factor: ")
print(feet_to_meter(25, 10))


```

    Function call with 3 values and a conversion factor of 0.25: 
    Using conversion factor = 0.25
    [0.75, 0.25, 2.5]
    Function call with 3 values and a conversion factor of 1/7 with slightly different name: 
    Using conversion factor = 0.14285714285714285
    [0.42857142857142855, 0.14285714285714285, 1.4285714285714284]
    Function call with 2 values with default conversion factor: 
    [7.62, 3.048]
    

## Default keyword arguments {#kwargs}

Keyword arguments can also be defined by default. The below example shows how the `conversion_factor` can be defaulted in the `def` function parentheses. Note that `conversion_factor` must be defined after any optional arguments `*args`.


```python
def feet_to_meter(*args, conversion_factor=0.3048):
    """ 
    :param *args: numeric values in feet
    :output: returns list of values in meter
    """
    value_list = []
   
    for arg in args:
        try:
            value_list.append(arg * conversion_factor)
        except TypeError:
            print(str(arg) + " is not a number.")
    return value_list
```

Now we can use `feet_to_meter` with or without or with a conversion factor and after the value list:


```python
print("Function call with a conversion factor of 0.313 and two values: ")
print(feet_to_meter(1, 10, conversion_factor=0.313))
                    
print("Function call with 3 values without any conversion factor: ")
print(feet_to_meter(3, 1, 10))
```

    Function call with a conversion factor of 0.313 and two values: 
    [0.313, 3.13]
    Function call with 3 values without any conversion factor: 
    [0.9144000000000001, 0.3048, 3.048]
    

## Function wrappers and Decorators {#wrappers}
If multiple functions contain similar lines, chances are that those functions can be further factorized by using function wrappers and decorators. A typical example is for example if a license checkout is needed in order to use a commercial *Python* module/package (e.g., Esri's `arcpy`) or if we want to use a recurring error statement with `try` - `except` statements. 

Consider two or more functions that should receive, process and produce numerical output from user input. These functions could look like this:


```python
def multiply_arguments(*args):
    result = 1.0
    try:
        for arg in args:
            result *= arg
        print("The result is: " + str(result))
    except TypeError:
        print("ERROR: The calculation could not be performed failed (input arguments: %s)" % ", ".join(args))
    except ValueError:
        print("ERROR: The calculation could not be performed failed (input arguments: %s)" % ", ".join(args))
    return result

def sum_up_arguments(*args):
    result = 0.0
    try:
        for arg in args:
            result += arg
    except TypeError:
        print("ERROR: The calculation could not be performed failed (input arguments: %s)" % ", ".join(args))
    except ValueError:
        print("ERROR: The calculation could not be performed failed (input arguments: %s)" % ", ".join(args))   
    return result
```

Both functions involve the statement `print("The result is: " + str(result))` to print results to the *Python* console (e.g., to get some intermediate information) or to run only on valid (i.e., numeric) input with the help of exception (`try` - `except`) statements. However, we want our functions to focus on the calculation only and this is where a wrapper function helps.

A wrapper function can be defined by first defining a normal function (e.g., `def verify_result`) and passing a function (`func`) as argument. In that function, we can then place a nested `def wrapper()` function that will embrace `func`. It is important to use both optional `*args` and optional keyword `**kwargs` in the wrapper and the call to `func` in order to make the wrapper as flexible as possible.


```python
def verify_result(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            print("Success. The result is %1.3f." % float(result))
            return result
        except TypeError:
            print("ERROR: The calculation could not be performed because of at least one non-numeric input (input arguments: %s)" % str(args))
            return 0.0
        except ValueError:
            print("ERROR: The calculation could not be performed because of non-nmumeric input (input arguments: %s)" % str(args))
            return 0.0
    return wrapper
```

Now, we can use an `@`-decorator to wrap the above function in the `verify_result(fun)` function. When *Python* reads the beautiful, code-decorating `@` sign, it will look for the wrapper function defined after the `@` sign to wrap the following function.


```python
@verify_result
def multiply_arguments(*args):
    result = 1.0
    for arg in args:
        result *= arg
    return result

@verify_result
def sum_up_arguments(*args):
    result = 0.0
    for arg in args:
        result += arg
    return result
```

The two functions (`multiply_arguments` and `sum_up_arguments`) can be called as usually, for example:


```python
multiply_arguments(3, 4)
multiply_arguments(3, 4, "not a number")
sum_up_arguments(3, 4)
sum_up_arguments("absolutely", "no", "valid", "input")
```

    Success. The result is 12.000.
    ERROR: The calculation could not be performed because of at least one non-numeric input (input arguments: (3, 4, 'not a number'))
    Success. The result is 7.000.
    ERROR: The calculation could not be performed because of at least one non-numeric input (input arguments: ('absolutely', 'no', 'valid', 'input'))
    




    0.0



The above wrapper function returns the wrapped function results, too. However, in order to use built-in function attributes (e.g., the function's name with `__name__`, the function's docstring with `__doc__`, or the module in which the function is defined with `__module__`) outside of the wrapper, we need the wrapper function to return the wrapped (decorated) function itself. This can be done as follows:


```python
def error_func(*args, **kwargs):
    return 0.0

def verify_result(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TypeError:
            print("ERROR: The calculation could not be performed because of at least one non-numeric input (input arguments: %s)" % str(args))
            return error_func(*args, **kwargs)
        except ValueError:
            print("ERROR: The calculation could not be performed because of non-nmumeric input (input arguments: %s)" % str(args))
            return error_func(*args, **kwargs)
    return wrapper
```

Note the difference: the `wrapper` function now returns `func(*arg, **kwargs)` instead of the numeric variable results. If the function can not be executed because of invalid input, the `wrapper` will return an error function (`error_func`), which ensures the consistency of the wrapper function. One may think that the error function returning 0.0 is obsolete, because the exception statements could directly return 0.0. However, 0.0 is a *float* variable, while `error_func` is a function and it is important that the function wrapper always returns the same data type, regardless of the an exception raise or successful execution. This is what makes code consistent.

This page shows examples for using the decorators in the shape of an `@` sign to wrap (embrace) a function. Decorators are also a useful feature in classes, for example when a class function returns static values. Read more about decorators in classes later in the chapter about [object orientation and classes](http://localhost:4000/hypy_classes.html#dec).

## Iterators and generators
A characteristic of *list*, *tuple*, and *dictionary* data types is their iterability, which is provided by their `__iter__` built-in method. For example, iterability is the reason why we can write:


```python
for e in [1, 2, 3]: print(e)
```

    1
    2
    3
    

Besides iterations, *Python* also enables to create generators (i.e., generator functions). Instead of using a `return` statement, a generator function ends with a `yield` statement, that returns data as long as a `next()` function (inherent step in iterations) is called. An application of a generator is for example the flattening of nested lists (i.e., remove sub-lists and write all variables directly into a non-nested list):


```python
from collections.abc import Iterable

def flatten(nested_list):
    for e in nested_list:
        if isinstance(e, Iterable) and not isinstance(e, str):
            for x in flatten(e):
                yield x
        else:
            yield e
            
a_nested_list = [[1, 2, 3], ["a", "b", "c"]]
flattened_list = list(flatten(a_nested_list))
print(flattened_list)
```

    [1, 2, 3, 'a', 'b', 'c']
    

{% include note.html content="The above example uses `Iterable` from the standard module `collections.abc`. More about importing packages and modules will be discussed on the [Modules & packages](hypy_pckg.html) page." %}

## Lambda functions {#lambda}

[Lambda (*&lambda;*) calculus](https://en.wikipedia.org/wiki/Lambda_calculus) is a formal language for expressing computations based on function abstraction and was introduced in the 1930s by Alonzo Church and Stephen Cole Kleene. Lambda functions originate from functional programming and represent short, anonymous (i.e, without name) functions. Although *Python* is not inherently a functional programming language, functional concepts were implemented early in *Python*, for example with the `map()`, `filter()`, and deprecated `reduce()` functions. 

In *Python*, an anonymous (nameless) lambda function can take any number of arguments, but can only have one expression. The list of arguments consists of a comma-separated list of variables and the expression uses these arguments. The **syntax** of `lambda` functions is:

`lambda arguments : expression`

The following example illustrates a `lambda` function with one argument and adds 1 to the argument:


```python
add_one = lambda number : number + 1
print(add_one(1))
```

    2
    

That was nice, but pretty useless. So here is an example of a lambda function that sums up two input arguments:


```python
sum_up = lambda x, y : x + y
print(sum_up(1, 5))
```

    6
    

The above-shown function for converting feet to meters can also be written as a lambda function:


```python
feet_to_meter = lambda ft_value : ft_value * 0.3048
print(feet_to_meter(10))
```

    3.048
    

Using a `lambda` function made the code here shorter and more efficient. In order to evaluate the `feet_to_meter` `lambda` function for multiple values, we can use the `map()` function. The syntax of a `map()` function is: 

`result = map(function, sequence)`

where `sequence` can be a *list* or a *tuple*. Thus, to evaluate a *tuple* of four values, we can write:


```python
four_ft_values = (4, 9.7, 7, 2)
print(list(map(feet_to_meter, four_ft_values)))
```

    [1.2192, 2.95656, 2.1336, 0.6096]
    

The `print` statement converts the `map()` object into a *list* to evaluate the `map()` object (otherwise, the result would be somethine like `<map object at ...>`).

If the `feet_to_meter` function is not needed at another place in the code, one can also write:


```python
print(list(map(lambda x : x * 0.3048, (4, 9.7, 7, 2))))
```

    [1.2192, 2.95656, 2.1336, 0.6096]
    

Another feature are `filter(function, list)` objects which provide an elegant solution to filter out those elements from a list for which the function returns `True`. The following code block illustrates a `filter` that eliminates all numbers from the `some_numbers` list, which can be divided by three. 


```python
some_numbers = list(range(1, 10))
print(list(filter(lambda x: x % 3, some_numbers)))
```

    [1, 2, 4, 5, 7, 8]
    

Formerly, a `reduce()` function was implemented in *Python* to merge list input into one value. However, the *Python* developer *Guido van Rossum* successfully banned it from *Python3* ([read his post](https://www.artima.com/weblogs/viewpost.jsp?thread=98196)), which is why it is not further mentioned here.

{% include exercise.html content="Get familiar with functions in the [Hydraulics (1D)](ex_ms.html) exercise." %}
