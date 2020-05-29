---
title: Python - Code Styles and Conventions
keywords: python
summary: "A robust code style facilitates programming."
sidebar: mydoc_sidebar
permalink: hypy_pystyle.html
folder: python-basics
---

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

## Package and module imports
Imports are at the top of the script, right after any [docstrings](#docstrings) or other module comments. Import libraries first, then third party packages, and lastly locally stored (own) modules.
Preferably use absolute import (e.g., `import package.module` or `from package import module`) and avoid wild card imports (`from module import *`). Every import should have an own line and avoid using the comma sign for multiple imports:


```python
# DO:
import os
import numpy as np
# DO NOT:
import os, sys
```

## Docstrings {#docstrings}
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
