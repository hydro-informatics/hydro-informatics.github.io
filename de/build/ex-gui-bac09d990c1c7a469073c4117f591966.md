---
description: Python-Übung zum Aufbau einer grafischen Benutzeroberfläche (GUI) mit tkinter, die ein Sedimenttransportmodul umschließt und objektorientierte Programmierung mit NumPy und Pandas kombiniert.
---

(ex-gui)=
# Erstellen einer GUI

```{admonition} Goals
This exercise features the creation of a {ref}`chpt-gui` based on the instructions in this eBook.
```

```{admonition} Requirements
:class: attention
* Python-Bibliotheken: {ref}`tkinter <chpt-gui>`, {ref}`numpy` und {ref}`pandas`. Lesen und verstehen Sie die Erstellung von {ref}`chpt-gui`.
* Verwirklichen Sie {ref}`sediment transport exercise <ex-py-sediment>`.
```

Machen Sie sich bereit, indem Sie das Übungsrepository klonen:

```
git clone https://github.com/Ecohydraulics/Exercise-gui.git
```

```{figure} ../img/python/hello-gui.png
```

Before getting started with the exercise, make sure to copy the code from the {ref}`Python sediment transport exercise <ex-py-sediment>` into the `sediment_transport` sub-folder of the GUI exercise repository (i.e., overwrite *bedload.py*, *fun.py*, *grains.py*, *hec.py*, *.py*, *main.py*, and *mpm.py* with your code). If the file names are different from the default names used in the sediment transport exercise, adapt the `__init__.py` file in the `sediment_transport` sub-folder. Thus, we created a module called `sediment_transport`, where the `main.py` file requires some modifications.

* Remove the `get_char_grain_size` function (will be replaced in the GUI).
* Fügen Sie der Funktion `main()` drei optionale Argumente hinzu:
  - `grain_file`, um die Auswahl einer benutzerdefinierten *csv*-Datei für `"grains.csv"` zu ermöglichen
  - `hec_file` um die Auswahl einer benutzerdefinierten Arbeitsmappe für *HEC-RAS* Ausgabe zu ermöglichen.
  - `out_folder`, um die Definition eines benutzerdefinierten Ausgabeverzeichnisses für die Arbeitsmappe "Geschiebefracht" zu ermöglichen.

* Ändern Sie die Aufrufe in der Funktion `main`:

```python
@log_actions
def main(D_char, hec_file, out_folder):
    hec = HecSet(hec_file)

    mpm_results = calculate_mpm(hec.hec_data, D_char)
    mpm_results.to_excel(out_folder + "\\bed_load_mpm.xlsx")
```



## Erstellen Sie den Application Frame

Erstellen Sie eine neue Python-Datei, rufen Sie sie `gui.py` auf und importieren Sie die folgenden Bibliotheken:

```python
import os
import tkinter as tk  # standard widgets (Label, Button, etc.)
from tkinter import ttk  # for Combobox widget
from tkinter.messagebox import askokcancel, showinfo  # infoboxes
from tkinter.filedialog import askopenfilename, askdirectory  # select files or folders
import webbrowser  # open files or URLs from string-type directories
```

Darüber hinaus müssen wir den Sedimenttransportcode importieren (konvertiert in ein Modul über die `__init__.py`-Datei im Ordner `sediment_transport`):

```python
import sediment_transport as sed
```

`tkinter` ist auf objektorientierte Anwendungen zugeschnitten und deshalb erstellen wir eine neue Klasse namens `SediApp` als Kind von `tk.Frame`:

```python
class SediApp(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
```

### Set Window Geometrie

Die Initialisierung der `tk.Frame`-Elternklasse ist der erste und wichtigste Schritt, den wir oben bereits umgesetzt haben. Als nächstes definieren Sie einen Fenstertitel und ein Fenstersymbol (verwenden Sie zum Beispiel das bereitgestellte Symbol `graphs/icon.ico` im Übungsrepository):

```python
  def __init__(self, master=None):
      ...
      self.master.title("Sedi App")
      self.master.iconbitmap("graphs/icon.ico")
```

```{admonition} TclError: bitmap "graphs/icon.ico" not defined
:class: error
If you get this error message or similar, make sure the icon path is correct. In addition, recall that some recent versions versions of `tkinter` cannot open icons because of an unknown error that might stem from relative path definitions in the library. Therefore, if you are sure the path is correct and the error message `TclError: bitmap "graphs/icon.ico" not defined` persists, the only solution might be to comment out the line `self.master.iconbitmap("graphs/icon.ico")`.
```

Weisen Sie eine Fenstergeometrie mit Fensterbreite und -höhe sowie *x* und *y* Position auf dem Bildschirm in Pixeleinheiten zu:

```python
  def __init__(self, master=None):
      ...
      ww = 628  # width
      wh = 382  # height
      # screen position
      wx = (self.master.winfo_screenwidth() - ww) / 2
      wy = (self.master.winfo_screenheight() - wh) / 2
      # assign geometry
      self.master.geometry("%dx%d+%d+%d" % (ww, wh, wx, wy)
```

