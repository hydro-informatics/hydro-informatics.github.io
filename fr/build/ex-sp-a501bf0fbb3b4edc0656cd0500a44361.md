---
description: Exercice Python pour le calcul du volume saisonnier de stockage des réservoirs à l'aide de l'algorithme Sequent Peak, avec traitement des données NumPy et analyse des séries chronologiques hydrologiques.
---

(ex-seq-peak)=
# Volume du réservoir (Algorithme de pic de séquence)

```{admonition} Goals & requirements
**Objectifs**: Écrivez des fonctions personnalisées, chargez les données à partir de fichiers texte délimités de type virgule et manipulez les données avec *numpy*. Utilisez efficacement les boucles et les exceptions d'erreur.

**Exigences**
    * Bibliothèques Python : {ref}`numpy` y compris *scipy* et *matplotlib*.
    * Lisez et comprenez le traitement des données avec {ref}`numpy` et {ref}`functions <chpt-functions>`.
```

Préparez-vous en clonant le dépôt d'exercices :

```
git clone https://github.com/Ecohydraulics/Exercise-SequentPeak.git
```

```{figure} https://github.com/Ecohydraulics/media/raw/main/jpg/new_bullards_bar.jpg
:alt: New Bullards Bar Dam California USA Yuba River
:name: new-bullards

Nouveau barrage Bullards Bar en Californie, États-Unis (source: Sebastian Schwindt 2017).
```


## Théorie
Les réservoirs de stockage saisonniers conservent l'eau pendant les mois humides (par exemple, la mousson ou les hivers pluvieux dans les climats méditerranéens) afin d'assurer un approvisionnement suffisant en eau potable et en agriculture pendant les mois secs. À cette fin, d'énormes volumes de stockage sont nécessaires, qui dépassent souvent 1 000 000 m$^3$.

Le volume de stockage nécessaire est déterminé à partir de mesures historiques des débits et des volumes cibles de rejets (p. ex., l'agriculture, l'eau potable, l'hydroélectricité ou les quantités d'eau résiduelles écologiques).
L'algorithme de pic séquentiel {cite:p}`potter1977` basé sur {cite:t}`rippl1883` est une procédure vieille de plusieurs décennies pour déterminer le volume de stockage saisonnier nécessaire basé sur une courbe de volume de stockage (*** courbe SD***). La figure ci-dessous montre une courbe exemplaire $SD$ avec des pics de volume (maxima locale) environ tous les 6 mois et des minima de volume locaux entre les pics. Le volume entre le dernier maximum local et le minimum local le plus bas suivant détermine le volume de stockage requis (voir la ligne bleu vif dans la figure).

```{figure} https://github.com/Ecohydraulics/media/raw/main/png/sequent_peak.png
:alt: sequent peak algorithm
:name: sequentpeak

Schéma de l'algorithme de crête séquentielle.
```

L'algorithme de crête séquentielle répète ce calcul sur plusieurs années et le volume le plus élevé observé détermine le volume requis.

Dans le cadre de cet exercice, nous utilisons des mesures quotidiennes des débits de la rivière Vanilla (dans le pays aride de Vanilla avec des périodes de mousson) et nous visons les volumes d'écoulement pour fournir aux agriculteurs et à la population du pays aride de Vanilla suffisamment d'eau pendant les saisons sèches. Cet exercice vous guide en chargeant les données de décharge quotidiennes, en créant la courbe mensuelle $SD$ (stockage) et en calculant le volume de stockage requis.


## Prétraitement des données de flux

