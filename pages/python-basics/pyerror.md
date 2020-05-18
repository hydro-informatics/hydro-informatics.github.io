---
title: Python Basics - Errors and debugging
keywords: python
summary: "Handle error types and troubleshoot (debug)."
sidebar: mydoc_sidebar
permalink: hypy_pyerror.html
folder: python-basics
---

## Error types

To err is human and *Python* helps us to find our mistakes by providing [error](https://docs.python.org/3/tutorial/errors.html) type descriptions. Here is a list of common errors:

| Error Type          | Description                                                 | Example                                                   |
|---------------------|-------------------------------------------------------------|-----------------------------------------------------------|
| `KeyError`          | A mapping key is not found.                                 | May occur when referencing a non-existing dictionary key. |
| `ImportError`       | Importing a module that does not exist                      | `import the_almighty_module`                             |
| `IndentationError`  | The code block indentation is not correct.                  | See [above](#indent)                                      |
| `IndexError`        | An index outside the range of a variable is used.           | `list = [1, 2]  print(list[2])`                           |
| `NameError`         | An undefined variable is referenced.                        | `print(a)`                                                |
| `TypeError`         | Incompatible data types and/or operators are used together. | "my_string" / 10                                          |
| `ValueError`        | Incorrect data type used.                                   | `int(input("Number:"))` answered with `t`                 |
| `ZeroDivisionError` | Division by zero.                                           | `3 / 0`                                                   |

Still, there are many more error types that can occur an *Python* developers maintain comprehensive descriptions of built-in exceptions on the [*Python* documentation web site](https://docs.python.org/3.8/library/exceptions.html).


## Exception handling with `try` - `except` 
`try` and `except` keywords test a code block and if it crashes, an `exception` is raised, but the script itself will not crash. The basic structure is:


```python
try:
    # code block
except ErrorType:
    print("Error / warning message.")
```

The `ErrorType` is technical not necessary (i.e., `except:` does the job, too), but adding an `ErrorType` is good practice to enable efficient debugging or making other users understand the origin of an error or warning. The following example illustrates an application of a `ValueError` in an interactive console script that requires users to type an integer value.


```python
try:
    x = int(input("How many scoops of ice cream do you want? "))
except ValueError:
    print("What's that? sorry, please try again.")
```

    How many scoops of ice cream do you want?  3.4
    

    What's that? sorry, please try again.
    

## The `pass` statement
When we start writing code we of start with a complex, modular and void code frame. In order to test the code, we need to run it incrementally (i.e., to debug the code). The above error type definitions help us to understand errors that we made in already written code. However, we want to run our code also with voids, or sometimes just to ignore minor errors silently. In this case, the `pass` statement helps:


```python
try:
    a = 5
    c = a + b # we want to define b later on with a complex formula
except NameError:
    pass # we know that we did not define b yet
```

{% include tip.html content="The `pass` statement should only be temporary and it has a much broader application range, for example in [functions](hypy_pyfun.html) and [classes](hypy_classes.html)." %}

## Debugging

Debugging is the act of removing bugs from code. Once you wrote more or less complex code, the big question is: *Will it run at the end?*

Large code blocks can be a nightmare for debugging and this section provides some principles to reduce the factor of scariness that debugging may involve.

### Use exceptions precisely
Embrace critical code blocks precisely with `try` - `except` keywords and possible errors. This will help later on to identify possible errors.
{% include tip.html content="Document self-written error messages in except statements from the beginning on (e.g., in a markdown document) and establish a developer [wiki](hy_documentation.html) including possible error sources and remedy descriptions." %}

### Use descriptive variable names
Give variables, functions and other objects descriptive and meaningful names. Abbreviations will always be necessary, but those should be descriptive. For variables and functions, use small letters only. For classes use CamelCase.

### Deal with errors
If an error message is raised, read the error message thoroughly and several times to understand the origin of the error. Error messages often indicate the particular script and the line number where the error was raised. In the case that the error is not an apparent result misused data types or any of the above error messages (e.g., an error raised within an external module/package), use your favorite search engine to troubleshoot the error.

### Verify outputs
The fact that code runs does not inherently imply that the result (output) is the desired output. Therefore, run the code with input parameters that yield existing output and verify that the code-produced output corresponds to the existing output.

### Code with a structured approach
Think about the code structure before starting with punching in a bunch of code blocks and storing them in some *Python* files. Structural and/or behavior diagrams aid developing a sophisticated code framework. The developers of the Unified Modeling Language (UML) provide solid guidelines for developing structure and behavior [UML diagrams](https://en.wikipedia.org/wiki/Unified_Modeling_Language#Diagrams) in software engineering.
{% include tip.html content="Take a sheet of paper and a pencil before you start to engineer code and sketch how the code will produce the desired output." %}

### Soft alternatives
Explain your problem to a friend (or just speak out loud). Rephrasing and trying to explain a problem to another person (even if it is just an imaginery person or group of people) often represents the troubleshot itself.
Take a walk, sleep on the problem or do other things with low brain occupation. While you are dealing with other things, your brain continues to think about the problem (Wikipedia devoted a page to this so-called process of [*incubation*](https://en.wikipedia.org/wiki/Incubation_(psychology)).