Um das Layout zu entspannen, verwenden wir später x- und y-Pads für die Widgets (Tasten, Etiketten und Combobox). Erstellen Sie zu diesem Zweck zwei * ganzzahlige * Variablen, die einen Puffer von 5 Pixeln um die Widgets herum definieren.

```python
  def __init__(self, master=None):
      ...
      self.padx = 5
      self.pady = 5
```

### Erstellen von Child Widgets (Buttons, Labels und Combobox)

Um die Auswahl der Grain- und *HEC-RAS*-Ausgabedatendateien zu ermöglichen, verwenden wir `tk.Button`s und `tk.Label`s informieren den Benutzer über ausgewählte Dateien und Verzeichnisse. Ein `tk.WIDGET` (Button, Label, etc.) kann entweder direkt ohne Instanziierung eines Objekts (z.B. `tk.Button(...).grid(...)`) oder als Objekt (z.B. `a_button = tk.Button(...)`) erstellt werden, das später konfiguriert werden kann (z.B. `a_button.grid(...)` oder `a_button.configure(...)`).

******

Wir erstellen drei Schaltflächen, damit der Benutzer auswählen kann:

1. An input `csv` file for grain size classification,
1. eine *HEC-RAS*-Ausgabe-Arbeitsmappe (`xlsx`) und
1. An output directory where the resulting `bed_load_mpm.xlsx` workbook will be stored.

Every button triggers a method of `SediApp`, which we will define later on. The methods to trigger are defined with the `command=self.METHOD()` keyword (recall the instructions for creating a {ref}`button <add-button>`).

The file and folder directories need to be initialized before we can use them in the button texts. Therefore, add to `__init__`:

```python
  def __init__(self, master=None):
      ...
      self.grain_file = "SELECT"
      self.grain_info = None  # will be a sed.GrainReader object when the user defined grains.csv
      self.hec_file = "SELECT"
      self.out_folder = "SELECT"
```

The three buttons for selecting files and directories do not need to be modified or re-configured later and we can directly place them in the `__init__` method:

```python
  def __init__(self, master=None):
      ...
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
  def __init__(self, master=None):
      ...
      self.b_run = tk.Button(master, bg="white", text="Compute", width=30,
                             command=lambda: self.run_program()
      self.b_run.grid(sticky=tk.W, row=7, column=0, padx=self.padx, pady=self.pady)
```

```{note}
There is a difference in the use of `.grid()` when it is attributed to a `tk.Button` instance rather than directly with `tk.Button`.
```

To let the user know (approve) the selected files and directories, create `tk.Label` objects, which need to be configurable (the selected directories will change). Add the following labels to `__init__`:

```python
  def __init__(self, master=None):
      ...
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
  def __init__(self, master=None):
      ...
      # Label for Combobox
      tk.Label(master, text="Select characteristic grain size:").grid(column=0, row=6, padx=self.padx, pady=self.pady, sticky=tk.W)
      # Combobox
      self.cbx_D_char = ttk.Combobox(master, width=5)
      self.cbx_D_char.grid(column=1, row=6, padx=self.padx, pady=self.pady, sticky=tk.W)
      self.cbx_D_char['state'] = 'disabled'
      self.cbx_D_char['values'] = [""]
```

### Methoden hinzufügen (Befehle) und mit Widgets aufrufen

The above-defined buttons call methods to open file names and directories (as *string*). As file selection dialogues are required twice (grains and *HEC-RAS* data), it makes sense to have a general function for selecting files. Therefore, add a new method to `SediApp` and call it `select_file`. The method uses  `askopenfilename` from `tkinter.filedialog` and takes two input arguments. The first argument (`description`) should be a (very) short description of the file to select. The second argument (`file_type`) represents the file type (ending) that the user should look for. Both arguments are bound as a {ref}`tuple` into a {ref}`list` of `filetypes` that `askopenfilename` uses to narrow down and clarify file selection options.

```{note}
Die Funktion `select_file` kann auch auf mehrere Dateitypen erweitert werden (z. B. mehrere Arten von Arbeitsmappen oder Textdateien mit `filetypes=[('Workbook', 'xlsx; xlsx; ods'), ('Text file', '*.csv; *.txt')]`).
```

The `initialdir` keyword argument defines the directory that opens up in the file dialogue window. The `title` keyword argument sets the dialog window's title and `parent` defines the parent window or `tk.Frame` (important when working with multiple `tk.Frame` objects such as [`ttk.Notebook`](https://docs.python.org/3.1/library/tkinter.ttk.html#tkinter.ttk.Notebook) tabs).

```python
    def select_file(self, description, file_type):
        return askopenfilename(filetypes=[(description, file_type)],
                               initialdir=os.path.abspath(""),
                               title="Select a %s file" % file_type,
                               parent=self)
```

