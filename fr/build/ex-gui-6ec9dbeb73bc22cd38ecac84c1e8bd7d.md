---
description: Exercice de Python pour la construction d'une interface utilisateur graphique (GUI) avec tkinter qui enveloppe un module de transport des sédiments, combinant la programmation orientée objet avec NumPy et pandas.
---

(ex-gui)=
# Créer une interface graphique

```{admonition} Goals
Cet exercice comporte la création d'un {ref}`chpt-gui` basé sur les instructions de ce livre électronique.
```

```{admonition} Requirements
:class: attention
* Bibliothèques Python : {ref}`tkinter <chpt-gui>`, {ref}`numpy`, et {ref}`pandas`. Lisez et comprenez la création de {ref}`chpt-gui`.
* Accomplir le {ref}`sediment transport exercise <ex-py-sediment>`.
```

Préparez-vous en clonant le dépôt d'exercices :

```
git clone https://github.com/Ecohydraulics/Exercise-gui.git
```

```{figure} ../img/python/hello-gui.png
```

Avant de commencer l'exercice, assurez-vous de copier le code de {ref}`Python sediment transport exercise <ex-py-sediment>` dans le sous-dossier `sediment_transport` du dépôt d'exercices GUI (c.-à-d. écraser *bedload.py*, *fun.py*, *grains.py*, *hec.py*, *.py*, *main.py* et *mpm.py* avec votre code). Si les noms des fichiers sont différents des noms par défaut utilisés dans l'exercice de transport des sédiments, adapter le fichier `__init__.py` dans le sous-dossier `sediment_transport`. Ainsi, nous avons créé un module appelé `sediment_transport`, où le fichier `main.py` nécessite quelques modifications.

