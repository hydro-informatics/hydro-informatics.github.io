---
title: Python Basics - Errors and debugging
keywords: python
summary: "Handle error types and troubleshoot (debug)."
sidebar: mydoc_sidebar
permalink: hypy_pyerror.html
folder: python-basics
---

## Errors & exceptions

### Error types

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


### Exception handling with `try` - `except` {#try-except}
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
    

What to do if you are unsure about the error type? Add an `else` statement:


```python
try:
    value = a_dictionary[key]
except KeyError:
    return key_not_found(key)
else:
    return handle_value(value)
```

### The `pass` statement
When we start writing code we of start with a complex, modular and void code frame. In order to test the code, we need to run it incrementally (i.e., to debug the code). The above error type definitions help us to understand errors that we made in already written code. However, we want to run our code also with voids, or sometimes just to ignore minor errors silently. In this case, the `pass` statement helps:


```python
try:
    a = 5
    c = a + b # we want to define b later on with a complex formula
except NameError:
    pass # we know that we did not define b yet
```

{% include tip.html content="The `pass` statement should only be temporary and it has a much broader application range, for example in [functions](hypy_pyfun.html) and [classes](hypy_classes.html)." %}

## Logging {#logging}

The `print()` function is useful to print variables or computation progress to the console (not too often though - output takes time and slow calculations). For robust reporting of errors or other important messages, however, a log file represents a better choice. So what is a log file or the act of logging? We know logbooks from discoverers or adventurers, who write down their experiences ordered by dates. Similarly, a code can write down (*log*) its "experiences", but in a file instead of a book. For this purpose, *Python* provides the standard [*logging* library](https://docs.python.org/3/howto/logging.html). For the moment, it is sufficient to know that the *logging* library can be imported in any *Python* script with `import logging` (more information about packages, modules, and libraries is provided later on the [Modules & packages](hypy_pckg.html) page).

The following script imports the *logging* module, and uses the following keyword arguments to set the `logging.basicConfig`:
* `filename="my-logfile.log"` makes the logging module write to a file named `"my-logfile.log"` in the same directory where the *Pyhton* script is executed.
* `format="%(asctime)s - %(message)s` sets the logging format to `YYYY-MM-DD HH:MM:SS.sss - `*Message text* (more format options are listed in the [*Python* docs](https://docs.python.org/3/howto/logging.html#displaying-the-date-time-in-messages)).
* `filemode="w"` overwrites previous messages in the log file (remove this argument to append messages instead of overwriting).
* `level=logging.DEBUG` defines the severity of messages written to the log file, where `DEBUG` is adequate for problem diagnoses in codes; other levels of event severity are:
    - `logging.INFO` writes all confirmation messages of events that worked as expected.
    - `logging.WARNING` (**default**) indicates when an unexpected event happened or when an event may cause an error in the future (e.g., because of insufficient disk space).
    - `logging.ERROR` reports serious problems that caused that the code could not be executed.
    - `logging.CRITICAL` is a broader serious problem indicator, where the program itself may not be able to continue running (e.g., *Python* crashes).

Until here, messages are only written to the log file, but we cannot see any message in the console. To enable simultaneous logging to the log file and the console (*Python* terminal), use `logging.getLogger().addHandler(logging.StreamHandler())` (appends an *io* stream handler).

To write a message to the log file (and *Python* terminal), use 
* `logging.debug("message")` for code diagnoses,
* `logging.info("message")` for progress information (just like we used `print("message")` before,
* `logging.warning("warning-message")` for unexpected event documentation (without the program being interrupted),
* `logging.error("error-message")` for errors that entail malfunction of the code, and
* `logging.critical("message")` for critical error that may lead to program (*Python*) crashes.

*Warning*, *error*, and *critical* message should be implemented in exception raises (see above `try` - `except` statements).

At the end of a script, logging should be stopped with `logging.shutdown()` because otherwise the log file is locked by *Python* and the *Python Kernel* needs to be stopped in order to make modifications of the log file.


```python
import logging

logging.basicConfig(filename="my-logfile.log", format="%(asctime)s - %(message)s", filemode="w", level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())
logging.debug("This message is logged to the file.")
logging.info("Less severe information is also logged to the file.")
logging.warning("Warning messages are logged, too.")

a = "text"

try:
    logging.info(str(a**2))
except TypeError:
    logging.error("The variable is not numeric.")

# stop logging
logging.shutdown()
```

    This message is logged to the file.
    Less severe information is also logged to the file.
    Warning messages are logged, too.
    The variable is not numeric.
    

And this is how `my-logfile.log` looks like:


```python
2050-00-00 18:51:46,657 - This message is logged to the file.
2050-00-00 18:51:46,666 - Less severe information is also logged to the file.
2050-00-00 18:51:46,667 - Warning messages are logged, too.
2050-00-00 18:51:46,669 - The variable is not numeric.
```

Events can also be documented by instantiating a logger object with `logger = logging.getLogger(__name__)`. This favorable solution is recommended for advanced coding such as writing a [custom *Python* library](hypy_pckg.html) (read more in the [*Python* docs on advanced logging](https://docs.python.org/3/howto/logging.html#advanced-logging-tutorial)). An example script with a more sophisticated logger is provided with the [Logger script at the course repository](https://github.com/hydro-informatics/material-py-codes/raw/master/logging/Logger.py) (available during lecture series).

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
