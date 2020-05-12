---
title: Python Basics - First steps
keywords: md markdown document
summary: "About Python, variable types and script execution."
sidebar: mydoc_sidebar
permalink: hypy_pybase.html
folder: python-basics
---

## Launch Python environment

These pages are written with [*Jupyter Lab*](https://jupyter.org/) <img style="max-width:10px;" src="https://jupyter.org/assets/main-logo.svg">. *Jupyter* notebooks (`.ipynb`) are great to explore an explain *Python*, but if you want to build more complex code, other *IDE*s may be more suitable. [Anaconda](hy_ide.html#anaconda) provides both the pluged-in installation of [*Jupyter Lab*](https://jupyter.org/) and [*PyCharm*](hy_ide.html#anaconda). For the best learning experience use both environments as follows:

* *Jupyter Lab* to follow course contents, inline exercises, and to produce own online material (mix of *Python* code and *markdown* text)
* *PyCharm* to accomplish assignments and project work (object-oriented code mainly)


{% include tip.html content="The setup of the [*PyCharm IDE*](hy_ide.html#ide) is explained on the [*Install Python*](hypy_install.html#ide-setup) pages." %}

## The first lines of code

The examples in the first steps revolve around ice cream to illustrate the utility of presented code blocks. So if you do not like ice cream, just replace it with another category of things ...

To start, let's get the very first "feedback" from the *Python* console by typing:


```python
print("This is an ice cream callback.")
```

In order to run the above `print`command in *Jupyter Lab*, just click in the above box, then click on the run (triangle) button in the top menu.

In order to run a print command in *PyCharm*:
* Expand the project branch (if not yet done: on left side of the window)
* Right-click in the project folder, select `New` > `Python File` and name the new *Python* (`.py`) file (e.g., `icecream_tutorial.py`). 
* Copy the above `print("...")` code into the new Python file and save it.
* Right-click in the Python file, then `Run icecream_tutorial.py` (alternatively: press the `Ctrl` + `Shift` + `F10`keys).
* Now, the *Python Console* should pop up at the bottom of the window and it will print the text in the above `print`command.

{% include note.html content="In the following, there will not be anymore the differentiation between using *PyCharm* (or any other *IDE*) and *Jupyter Lab*. Thus, **Run the script** means: run the script in your favorite *IDE* in the following." %}

With the `"` apostrophes in the `print` command, we pass a ***string*** variable to the `print` command. Instead of using `"`, one can also use `'`, but it is important to use the same type of apostrophe at the beginning and at the end of the string (text) variable. 

{% include warning.html content="Be reasonable with the usage of `print`. Especially in loops, the use of `print` leads to unnecessary system load and slows down the script." %}

A marginal note: In Python3 `print` is a function, not a keyword as in Python2. `print` is usefull for example to make a running script show where it currently is.

It is also possible to print other types of variables than strings, but the combination of numerical and text variables requires more encoding. 


## Python variables and data types

The above print command already introduced string variables. In sum, there are five standard variable (or data) types in *Python*:

 - text
 - boolean
 - number (numeric)
 - tuple
 - list
 - dictionary
 
 {% include tip.html content="Data and variable types are difficult to understand if you simply try to learn them by heart. Remember that there are different data types that can be useful when writing code and that the most relevant data types are listed here in tabular form." %}
 

### Text

| Type | Example     | Description                        |
|------|:-----------:|------------------------------------|
| str  | `"apple"`   | String embraced with double quotes |
|      | `'apple'`   | String embraced with single quotes |
|      | `"""apple"""` | Literal string (multi-line text)   |
| chr  | `"a"`       | Character (unit of a string)       |

In addition, string variables have some built-in functions that facilitate coding. To create (instantiate) a string variable, use the `=` sign as follows:


```python
flavor1 = "vanilla" # str
first_letter = "v" # str / char
print(flavor1.upper())
print(flavor1[0])
print(flavor1.split("ll")[0])
```

    VANILLA
    v
    vani
    

Characters can be converted to numbers and other way round. This feature can be useful in loops to iterate for example over alphabetically ordered lists (attention: the conversion depends on how your operating system is configured).


```python
print(chr(67))
print(int("c", 36)) # use int(letter, literal)
```

    C
    12
    

### Boolean

Boolean variables are either True (1) or False (0) with many useful code implementations. We will come back to booelans later on in conditional statements.


```python
bowl = False
print("The bowl exists: " + str(bowl))
```

    The bowl exists: False
    

### Numbers (numeric)

| Type    | Example | Description                                              |
|---------|:-------:|----------------------------------------------------------|
| `int`   | `10`    | Signed Integer                                           |
| `float` | `5.382` | Floating point real number                               |
| `complex` | `1.43J` | Complex number where J is in the range between 0 and 255 |

To create a variable, use the `=` sign as follows:


```python
scoops = 2 # int
weight = 0.453 # float
```

*Python* does not require a type assignment for a variable because it is a high-level, interpreted programming language (other than for example *C++*). However, once a variable was assigned a data type, do not change it in the code (it is just good practice - so that scoops remain integers).

If a print statement combines numeric and text variables, the numeric variables first have to be converted to text and then *concatenated* to a string. There are several ways to combine multiple variables in a text string.


```python
print("My ice cream consists of %d scoops." % scoops) # use %d for integers, %f for floats and %s for strings
print("My ice cream weighs %1.3f kg." % weight)
print("My ice cream weighs " + str(weight) + " kg.")
print("My ice cream weighs {0} kg and has {1} scoops".format(weight * scoops, scoops)) # multiple variable conversion
```

    My ice cream consists of 2 scoops.
    My ice cream weighs 0.453 kg.
    My ice cream weighs 0.453 kg.
    My ice cream weighs 0.906 kg and has 2 scoops
    


```python
print("My ice cream weighs " + weight + " kg.") # this cannot work because weight is a float
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    <ipython-input-12-294b0900d1bd> in <module>
    ----> 1 print("My ice cream weighs " + weight + " kg.") # this cannot work because weight is a float
    

    TypeError: can only concatenate str (not "float") to str


### List

A list is a series of values, which is embraced with brackets `[]`. The values can be any other data type (i.e., numeric, text, dictionary or tuple) - even a list (so-called *nested lists*).


```python
flavors = ["chocolate", "bread", flavor1] # a list of strings
nested_list = [[1, 2, 3], ["a", "b", "c"]]
print(nested_list)
```

    [[1, 2, 3], ['a', 'b', 'c']]
    

The items of a list are called *entries* and *entries* can be appended, inserted or deleted from a list.
{% include note.html content="*Python* alway starts counting from zero. Thus, the first entry of a list is entry number 0." %}
Also lists have many useful built-in functions:


```python
flavors = ["chocolate", "bread", flavor1]
flavors.append("cherry") # append an entry at the end
print(flavors)
flavors.insert(0, "lemon") # insert an entry at position 0
print(flavors)
print("There are %d flavors in my list." % flavors.__len__())
print(*flavors) # print all elements in list - dows not work in combination with str
print("This is all I have: " + str(flavors[:]).strip("[]"))
flavors.__delitem__(2) # bread is not a flavor, so let's remove it
print("This is all I have: " + ", ".join(flavors))
      
```

    ['chocolate', 'bread', 'vanilla', 'cherry']
    ['lemon', 'chocolate', 'bread', 'vanilla', 'cherry']
    There are 5 flavors in my list.
    lemon chocolate bread vanilla cherry
    This is all I have:'lemon', 'chocolate', 'bread', 'vanilla', 'cherry'
    This is all I have:lemon, chocolate, vanilla, cherry
    

### Dictionary

Dictionaries are a powerful data type in *Python* and have the basic structure `my_dict = {key: value}`. In contrast to lists, an element of a dictionary is called by invoking a `key` rather than an entry number. A dictionary is not enumerated and `key`s just point to their `value`s (whatever data type the `value`then is).


```python
my_dict =  {1: "Value 1", 2: "Value 2"}
another_dict = {"list1": [1, 2, 3], "number2": 1}
my_dict [1]

```




    'Value 1'



Also dictionary data types have many useful built-in functions.


```python
my_dict.update({3: "Value 3"})  # add a dictionary element 
my_dict
my_dict.__delitem__(1) # delete a dictionary element 
my_dict.__len__() # get the length (number of dictionary elements)

```

## Summary exercise and outlook
Let's practice a little bit with the data types and take already a "bite" of `for`loops and conditional `if` statements ...


```python
scoops = 2 # re-define the number of sccops
favorite_flavor = "vanilla" # choose your favorite flavor

size_scoops = {1: "small", 2: "medium", 3: "this is too much ice cream"}
price_scoops = {1: "3 dollars", 2: "5 dollars", 3: "your health"}
print("Hi,\n I want % d scoop in a waffle, please." % scoops)
size = " " + str(size_scoops[scoops])
price = str(price_scoops[scoops])

print("My pleasure to serve you. You have chosen a" + size + " ice cream. The price is " + price + ".")
print("Let me guess your favorite flavor. Say stop when I \'m correct.")
for f in flavors:
    print("I guess your favorite flavor is %s." % f)
    if f == favorite_flavor:
        print("Stop, that\'s it!")
        if f == "bread":
            print("Sorry, this is not a bakery.")
        break 


```