* Supprimer la fonction `get_char_grain_size` (sera remplacée dans l'interface graphique).
* Ajouter trois arguments optionnels à la fonction `main()`:
  - `grain_file` pour activer la sélection d'un fichier *csv* défini par l'utilisateur pour `"grains.csv"`
  - `hec_file` pour activer la sélection d'un classeur défini par l'utilisateur pour la sortie *HEC-RAS*.
  - `out_folder` pour activer la définition d'un répertoire de sortie défini par l'utilisateur pour le cahier des résultats de la charge de lit.

* Modifier les appels dans la fonction `main`:

```python
@log_actions
def main(D_char, hec_file, out_folder):
    hec = HecSet(hec_file)

    mpm_results = calculate_mpm(hec.hec_data, D_char)
    mpm_results.to_excel(out_folder + "\\bed_load_mpm.xlsx")
```



## Faire le cadre d'application

Créer un nouveau fichier Python, l'appeler `gui.py` et importer les bibliothèques suivantes :

```python
import os
import tkinter as tk  # standard widgets (Label, Button, etc.)
from tkinter import ttk  # for Combobox widget
from tkinter.messagebox import askokcancel, showinfo  # infoboxes
from tkinter.filedialog import askopenfilename, askdirectory  # select files or folders
import webbrowser  # open files or URLs from string-type directories
```

De plus, nous devons importer le code de transport des sédiments (converti dans un module à travers le fichier `__init__.py` dans le dossier `sediment_transport`):

```python
import sediment_transport as sed
```

`tkinter` est adapté aux applications orientées objet et c'est pourquoi nous créons une nouvelle classe appelée `SediApp` comme un enfant de `tk.Frame`:

```python
class SediApp(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
```

### Définir la géométrie de la fenêtre

L'initialisation de la classe `tk.Frame` parent est la première et la plus importante étape que nous avons déjà mise en œuvre ci-dessus. Ensuite, définissez un titre de fenêtre et une icône de fenêtre (utiliser par exemple l'icône fournie `graphs/icon.ico` dans le dépôt d'exercices):

```python
  def __init__(self, master=None):
      ...
      self.master.title("Sedi App")
      self.master.iconbitmap("graphs/icon.ico")
```

```{admonition} TclError: bitmap "graphs/icon.ico" not defined
:class: error
Si vous obtenez ce message d'erreur ou similaire, assurez-vous que le chemin de l'icône est correct. En outre, rappelez-vous que certaines versions récentes de `tkinter` ne peuvent pas ouvrir d'icônes à cause d'une erreur inconnue qui pourrait découler de définitions relatives de chemin dans la bibliothèque. Par conséquent, si vous êtes sûr que le chemin est correct et que le message d'erreur `TclError: bitmap "graphs/icon.ico" not defined` persiste, la seule solution pourrait être de commenter la ligne `self.master.iconbitmap("graphs/icon.ico")`.
```

Attribuer une géométrie de fenêtre avec largeur et hauteur de fenêtre, ainsi que *x* et *y* position sur l'écran en unités de pixel:

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

Pour détendre la mise en page, nous utiliserons plus tard des tampons x et y pour les widgets (boutons, étiquettes et combobox). Pour cela, créez deux variables *entier* qui définissent un tampon de 5 pixels autour des widgets.

```python
  def __init__(self, master=None):
      ...
      self.padx = 5
      self.pady = 5
```

### Créer des widgets pour enfants (boutons, étiquettes et combobox)

Pour activer la sélection des fichiers de données grain et *HEC-RAS*, nous utiliserons `tk.Button`s et `tk.Label`s informera l'utilisateur des fichiers et répertoires sélectionnés. Une adresse `tk.WIDGET` (bouton, étiquette, etc.) peut être créée soit directement, soit sans mettre en place un objet (par exemple, `tk.Button(...).grid(...)`) ou en tant qu'objet (par exemple, `a_button = tk.Button(...)`) qui peut être configuré plus tard (par exemple, `a_button.grid(...)` ou `a_button.configure(...)`).

****

Nous allons créer trois boutons pour laisser l'utilisateur sélectionner :

1. Une entrée `csv` fichier pour la classification de la taille du grain,
1. un manuel de sortie *HEC-RAS* (`xlsx`) et
1. Un répertoire de sortie où le cahier de travail `bed_load_mpm.xlsx` sera stocké.

Chaque bouton déclenche une méthode de `SediApp`, que nous définirons plus tard. Les méthodes à déclencher sont définies avec le mot clé `command=self.METHOD()` (appelez les instructions pour créer un {ref}`button <add-button>`).

Les répertoires de fichiers et de dossiers doivent être initialisés avant de pouvoir les utiliser dans les textes des boutons. Par conséquent, ajouter à `__init__`:

```python
  def __init__(self, master=None):
      ...
      self.grain_file = "SELECT"
      self.grain_info = None  # will be a sed.GrainReader object when the user defined grains.csv
      self.hec_file = "SELECT"
      self.out_folder = "SELECT"
```

Les trois boutons de sélection des fichiers et des répertoires n'ont pas besoin d'être modifiés ou reconfigurés plus tard et nous pouvons les placer directement dans la méthode `__init__`:

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

Pour exécuter le programme (calcul de la charge de chargement), nous avons besoin d'un autre bouton, que nous voulons modifier plus tard pour communiquer que le programme a fonctionné avec succès. Ajouter le bouton d'exécution à `__init__`:

```python
  def __init__(self, master=None):
      ...
      self.b_run = tk.Button(master, bg="white", text="Compute", width=30,
                             command=lambda: self.run_program()
      self.b_run.grid(sticky=tk.W, row=7, column=0, padx=self.padx, pady=self.pady)
```

```{note}
Il y a une différence dans l'utilisation de `.grid()` quand elle est attribuée à une instance `tk.Button` plutôt que directement à `tk.Button`.
```

Pour informer l'utilisateur (approuver) des fichiers et répertoires sélectionnés, créez des objets `tk.Label` qui doivent être configurables (les répertoires sélectionnés vont changer). Ajouter les étiquettes suivantes à `__init__`:

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

Ajouter un `ttk.Combobox` qui énumère les tailles de grain et permet à l'utilisateur de choisir la valeur à utiliser pour la taille de grain caractéristique. Placez la combobox (avec une liste vide) et placez une étiquette devant la combobox (il n'est pas nécessaire de modifier) dans la méthode `__init__`:

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

### Ajouter des méthodes (commandes) et les appeler avec Widgets