Les données quotidiennes de débit de la rivière Vanilla sont disponibles de 1979 à 2001 sous la forme de fichiers `.csv` ([`flows` dossier](https://github.com/Ecohydraulics/Exercise-SequentPeak/tree/master/flows)).

### Écrire une fonction pour lire les données de flux

La fonction va passer en boucle les noms de fichiers *csv* et ajouter le contenu du fichier à un dictionnaire de tableaux *numpy*. Assurez-vous à `import numpy as np`, `import os` et `import glob`.

* Choisissez un nom de fonction (p. ex. `def read_data(args):`) et utilisez les arguments d'entrée suivants :
    * `directory`: *string* d'un chemin vers les fichiers
    * `fn_prefix`: *string* du préfixe de fichier pour enlever les clés de dictée d'un nom de fichier
    * `fn_suffix`: *string* du suffixe de fichier pour enlever les clés de dictées d'un nom de fichier
    * `ftype`: *chaîne* de fin de fichier
    * `delimiter`: *chaîne* du séparateur de colonnes
* In the function, test if the provided directory ends on `"/"` or `"\\"` with <br> `directory.endswith("/") or directory.endswith("\\")`<br>and read all files that end with `ftype` (we will use `ftype="csv"` here) with the `glob` library:
    * `if True:` obtenir la liste des fichiers *csv* (`ftype`) comme <br> `file_list = glob.glob(directory + "*." + ftype.strip(".")`.
    * `if False:` obtenir la liste de fichiers *csv* (`ftype`) comme <br> `file_list = glob.glob(directory + "/*." + ftype.strip(".")` (la différence n'est qu'un puissant `"/"` signe).
* Créez le dictionnaire vide qui contiendra le contenu du fichier sous forme de tableaux *numpy* : `file_content_dict = {}`
* Loop sur tous les fichiers de la liste de fichiers avec `for file in file_list:`
    * Générer une clé pour `file_content_dict`:
        - Détachez le nom du fichier `file` (répertoire + nom du fichier + fichier se terminant `ftype`) avec `raw_file_name = file.split("/")[-1].split("\\")[-1].split(".csv")[0]`
        - Enlevez le nom du fichier brut `fn_prefix` et `fn_suffix` *strings* et utilisez une déclaration `try:` pour convertir les caractères restants en une valeur numérique : `int(raw_file_name.strip(fn_prefix).strip(fn_suffix)`
        - *Note: Nous utiliserons plus tard `fn_prefix="daily_flows_` et `fn_suffix=""` pour tourner l'année contenue dans les noms de fichiers *csv* vers la clé `file_content_dict`.
        - Utilisez `except ValueError:` dans le cas où le reste *string* ne peut pas être converti en `int`: `dict_key = raw_file_name.strip(fn_prefix).strip(fn_suffix)` (si tout est bien codé, le script ne devra pas sauter dans cette déclaration d'exception plus tard).
    * Ouvrir le fichier `file` (annuaire complet) en tant que fichier: `with open(file, mode="r") as f:`
        - Lisez le contenu du fichier avec `f_content = f.read()`. La variable *string* `f_content` ressemblera à quelque chose comme `";0;0;0;0;0;0;0;0;0;2.1;0;0\n;0..."`.

```{admonition} Some *string* explanations
:class: tip
Les données de la colonne sont délimitées par un `";"` et chaque colonne représente une valeur par mois (c.-à-d. 12 valeurs par ligne). Les lignes indiquent des jours (c'est-à-dire qu'il y a 31 lignes dans chaque fichier correspondant au nombre maximal de jours en un mois d'année). En conséquence, chaque ligne doit contenir 11 signes `";"` pour séparer 12 colonnes et le fichier entier (`f_content`) doit contenir 30 signes `"\n"` pour séparer 31 lignes. Cependant, nous comptons 12 signes `";"` par ligne et 32 à 33 `"\n"` signe `f_content` parce que le enregistreur de données a écrit `";"` au début de chaque ligne et ajouté une à deux lignes vides à la fin de chaque fichier. Par conséquent, nous devons `strip()` le mauvais `";"` et `"\n"` signe dans ce qui suit.
```

  * Pour obtenir le nombre de lignes (valables) dans chaque fichier utiliser
  ```
  rows = f_content.strip("\n").split("\n").__len__()
  ```
  * Pour obtenir le nombre de colonnes (valables) dans chaque fichier utiliser
  ```
  cols = f_content.strip("\n").split("\n")[0].strip(delimiter).split(delimiter).__len__()
  ```
  * Maintenant, nous pouvons créer un tableau *numpy* vide de la taille (forme) correspondant au nombre de lignes et de colonnes valides dans chaque fichier:
  ```
  data_array = np.empty((rows, cols), dtype=np.float32)
  ```
  * *Pourquoi n'utilisons-nous pas directement `np.empty((31, 12)` même si la forme de tous les fichiers est la même?<br> Nous voulons écrire une fonction généralement valide et les deux lignes pour calculer le nombre valide de lignes et de colonnes font la tâche de généralisation.*
  * Ensuite, nous devons analyser les valeurs de chaque ligne et les ajouter au vide jusqu'à présent `data_array`. Par conséquent, nous avons divisé `f_content` en ses lignes avec `split("\n)` et utiliser une boucle *for*: `for iteration, line in enumerate(f_content.strip("\n").split("\n"):`. <br> Créer une liste vide pour stocker les données de ligne `line_data = []`. <br> Dans une autre boucle *for*, strip et split la ligne par l'utilisateur-défini `delimiter` (rappel: nous utiliserons `delimiter=";"`) `for e in line.strip(delimiter).split(delimiter):`. Dans la boucle *e-for*, `try:` pour ajouter `e` comme numéro *float* `line_data.append(np.float32(e)` et utiliser `except ValueError:` à `line_data.append(np.nan)` (i.e., ajouter une valeur non-a-numéro dont nous aurons besoin parce que tous les mois n'ont pas 31 jours).<br> Mettre fin à la boucle *e-for* en faisant un retour à la boucle `for iteration, line in ...` et en ajoutant le tableau `line_data` *list* comme tableau *numpy* à `data_array`: `data_array[iteration] = np.array(line_data)`
  * De retour dans l'énoncé `with open(file, ...` (utiliser le niveau d'indentation correct!), mettre à jour `file_content_dict` avec le found `dict_key` et le `data_array` du `file as f`: `file_content_dict.update({dict_key: data_array})`

* Retourner au niveau de la fonction (`def read_data(...):` - attention à l'indentation correcte!), `return file_content_dict`

Vérifiez si la fonction fonctionne comme désiré et suivez les instructions dans la section {ref}`standalone` pour mettre en œuvre une déclaration `if __name__ == "__main__":` à la fin du fichier. Ainsi, le script devrait ressembler au bloc de code suivant:

```python
import glob
import os
import numpy as np


def read_data(directory="", fn_prefix="", fn_suffix="", ftype="csv", delimiter=","):
    # see above


if __name__ == "__main__":
    # LOAD DATA
    file_directory = os.path.abspath("") + "\\flows\\"
    daily_flow_dict = read_data(directory=file_directory, ftype="csv",
                                fn_prefix="daily_flows_", fn_suffix="",
                                delimiter=";")
    print(daily_flow_dict[1995])
```

L'exécution du script renvoie le `numpy.array` des flux moyens quotidiens pour l'année 1995 :

```python
    [[  0.    0.    0.    0.    0.    0.    0.    0.    0.    0.    0.    0. ]
     [  0.    0.    0.    0.    0.    0.    0.    0.    0.    0.    0.    0. ]
     [  0.    0.    0.    0.    0.    0.    0.    0.    0.    0.    0.    0. ]
     [  0.    4.    0.   14.2   0.    0.    0.   81.7   0.    0.    0.    0. ]
     [  0.    0.    0.    0.    0.    0.    0.    0.    0.    0.    0.    0. ]
     [  0.    0.    0.    0.    0.    0.    0.    0.    0.    0.   19.7   0. ]
     [  0.    0.   19.8   0.    0.    0.    0.    0.    0.    0.    0.    0. ]
     [  0.    0.    4.8   0.    0.    0.   77.2   0.    0.    0.    0.    0. ]
     [  0.    0.    0.    0.    0.    0.    0.    0.    0.    0.    0.    0. ]
     [  0.    0.    0.    0.    0.    0.    0.    0.    0.    0.    0.    0. ]
     [  0.    0.    0.    0.    0.    0.    0.    0.    0.    0.    0.    0. ]
     [  0.    0.    0.    0.   10.2   0.    0.    0.    0.    0.    0.   12. ]
     [  0.    0.    0.    0.    0.    0.    0.    0.    0.    0.    0.  671.8]
     [  0.    0.    0.    0.    0.    0.    0.    0.    0.    0.    0.    0. ]
     [  4.6   0.    0.    0.    0.    0.    0.    0.    0.    0.    0.    0. ]
     [  0.    0.    0.    0.    0.    0.    0.   34.2   0.    0.    0.    0. ]
     [  0.    0.    0.    6.3   0.    0.    0.    0.    0.    0.    0.    0. ]
     [  0.    0.    0.    0.    0.    0.    0.    0.    0.    0.    0.    0. ]
     [  0.    0.    0.    0.    0.    0.    0.    0.    0.   25.3   0.    0. ]
     [  0.    0.    0.    0.    0.    0.    0.    0.    0.    0.    0.    0. ]
     [  0.    0.    0.    0.    0.    0.    0.    0.    0.    0.    0.    0. ]
     [  0.    0.    0.    0.    0.    0.    0.    0.    0.    0.    0.    0. ]
     [  0.    0.    0.    0.    0.    5.    0.    0.    0.    0.    0.    0. ]
     [  0.    0.    0.    0.    0.    0.    0.    0.    0.    0.    0.    0. ]
     [  0.    0.    0.    0.    0.    0.    0.    0.    0.    0.    0.    0. ]
     [  0.    0.    0.    0.    0.    0.   98.7   0.    0.    0.    0.    0. ]
     [  0.    0.    0.    0.    0.    0.    0.    0.   22.1   0.    0.    0. ]
     [  0.    0.    0.    0.    0.    0.    0.    0.    0.    0.    0.    0. ]
     [  0.    nan   0.    0.    0.    0.    0.    0.    0.    0.    0.    0. ]
     [  0.    nan   0.    0.    0.    0.    0.    0.    0.    0.    0.    0. ]
     [  0.    nan   0.    nan   0.    nan   0.    0.    nan   0.    nan   0. ]]
```


### Convertir les débits quotidiens en volumes mensuels

L'algorithme de crête séquentielle prend des débits mensuels, ce qui correspond à la somme de la décharge moyenne quotidienne multipliée par la durée d'une journée (par exemple, 11,0 m$^3$/s $\cdot$ 24 h/d $\cdot$ 3600 s/h). Lire les données de flux comme ci-dessus montre les résultats dans les tableaux de flux annuels (flux quotidiens moyens en m$^3$/s) avec les `numpy.array`s des tableaux de forme 31x12 ( matrices) pour chaque année. Nous voulons obtenir les montants de la colonne et multiplier la somme par 24 h/d $\cdot$ 3600 s/h. Parce que les volumes mensuels sont de l'ordre de millions de mètres cubes (CMS), diviser les montants mensuels par `10**6` simplifiera la représentation des nombres.

Écrire une fonction (p. ex., `def daily2monthly(daily_flow_series)`) pour effectuer la conversion des séries de flux moyens quotidiens en volumes mensuels à 10$^{6}$m$^3$:

* La fonction doit être appelée pour chaque entrée de dictionnaire (année) de la série de données. Par conséquent, l'argument d'entrée `daily_flow_series` devrait être un `numpy.array`, la forme étant `(31, 12)`.
* Pour obtenir des statistiques en colonne (mensuelles), transposez le tableau d'entrées :
```
daily_flow_series = np.transpose(daily_flow_series)
```
* Create a void list to store monthly flow values:<br> `monthly_stats = []`
* Plongez sur la ligne de la (transposée) `daily_flow_series` et ajoutez la somme multipliée par `24 * 3600 / 10**6` à `monthly_stats`
```
for daily_flows_per_month in daily_flow_series:
    monthly_stats.append(np.nansum(daily_flows_per_month * 24 * 3600) / 10**6)
```
* Retour `monthly_stats` as `numpy.array`:
```
return np.array(monthly_stats)
```

En utilisant une boucle, nous pouvons maintenant écrire les volumes mensuels semblables aux flux quotidiens dans un dictionnaire, que nous prolongeons d'un an à la fois dans l'énoncé `if __name__ == "__main__"`:

```python
import ...


def read_data(directory="", fn_prefix="", fn_suffix="", ftype="csv", delimiter=","):
    # see above section


def daily2monthly(daily_flow_series):
    # see above descriptions


if __name__ == "__main__":
    # LOAD DATA
    ...
    # CONVERT DAILY TO MONTHLY DATA
    monthly_vol_dict = {}
    for year, flow_array in daily_flow_dict.items():
        monthly_vol_dict.update({year: daily2monthly(flow_array)})
```

## Algorithme de pic de séquence

Avec les routines ci-dessus pour la lecture des données de flux, nous avons calculé des volumes mensuels d'entrée $In_{m}$ in million m$^3$ (stockés à `monthly_vol_dict`). Pour l'irrigation et l'approvisionnement en eau potable, le pays aride de la Vanille veut retirer du réservoir le volume annuel suivant :

| ***Month***    | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec |
|----------------|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| ***Vol.*** (10$^{6}$ m$^3$) | 1.5 | 1.5 | 1.5 | 2   | 4   | 4   | 4   | 5   | 5   | 3   | 2   | 1.5 |

Suivant le schéma des volumes entrants, nous pouvons créer un `numpy.array` pour les volumes sortants mensuels $Out_{m}$.

```python
monthly_supply = np.array([1.5, 1.5, 1.5, 2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 3.0, 2.0, 1.5])
```

### Volume de stockage et différences (ligne SD) Courbes
Le volume de stockage du présent mois $S_{m}$ est calculé en fonction du bilan hydrique du dernier mois, par exemple:<br>

$S_{2}$ = $S_{1}$ + $In_{1}$ - $Out_{1}$<br>
$S_{3}$ = $S_{2}$ + $In_{2}$ - $Out_{2}$ = $S_{1}$ + $In_{1}$ + $In_{2}$ - $Out_{1}$ - $Out_{2}$<br>

En notation sommaire, nous pouvons écrire:

$S_{m+1} = S_{1} + \Sigma_{i=[1:m]} In_{i} - \Sigma_{i=[1:m]}Out_{i}$

Les deux derniers termes constituent la différence de stockage ($SD$) ligne:

$SD_{m} = \Sigma_{i=[1:m]}(In_{i} - Out_{i})$

Ainsi, la courbe de stockage en fonction de la ligne $SD$ est :

$S_{m+1} = S_{1} + SD_{m}$

La notation de sommation de la courbe de stockage en fonction de la ligne $SD$ nous permet d'implémenter le calcul en une simple fonction `def sequent_peak(in_vol_series, out_vol_target):`.

```{note}
Les instructions suivantes supposent que `in_vol_series` corresponde à la *dictionnaire* des volumes mensuels d'entrée et `out_vol_target` est la `numpy.array` des volumes mensuels cibles de sortie. Une autre approche qui utilise `in_vol_series` comme séquence de `numpy.array`s peut être utilisée.
```

La nouvelle fonction `def sequent_peak(in_vol_series, out_vol_target):` doit :

* Calculer les différences mensuelles de stockage ($In_{m}$ - $Out_{m}$), par exemple dans une boucle *for* sur le dictionnaire `in_vol_series`:

```python
    # create storage-difference SD dictionary
    SD_dict = {}
    for year, monthly_volume in in_vol_series.items():
        # add a new dictionary entry for every year
        SD_dict.update({year: []})
        for month_no, in_vol in enumerate(monthly_volume):
            # append one list entry per month (i.e., In_m - Out_m)
            SD_dict[year].append(in_vol - out_vol_target[month_no])
```

* Aplatissez le dictionnaire sur une liste (nous aurions pu le faire directement) correspondant à la ligne $SD$:

```python
    SD_line = []
    for year in SD_dict.keys():
        for vol in SD_dict[year]:
            SD_line.append(vol)
```

* Calculer la ligne de stockage avec `storage_line = np.cumsum(SD_line)`
* Trouvez l'extrémité locale et il y a deux (et plus) options:

1. Utilisez `from scipy.signal import argrelextrema` et obtenez les indices (positions de) local extrema et leur valeur à partir de `storage_line`:

```python
seas_max_index = np.array(argrelextrema(storage_line, np.greater, order=12)[0]) 
seas_min_index = np.array(argrelextrema(storage_line, np.less, order=12)[0])
seas_max_vol = np.take(storage_line, seas_max_index)
seas_min_vol = np.take(storage_line, seas_min_index)
```


2. Écrire deux fonctions, qui trouvent consécutivement maxima local et puis minima locaux situés entre l'extrémité (cours **travail à domicile**) OU utilisez `from scipy.signal import find_peaks` pour trouver les indices (positions) - envisager d'écrire une fonction `find_seasonal_extrema(storage_line)`.

* Assurez-vous que les courbes et l'extrémité sont correctes en copiant la courbe `plot_storage_curve` à votre script ([disponible dans le dépôt d'exercice](https://raw.githubusercontent.com/Ecohydraulics/Exercise-SequentPeak/master/plot_function.py)) et en l'utilisant comme suit :

```python
plot_storage_curve(storage_line, seas_min_index, seas_max_index, seas_min_vol, seas_max_vol)
```

```{figure} https://github.com/Ecohydraulics/media/raw/main/png/storage_curve.png
:alt: sequent peak storage difference sd curve
:name: SDline

Courbe de la différence de stockage (SD).
```

### Calculer le volume de stockage requis

Le volume de stockage requis correspond à la plus grande différence entre un maximum local et son minimum local le plus bas consécutif. Par conséquent, ajouter les lignes suivantes à la fonction `sequent_peak`:

```python
    required_volume = 0.0
    for i, vol in enumerate(list(seas_max_vol):
        try:
            if (vol - seas_min_vol[i]) > required_volume:
                required_volume = vol - seas_min_vol[i]
        except IndexError:
            print("Reached end of storage line.")
```

Fermer la fonction `sequent_peak` avec `return required_volume`

### Appeler l'algorithme du pic Sequent
Avec toutes les fonctions requises écrites, la dernière tâche est d'appeler les fonctions dans l'énoncé `if __name__ == "__main__"`:

```python
import ...


def read_data(directory="", fn_prefix="", fn_suffix="", ftype="csv", delimiter=","):
    # see above section


def daily2monthly(daily_flow_series):
    # see above section


def sequent_peak(in_vol_series, out_vol_target):
    # see above descriptions

if __name__ == "__main__":
    # LOAD DATA
    ...
    # CONVERT DAILY TO MONTHLY DATA
    ...
    # MAKE ARRAY OF MONTHLY SUPPLY VOLUMES (IN MILLION CMS)
    monthly_supply = np.array([1.5, 1.5, 1.5, 2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 3.0, 2.0, 1.5])
    # GET REQUIRED STORAGE VOLUME FROM SEQUENT PEAK ALGORITHM
    required_storage = sequent_peak(in_vol_series=monthly_vol_dict, out_vol_target=monthly_supply)
    print("The required storage volume is %0.2f million CMS." % required_storage)
```

## Remarques finales

L'utilisation de l'algorithme de crête séquentielle (aussi connu sous le nom de méthode de *Rippl* en raison de son auteur original) a évolué et a été mise en œuvre dans des algorithmes sophistiqués de contrôle du volume de stockage avec des modèles prédicteurs (statistiques et/ou numériques).

Finalement, il y a plusieurs algorithmes et moyens de les coder. De nombreux facteurs (p. ex. terrain ou zone climatique) déterminent si un stockage saisonnier est possible ou nécessaire. Pour déterminer le volume de stockage, il ne faut pas négliger les aspects sociaux et environnementaux. Chaque grain de sédiments conservé est manquant dans les sections en aval de la rivière, chaque poisson qui n'est plus en mesure de migrer subit une perte d'habitat, et plus que tout autre, tout habitant qui subit des pertes économiques ou est même contraint de se réinstaller en raison du barrage doit être évité ou adéquatement compensé.

```{admonition} Homework

Re-write the peak (extrema) analysis either with two consecutive functions or using [`from scipy.signal import find_peaks`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html).
```
