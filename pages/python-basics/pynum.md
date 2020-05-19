---
title: Python Basics - Data handling, read & write files
keywords: python, numpy, array, matrix, scipy
summary: "This page shows how data from basic text files can be imported and written with Python. In addition, the math and numeric data handling modules NumPy and pandas are introduced. "
sidebar: mydoc_sidebar
permalink: hypy_pynum.html
folder: python-basics
---

## Load and write data files

Data can be stored in many different (text) file formats such as *txt* or *csv* files. *Python* provides the `open(file)` and `write(...)` functions to read and write data from nearby every text file format, respectively. There are packages such as `csv` (for *csv* files), which simplify handling specific file types. This section illustrates the use of the `load(file)` and `write(...)` functions, and introduces the *pandas* module with its capacity to import and export numeric data along with row and column headers.

### Load (open) text file with data

The `open` command loads text files as file object in *Python*. The syntax of the `open` command is: {#open-modes}


```python
open("file-name", "mode")
```

where:

* `file-name` is the file to open (e.g., `"data.txt"`); if the file is not in the script directory, the *file name* needs to be extended by the full directory (path) to the data file (e.g., `"C:/experiment1/data.txt"`).
* `mode` defines the access type to the file and it can take the following values:
    - `"r"` - read only (default value if no `"mode"` value is provided (the file cannot be modified nor overwritten).
    - `rb"` - read-only in binary format; the binary format is advantageous if the file is not a text file but media such as pictures or videos.
    - `"r+"` - read and write.
    - `"w"` - write only; a new file is created if a file with the same name does not yet exist.
    - `"wb"` - write-only file in binary mode.
    - `"w+"` - write and read.
    - `"wb+"` - write and read in binary mode.
    - `"a"` - append new data to a file; the write-pointer is placed at the end of the file and a new file is created if a file with the provided file name does not yet exist.
    - `"ab"` - append new data in binary mode.
    - `"a+"` - both append (write at the end) and read.
    - `"ab+"` - append and read data in binary mode.

When `"r"` or `"w"` modes are used, the file pointer (i.e, the blinking cursor that you can see for example in Word documents) is place at the beginning of the file. For `"a"` modes, the file pointer is placed at the end of the file.

### Read-only {#read}
Once the file object is created, we can parse the file and copy the file data content to a desired *Python* [data type](hypy_pybase.html#var) (e.g., a list, tuple or dictionary). Parsing the data uses [*for-loops*](hypy_pyloop.html#for) (other loop types will also work) to iterate on lines and line entries. The lines represent *strings*, where the data columns can be separated by using the built-in *string* function `line_as_list = str().split("SEPARATOR")`, where `"SEPARATOR"` can be `","` (comma), `";"` (semicolon), `"|t"` (tab), or any other sign. After reading all data from a file, use `file_object.close()` to avoid that the file is locked by *Python* and cannot be opened by another program.

The following example opens a text file called *pure-numbers.txt* (located in a sub-folder called *data*) that contains *float* numbers between 0.0 and 10.0. The file has 17 data rows (e.g., for 17 experimental runs) and 4 data columns (e.g., for 4 measurements per experimental run), which are separated by a *TAB* (`"\t"` separator) The code snippet uses the built-in function `readlines()` to parse the file lines, splits the lines using the `"\t"` separator, and loops over the line entries to append them to the list variable `data_list`, if `entry` is numeric (verified with the `try` - `except` statement). `data_list` is a nested list that is initiated at the beginning of the script and a sub-list (nested list) is appended for every file line (row).


```python
file_object = open("data/pure-numbers.txt")  # read file with default "mode"="r"

data_list = []  # this will be a nested list with 17 sub-lists (rows) containing 4 entries (columns)=

for line in file_object.readlines():
    line_as_list = line.split("\t")  # converts the line into a list using a tab (\t) separator
    data_list.append([])  # append an empty sub-list for every file line (17 rows)
    for entry in line_as_list:
        try:
            # try to append the entry as floating point number to the last sub-list, which is pointed at using [-1]
            data_list[-1].append(float(entry))
        except ValueError:
            # if entry is not numeric, append 0.0 to the sub-list and print a warning message
            print("Warning: %s is not a number. Replacing value with 0.0." % str(entry))

# verify that data_list contains the 17 rows (sub-lists) with the built-in list function __len__()
print("Number of rows: %d" % data_list.__len__()) 

# verify that the first sub-list has four entries (number of columns)
print("Number of columns: %d" % data_list[0].__len__())

file_object.close()  # close file (otherwise it will be locked as long as Python is still running!)
print(data_list)  # print the data
```

    Number of rows: 17
    Number of columns: 4
    [[2.59, 5.44, 4.06, 4.87], [4.43, 1.67, 1.26, 2.97], [4.04, 8.07, 2.8, 9.8], [2.25, 5.32, 0.04, 5.57], [6.26, 6.15, 5.98, 8.91], [7.93, 0.85, 5.88, 5.4], [4.72, 1.29, 4.18, 2.46], [7.03, 1.43, 5.53, 9.7], [5.2, 7.87, 1.44, 1.13], [3.18, 5.38, 3.6, 7.32], [5.37, 0.62, 5.29, 4.26], [3.48, 2.26, 3.11, 7.3], [1.36, 1.68, 3.38, 6.4], [1.68, 2.31, 9.29, 3.59], [1.33, 1.73, 3.98, 5.74], [2.38, 9.69, 0.06, 4.16], [9.3, 6.47, 9.14, 3.33]]
    

### Create and write files {#create}

A file is created with the `"w"`... file open modes ([see above](#open-modes)) or with `open(file_name, mode="a")`.

{% include tip.html content="When `mode='w'...`, the provided file is opened with the pointer at position zero. Writing data will make the pointer overwrite any existing data at the position. That means any existing data in the opened file will be overwritten. To avoid overwriting of existing file data use `mode='w'...`." %}

Imagine that the above-loaded `data_list` represents measurements in *mm* and we know that the precision of the measuring device was 1.0 *mm*. Thus, all data smaller than 1.0 are within the error margin, which we want to exclude from further analyses by overwriting such values with ***nan*** (***not-a-number***). For this purpose, we first create a new list variable `new_data_list`, where we append *nan* values if `data_list[i, j] <= 1.0` and otherwise we preserve the original numeric value of `data_list`.
With `open("data/modified-data.csv", mode="w+")`, we create a new *csv* (comma-separated values) file in the *data* sub-folder. A *for-loop* iterates on the sub_lists of `new_data_list` and joins them with a comma-separator. In order to join the list elements of `i` (i.e., the sub-lists) with `", ".join(list_of_strings)"`, all list entries first need to be converted to *strings*, which is achieved through the expression `[str(e) for e in row]`. The `"\n"` *string* needs to be concatenated at the end of every line to create a line break (`"\n"` itself will not be visible in the file). The command `new_file.write(new_line)` write the sub-list-converted-to-string to the file `"data/modified-data.csv"`. Once again, `new_file.close()` is needed to avoid that the new *csv* file is locked by *Python*.


```python
# create a new list and overwrite all values <= 1.0 with nan
new_data_list = []  
for i in data_list:
    new_data_list.append([])
    for j in i:
        if j <= 1.0:
            new_data_list[-1].append("nan")
        else:
            new_data_list[-1].append(j)

print(new_data_list)
# write the modified new_data_list to a new text file
new_file = open("data/modified-data.csv", mode="w+")  # lets just use csv: Python does not care about the file ending (could also be file.wayne)
for row in new_data_list:
    new_line = ", ".join([str(e) for e in row]) + "\n"
    new_file.write(new_line)
new_file.close()

```

    [[2.59, 5.44, 4.06, 4.87], [4.43, 1.67, 1.26, 2.97], [4.04, 8.07, 2.8, 9.8], [2.25, 5.32, 'nan', 5.57], [6.26, 6.15, 5.98, 8.91], [7.93, 'nan', 5.88, 5.4], [4.72, 1.29, 4.18, 2.46], [7.03, 1.43, 5.53, 9.7], [5.2, 7.87, 1.44, 1.13], [3.18, 5.38, 3.6, 7.32], [5.37, 'nan', 5.29, 4.26], [3.48, 2.26, 3.11, 7.3], [1.36, 1.68, 3.38, 6.4], [1.68, 2.31, 9.29, 3.59], [1.33, 1.73, 3.98, 5.74], [2.38, 9.69, 'nan', 4.16], [9.3, 6.47, 9.14, 3.33]]
    

### Modify existing files

Existing text files can be opened and modified in either `mode="r+"` (pretending that information needs to be read before it is modified) or `mode="a+"`. Recall that `"r+"` will place the pointer at the beginning of the file and `"a+"` will place the pointer at the end of the file. So if we want to modify existing lines, `"r+"` is the good choice and if we want to append data at the end of the file, `"a+"` is the good choice (`+` is not strictly needed in the case of `"a+"`). This section shows to examples: (1) modification of existing data in a file using `"r+"`, and (2) appending data to an existing file using `"a+"`.

***First example - replacing data:*** In the previous example, we eliminated all measurements that were smaller than 1 *mm* because of the precision of the measurement device. However, we have retained all other values with two-digit accuracy - an accuracy which is not given. Consequently, all decimal places in the measurements must also be eliminated. To achieve this we have to round all measured values with *Python*'s built-in rounding function (`round(number, n-digits`) to zero decimal places (i.e., `n-digits = 0`).
In this example, an exception `IOError` is raised when the file `"data/modified-data.csv"` does not exist (or is locked by another software). An `if` statement ensures that rounding the data is only attempted if the file exists.
The overwriting procedures first reads all lines of the file into the `lines` variable. After reading the lines, the pointer is at the end of the file and `file.seek(0)` puts the pointer back to position 0 (i.e., at the beginning of the file). `file.truncate()` purges the file. Yes, the original file is blank for a moment and all file contents are stored in the `lines` variable. Rounding the data happens within a *for-loop* that:

* Splits the comma-separated line *string* (produces `lines_as_list`).
* Creates the temporary list `_numeric_line_`, where rounded, numeric value are stored (the variable is overwritten in every iteration).
* Loops over the line entries (`line_as_list`), where an exception statement appends rounded (to zero digits), numeric values and appends `"nan"` when an entry is not numeric.
* Writes the modified line to the `"data/modified-data.csv"` *csv* file.

Finally, the *csv* is closed with `modified_file.close()`.


```python
try:
    modified_file = open("data/modified-data.csv", mode="r+")  # re-open the above data file in read-write
except IOError:
    print("The file does not exist.")
    
if modified_file:
    # go here only if the file exists
    lines = modified_file.readlines()  # read lines > pointer moves to file end
    modified_file.seek(0)  # return pointer to file beginning
    modified_file.truncate()  # clear file content
    for line in lines:
        line_as_list = line.split(", ")  # converts the line into a list using comma separator
        _numeric_line_ = []
        for e in line_as_list:
            try: 
                _numeric_line_.append(round(float(e), 0))  # try to convert line entry to float and round to 0 digits
            except ValueError:
                _numeric_line_.append(e)  # for nan values 
        # write rounded values
        modified_file.write(", ".join([str(e) for e in _numeric_line_]) + "\n")
    print("Processed file." )
    modified_file.close()
    
```

    Processed file.
    

Theoretically the above code snippet can be re-written as a function to modify any data in a file. In addition, other threshold values or particular data ranges can be filtered using `if` - `else` statements.

***Second example - appending data:*** By coincidence, you find on one of the measurement protocols that there is an 18th experimental run that is not in the electronic measurement data file due to a data transmission error. Now, we want to add the data to the above-produce *csv* file manually. Entering the data does not take much work, because only 4 measurements were performed per experimental run and we could already manually apply the above filters (`"nan"` and rounding) in a list variable called `forgotten_data`.
This example uses the `os` module ([recall modules](hypy_pckg.html)) to verify if the data file exists with `os.path.isfile()` (the `os.getcwd()` statement is a gadget here). This example features another way of directly opening and writing to the data file using a `with` statement. The `with` statement is particularly useful for file handling because the file object only exists in the indented `with` block, which makes the tedious call to `file.close()` obsolete.

The essential part that writes the line to the data file is `file.write(line)`, where `line` corresponds to the above-introduced `", ".join(list-of-strings) + "\n"` *string*.


```python
import os
print(os.getcwd())
forgotten_data = [4.0, 3.0, "nan", 8.0]

if os.path.isfile("data/modified-data.csv"):
    with open("data/modified-data.csv", mode="a") as file_object:
        file_object.write(", ".join([str(e) for e in forgotten_data]) + "\n")
    print("Data appended.")
else:
    print("The file does not exist.")
```

    C:\Users\schwindt\jupyter\hypy
    Data appended.
    

{% include idea.html content="The code block `', '.join([str(e) for e in a_list]) + '\n'` is a recurring expression in the above code snippets. How can a function look like, which avoids to type this code block again and again?" %}


## NumPy

*NumPy* provides high-level mathematical functions for linear algebra including operations on multi-dimensional arrays and matrices. The open-source *NumPy* package is written in *Python* and [*C*](https://en.wikipedia.org/wiki/C_(programming_language)), and comes with comprehensive documentation ([download the latest version on the developer's web site](https://numpy.org/doc/) or [read the developer's online tutorial](https://numpy.org/devdocs/user/quickstart.html)).

### Installation

*NumPy* can be installed within anaconda ([read instructions](hypy_install.html#install-pckg)) and the developers recommend to use a scientific *Python* distribution (such as *Anaconda*) with [*SciPy Stack*](https://www.scipy.org/install.html).


### Usage

The *NumPy* module (package) is typically imported with `import numpy as np`. Array handling is the baseline of linear algebra and *NumPy*, where arrays represent nested data lists. To create a *NumPy* array, use `np.array((values))`, where `values` is a sequences of values. The rounded parentheses indicated that the value sequence represents a tuple that may contain lists for creating multi-dimensional array. Thus, for creating an *2x3* array (with some random values), we can write:


```python
import numpy as np
an_array = np.array(([2, 3, 1], [4, 5, 6]))
print(an_array)
```

    [[2 3 1]
     [4 5 6]]
    

In the above example, measurement data were loaded from text files, manipulated, and modified text file were written. The data manipulation involved the introduction of `"nan"` (*not-a-number*) values, which were excluded because measurements *<1 mm* were considered errors. Why didn't we use zeros here? Well, zeros are numbers, too, and have significant effect on data statistics (e.g., for calculting mean values). However, the `"nan"` *string* value caused difficulties in data handling, in particular regarding the consistency of function output. *NumPy* provides with the `numpy.nan` data type a powerful alternative to the tedious `"nan"` *string*.

## Array and file handling with pandas

