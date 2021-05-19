#!/usr/bin/env python
# coding: utf-8

# (ooc)=
# # Object Orientation and Classes
# 
# Leverage the power of Python by writing new classes. For interactive reading and executing code blocks [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/hydro-informatics/hydro-informatics.github.io/main?filepath=jupyter) and find *classes.ipynb* or {ref}`install-python` locally along with {ref}`jupyter`.
# 
# ## The Class of Classes
# 
# *Python* is an inherently object-oriented language and makes the deployment of classes and objects extremely easy. Let's start with essential definitions.
# 
# ### What is Object-Oriented Programming (OOP)?
# 
# Object-Oriented Programming (OOP) is a programming paradigm that aligns the architecture of software with reality. Object orientation starts with the design of software, where a structured model is established. The structured model contains information about objects and their abstractions. The development and implementation of object-oriented software requires a structured way of thinking and the conceptual understanding of classes, inheritance, polymorphism and encapsulation.
# 
# 
# ### Objects and Classes
# In computer language, an **object** is an instance that contains data in the shape of fields (called *attributes* or *properties*) and code in the shape of features (*functions* or *methods*). The features of an object enable access (read) and manipulation of its data fields. Objects have a concept of `self` regarding their attributes, methods and data fields. `self` internally references attributes, properties or methods belonging to an object.
# 
# In *Python*, an object is an instance of a class. Thus, a **class** represents a blueprint for many similar objects with the same attributes and methods. A class does not use system memory and only its instance (i.e., objects) will use memory.
# 
# ![img](https://raw.githubusercontent.com/sschwindt/hydroinformatics/main/docs/img/classes_objects.png)
# 
# 
# The simplest form of a class in *Python* only includes some statements, and it is highly recommended to add an `__init__` statement where class variables are defined. We will come back to the `__init__` statement later in the section on *magic* methods. The following example shows one of the simplest classes with an `__init__` method. Note the usage of `self` in the class, which becomes `object_name.attribute` for instances of the class.

# In[1]:


class IceCream:
    def __init__(self, *args, **kwargs):
        self.flavors=["vanilla", "chocolate", "bread"]
    
    def add_flavor(self, flavor):
        self.flavors.append(flavor)
        
    def print_flavors(self):
        print(", ".join(self.flavors))

# create an instance of IceCream and use the print_flavors method
some_scoops = IceCream()
some_scoops.add_flavor("lemon")

# the following statements have similar effects
some_scoops.print_flavors()
print(some_scoops.flavors)


# ### Inheritance
# The *Cambridge Dictionary* defines inheritance (biology) as *"particular characteristics received from parents through genes"*. Similarly, inheritance in OOP describes the hierarchical relationship between classes with *is-a-type-of* relationships. For example, a class `Salmon` may inherit from a class `Fish`. In this case, `Fish` is the parent class (or super-class) and `Salmon` is the child class (or sub-class), where `Fish` might define attributes like `preferred_flow_depth` or `preferred_flow_velocity` and fuzzification methods to describe other habitat preferences. Such a class inheritance could look like this:

# In[2]:


# define the parent class Fish
class Fish:
    def __init__(self, *args, **kwargs):
        self.preferred_flow_depth = float()
        self.preferred_flow_velocity = float()
        self.species = ""
        self.xy_position = tuple()
        
    def print_habitat(self):
        print("The species {0} prefers {1}m deep and {2}m/s fast flowing waters.".format(self.species, str(self.preferred_flow_depth), str(self.preferred_flow_velocity)))
        
    def swim_to_position(self, new_position=()):
        self.xy_position = new_position


# define the child class Salmon, which inherits (is-a-type-of) from Fish
class Salmon(Fish):
    def __init__(self, species, *args, **kwargs):
        Fish.__init__(self)
        self.family = "salmonidae"
        self.species = species
        
    def habitat_function(self, depth, velocity):
        self.preferred_flow_depth = depth
        self.preferred_flow_velocity = velocity


atlantic_salmon = Salmon("Salmo salar")
atlantic_salmon.habitat_function(depth=0.4, velocity=0.5)
atlantic_salmon.print_habitat()

pacific_salmon = Salmon("Oncorhynchus tshawytscha")
pacific_salmon.habitat_function(depth=0.6, velocity=0.8)
pacific_salmon.print_habitat()


