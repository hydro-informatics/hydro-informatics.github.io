---
description: Python Übung zum Aufbau einer grafischen Benutzeroberfläche (GUI) mit tkinter, die ein Sedimenttransportmodul wickelt, kombiniert objektorientierte Programmierung mit NumPy und Pandas.
---

(ex-gui)=
# Erstellen einer GUI

```{admonition} Goals
Diese Übung beinhaltet die Erstellung eines {ref}`chpt-gui` basierend auf den Anweisungen in diesem eBook.
```

```{admonition} Requirements
:class: attention
* Python-Bibliotheken: {ref}`tkinter <chpt-gui>`, {ref}`numpy` und {ref}`pandas`. Lesen und verstehen Sie die Erstellung von {ref}`chpt-gui`.
* Erleben Sie die {ref}`sediment transport exercise <ex-py-sediment>`.
```

Bereiten Sie sich durch Klonen des Übungs-Repository:

```
git clone https://github.com/Ecohydraulics/Exercise-gui.git
```

```{figure} ../img/python/hello-gui.png
```

Before getting started with the exercise, make sure to copy the code from the {ref}`Python sediment transport exercise <ex-py-sediment>` into the `sediment_transport` sub-folder of the GUI exercise repository (i.e., overwrite *bedload.py*, *fun.py*, *grains.py*, *hec.py*, *.py*, *main.py*, and *mpm.py* with your code). If the file names are different from the default names used in the sediment transport exercise, adapt the `__init__.py` file in the `sediment_transport` sub-folder. Thus, we created a module called `sediment_transport`, where the `main.py` file requires some modifications.

* Entfernen Sie die `get_char_grain_size`-Funktion (wird in der GUI ersetzt).
* Fügen Sie drei optionale Argumente an die `main()`Funktion hinzu:
  - `grain_file`, um die Auswahl einer benutzerdefinierten *csv*-Datei für `"grains.csv"` zu ermöglichen
  - `hec_file`, um die Auswahl eines benutzerdefinierten Arbeitsbuchs für *HEC-RAS* Ausgabe zu ermöglichen.
  - `out_folder`, um die Definition eines benutzerdefinierten Ausgabeverzeichnisses für das Geschiebetransport-Ergebnis-Workbook zu aktivieren.

* Ändern Sie die Anrufe in der `main` Funktion:

```python
@log_actions
def main(D_char, hec_file, out_folder):
    hec = HecSet(hec_file)

    mpm_results = calculate_mpm(hec.hec_data, D_char)
    mpm_results.to_excel(out_folder + "\\bed_load_mpm.xlsx")
```



## Machen Sie den Anwendungsrahmen

Erstellen Sie eine neue Python-Datei, rufen Sie sie an `gui.py` und importieren Sie die folgenden Bibliotheken:

```python
import os
import tkinter as tk  # standard widgets (Label, Button, etc.)
from tkinter import ttk  # for Combobox widget
from tkinter.messagebox import askokcancel, showinfo  # infoboxes
from tkinter.filedialog import askopenfilename, askdirectory  # select files or folders
import webbrowser  # open files or URLs from string-type directories
```

Darüber hinaus müssen wir den Sedimenttransportcode importieren (über die `__init__.py`-Datei im `sediment_transport`-Ordner an ein Modul konvertiert):

```python
import sediment_transport as sed
```

`tkinter` ist auf objektorientierte Anwendungen zugeschnitten und deshalb schaffen wir eine neue Klasse namens `SediApp` als Kind von `tk.Frame`:

```python
class SediApp(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
```

### Window Geometrie

Die Initialisierung der `tk.Frame` Elternklasse ist der erste und wichtigste Schritt, den wir bereits oben umgesetzt haben. Dann definieren Sie einen Fenstertitel und ein Fenstersymbol (zum Beispiel das bereitgestellte Symbol `graphs/icon.ico` im Übungsarchiv):

```python
  def __init__(self, master=None):
      ...
      self.master.title("Sedi App")
      self.master.iconbitmap("graphs/icon.ico")
```