To enable the selection of a grain `csv` file, write a `set_grain_file` method as used with the above `tk.Button`. The `set_grain_file` method opens a file selection dialog and tries to open the file as a `GrainReader` object ([recall the sediment transport exercise](https://github.com/Ecohydraulics/Exercise-SedimentTransport#read-grain-size-data)). If it cannot open the selected grain size `csv` file, the method falls into an `OSError` statement and opens a `showinfo` box (from `tkinter.messagebox`) that notifies the user about the error. Otherwise (if everything is OK), the method updates the grain label (`self.grain_label`) and the combobox (`self.cbx_D_char`) with the information read from the grain size `csv` file.

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

To enable the selection of a *HEC-RAS* {cite:p}`us_army_corps_of_engineeers_hydrologic_2016` output workbook, define a `set_hec_file` method as used in the above `tk.Button`. After the user's file selection, the method needs to update the *hec*-label object (`self.hec_label`).

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

******

***Sind alle Benutzereingaben korrekt definiert?***

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

### Definieren Sie die Run Program Methode

To finalize the app, add a `self.run_program` method corresponding to the `command` function of the `"Compute"` button (`self.b_run`) . The `run_program` method must ensure that the user has specified the necessary files and folders by calling the `valid_selections` method (and return `-1` otherwise). Then, the characteristic grain size selected by the user in the combobox is determined by `self.cbx_D_char.get()`. If the provided grain `csv` file has no valid numeric entry for the selected characteristic grain size, `run_program`  should fall into a `ValueError` statement and inform the user about the issue in a `showinfo` box.

An `askokcancel` pop-up window (from `tkinter.messagebox`) asks the user to press *OK*/*Cancel* to run/abort the program. If the user clicks *OK*, the pop-up window returns `True` and starts the bed load computation through the `main()` function of `sed` (see above import of the `sediment_transport` module).

Nach dem erfolgreichen Ablauf des Programms setzt die `run_program`-Methode die Vordergrund (Text) Farbe des `self.b_run`-Buttons auf `"forest green"` und fügt den Text `"Success: Created %s" % str(self.out_folder + "/bed_load_mpm.xlsx")` zu `self.run_label` hinzu (definiert in der `__init__`-Methode). Die `webbrowser`-Modul `open`-Methode öffnet die neu produzierte {cite:t}`meyer-peter_formulas_1948` Geschiebetransport-Arbeitsmappe (Ergebnis von `sed.main(...)`).

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

## Machen Sie das Script Stand-alone
Um das Fenster zu erstellen, machen Sie `gui.py` stand-alone ausführbar, indem Sie die folgende Anweisung zum Dateiboden hinzufügen (rufen Sie {ref}`stand-alone descriptions <standalone>` an):

```python
if __name__ == '__main__':
    SediApp().mainloop()
```


## Starten Sie die GUI

Run the *gui.py* script (e.g., in {ref}`PyCharm <pycharm>`  right-click in the `gui.py` script and click `> Run 'gui'`). If the script crashes or raises error messages, trace them back, and fix the issues. Otherwise, a `tkinter` window opens:

![guistart](https://github.com/Ecohydraulics/Exercise-gui/raw/main/graphs/gui-start.png)

Verwenden Sie die Schaltflächen, um eine Grain-`csv`-Datei auszuwählen (z. B. [grains.csv](https://github.com/Ecohydraulics/Exercise-SedimentTransport/raw/main/grains.csv) aus der Sedimenttransportübung), eine *HEC-RAS*-Ausgabe `xlsx`-Arbeitsmappe (z. B. [HEC-RAS/output.xlsx](https://github.com/Ecohydraulics/Exercise-SedimentTransport/raw/main/HEC-RAS/output.xlsx) aus der Sedimenttransportübung) und ein Ausgabeverzeichnis zu definieren (z. B. *.../Exercise-gui/*). Stellen Sie sicher, dass Sie eine charakteristische Korngröße in der Combobox auswählen (z. B. `D84`) und klicken Sie auf die Schaltfläche `Compute`.

Nach einem erfolgreichen Durchlauf öffnet sich die Datei `bed_load_mpm.xlsx`, der `Compute`-Button wird grün und das Label unter dem Button bestätigt den erfolgreichen Durchlauf (sonst werden Rückverfolgungsfehler behoben). Die GUI sollte nun so aussehen:

![guiend](https://github.com/Ecohydraulics/Exercise-gui/raw/main/graphs/gui-end.png)


```{admonition} Homework
Optimieren Sie die Gültigkeitsprüfung der Benutzereingaben. Deaktivieren Sie die Schaltfläche `self.b_run` mit `self.b_run["state"] = "disabled"` und aktivieren Sie die Schaltfläche (`self.b_run["state"] = "normal"`), wenn die Benutzereingaben korrekt sind (Ergebnis von `valid_selections`). Zu diesem Zweck muss der Aufruf an `valid_selections` außerhalb der `run_program`-Methode verschoben werden.
```
