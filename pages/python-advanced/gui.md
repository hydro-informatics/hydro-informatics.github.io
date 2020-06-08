---
title: Advanced Python - Graphical User Interfaces (GUIs)
keywords: gui python
sidebar: mydoc_sidebar
permalink: hypy_gui.html
folder: python-advanced
---

{% include image.html file="hello-gui.png" %}

A Graphical User Interface (GUI) facilitates setting input variables of scripts. This is particularly useful if you want to reuse a script that you have written a long time ago without having to study the whole script again in detail. Although it is arguable whether GUIs are still appropriate in times of web applications, large and in particular copyrighted data must be processed locally. And for local data processing, a GUI is a very convenient way to control self-written, custom programs.

Several GUI library (packages) are available for *Python* and this introduction uses the [`tkinter`](https://docs.python.org/3/library/tkinter.html) library. Alternatives are, for example, [*wxPython*](https://www.wxpython.org/) or [*Jython*](https://www.jython.org/) (a *Java* implementation of *Python 2*). `tkinter` is a standard library, which does not need to be installed additionally. For a quick example, type in the terminal (e.g., *PyCharm* or *Linux* terminal - not in the *Python* console):
python -m tkinter
{% include unix.html content="If you encounter troubles with `tkinter` on *Linux*, make sure that `tkinter` for *Python* is installed, either with <br>`sudo apt-get install python3-tk`  or <br>`sudo apt-get install python3.X-tk` (replace `X` with your *Python* version) or<br> `sudo apt install tk8.6-dev` to install the library only (this should be sufficient). <br>If the above comments do not work, make sure that the `tkinter` repository is available to your system: `sudo add-apt-repository ppa:deadsnakes/ppa` (the repository address may change and depends on your *Linux* and *Python* versions)." %}

`tkinter` works on many popular platforms (*Linux*, *macOS*, *Windows*) and is not only available to *Python*, but also to [*Ruby*](https://www.ruby-lang.org), [*Perl*](https://www.perl.org/), [*Tcl*](https://www.tcl-lang.org/) (the origin of of `tkinter`), and many more languages. Because of its support for languages like *Ruby* or *Perl*, `tkinter` can be used for local GUIs as well as for web applications.

## The first GUI 
The very first step is to import `tkinter`, usually using the alias `as tk`. With `tk.Tk()`, a so-called parent window (e.g., `top`) can be created, in which all further elements will be accommodated. All futher elements are created as `tk` objects as child of the parent window and placed (arranged) in the parent window using the `pack()` or `.grid()` method. Here, we will use `pack` most of the time and `grid` will be useful to place elements at an exact position on the window (e.g., `tk.ELEMENT.grid(row=INT, column=INT)`). To display the GUI, the parent window `top` must be launched with `top.mainloop()` after arranging all elements. The following code block shows how to create a parent window with a label element (`tk.Label`).


```python
import tkinter as tk
top = tk.Tk()
a_label = tk.Label(top, text = "A label just shows some text.")
a_label.pack()
top.mainloop()
```

{% include image.html file="py-tk-first.png" %}

After calling the `mainloop()` method the window is in a *wait* state. That means, the window is waiting for `events` being triggered through user action action (e.g., a click on a button). This is called *event-driven programming*, where *event handlers* are called rather than a single linear flow of (*Python*) commands.

For now, our window uses default values, for example for the window title, size and background color. These window properties can be modified with the `title`, `minsize` or `maxsize`, and `configure` attributes of the `top` parent window:


```python
top = tk.Tk()
a_label = tk.Label(top, text="A label just shows some text.")
a_label.pack()

top.title("My first GUI App")
top.minsize(628, 382)
top.configure(bg="sky blue")
top.mainloop()
```

{% include image.html file="py-tk-first-config.png" %}

## Add a Button to call a function
 
So far our window only shows a (boring) label and waits for events that do not exist. With a `tk.Button` we now add an event trigger. So that the event has something to trigger, we define a `call_back` function that creates an infobox. The infobox is an object of `showinfo` from `tkinter.messagebox`.


```python
from tkinter.messagebox import showinfo
# more message boxes: askokcancel, askyesno

def call_back(message):
    showinfo("This is an Infobox", message)


top = tk.Tk()
a_label = tk.Label(top, text="Here is the button.")
a_label.pack()
# add a button
a_button = tk.Button(top, text = ">> Click <<", command=lambda: call_back("Greetings from the Button."))
a_button.pack()
top.mainloop()
```

{% include image.html file="py-tk-button.png" %}

{% include note.html content="The `command` receives a [`lambda`](hypy_pyfun.html#lambda) function that links to the `call_back` function. Why do we need this complication? The answer is that the `call_back` function will be automatically triggered with the `mainloop()` method if we were not using a `lambda` function here." %}

## A vanilla `tkinter` program

So far we have created single `tkinter` objects (*widgets*) in script-style. However, when we write a GUI, we most likely want to start an application (*App*) by just running a script. This is why `tkinter` widgets are usually created as objects of custom classes. Therefore, we want to recast our example as object-oriented code according to the template from the [lecture on *Python* classes](hypy_classes.html#template).

The below example creates a `VanillaApp`, which is a child of `tk.Frame` (`tkinters` master frame). The initialization method `__init__` needs to invoke `tk.Frame` and `pack()` it to initialize the window. After that, we can place other `widget`s such as labels and buttons as before. In the `VanillaApp`, we can also directly implement the `call_back` function from above as a method. Moreover, we want the below script to run stand-alone, also it is not part of a beautiful *jupyter* notebook. For this reason, the `if __name__ == "__main__": VanillaApp().mainloop()` statement is required at the bottom of the script (read more about the `__main__` statement on the [packages page](hypy_pckg.html#standalone)).


```python
# define the VanillaApp class
class VanillaApp(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        
        table_label = tk.Label(master, text="Do you want vanilla ice?")
        table_label.pack()
        vanilla_button = tk.Button(master, text = "I want Vanilla", command=lambda: call_back("Here is Vanilla!"))
        vanilla_button.pack()
        no_vanilla_button = tk.Button(master, text = "I want something else", command=lambda: call_back("Here is bread!"))
        no_vanilla_button.pack()
        
    def call_back(self, message):
        showinfo("This is an Infobox", message)


# instantiate a VanillaApp object
if __name__ == "__main__":
    VanillaApp().mainloop()
```

{% include image.html file="py-tk-vanilla.png" %}

{% include tip.html content="The above code block with the `VanillaApp` class can be copied to any external *Python* file and saved as, for example, `vanilla_app.py`. With *Python*  being defined as a [system variable](https://docs.python.org/3/using/windows.html#excursus-setting-environment-variables) (only necessary in *Windows* - point at your *Anaconda* base environment's *Python* executable), the GUI can then be started as follows:<br>1) Open Terminal (or command line `cmd` in *Windows*).<br>2) Navigate to the directory where the script is located (use `cd` in [*Windows*](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/cd) or [*Linux/macOS*](http://www.linfo.org/cd.html)).<br>3) Type `python vanilla_app.py` (or `python -m vanilla_app.py`) to launch the GUI.<br>Another tip: this sequence of commands can also be written to a batch file ([`.bat` on *Windows*](https://www.wikihow.com/Write-a-Batch-File)) or shell script ([.sh on *Linux/macOS*](https://www.linux.com/training-tutorials/writing-simple-bash-script/) - [alternative source](http://linuxcommand.org/lc3_writing_shell_scripts.php)). Then, a double click on the batch file starts the *Python* based GUI." %}

## More *Widget*s

Are there only labels and buttons? There are many more widgets and the following illustration features some of them.