```{admonition} TclError: bitmap "graphs/icon.ico" not defined
:class: error
Wenn Sie diese Fehlermeldung oder ähnliche erhalten, stellen Sie sicher, dass der Symbolpfad korrekt ist. Darüber hinaus erinnern Sie daran, dass einige neuere Versionen von `tkinter` wegen eines unbekannten Fehlers, der aus relativen Pfaddefinitionen in der Bibliothek stammen könnte, keine Icons öffnen können. Wenn Sie also sicher sind, dass der Pfad korrekt ist und die Fehlermeldung `TclError: bitmap "graphs/icon.ico" not defined` anhält, kann die einzige Lösung sein, die Zeile `self.master.iconbitmap("graphs/icon.ico")` zu kommentieren.
```

Zuordnen einer Fenstergeometrie mit Fensterbreite und Höhe sowie *x* und *y* Position auf dem Bildschirm in Pixeleinheiten:

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

Um das Layout zu entspannen, verwenden wir später x- und y-Pads für die Widgets (Buttons, Labels und Kombibox). Dazu erstellen Sie zwei *Integer*-Variablen, die einen Puffer von 5 Pixeln um die Widgets definieren.

```python
  def __init__(self, master=None):
      ...
      self.padx = 5
      self.pady = 5
```

### Erstellen von Child Widgets (Buttons, Labels und Combobox)

Um die Auswahl von Getreide- und *HEC-RAS*-Datendateien zu aktivieren, verwenden wir `tk.Button`s und `tk.Label`s informieren den Benutzer über ausgewählte Dateien und Verzeichnisse. Eine `tk.WIDGET` (Button, Label, etc.) kann entweder direkt ohne Instantiation eines Objekts (z.B. `tk.Button(...).grid(...)`) oder als Objekt (z.B. `a_button = tk.Button(...)`) erstellt werden, das später konfiguriert werden kann (z.B. `a_button.grid(...)` oder `a_button.configure(...)`).

***

Wir erstellen drei Tasten, um den Benutzer wählen zu lassen:

1. Eine Eingabe `csv` Datei zur Korngrößenklassifikation,
1. Eine *HEC-RAS* Ausgabe-Workbook (`xlsx`)-Datei und
1. Ein Ausgabeverzeichnis, in dem das resultierende `bed_load_mpm.xlsx`workbook gespeichert wird.

Jede Schaltfläche löst eine Methode von `SediApp` aus, die wir später definieren. Die auszulösenden Methoden werden mit dem `command=self.METHOD()`-Keyword definiert (Anweisungen zur Erstellung eines {ref}`button <add-button>`).

Die Datei- und Ordnerverzeichnisse müssen initialisiert werden, bevor wir sie in den Buttontexten verwenden können. Daher fügen Sie `__init__`:

```python
  def __init__(self, master=None):
      ...
      self.grain_file = "SELECT"
      self.grain_info = None  # will be a sed.GrainReader object when the user defined grains.csv
      self.hec_file = "SELECT"
      self.out_folder = "SELECT"
```

Die drei Tasten zur Auswahl von Dateien und Verzeichnissen müssen nicht später geändert oder neu konfiguriert werden und wir können sie direkt in die `__init__`-Methode einfügen:

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

Um das Programm auszuführen (Bett-Lasttransport-Berechnung), benötigen wir eine andere Schaltfläche, die wir später ändern möchten, um zu kommunizieren, dass das Programm erfolgreich lief. Fügen Sie den Run-Button an `__init__`:

```python
  def __init__(self, master=None):
      ...
      self.b_run = tk.Button(master, bg="white", text="Compute", width=30,
                             command=lambda: self.run_program()
      self.b_run.grid(sticky=tk.W, row=7, column=0, padx=self.padx, pady=self.pady)
```

```{note}
Es gibt einen Unterschied in der Nutzung von `.grid()`, wenn es auf eine `tk.Button`Instanz anstatt direkt mit `tk.Button` zugeschrieben wird.
```

Um den Benutzer die ausgewählten Dateien und Verzeichnisse kennen (zusagen) zu lassen, erstellen Sie `tk.Label` Objekte, die konfigurierbar sein müssen (die ausgewählten Verzeichnisse ändern sich). Folgende Labels an `__init__`:

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

Fügen Sie eine `ttk.Combobox` hinzu, die Korngrößen auflistet und lassen Sie den Benutzer wählen, welchen Wert für charakteristische Korngröße zu verwenden ist. Legen Sie die Kombibox (mit einer leeren Liste) und legen Sie ein Etikett vor der Kombibox (es muss nicht geändert werden) in der `__init__` Methode:

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

### Methoden (Befehle) hinzufügen und mit Widgets anrufen

