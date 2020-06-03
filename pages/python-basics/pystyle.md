---
title: Python - Code Styles and Conventions
keywords: python
summary: "A robust code style facilitates programming."
sidebar: mydoc_sidebar
permalink: hypy_pystyle.html
folder: python-basics
---

Take a deep breath, take off and look at what you have learned so far from a new perspective. After this chapter it is worth to have another look at old codes and to format them robustly. The style guidelines presented here go far beyond visual aesthetics and aid in writing effective codes.

## Background and PEP

This style guide highlights parts of the *PEP 8 - Style Guide for Python Code* by Guido van Rossum, Barry Warsaw and Nick Coghlan. The full document is available at [python.org](https://www.python.org/dev/peps/pep-0008/) and only aspects with relevance for the applications shown at *hydro-informatics.github.io* are featured on this page.

**So what is *PEP*?** *PEP* stands for ***P**ython **E**nhancement **P**roposals*, in which *Python* developers communicate features and developments of *Python*. At the time of writing these lines, there are twelve (minus two) *PEP*s dedicated to the development of *Python* modules, bug fix releases, and also style guides (read the full and current list of *PEP*s at [python.org](https://www.python.org/dev/peps/#id6)). Here, we will use recommendations of *PEP* 8, the style guide for *Python* code.

Many *IDE*s, including *PyCharm* provide auto-completion and tool tips with *PEP* style guidance to aid consistent programming. So if *PyCharm* underlines anything in your script, check the reason for that and consider to modify the code accordingly.

## The Zen of *Python*

Are we getting spiritual now? Far from it. [The Zen of *Python*](https://www.python.org/dev/peps/pep-0020/) is an informational *PEP* (20) by Tim Peters to guide programmers. It is a couple of lines summarizing good practice in coding. The *Easter Egg* `import this` prints the Zen of *Python* in any *Python* interpreter:


```python
import this
```

    The Zen of Python, by Tim Peters
    
    Beautiful is better than ugly.
    Explicit is better than implicit.
    Simple is better than complex.
    Complex is better than complicated.
    Flat is better than nested.
    Sparse is better than dense.
    Readability counts.
    Special cases aren't special enough to break the rules.
    Although practicality beats purity.
    Errors should never pass silently.
    Unless explicitly silenced.
    In the face of ambiguity, refuse the temptation to guess.
    There should be one-- and preferably only one --obvious way to do it.
    Although that way may not be obvious at first unless you're Dutch.
    Now is better than never.
    Although never is often better than *right* now.
    If the implementation is hard to explain, it's a bad idea.
    If the implementation is easy to explain, it may be a good idea.
    Namespaces are one honking great idea -- let's do more of those!
    

## Code layout
### Maximum line length
The maximum length of a line is 79 characters and in-line comments, including [docstrings](#docstrings), should not exceed 72 characters.

### Indentation
Indentation designates the sifting of code (blocks) to the right. Indentation is necessary for example in loops or functions to assign code blocks to a `for` or `def` statement. Multiple levels of indentation occur when nested statements are used (e.g., an `if` condition nested in a `for` loop). One level of indentation corresponds to 4 spaces.


```python
for i in range(1,2):
    print("I'm one level indented.")
    if i == 1:
        print("I'm two levels indented.")
```

    I'm one level indented.
    I'm two levels indented.
    

Because long lines of code are bad practice, we sometimes need to use line breaks when assigning for example a *list* or calling a function. In these cases, the next, continuing is also indented and there are different options to indent multi-line assignments. Here, we want to use the style code of using an opening delimiter for indentation:


```python
a_too_long_list = ["Do", "not" "hard-code", "something", "like", "this.",
                   "There", "are", "better", "ways."]
```

Recall that *PyCharm* and many other *IDE*s automatically lays indentation out.

### Line breaks of expressions with binary operators
When binary operators are part of an expression that exceeds the maximum line length of 79 characters, the line break should be before binary operators.


```python
dummy_df = pd.get_dummies(pd.Series(['variable1', 'parameter2', 'sensor3']))

dum_sum = (dummy_df['variable1']
           + dummy_df['parameter2']
           - dummy_df['sensor3'])
```

### Blank lines
To separate code blocks, hitting the *Enter* key many times is a very inviting option. However, the random and mood-driven use of blank lines results in unstructured code. This is why the *PEP* 8 Authors provide guidance also on the use of blank lines:

* Surround class definitions and top-level functions (i.e., functions where the `def`-line is not indented) with two blank lines.
* Surround methods (e.g., functions within a class) with one blank line.
* Use blank lines sparsely in all other code to indicate logical sections.


```python
# blank 1 before top-level function
# blank 2 before top-level function
def top_level_function():
    pass
# blank 1 after top-level function
# blank 2 after top-level function
```

### Blanks (whitespaces)

Whitespaces aid to relax the code layout, but too many white spaces should be avoided as for example:

* in parentheses, brackets or braces (no: `list( e1, e2 )` vs. yes: `list(e1, e2)`)
* in parentheses with tailing commas (no: `a_tuple = (1, )` vs. yes: `a_tuple = (1,)`)
* immediately before any comma
* between function name and argument parentheses (no: `fun (arg)` vs. yes: `fun(arg)`) and similar for list or dictionary elements
* around the `=` sign of unannotated function parameters indicating a default value (no: `def fun(arg = 0.0)` vs. yes: `def fun(arg=0.0)`)
* before `:` unless parentheses or brackets follow the `:` (e.g., `a_dict = {a_key: a_value}`)

Whitespaces should be added:

* around any operator, boolean, or (augmented) assignment (e.g., `==, <, >, !=, <>, <=, >=, in, not in, is, is not, and, or, not, +=, -=`)
* after colons `:` if a value antecedes the `:` and no parentheses or brackets follow immediately after the `:` (e.g., `a_dict = {a_key: a_value}`)

## Packages and modules

### Imports
Imports are at the top of the script, right after any [docstrings](#docstrings) or other module comments. Import libraries first, then third party packages, and lastly locally stored (own) modules.
Preferably use absolute import (e.g., `import package.module` or `from package import module`) and avoid wild card imports (`from module import *`). Every import should have an own line and avoid using the comma sign for multiple imports:


```python
# DO:
import os
import numpy as np
# DO NOT:
import os, sys
```

### Name convention
New, custom packages or modules should have short and all-lowercase names, where underscores may be used to improve readability (discouraged for packages).

## Comments

### Block and inline comments
Block comments start with a single `#` at the first place of a line, followed by a whitespace and the comment text.

Inline comments follow an expression and are indented with two whitespaces. The usage of inline comments is deprecated (i.e., do not use them or be sparse on their usage)



### Docstrings {#docstrings}
Docstrings are short text descriptions within a module, function, class or method with specifications of arguments, usage and output. When instantiating a standard object, or referencing to a class method, the `__doc__` attribute will print the object's docstring information. For example: 


```python
a_list = [1, 2]
print(a_list.__doc__)
```

    Built-in mutable sequence.
    
    If no argument is given, the constructor creates a new empty list.
    The argument must be an iterable if specified.
    

When writing a *Python*, docstrings are introduced immediately after the `def ...` line with triple double-apostrophes:


```python
def let_there_be_light(*args, **kwargs):
    """
    Bright function accepting any input argument with indifferent behavior.
    :param an_input_argument: STR or anything else
    :param another_input_argument: FLOAT or anything else
    :return: True (in all cases)
    """
    print("Sunrise")
    return True

print(let_there_be_light.__doc__)
```

    
        Bright function accepting any input argument with indifferent behavior.
        :param an_input_argument: STR or anything else
        :param another_input_argument: FLOAT or anything else
        :return: True (in all cases)
        
    

Note that the recommendations on docstringsare provided with [*PEP* 257](https://www.python.org/dev/peps/pep-0257/) rather than *PEP* 8.

## Name conventions

### Definition of name styles
The naming conventions use the following styles (source: [*python.org*](https://www.python.org/dev/peps/pep-0008/#naming-conventions)):

* `b` (single lowercase letter)
* `B` (single uppercase letter)
* `lowercase`
* `lower_case_with_underscores`
* `UPPERCASE`
* `UPPER_CASE_WITH_UNDERSCORES`
* `CamelCase` or `CapWords` or `CapitalizedWords` or `StudlyCaps`. <br>Note: When using acronyms in `CapWords`, capitalize all the letters of the acronym (e.g., `HTTPResponse` is better than `HttpResponse`).
* `mixedCase` (differs from `CapitalizedWords` by initial lowercase character!)
* `Capitalized_Words_With_Underscores` (deprecated)

Some variable name formats imply a particular behavior of *Python*:

* `_single_leading_underscore` variables indicate weak internal use and will not be imported with `from module import *`
* `__double_leading_underscore` variables invoke name mangling in classes (e.g., a method called `__dlu` within the class `MyClass` will be mangled into `_MyClass__dlu`)
* `__double_leading_and_tailing_underscore__` variables are *magic* objects or attributes in user-controlled namespaces (e.g., `__init__` or `__call__` in classes) <br>Only use documented magic object/attributes and never invent them. Read more about magic methods on the page on *Python* [classes](hypy_classes.html#magic).
* `single_tailing_underscore__` variables are used to avoid conflicts with *Python* keywords (e.g., `MyClass(class_='AnotherClass')`)


### Object names {#object-styles}

Use the following styles for naming

* Classes: `CamelCase` (`CapWords`) letters only such as `MyClass`
* Constants: `UPPERCASE` letters only, where underscores may improve readability (e.g., use at a module level for example to assign water density `RHO = 1000`)
* Exceptions: `CamelCase` (`CapWords`) letters only (exceptions should be classes and typically use the suffix `Error` (e.g., `TypeError`)
* Functions: `lowercase` letters only, where underscores may improve readability; sometimes `mixedCase` applies to ensure backwards compatibility of prevailing styles
* Methods (class function, non-public): `_lowercase` letters only with leading underscore, where underscores may improve readability
* Methods (class function, public): `lowercase` letters only, where underscores may improve readability
* Modules: `lowercase` letters only, where underscores may improve readability
* Packages: `lowercase` letters only, where underscores are discouraged
* Variables: `lowercase` letters only, where underscores may improve readability
* Variables (global): `lowercase` letters only, where underscores may improve readability; note that "global" should limit to variable usage within a module only ...


## More code style recommendations

In order to ensure code compatibility and programm efficiency, the *PEP 8* style guide provides some general recommendations ([read more](https://www.python.org/dev/peps/pep-0008/#programming-recommendations)):

* Prefer `is` or `is not` over equality operators
* Prefer `is not` over `not ... is` expressions
* When defining a function, prefer `def` statements over `lambda` expressions, which are only reasonable for one-time usage
* When exceptions are expected, use `try` - `except` clauses (see [errors and exceptions](hypy_pyerror.html#try-except))
* Ensure that methods and functions return objects consistently - for example:


```python
def a_function_with_return(x):
    if x > 0:
        return np.sqrt(x)
    else:
        return None
```