Les boutons ci-dessus appellent des méthodes pour ouvrir les noms de fichiers et les répertoires (comme *string*). Comme les dialogues de sélection des fichiers sont requis deux fois (grains et données *HEC-RAS*), il est logique d'avoir une fonction générale pour sélectionner les fichiers. Par conséquent, ajouter une nouvelle méthode à `SediApp` et l'appeler `select_file`. La méthode utilise `askopenfilename` de `tkinter.filedialog` et prend deux arguments d'entrée. Le premier argument (`description`) doit être une courte description du fichier à sélectionner. Le deuxième argument (`file_type`) représente le type de fichier (fin) que l'utilisateur devrait rechercher. Les deux arguments sont liés comme un {ref}`tuple` dans un {ref}`list` de `filetypes` que `askopenfilename` utilise pour restreindre et clarifier les options de sélection de fichiers.

```{note}
La fonction `select_file` pourrait aussi être étendue à plusieurs types de fichiers (p. ex., inclure plusieurs types de cahiers de travail ou de fichiers texte avec `filetypes=[('Workbook', 'xlsx; xlsx; ods'), ('Text file', '*.csv; *.txt')]`).
```

The `initialdir` keyword argument defines the directory that opens up in the file dialogue window. The `title` keyword argument sets the dialog window's title and `parent` defines the parent window or `tk.Frame` (important when working with multiple `tk.Frame` objects such as [`ttk.Notebook`](https://docs.python.org/3.1/library/tkinter.ttk.html#tkinter.ttk.Notebook) tabs).

```python
    def select_file(self, description, file_type):
        return askopenfilename(filetypes=[(description, file_type)],
                               initialdir=os.path.abspath(""),
                               title="Select a %s file" % file_type,
                               parent=self)
```

