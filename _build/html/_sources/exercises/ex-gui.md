# Create a **G**raphical **U**ser **I**nterface (GUI)


```{admonition} Goals
This exercise features the creation of a Graphical User Interface based on the [course instructions](../python-basics/gui).
```

```{admonition} Requirements
*Python* libraries: *tkinter*, *numpy*, and *pandas*. Read and understand the [creation of GUIs](../python-basics/gui). Accomplish the [sediment transport exercise](https://github.com/Ecohydraulics/Exercise-SedimentTransport).
```

Get ready by cloning the exercise repository:

```
git clone https://github.com/Ecohydraulics/Exercise-gui.git
```

```{figure} ../img/hello-gui.png
:alt: graphical user interface illustration
:name: hello-gui
```

Before getting started with the exercise, make sure to copy the code from the [sediment transport exercise](https://github.com/Ecohydraulics/Exercise-SedimentTransport) into the `sediment_transport` sub-folder of the GUI exercise repository (i.e., overwrite *bedload.py*, *fun.py*, *grains.py*, *hec.py*, *.py*, *main.py*, and *mpm.py* with your code). If the file names are different from the default names used in the sediment transport exercise, adapt the `__init__.py` file in the `sediment_transport` sub-folder. Thus, we created a module called `sediment_transport`, where the `main.py` file requires some modifications.

* Remove the `get_char_grain_size` function (will be replaced in the GUI).
* Add three optional arguments to the `main()` function:
    - `grain_file` to enable the selection of a user-defined *csv* file for `"grains.csv"`
    - `hec_file` to enable the selection of a user-defined workbook for *HEC-RAS* output.
    - `out_folder` to enable the definition of a user-defined output directory for the bed load results workbook.

* Modify the calls in the `main` function:

```python
@log_actions
def main(D_char, hec_file, out_folder):
    hec = HecSet(hec_file)

    mpm_results = calculate_mpm(hec.hec_data, D_char)
    mpm_results.to_excel(out_folder + "\\bed_load_mpm.xlsx")
```



## Make the application frame

Create a new *Python* file, call it `gui.py` and import the following libraries:

```python
import os
import tkinter as tk  # standard widgets (Label, Button, etc.)
from tkinter import ttk  # for Combobox widget
from tkinter.messagebox import askokcancel, showinfo  # infoboxes
from tkinter.filedialog import askopenfilename, askdirectory  # select files or folders
import webbrowser  # open files or URLs from string-type directories
```

Moreover, we need to import the sediment transport code (converted to a module through the `__init__.py` file in the `sediment_transport` folder):

```python
import sediment_transport as sed
```

`tkinter` is tailored for object-oriented applications and this is why we create a new class called `SediApp` as a child of `tk.Frame`:

```python
class SediApp(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
```

### Set window geometry (`__init__`)

The initialization of the `tk.Frame` parent class is the first and most important step that we have already implemented above. Next, define a window title and a window icon (use for example the provided icon `graphs/icon.ico` in the exercise repository):

```python
        self.master.title("Sedi App")
        self.master.iconbitmap("graphs/icon.ico")
```

```{note}
Make sure to get the icon path right. Otherwise the app may crash.
```

Assign a window geometry with window width and height, as well as *x* and *y* position on the screen in pixel units:

```python
        ww = 628  # width
        wh = 382  # height
        # screen position
        wx = (self.master.winfo_screenwidth() - ww) / 2
        wy = (self.master.winfo_screenheight() - wh) / 2
        # assign geometry
        self.master.geometry("%dx%d+%d+%d" % (ww, wh, wx, wy)
```

To relax the layout, we will use x and y pads later for the widgets (buttons, labels, and combobox). For this purpose, create two *integer* variables that define a buffer of 5 pixels around the widgets.

```python
        self.padx = 5
        self.pady = 5
```

### Create child widgets (Buttons, Labels and Combobox in `__init__` method)

To enable the selection of grain and *HEC-RAS* output data files, we will use `tk.Button`s and `tk.Label`s will inform the user about selected files and directories. A `tk.WIDGET` (button, label, etc.) can be created either directly without instantiating an object (e.g., `tk.Button(...).grid(...)`) or as an object (e.g., `a_button = tk.Button(...)`) that can be configured later on (e.g., `a_button.grid(...)` or `a_button.configure(...)`).

***

We will create three buttons to let the user select:

1. An input `csv` file for grain size classification,
1. A *HEC-RAS* output workbook (`xlsx`) file, and
1. An output directory where the resulting `bed_load_mpm.xlsx` workbook will be stored.

Every button triggers a method of `SediApp`, which we will define later on. The methods to trigger are defined with the `command=self.METHOD()` keyword ([recall the instructions for creating a *button*](python-basics/pygui.html#add-a-button-to-call-a-function)).

The file and folder directories need to be initialized before we can use them in the button texts. Therefore, add to `__init__`:

```python
        self.grain_file = "SELECT"
        self.grain_info = None  # will be a sed.GrainReader object when the user defined grains.csv
        self.hec_file = "SELECT"
        self.out_folder = "SELECT"
```

The three buttons for selecting files and directories do not need to be modified or re-configured later and we can directly place them in the `__init__` method:

```python
        # grain file button
        tk.Button(master, text="Select grain csv file", width=30,
                  command=lambda: self.set_grain_file()).grid(column=0, row=0,
                                                              padx=self.padx, pady=self.pady,
                                                              sticky=tk.W)

        # hec file button
        tk.Button(master, text="Select HEC-RAS data workbook", width=30,
                  command=lambda: self.set_hec_file()).grid(column=0, row=2,
                                                            padx=self.padx, pady=self.pady,
                                                            sticky=tk.W)

        # output folder button
        tk.Button(master, text="Select output folder", width=30,
                  command=lambda: self.select_out_directory()).grid(column=0, row=4,
                                                                    padx=self.padx, pady=self.pady,
                                                                    sticky=tk.W)
```

To run the program (bed load transport calculation), we need another button, which we want to modify later on to communicate that the program ran successfully. Add the run button to `__init__`:

```python
        self.b_run = tk.Button(master, bg="white", text="Compute", width=30,
                               command=lambda: self.run_program()
        self.b_run.grid(sticky=tk.W, row=7, column=0, padx=self.padx, pady=self.pady)
```

```{note}
There is a difference of the use of `.grid()` when it is attributed to a `tk.Button` instance rather than directly with `tk.Button`.
```

To let the user know (approve) the selected files and directories, create `tk.Label` objects, which need to be configurable (the selected directories will change). Add the following labels to `__init__`:

```python
        self.grain_label = tk.Label(master, text="Grain file (csv): " + self.grain_file)
        self.grain_label.grid(column=0, columnspan=3, row=1, padx=self.padx, pady=self.pady, sticky=tk.W)
        self.hec_label = tk.Label(master, text="HEC-RAS data file (xlsx): " + self.hec_file)
        self.hec_label.grid(column=0, columnspan=3, row=3, padx=self.padx, pady=self.pady, sticky=tk.W)
        self.out_label = tk.Label(master, text="Output folder: " + self.out_folder)
        self.out_label.grid(column=0, columnspan=3, row=5, padx=self.padx, pady=self.pady, sticky=tk.W)
        self.run_label = tk.Label(master, fg="forest green", text="")
        self.run_label.grid(column=0, columnspan=3, row=8, padx=self.padx, pady=self.pady, sticky=tk.W)
```

Add a `ttk.Combobox` that lists grain sizes and lets the user choose which value to use for characteristic grain size. Place the combobox (with a void list) and put a label in front of the combobox (does not need to be modified) in the `__init__` method:

```python
        # Label for Combobox
        tk.Label(master, text="Select characteristic grain size:").grid(column=0, row=6, padx=self.padx, pady=self.pady, sticky=tk.W)
        # Combobox
        self.cbx_D_char = ttk.Combobox(master, width=5)
        self.cbx_D_char.grid(column=1, row=6, padx=self.padx, pady=self.pady, sticky=tk.W)
        self.cbx_D_char['state'] = 'disabled'
        self.cbx_D_char['values'] = [""]
```

### Add methods (commands) called through widgets

The above-defined buttons call methods to open file names and directories (as *string*). As file selection dialogues are required twice (grains and *HEC-RAS* data), it makes sense to have a general function for selecting files. Therefore, add a new method to `SediApp` and call it `select_file`. The method uses  `askopenfilename` from `tkinter.filedialog` and takes two input arguments. The first argument (`description`) should be a (very) short description of the file to select. The second argument (`file_type`) represents the file type (ending) that the user should look for. Both arguments are bound as a *tuple* into a *list* of `filetypes` that `askopenfilename` uses to narrow down and clarify file selection options.

```{note}
The `select_file` function could also be extended to multiple file types (e.g., include multiple types of workbooks or text files with `filetypes=[('Workbook', 'xlsx; xlsx; ods'), ('Text file', '*.csv; *.txt')]`).
```

The `initialdir` keyword argument defines the directory that opens up in the file dialogue window. The `title` keyword argument sets the dialog window's title and `parent` defines the parent window or `tk.Frame` (important when working with multiple `tk.Frame` objects such as [`ttk.Notebook`](https://docs.python.org/3.1/library/tkinter.ttk.html#tkinter.ttk.Notebook) tabs).

```python
    def select_file(self, description, file_type):
        return askopenfilename(filetypes=[(description, file_type)],
                               initialdir=os.path.abspath(""),
                               title="Select a %s file" % file_type,
                               parent=self)
```

To enable the selection of a grain `csv` file, write a `set_grain_file` method as used with the above `tk.Button`. The `set_grain_file` method opens a file selection dialog and tries to open the file as a `GrainReader` object ([recall sediment transport exercise](https://github.com/Ecohydraulics/Exercise-SedimentTransport#read-grain-size-data)). If it cannot open the selected grain size `csv` file, the method falls into an `OSError` statement and opens a `showinfo` box (from `tkinter.messagebox`) that notifies the user about the error. Otherwise (if everything is OK), the method updates the grain label (`self.grain_label`) and the combobox (`self.cbx_D_char`) with the information read from the grain size `csv` file.

```python
    def set_grain_file(self):
        self.grain_file = self.select_file("grain file", "csv")
        try:
            self.grain_info = sed.GrainReader(self.grain_file)
        except OSError:
            showinfo("ERROR", "Could not open %s." % self.grain_file)
            self.grain_file = "SELECT"
            return -1

        # update grain label
        self.grain_label.config(text="Grain file (csv): " + self.grain_file)

        # update and enable combobox
        self.cbx_D_char['state'] = 'readonly'
        self.cbx_D_char['values'] = list(self.grain_info.size_classes.index)
        self.cbx_D_char.set('D84')
```

To enable the selection of an *HEC-RAS* output workbook, define a `set_hec_file` method as used in the above `tk.Button`. After the user's file selection, the method needs to update the *hec*-label object (`self.hec_label`).

```python
    def set_hec_file(self):
        self.hec_file = self.select_file("HEC-RAS output file", "xlsx")
        # update hec label
        self.hec_label.config(text="HEC-RAS output file (xlsx): " + self.hec_file)
```

The selection of an output directory uses `askdirectory`, which is another method from `tkinter.filedialog`. After the user's folder selection, the method needs to update the output folder label object (`self.out_label`).

```python
    def select_out_directory(self):
        self.out_folder = askdirectory()
        # update output folder label
        self.out_label.config(text="Output folder: " + self.out_folder)
```

***

***Are all user inputs correctly defined?***

Before running the bed load computation, we need to make sure that a grain size file, *HEC-RAS* workbook, and output directory are defined because the user can press the `self.b_run` button at any time. To ensure that the necessary inputs are provided, parse `self.grain_file`, `self.hec_file`, and `self.out_folder` for the *string* `"SELECT"`, which is the default value of these variables (i.e., if the user did not make a choice, the variables contain the *string* `"SELECT"`). Implement the validity check in a method called `valid_selections`:

 ```python
    def valid_selections(self):
        if "SELECT" in self.grain_file:
            showinfo("ERROR", "Select grain size file.")
            return False
        if "SELECT" in self.hec_file:
            showinfo("ERROR", "Select HEC-RAS output file.")
            return False
        if "SELECT" in self.out_folder:
            showinfo("ERROR", "Select output folder.")
            return False
        return True
```

### Define the run program method

To finalize the app, add a `self.run_program` method corresponding to the `command` function of the `"Compute"` button (`self.b_run`) . The `run_program` method must ensure that the user has specified the necessary files and folders by calling the `valid_selections` method (and return `-1` otherwise). Then, the characteristic grain size selected by the user in the combobox is determined by `self.cbx_D_char.get()`. If the provided grain `csv` file has no valid numeric entry for the selected characteristic grain size, `run_program`  should fall into a `ValueError` statement and inform the user about the issue in a `showinfo` box.

An `askokcancel` pop-up window (from `tkinter.messagebox`) asks the user to press *OK*/*Cancel* to run/abort the program. If the user clicks *OK*, the pop-up window returns `True` and starts the bed load computation through the `main()` function of `sed` (see above import of the `sediment_transport` module).

After the successful run of the program, the `run_program` method sets the foreground (text) color of the `self.b_run` button to `"forest green"` and adds the text `"Success: Created %s" % str(self.out_folder + "/bed_load_mpm.xlsx")` to `self.run_label` (defined in the `__init__` method). The `webbrowser` module's `open` method opens the newly produced [Meyer-Peter & Müller (1948)](https://github.com/Ecohydraulics/Exercise-SedimentTransport#mpm) bed load transport workbook (result of `sed.main(...)`).

```python
    def run_program(self):
        # ensure that user selected all necessary inputs
        if not self.valid_selections():
            return -1

        # get selected characteristic grain size
        try:
            D_char = float(self.grain_info.size_classes["size"][str(self.cbx_D_char.get()])
        except ValueError:
            showinfo("ERROR", "The selected characteristic grain size is not correctly defined in the csv file (float?).")
            return -1
        if askokcancel("Start calculation?", "Click OK to start the calculation."):
            sed.main(D_char, self.hec_file, self.out_folder)
            self.b_run.config(fg="forest green")
            self.run_label.config(text="Success: Created %s" % str(self.out_folder + "/bed_load_mpm.xlsx")
            webbrowser.open(self.out_folder + "/bed_load_mpm.xlsx")
```

## Make the script stand-alone
To create the window, make `gui.py` stand-alone executable by adding the following statement to the file bottom ([recall the stand-alone descriptions](python-basics/pypckg.html#standalone):

```python
if __name__ == '__main__':
    SediApp().mainloop()
```


## Launch the GUI
Using [*PyCharm*](get-started/ide.html#pycharm), right-click in the `gui.py` script and click `> Run 'gui'`. If the script crashes or raises error messages, trace them back, and fix the issues. Otherwise, a `tkinter` window opens:

![guistart](https://github.com/Ecohydraulics/Exercise-gui/raw/master/graphs/gui-start.png)

Use the buttons to select a grain `csv` file (e.g., [grains.csv](https://github.com/Ecohydraulics/Exercise-SedimentTransport/raw/master/grains.csv) from the sediment transport exercise), a *HEC-RAS* output `xlsx` workbook (e.g., [HEC-RAS/output.xlsx](https://github.com/Ecohydraulics/Exercise-SedimentTransport/raw/master/HEC-RAS/output.xlsx) from the sediment transport exercise), and define an output directory (e.g., *.../Exercise-gui/*). Make sure to select a characteristic grain size in the combobox (e.g., `D84`) and click on the `Compute` button.

After a successful run, the file `bed_load_mpm.xlsx` opens, the `Compute` button turns green, and the label below the button confirms the successful run (otherwise traceback errors and fix them). The GUI should now look like this:

![guiend](https://github.com/Ecohydraulics/Exercise-gui/raw/master/graphs/gui-end.png)


```{admonition} Homework
Tweak the validity check of user inputs. Deactivate the `self.b_run` button with `self.b_run["state"] = "disabled"` and re-activate the button (`self.b_run["state"] = "normal"`) if the user inputs are correct (result of `valid_selections`). For this purpose, the call to `valid_selections` must be moved outside the `run_program` method.
```