The above-defined buttons call methods to open file names and directories (as *string*). As file selection dialogues are required twice (grains and *HEC-RAS* data), it makes sense to have a general function for selecting files. Therefore, add a new method to `SediApp` and call it `select_file`. The method uses  `askopenfilename` from `tkinter.filedialog` and takes two input arguments. The first argument (`description`) should be a (very) short description of the file to select. The second argument (`file_type`) represents the file type (ending) that the user should look for. Both arguments are bound as a {ref}`tuple` into a {ref}`list` of `filetypes` that `askopenfilename` uses to narrow down and clarify file selection options.

```{note}
Die `select_file`-Funktion könnte auch auf mehrere Dateitypen erweitert werden (z.B. mehrere Arten von Arbeitsmappen oder Textdateien mit `filetypes=[('Workbook', 'xlsx; xlsx; ods'), ('Text file', '*.csv; *.txt')]`).
```

The `initialdir` keyword argument defines the directory that opens up in the file dialogue window. The `title` keyword argument sets the dialog window's title and `parent` defines the parent window or `tk.Frame` (important when working with multiple `tk.Frame` objects such as [`ttk.Notebook`](https://docs.python.org/3.1/library/tkinter.ttk.html#tkinter.ttk.Notebook) tabs).

```python
    def select_file(self, description, file_type):
        return askopenfilename(filetypes=[(description, file_type)],
                               initialdir=os.path.abspath(""),
                               title="Select a %s file" % file_type,
                               parent=self)
```