# ```{tip}
# To make initial attributes of the parent class (`Fish`) directly accessible, use `ParentClass.__init__(self)` in the `__init__` method of the child class.
# ```

# (polymorphism)=
# ### Polymorphism
# In computer science, polymorphism refers to the ability of presenting the same programming interface for different basic structures. Admittedly, a definition cannot be much more abstract. So it is sufficient to focus here only on the meaning of polymorphism relevant in *Python* and that is when child classes have methods of the same name as the parent class. For example, polymorphism in *Python* is when we re-define the `swim_to_position` function of the above show `Fish` parent class in the `Salmon` child class.
# 
# ### Encapsulation (Public and Non-public Attributes)
# The concept of encapsulation combines data and functions to manipulate data, whereby both (data and functions) are protected against external interference and manipulation. Encapsulation is also the baseline of [data hiding](https://en.wikipedia.org/wiki/Information_hiding) in computer science, which segregates design decisions in software regarding objects that are likely to change. Here, the most important aspect of encapsulation is the differentiation between `private` and `public` class variables. 
# 
# `private` attributes cannot be modified from outside (i.e., they are protected and cannot be changed for an instance of a class). In *Python*, there are no inherently `private` variables and this is why *Python* docs talk about `non-public` attributes (i.e., `_single_leading_underscore` *def*s in a class) rather than `private` attributes. While using a single underscore is rather good practice without technical support, we can use `__double_leading_underscore` attributes to emulate private behavior with a mechanism called *name mangling*. Read more about variable definition styles in the [style guide](pystyle.html#object-styles).
# 
# `public` attributes can be modified externally (i.e., different values can be assigned to `public` attributes of different instances of a class).
# 
# In the above example of the `Salmon` class, we use a public variable `self.family`. However, the family attribute of the `Salmon` class is an attribute that should not be modifiable. A similar behavior would be desirable for an `self.aggregate_state = 'frozen'` of the `IceCream` class. So let's define another child of the `Fish` class with a non-public `__family` attribute. The `__family` attribute is not directly accessible for instances of the new child class `Carp`. Still, we want the `Carp` class to have a `family` attribute and we want to be able to print its value. This is why we need a special method `def family(self)`, which has an `@property` decorator (recall [decorators on the functions page](pyfun.html#wrappers)). The below example features another special method `def family(self, value)` that is embraced with a `@property.setter` decorator that enables re-defining the non-public `__family` property (even though this is logically nonsense here because we do not want to enable renaming the `__family` property).
# 

# In[3]:


class Carp(Fish):
    def __init__(self, species, *args, **kwargs):
        Fish.__init__(self)
        self.__family = "cyprinidae"
        self.species = species
        
    @property
    def family(self):
        return self.__family
    
    @family.setter
    def family(self, value):
        self.__family = value
        print("family set to \'%s\'" % self.__family)
        
        
european_carp = Carp("Cyprinus carpio carpio")
print(european_carp.family)

try:
    print(european_carp.__family)
except AttributeError:
    print("__family is not directly accessible.")

# re-definition of __family through @family.setter method
european_carp.family="lamnidae"


# (dec)=
# ## Decorators
# 
# In the last example, we have seen the implementation of the `@property` decorator, which tweaks a method into a non-callable attribute (property), and the `@attribute.setter` decorator to re-define a non-public variable. 
# 
# ```{tip}
# What are decorators and wrappers again? If you are hesitating to answer this question, refresh your memory on the [functions page](pyfun.html#wrappers).
# ```
# 
# Until now, we only know decorators as a nice way to simplify functions. However, decorators are an even more powerful tool in object-oriented programming of classes, where decorators can be used to wrap class methods similar to functions. Let's define another child of the `Fish` class explore the `@property` decorator with its `deleter`, `getter`, and `setter` methods.

# In[4]:


class Bullhead(Fish):
    def __init__(self, species, *args, **kwargs):
        Fish.__init__(self)
        self.__family = "cottidae"
        self.species = species
        self.__length = 7.0
        
    @property
    def length(self):
        return self.__length
    
    @length.setter
    def length(self, value):
        try:
            self.__length = float(value)
        except ValueError:
            print("Error: Value is not a real number.")
            
    @length.deleter
    def length(self):
        del self.__length
        
european_bullhead = Bullhead("Cottus gobio")

# make use of @property.getter, which directly results from the @property-embraced def length method
print(european_bullhead.length)