Pour permettre la sélection d'un fichier de grain `csv`, écrivez une méthode `set_grain_file` telle qu'utilisée avec la méthode `tk.Button` ci-dessus. La méthode `set_grain_file` ouvre une boîte de dialogue de sélection des fichiers et tente d'ouvrir le fichier sous la forme d'un objet `GrainReader` ([rappeler l'exercice de transport des sédiments](https://github.com/Ecohydraulics/Exercise-SedimentTransport#read-grain-size-data)). S'il ne peut pas ouvrir le fichier `csv`, la méthode tombe dans une déclaration `OSError` et ouvre une boîte `showinfo` (à partir de `tkinter.messagebox`) qui avise l'utilisateur de l'erreur. Autrement (si tout est OK), la méthode met à jour l'étiquette du grain (`self.grain_label`) et la combobox (`self.cbx_D_char`) avec les informations lues à partir de la taille du grain `csv` fichier.

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

Pour permettre la sélection d'un workbook de sortie *HEC-RAS* {cite:p}`us_army_corps_of_engineeers_hydrologic_2016`, définissez une méthode `set_hec_file` telle qu'utilisée dans la méthode `tk.Button` ci-dessus. Après la sélection du fichier de l'utilisateur, la méthode doit mettre à jour l'objet *hec*-label (`self.hec_label`).

```python
    def set_hec_file(self):
        self.hec_file = self.select_file("HEC-RAS output file", "xlsx")
        # update hec label
        self.hec_label.config(text="HEC-RAS output file (xlsx): " + self.hec_file)
```

La sélection d'un répertoire de sortie utilise `askdirectory`, qui est une autre méthode de `tkinter.filedialog`. Après la sélection du dossier de l'utilisateur, la méthode doit mettre à jour l'objet d'étiquette du dossier de sortie (`self.out_label`).

```python
    def select_out_directory(self):
        self.out_folder = askdirectory()
        # update output folder label
        self.out_label.config(text="Output folder: " + self.out_folder)
```

****

***Toutes les entrées utilisateur sont-elles correctement définies?***

Avant d'exécuter le calcul de la charge de lit, nous devons nous assurer qu'un fichier de taille de grain, un cahier de travail *HEC-RAS* et un répertoire de sortie sont définis parce que l'utilisateur peut appuyer sur le bouton `self.b_run` à tout moment. Pour s'assurer que les entrées nécessaires sont fournies, analysez `self.grain_file`, `self.hec_file`, et `self.out_folder` pour le *string* `"SELECT"`, qui est la valeur par défaut de ces variables (i.e., si l'utilisateur n'a pas fait de choix, les variables contiennent le *string* `"SELECT"`). Mettre en œuvre la vérification de validité dans une méthode appelée `valid_selections`:

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

### Définir la méthode d'exécution du programme

Pour finaliser l'application, ajoutez une méthode `self.run_program` correspondant à la fonction `command` du bouton `"Compute"` (`self.b_run`) . La méthode `run_program` doit s'assurer que l'utilisateur a spécifié les fichiers et dossiers nécessaires en appelant la méthode `valid_selections` (et retour `-1` sinon). Ensuite, la taille caractéristique du grain sélectionnée par l'utilisateur dans la combobox est déterminée par `self.cbx_D_char.get()`. Si le fichier de grain fourni `csv` n'a pas d'entrée numérique valide pour la taille de grain caractéristique sélectionnée, `run_program` devrait tomber dans une déclaration `ValueError` et informer l'utilisateur du problème dans une boîte `showinfo`.

Une fenêtre `askokcancel` pop-up (à partir de `tkinter.messagebox`) demande à l'utilisateur d'appuyer sur *OK*/*Annuler* pour exécuter/avorter le programme. Si l'utilisateur clique *OK*, la fenêtre pop-up retourne `True` et commence le calcul de la charge de lit par la fonction `main()` `sed` (voir ci-dessus l'importation du module `sediment_transport`).

Après la réussite du programme, la méthode `run_program` définit la couleur du premier plan (texte) du bouton `self.b_run` à `"forest green"` et ajoute le texte `"Success: Created %s" % str(self.out_folder + "/bed_load_mpm.xlsx")` à `self.run_label` (défini dans la méthode `__init__`). La méthode `webbrowser` du module `open` ouvre le nouveau manuel de transport de charge de lit {cite:t}`meyer-peter_formulas_1948` (résultat de `sed.main(...)`).

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

## Faites le script autonome
Pour créer la fenêtre, faites `gui.py` exécutable autonome en ajoutant la déclaration suivante au bas du fichier (appelez {ref}`stand-alone descriptions <standalone>`):

```python
if __name__ == '__main__':
    SediApp().mainloop()
```


## Lancez l'interface graphique

Exécutez le script *gui.py* (par exemple, {ref}`PyCharm <pycharm>` clic droit dans le script `gui.py` et cliquez sur `> Run 'gui'`). Si le script s'écrase ou soulève des messages d'erreur, retracez-les et corrigez les problèmes. Sinon, une fenêtre `tkinter` s'ouvre :

[guistart](https://github.com/Ecohydraulics/Exercise-gui/raw/main/graphs/gui-start.png)

Utilisez les boutons pour sélectionner un fichier de grain `csv` (p. ex., [grains.csv](https://github.com/Ecohydraulics/Exercise-SedimentTransport/raw/main/grains.csv) de l'exercice de transport des sédiments), une sortie *HEC-RAS* `xlsx` workbook (p. ex., [HEC-RAS/output.xlsx](https://github.com/Ecohydraulics/Exercise-SedimentTransport/raw/main/HEC-RAS/output.xlsx) de l'exercice de transport des sédiments) et définir un répertoire de sortie (p. ex., *.../Exercise-gui/*). Assurez-vous de sélectionner une taille de grain caractéristique dans la combobox (p. ex. `D84`) et cliquez sur le bouton `Compute`.

Après une course réussie, le fichier `bed_load_mpm.xlsx` s'ouvre, le bouton `Compute` devient vert, et l'étiquette ci-dessous le bouton confirme la course réussie (autrement les erreurs de trace de retour et de les corriger). L'interface utilisateur devrait maintenant ressembler à ceci :

[guiend](https://github.com/Ecohydraulics/Exercise-gui/raw/main/graphs/gui-end.png)


```{admonition} Homework
Modifier la vérification de validité des entrées utilisateur. Désactiver le bouton `self.b_run` avec `self.b_run["state"] = "disabled"` et réactiver le bouton (`self.b_run["state"] = "normal"`) si les entrées utilisateur sont correctes (résultat `valid_selections`). À cette fin, l'appel à `valid_selections` doit être déplacé en dehors de la méthode `run_program`.
```