Um die Auswahl einer Korn-`csv`-Datei zu ermöglichen, schreiben Sie eine `set_grain_file`-Methode, wie sie mit der obigen `tk.Button` verwendet wird. Die Methode `set_grain_file` öffnet einen Dateiauswahldialog und versucht, die Datei als `GrainReader` Objekt zu öffnen ([Hinzurufen der Sedimenttransport-Übung](https://github.com/Ecohydraulics/Exercise-SedimentTransport#read-grain-size-data)). Wenn sie die gewählte Korngröße `csv`-Datei nicht öffnen kann, fällt die Methode in eine `OSError`-Anweisung und öffnet eine `showinfo`box (von `tkinter.messagebox`), die den Benutzer über den Fehler informiert. Ansonsten (wenn alles in Ordnung ist), aktualisiert die Methode das Getreidelabel (`self.grain_label`) und die Kombibox (`self.cbx_D_char`) mit den Informationen aus der Korngröße `csv`.

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

Um die Auswahl eines *HEC-RAS* {cite:p}`us_army_corps_of_engineeers_hydrologic_2016` Output workbook zu ermöglichen, definieren Sie eine `set_hec_file`-Methode, wie sie in der oben genannten `tk.Button` verwendet wird. Nach der Dateiauswahl des Benutzers muss die Methode das *hec*-label-Objekt (`self.hec_label`) aktualisieren.

```python
    def set_hec_file(self):
        self.hec_file = self.select_file("HEC-RAS output file", "xlsx")
        # update hec label
        self.hec_label.config(text="HEC-RAS output file (xlsx): " + self.hec_file)
```

Die Auswahl eines Ausgabeverzeichnisses verwendet `askdirectory`, das ist eine weitere Methode von `tkinter.filedialog`. Nach der Ordnerauswahl des Benutzers muss die Methode das Ausgabeordner-Labelobjekt (`self.out_label`) aktualisieren.

```python
    def select_out_directory(self):
        self.out_folder = askdirectory()
        # update output folder label
        self.out_label.config(text="Output folder: " + self.out_folder)
```

***

*** Sind alle Benutzereingänge richtig definiert?**

Vor der Beladungsberechnung müssen wir sicherstellen, dass eine Korngrößendatei, *HEC-RAS* Arbeitsmappe und Ausgabeverzeichnis definiert werden, da der Benutzer die `self.b_run`-Taste jederzeit drücken kann. Um sicherzustellen, dass die notwendigen Eingaben bereitgestellt werden, parse`self.grain_file`,`self.hec_file` und `self.out_folder` für den *string*`"SELECT"`, der der Standardwert dieser Variablen ist (d.h. wenn der Benutzer keine Wahl getroffen hat, enthalten die Variablen die *string*`"SELECT"`). Umsetzung der Gültigkeitsprüfung in einer Methode namens `valid_selections`:

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

### Bestimmung der Laufzeitprogrammmethode

Um die App abzuschließen, fügen Sie eine `self.run_program`-Methode hinzu, die der `command`-Funktion der `"Compute"`-Taste (`self.b_run`) entspricht. Die `run_program`-Methode muss sicherstellen, dass der Benutzer die notwendigen Dateien und Ordner durch die `valid_selections`-Methode angegeben hat (und `-1` andernfalls zurückgeben). Dann wird die vom Benutzer in der Kombibox gewählte charakteristische Korngröße von `self.cbx_D_char.get()` bestimmt. Wenn die bereitgestellte Korn `csv`-Datei keinen gültigen numerischen Eintrag für die gewählte charakteristische Korngröße hat, sollte `run_program` eine `ValueError`-Anweisung angeben und den Benutzer über die Ausgabe in einer `showinfo`box informieren.

Ein `askokcancel`Pop-up-Fenster (von `tkinter.messagebox`) bittet den Benutzer, *OK*/*Cancel* zu drücken, um das Programm auszuführen/abbrechen. Wenn der Benutzer auf *OK* klickt, gibt das Pop-up-Fenster `True` zurück und startet die Bettlastberechnung über die `main()`-Funktion von `sed` (siehe oben Import des `sediment_transport`-Moduls).

Nach erfolgreichem Programmablauf setzt die `run_program` Methode die Vordergrundfarbe der `self.b_run`-Taste an `"forest green"` und fügt den Text `"Success: Created %s" % str(self.out_folder + "/bed_load_mpm.xlsx")` an `self.run_label` (definiert in der `__init__`-Methode) hinzu. Das `webbrowser`-Modul `open`-Verfahren eröffnet das neu produzierte {cite:t}`meyer-peter_formulas_1948`-Bett-Lasttransport-Arbeitsbuch (Ergebnis `sed.main(...)`).

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

## Machen Sie das Skript Stand-alone
Um das Fenster zu erstellen, machen Sie `gui.py`stand-alone ausführbar, indem Sie die folgende Erklärung zum Dateiuntergrund hinzufügen (Recall the {ref}`stand-alone descriptions <standalone>`):

```python
if __name__ == '__main__':
    SediApp().mainloop()
```


## Starten Sie die GUI

Führen Sie das Skript *gui.py* aus (z.B. unter {ref}`PyCharm <pycharm>` Rechtsklick im Skript `gui.py` und klicken Sie auf `> Run 'gui'`). Wenn das Skript abstürzt oder Fehlermeldungen anhebt, sie zurückverfolgen und die Probleme beheben. Ansonsten öffnet sich ein Fenster `tkinter`:

![guistart](https://github.com/Ecohydraulics/Exercise-gui/raw/main/graphs/gui-start.png)

Verwenden Sie die Tasten, um eine Korn `csv`-Datei auszuwählen (z.B. [grains.csv](https://github.com/Ecohydraulics/Exercise-SedimentTransport/raw/main/grains.csv) aus der Sedimenttransportübung), eine *HEC-RAS* Ausgabe `xlsx`workbook (z.B. [HEC-RAS/output.xlsx](https://github.com/Ecohydraulics/Exercise-SedimentTransport/raw/main/HEC-RAS/output.xlsx) aus der Sedimenttransportübung) und definieren Sie ein Ausgabeverzeichnis (z.B., *-, */Exec. Stellen Sie sicher, eine charakteristische Korngröße in der Kombibox auszuwählen (z.B.`D84`) und klicken Sie auf die Schaltfläche `Compute`.

Nach einem erfolgreichen Start öffnet die Datei `bed_load_mpm.xlsx`, die Schaltfläche `Compute` wird grün, und das Etikett unter der Schaltfläche bestätigt den erfolgreichen Ablauf (andere Rückverfolgungsfehler und beheben sie). Die GUI sollte nun so aussehen:

![guiend](https://github.com/Ecohydraulics/Exercise-gui/raw/main/graphs/gui-end.png)


```{admonition} Homework
Überprüfen Sie die Gültigkeitsprüfung der Benutzereingänge. Aktivieren Sie den `self.b_run`-Button mit `self.b_run["state"] = "disabled"` und aktivieren Sie den Button (`self.b_run["state"] = "normal"`) erneut, wenn die Benutzereingänge korrekt sind (Ergebnis `valid_selections`). Dazu muss der Anruf an `valid_selections` außerhalb der `run_program`-Methode verschoben werden.
```