# make use of @property.setter method
european_bullhead.length = 6.5
print(european_bullhead.length)

# make use of @property.delete method
del european_bullhead.length
try:
    print(european_bullhead.length)
except AttributeError:
    print("Error: You cannot print a nonexistent property.")


# (magic)=
# ## Overloading and Magic Methods
# 
# The above examples introduced already the special, or magic, method `__init__`. We have already seen that `__init__` is nothing magical itself and there are many more of such predefined methods in *Python*. Before we get to *magic* methods, it is important to understand the concept of overloading in *Python*. So did you already wonder why the same operator can have different effects depending on the data type?
# 
# For example, the `+` operator concatenates *strings*, but sums up numeric data types:

# In[5]:


a_string = "vanilla"
b_string = "cream"
print("+ operator applied to strings: " + str(a_string + b_string))

a_number = 50
b_number = 30
print("+ operator applied to integers: " + str(a_number + b_number))


# This behavior is called operator (or function) overloading in *Python* and overloading is possible because of pre-defined names of *magic methods* in *Python*. Now, we are ready to get to *magic* methods.
# 
# Magic methods are one of the key elements that make *Python* easy and clear to use. Because of their declaration using double underscores (`__this_is_magic__`), magic methods are also called *dunder* (**d**ouble **under**score) methods. Magic methods are special methods with fixed names and their *magic* name is because they do not need to be directly invoked. Behind the scenes, *Python* constantly uses *magic* methods, for example when a new instance of a class is assigned: When you write `var = MyClass()`, *Python* automatically calls `MyClass`'es `__init__()` and `__new__()` *magic* methods. Magic methods also apply to any operator or (augmented) assignment. For example, the `+` binary operator makes *Python* look for the magic method `__add__`. Thus, when we type `a + b`, and both variables are instances of `MyClass`, *Python* will look for the `__add__` method of `MyClass` in order to apply `a.__add__(b)`. If *Python* cannot find the `__add__` method in `MyClass`, it returns a `TypeError: unsupported operand`.  
# 
# The following sections list some documented magic methods for use in classes and packages in tabular format. The tables provide the most common magic methods and more documented magic objects or attributes exist. 
# 
# ### Operator (binary) and assignment methods
# 
# For any new class that we want to be able to deal with an operator (e.g., to enable summing up objects with `result = object1 + object2`), we need to implements (overload) the following methods.
# 
# |  Operator    |  Method                                        |  | Assignment   |  Method                                         |
# |--------------|------------------------------------------------|--|--------------|-------------------------------------------------|
# |  `+`         |  `object.__add__(self, *args, **kwargs)`       |  |  `+=`        |  `object.__iadd__(self, *args, **kwargs)`       |
# |  `-`         |  `object.__sub__(self, *args, **kwargs)`       |  |  `-=`        |  `object.__isub__(self, *args, **kwargs)`       |
# |  `*`         |  `object.__mul__(self, *args, **kwargs)`       |  |  `*=`        |  `object.__imul__(self, *args, **kwargs)`       |
# |  `//`        |  `object.__floordiv__(self, *args, **kwargs)`  |  |  `/=`        |  `object.__idiv__(self, *args, **kwargs)`       |
# |  `/`         |  `object.__truediv__(self, *args, **kwargs)`   |  |  `//=`       |  `object.__ifloordiv__(self, *args, **kwargs)`  |
# |  `%`         |  `object.__mod__(self, *args, **kwargs)`       |  |  `%=`        |  `object.__imod__(self, *args, **kwargs)`       |
# |  `**`        |  `object.__pow__(self, *args, **kwargs)`       |  |  `**=`       |  `object.__ipow__(self, *args, **kwargs)`       |
# |  `<<`        |  `object.__lshift__(self, *args, **kwargs)`    |  |  `<<=`       |  `object.__ilshift__(self, *args, **kwargs)`    |
# |  `>>`        |  `object.__rshift__(self, *args, **kwargs)`    |  |  `>>=`       |  `object.__irshift__(self, *args, **kwargs)`    |
# |  `&`         |  `object.__and__(self, *args, **kwargs)`       |  |  `&=`        |  `object.__iand__(self, *args, **kwargs)`       |
# |  `^`         |  `object.__xor__(self, *args, **kwargs)`       |  |  `^=`        |  `object.__ixor__(self, *args, **kwargs)`       |
# |  `|`         |  `object.__or__(self, *args, **kwargs)`        |  |  `|=`        |  `object.__ior__(self, *args, **kwargs)`        |
# 
# 
# ### Operator (unary) and Comparator Methods
# 
# Also unary or comparative operators can be defined in classes. Unary operators deal with only one input in contrast to the above listed binary operators. Unary operators is what we typically use to increment or decrement variables with for example `++x` or `--x`. In addition, comparative operators (comparators) involve magic methods, such as `__ne__`, as synonym for **n**ot **e**qual.
# 
# |  Operator     |  Method                      |  | Comparator   |  Method                                  |
# |---------------|------------------------------|--|--------------|------------------------------------------|
# |  `-`          |  `object.__neg__(self)`      |  |  `<`         |  `object.__lt__(self, *args, **kwargs)`  |
# |  `+`          |  `object.__pos__(self)`      |  |  `<=`        |  `object.__le__(self, *args, **kwargs)`  |
# |  `abs()`      |  `object.__abs__(self)`      |  |  `==`        |  `object.__eq__(self, *args, **kwargs)`  |
# |  `~`          |  `object.__invert__(self)`   |  |  `!=`        |  `object.__ne__(self, *args, **kwargs)`  |
# |  `complex()`  |  `object.__complex__(self)`  |  |  `>=`        |  `object.__ge__(self, *args, **kwargs)`  |
# |  `int()`      |  `object.__int__(self)`      |  |  `>`         |  `object.__gt__(self, *args, **kwargs)`  |
# |  `long()`     |  `object.__long__(self)`     |  |              |                                          |
# |  `float()`    |  `object.__float__(self)`    |  |              |                                          |
# 
# 
# A rather old (*Python* 2-based), but comprehensive and inclusive summary of magic methods is provided by [Rafe Kettler](https://rszalski.github.io/magicmethods/).
# 
# Still, you may wonder how does a class look like that is capable of using for example the `+` operator with an `__add__` method? Let's define another child of the `Fish` class to build a swarm:

# In[6]:


class Mackerel(Fish):
    def __init__(self, species, *args, **kwargs):
        Fish.__init__(self)
        self.__family = "scombridae"
        self.species = species
        self.count = 1
        
    def __add__(self, value):
        self.count += value
        return self.count
    
    def __mul__(self, multiplier):
        self.count *= multiplier
        return self.count
        
atlantic_mackerel = Mackerel("Scomber scombrus")
print(atlantic_mackerel + 1)
print(atlantic_mackerel * 10)


# (template)=
# ## Custom *Python* Class Template
# 
# This section features a couple of examples with options for implementing public and non-public properties and customizations of *magic* methods to enable the use of operators such as `+` or `<=` with custom classes. So there are many options in writing custom classes and all custom classes should at least incorporate the following methods:
# 
# * `__init__(self, [...)` is the class initializer, which is called when an instance of the class is created. More precisely, it is called along with the `__new__(cls, [...)` method, which is rarely used (read more at [python.org](https://docs.python.org/3/reference/datamodel.html?highlight=__new__%20method#object.__new__)). The initializer gets the arguments passed with which the object was called. For example when `var = MyClass(1, 'vanilla' )`, the `__init__(self, [...)` method gets `1` and `'vanilla'`.
# * `__call__(self, [...)` enables to call a class instance directly, for example `var('cherry')` (corresponds to `var.__call__('cherry')`) may be used to change from `'vanilla'` to `'cherry'`.
# 
# As a result, a robust class skeleton to start with looks like this:

# In[7]:


class NewClass:
    def __init__(self, *args, **kwargs):
        # initialize any class variable here (all self.attributes should be here)
        pass
    
    def methods1_n(self, *args, **kwargs):
        # place class methods between the __init__ and the __call__ methods
        pass
    
    def __call__(self, *args, **kwargs):
        # example prints class structure information to console
        print("Class Info: <type> = NewClass (%s)" % os.path.dirname(__file__))
        print(dir(self))


# Understanding the power and structure of classes and object orientation takes time and requires practicing. The next pages provide some more examples of classes to get more familiar with the concept.

# ```{admonition} Exercise
# Get more familiar with object orientation in the [Sediment transport (1D)](../exercises/ex-sediment) exercise.
# ```

# In[ ]:




