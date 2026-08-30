---
description: Exercice Python orienté objet pour le transport de sédiments en charge de lit en 1D en utilisant la formule Meyer-Peter et Müller, avec pandas DataFrames, cahiers Excel et hydraulique Manning-Strickler.
---

(ex-py-sediment)=
# 1d Transport des sédiments

```{admonition} Goals
Cet exercice comprend l'application des formules de transport Meyer-Peter & Müller (1948) {term}`bedload <Bedload>` à une application valide : hydraulique moyenne de 1d. Écrire un code orienté objet avec des classes personnalisées pour les interactions sur mesure avec les cahiers de travail *xlsx*. Les devoirs impliquent des méthodes intégrées de {ref}`pandas` DataFrames et de complot.
```

```{admonition} Requirements
:class: attention
Lisez et comprenez le traitement des données avec {ref}`numpy` et {ref}`pandas` ainsi que {ref}`ooc`.
```

Préparez-vous en clonant le dépôt d'exercices :

```
git clone https://github.com/Ecohydraulics/Exercise-SedimentTransport.git
```

```{figure} https://github.com/Ecohydraulics/media/raw/main/jpg/arbogne.jpg
:alt: arbogne Switzerland Fribourg
:name: arbogne

La rivière Arbogne en Suisse (source: Sebastian Schwindt 2013).
```


## Théorie

### 1d Moyenne de section Hydrodynamique
À partir de l'exercice [formule Manning-Strickler*]](https://github.com/Ecohydraulics/Exercise-ManningStrickler), nous nous souvenons de la formule pour calculer la relation entre la profondeur d'eau $h$ (intégrée dans le rayon hydraulique $R_{h}$) et la vitesse d'écoulement $u$:

$$
u = 1/n_m \cdot S_{e}^{1/2} \cdot R_{h}^{2/3}
$$

où
* $n_m$ est le coefficient [*Manning*](http://www.fsl.orst.edu/geowater/FX3/help/8_Hydraulic_Reference/Mannings_n_Tables.htm) dans *fictionnel* des unités (s/m$^{1/3}$).
* $S_{e}$ est la pente d'énergie hypothétique (m/m) et correspond à la pente du chenal pour des conditions d'écoulement stables et uniformes (non existantes dans les rivières naturelles).
* rayon hydraulique $R_{h} = A / P$, où (pour une section trapézoïdale):
  - la zone transversale (trapézoïdale) mouillée est $A = h \cdot 0.5\cdot (b + B) = h \cdot (b + h\cdot m)$;
  - le périmètre mouillé d'un trapèze est $P = b + 2h\cdot(m^2 + 1)^{1/2}$;
  - $b$ (largeur de base du canal) et $m$ (la pente de la rive) sont illustrés dans la figure ci-dessous pour calculer la largeur de surface de l'eau dépendante de la profondeur $B=b+2\cdot h\cdot m$.


```{figure} https://github.com/Ecohydraulics/media/raw/main/png/flow-cs.png
:alt: 1d hydraulics parameters
:name: cs-sed
```

Cet exercice utilise des données hydrauliques moyennes de section unidimensionnelle (1d) produites avec le logiciel HEC-RAS du US Army Corps of Engineers {cite:p}`us_army_corps_of_engineeers_hydrologic_2016`, qui résout numériquement la formule Manning-Strickler pour toute forme de section transversale de flux. Dans cet exercice, *HEC-RAS* fournit les données hydrauliques nécessaires pour déterminer la capacité {term}`sediment transport <Sediment transport>` d'une section de canal, bien qu'aucune explication pour créer, exécuter et exporter des données à partir des modèles *HEC-RAS* ne soit donnée.

### Transport des sédiments

Fluvial {term}`Sediment transport` peut être distingué en deux modes : (1) {term}`suspended load <Suspended load>` et (2) {term}`bedload <Bedload>` (voir {numref}`Fig. %s <transport-modes>`). Les particules plus fines dont le poids peut être transporté par le fluide (eau) sont transportées comme {term}`suspended load <Suspended load>`. Les particules grossières qui roulent, glissent et sautent sur le lit du canal sont transportées comme {term}`bedload <Bedload>`. Il y a un autre type de transport, la soi-disant charge de lavage, qui est plus fine que le gros {term}`bedload <Bedload>`, mais trop lourd (large) pour être transporté en suspension {cite:p}`einstein_bed-load_1950`.

```{figure} https://github.com/Ecohydraulics/media/raw/main/png/sediment-transport.png
:alt: 1d sediment transport
:name: transport-modes

Deux modes de transport des sédiments (source: {cite:p}`schwindt_hydro-morphological_2017`).
```

Dans ce qui suit, nous examinerons le mode de transport {term}`bedload <Bedload>`. Dans ce cas, une particule de sédiments située dans ou sur le lit de la rivière est mobilisée par les forces de cisaillement de l'eau dès qu'elles dépassent une valeur critique (voir figure ci-dessous). Dans l'hydraulique fluviale, la contrainte dite de cisaillement du lit sans dimension ou la contrainte *Shields* {cite:p}`shields_anwendung_1936` est souvent utilisée comme valeur seuil pour la mobilisation des sédiments du lit du fleuve (voir {numref}`Fig. %s <bedload-uptake>`). Cet exercice utilise une des approches de contrainte de cisaillement de lit sans dimension et la section suivante fournit plus d'explications.

```{figure} https://github.com/Ecohydraulics/media/raw/main/png/sediment-uptake.png
:alt: sediment uptake mobilization
:name: bedload-uptake

Le principe de la mobilisation des sédiments.
```

(mpm)=
### Formule Meyer-Peter et Müller (1948)

La formule {cite:t}`meyer-peter_formulas_1948` pour estimer le transport {term}`bedload <Bedload>` a été publiée par les chercheurs suisses Eugen Meyer-Peter (fondateur du [Laboratoire d'hydraulique, d'hydrologie et de glaciologie (VAW)](https://vaw.ethz.ch/en/) et Robert Müller. Leur étude a commencé un an après la création de la VAW en 1931 quand Robert Müller a été nommé assistant d'Eugen Meyer-Peter. Les deux scientifiques ont travaillé en collaboration avec Henry Favre et Hans Albert, le fils d'Albert Einstein. En 1934, le laboratoire a publié pour la première fois une formule pour le calcul du transport {term}`bedload <Bedload>` et sa relation fondamentale entre les contraintes de cisaillement de lit observées $\tau_{x}$ et critiques $\tau_{x,cr}$ est utilisée jusqu'à aujourd'hui. Le taux de transport sans dimension {term}`bedload <Bedload>` $\Phi_b$ selon {cite:t}`meyer-peter_formulas_1948` est:

$$
\Phi_b \approx 8 \cdot (\tau_{x} - \tau_{x,cr})^{3/2}
$$ (eq-py-mpm)

```{admonition} Bed shear stress
:name: taux
* $\tau_{x,cr}$ $\approx$ 0.047 (up to 0.07 in mountain rivers), and
* $\tau_{x}$ = $R_{h} \cdot S_{e} / [(s - 1) \cdot D_{char}]$
```

Les autres paramètres sont:
* $s$ $\approx$ 2.68, the dimensionless ratio of sediment grain density $\rho_{s}$ ($\approx$ 2680 kg/m³) and water density $\rho_{w}$ ($\approx$ 1000 kg/m³);
* $D_{char}$, la taille caractéristique du grain en (m). On peut supposer que $D_{char} \approx D_{84}$ (c.-à-d. le diamètre du grain dont 84% d'un mélange de sédiments est plus petit) correspond à la littérature scientifique (p. ex. {cite:t}`rickenmann_evaluation_2011`).

La formule *Meyer-Peter & Müller* ne s'applique (comme toute autre formule {term}`Sediment transport`) qu'à certaines rivières présentant les caractéristiques suivantes (étendue de validité) :
* 0.4 $\cdot$ 10$^{-3}$ m $< D_{char}$ < 28.6 $\cdot$ 10$^{-3}$ m
* 10$^{-4}$ m $< Fr <$ 639 ($Fr$ denotes the dimensionless [{term}`Froude number`](https://en.wikipedia.org/wiki/Froude_number))
* 0,0004 $< S_{e} <$ 0,02
* 0,0002 m$^3$/(s $\cdot$ m) $< q <$ 2.0 m$^3$/(s $\cdot$ m) ($q$ est la décharge de l'unité, c'est-à-dire $q=Q/[0. 5\cdot (b + B)]$)
* 0.25 $< s <$ 3.2

L'expression sans dimension pour {term}`bedload <Bedload>` $\Phi_b$ a été utilisée pour permettre le transfert d'informations entre différents canaux à travers les échelles en préservant la similitude géométrique, cinématique et dynamique. L'ensemble des paramètres sans dimension utilise les résultats de [Buckingham's $\Pi$ theorem](https://pint.readthedocs.io/en/stable/pitheorem.html) {cite:p}`buckingham_model_1915`.
Par conséquent, pour ajouter des dimensions à $\Phi_b$, il faut les multiplier avec le même ensemble de paramètres utilisés pour dériver l'expression sans dimension de *Meyer-Peter & Müller*. Leur ensemble de paramètres implique la taille caractéristique du grain $D_{char}$, la densité du grain $\rho_{s}$, et l'accélération gravitationnelle $g$. Ainsi, l ' unité dimensionnelle {term}`bedload <Bedload>` est (en kg/s et largeur du compteur, c ' est-à-dire kg/(s$\cdot$m):

```{admonition} Dimensional unit bedload
:name: qb
$$
q_{b} = \Phi_b \cdot ((s-1) \cdot g \cdot D_{char}^{3})^{1/2} \cdot \rho_{s}
$$
```

The cross-section averaged {term}`bedload <Bedload>` $Q_{b}$ (kg/s) is then:

```{admonition} Dimensionless cross-section-averaged bedload
:name: qbx
$$
Q_{b} = b_{eff} \cdot q_{b} = b_{eff} \cdot \Phi_b \cdot [(s-1) \cdot g \cdot D_{char}^{3}]^{1/2} \cdot \rho_{s}
$$
```

où $b_{eff}$ est la largeur du canal hydrauliquement actif de la section transversale du flux (par exemple, pour un trapèze $b_{eff} = 0.5 \cdot (b + B)$).


## Code

### Définir le cadre
Le code orienté objet utilisera des classes personnalisées que nous appellerons dans un script **`main.py`**. Créer les scripts ** supplémentaires** suivants, qui contiendra les classes et les fonctions personnalisées pour contrôler l'enregistrement.

* `fun.py` contiendra des fonctions d'enregistrement.
* `hec.py` contiendra une classe `HecSet` pour lire les données de sortie hydraulique de *HEC-RAS* comme objets structurés.
* `grains.py` contiendra une classe `GrainReader` pour lire les informations de classe de taille de grain comme objets structurés.
* `bedload.py` contiendra la classe `BedCore` avec les éléments de base que la plupart des formules {term}`bedload <Bedload>` ont en commun.
* `mpm.py` contiendra la classe `MPM`, qui hérite de `BedCore` et calcule {term}`bedload <Bedload>` comme décrit ci-dessus (Meyer-Peter & Müller 1948).

Nous allons créer les classes et les fonctions dans les scripts indiqués selon le diagramme de flux suivant:

```{figure} https://github.com/Ecohydraulics/Exercise-SedimentTransport/raw/main/graphs/uml.png
:alt: sediment transport calculation python code structure
:name: structure
```

Pour commencer avec le script `main.py`, ajoutez une fonction `main` ainsi qu'une fonction `get_char_grain_size` et une fonction `calculate_mpm`. De plus, rendre le script *stand-alone* exécutable :

```python
# This is main.py
import os


def get_char_grain_size(file_name, D_char):
    return None


def calculate_mpm(hec_df, D_char):
    return None


def main():
    pass


if __name__ == '__main__':
    main()

```

### Fonctions d'exploitation
Le script `fun.py` contiendra deux fonctions :

1. `start_logging` pour configurer des formats de journalisation et un nom de fichier journal comme décrit dans la section sur {ref}`logging <logging>`, et
1. `log_actions`, qui est une fonction d'emballage pour les fonctions `main()` (`main.py`) pour enregistrer les messages d'exécution de script.

La fonction `start_logging` devrait ressembler à cela (changer le nom du fichier journal si désiré):

```python
import logging


def start_logging():
    logging.basicConfig(filename="logfile.log", format="[%(asctime)s] %(message)s",
                        filemode="w", level=logging.DEBUG)
    logging.getLogger().addHandler(logging.StreamHandler()

```

La fonction `log_actions` wrapper suit les instructions de {ref}`functions theory section <wrappers>`:

```python
def log_actions(fun):
    def wrapper(*args, **kwargs):
        start_logging()
        fun(*args, **kwargs)
        logging.shutdown()
    return wrapper
```

Pour utiliser l'enveloppe `log_actions` tout au long du programme, nous le mettrons en œuvre au plus haut niveau, qui est la fonction `main()` à `main.py`:

```python
# main.py
from fun import *

...

@log_actions
def main():
    logging.info("This is a test message (do not keep in the function).")


if __name__ == '__main__':
    main()

```

Maintenant, nous pouvons enregistrer des messages à différents niveaux (info, avertissement, erreur, ou autres) dans toutes les fonctions appelées dans `main()` en utilisant par exemple `logging.info("Message")`, `logging.warning("Message")`, ou `logging.error("Message")` plutôt que la fonction `print()`.


### Lire les données sur la taille du grain

Sediment grain size classes (ranging from $D_{16}$ to $D_{max}$) are provided in the file [`grains.csv`](https://github.com/Ecohydraulics/Exercise-SedimentTransport/raw/main/grains.csv) (`delimiter=","`) and can be customized.

Écrire une classe `GrainReader` qui utilise la méthode `read_csv` de {ref}`pandas` pour lire la distribution de la taille du grain de `grains.csv`. Écrire la classe dans un script distinct *Python* (par exemple, `grains.py` comme indiqué dans la figure ci-dessus) :

```python
class GrainReader:
    def __init__(self, csv_file_name="grains.csv", delimiter=","):
        self.sep = delimiter
        self.size_classes = pd.DataFrame
        self.get_grain_data(csv_file_name)
```

La méthode `get_grain_data` devrait ressembler à ceci pour la lecture des classes de granulométrie fournies:

```python
    def get_grain_data(self, csv_file_name):
        self.size_classes = pd.read_csv(csv_file_name,
                                        names=["classes", "size"],
                                        skiprows=[0],
                                        sep=self.sep,
                                        index_col=["classes"])
```

```{admonition} Challenge
Ajouter une méthode `__call__()` à la classe `GrainReader`.
```

Implémenter l'instantiation d'un objet `GrainReader` dans le script `main.py` dans la fonction `get_char_grain_size`. La fonction devrait recevoir les arguments de type *string* `file_name` (ici: `"grains.csv"`) et `D_char` (i.e., la taille caractéristique du grain à utiliser de `grains.csv`). La fonction `main()` appelle la fonction `get_char_grain_size` avec les arguments `file_name=os.path.abspath("..") + "\\grains.csv"` et `D_char="D84"` (correspond à la première colonne `grains.csv`).

```python
# main.py
import os
from grains import GrainReader

def get_char_grain_size(file_name=str, D_char=str):
    grain_info = GrainReader(file_name)
    return grain_info.size_classes["size"][D_char]

...

@log_actions
def main():
    # get characteristic grain size = D84
    D_char = get_char_grain_size(file_name=os.path.abspath("..") + "\\grains.csv",
                                 D_char="D84")
```


### Lire les données d'entrée HEC-RAS

The provided *HEC-RAS* dataset is stored in the *xlsx* workbook [`HEC-RAS/output.xlsx`](https://github.com/Ecohydraulics/Exercise-SedimentTransport/raw/main/HEC-RAS/output.xlsx) and contains the following output:

**Col. no******Col. alphabétique****Variable******Type/Unité****Description**
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
Col. 01: 01: 01: 01: 01: 01: 01: 01: 01
Col. 02: B: Sta de la rivière [m]: Position sur l'axe longitudinal de la rivière.
C'est ce qu'a dit le Col 03 C' Profil *string*
* Col.
* Col. 05* E* Min Ch El* [m a.s.l.]
* Col. 06* F.S. Elev*
Col. 07. G. Vel Chnl. [m]
Col. 08:00 H:00 Zone de débit [m2]
* Col. 09* I* Froude\# Chl* {term}`Froude number` du canal (si 1, erreur de calcul - ne pas utiliser!)
Col. 10:00 J:00 Rayon hydraulique
Col. 11:00 K:00 Profondeur de l'eau (moyenne de section active)
Col. 12, rue E.G. Slope (en m/m)

Pour charger les données de sortie *HEC-RAS*, écrivez une classe personnalisée (dans un script séparé appelé `hec.py`) qui prend le nom du fichier comme argument d'entrée et lit le fichier *HEC-RAS* comme cadre de données *pandas* :

```python
class HecSet:
    def __init__(self, xlsx_file_name="output.xlsx"):
        self.hec_data = pd.DataFrame
        self.get_hec_data(xlsx_file_name)
```

La méthode `get_hec_data` devrait ressembler à ceci :
```python
    def get_hec_data(self, xlsx_file_name):
        self.hec_data = pd.read_excel(xlsx_file_name,
                                      skiprows=[1],
                                      header=[0])
```

Pour créer un objet `HecSet` dans la fonction `main()` (`main.py`), nous devons l'importer et l'actualiser par exemple sous le nom de `hec = HecSet(file_name)`. En outre, nous pouvons déjà implémenter le passage des données `pd.DataFrame` de *HEC-RAS* à la fonction `calculate_mpm` (également à `main.py`) que nous compléterons plus tard.

```python
# main.py
import os
from ...
from hec import HecSet

...

@log_actions
def main():
    D_char = ...

    hec_file = os.path.abspath("..") + "{0}HEC-RAS{0}output.xlsx".format(os.sep)
    hec = HecSet(hec_file)
```

### Créer une classe de base de charge de lit

Une classe `BedCore` écrite dans le script `bedload.py` fournit des variables et des méthodes, qui sont pertinentes à de nombreuses formules de calcul {term}`bedload <Bedload>` et {term}`Sediment transport`, comme la correction *Parker-Wong* {cite:p}`wong_reanalysis_2006` ou {cite:t}`smart_sedimenttransport_1983` ([téléchargement direct](https://ethz.ch/content/dam/ethz/special-interest/baug/vaw/vaw-dam/documents/das-institut/mitteilungen/1980-1989/064.pdf)). De plus, la classe `BedCore` contient des constantes telles que l'accélération gravitationnelle $g$ (i.e., `self.g=9.81`), le rapport entre le grain de sédiments et la densité d'eau $s$ (i.e., `self.s=2.68`) et la contrainte critique de cisaillement du lit sans dimension $\tau_{x,cr}$ (i.e., `self.tau_xcr=0.047`, qui peut être redéfinie par les utilisateurs). L'en-tête de la classe `BedCore` devrait ressembler à ceci :

```python
from fun import *
import numpy as np


class BedCore:
    def __init__(self):
        self.tau_x = np.nan
        self.tau_xcr = 0.047
        self.g = 9.81
        self.s = 2.68
        self.rho_s = 2680.0  # kg/m3 sediment grain density
        self.Se = np.nan  # energy slope (m/m)
        self.D = np.nan  # characteristic grain size
        self.Fr = np.nan  # Froude number
        self.h = np.nan  # water depth (m)
        self.phi = np.nan  # dimensionless bedload
        self.Q = np.nan  # discharge (m3/s)
        self.Rh = np.nan  # hydraulic radius (m)
        self.u = np.nan  # flow velocity (m/s)
```

```{note}
Importer `fun` (le script avec les fonctions de journalisation) pour permettre l'utilisation des messages `logging.warning(...)` dans les méthodes `BedCore` et ses classes d'enfants.
```

Ajouter une méthode pour convertir la valeur sans dimension {term}`bedload <Bedload>` transport $\Phi_b$ en valeur dimensionnelle (kg/s). En plus des variables définies dans la méthode `__init__`, la méthode `add_dimensions` exigera la largeur effective du canal $b_{eff}$ ({ref}`recall the above calculus <qb>`):

```python
    def add_dimensions(self, b):
        try:
            return self.phi * b * np.sqrt((self.s - 1) * self.g * self.D ** 3) * self.rho_s
        except ValueError:
            logging.warning("Non-numeric data. Returning Qb=NaN.")
            return np.nan
```

De nombreuses formules de transport {term}`bedload <Bedload>` impliquent la contrainte de cisaillement du lit sans dimension [$\tau_{x}$ (voir ci-dessus {ref}`definitions <taux>`) associée à un ensemble de paramètres hydrauliques moyens de section transversale. Par conséquent, appliquer la méthode de calcul `compute_tau_x` à `BedCore`:

```python
    def compute_tau_x(self):
        try:
            return self.Se * self.Rh / ((self.s - 1) * self.D)
        except ValueError:
            logging.warning("Non-numeric data. Returning tau_x=NaN.")
            return np.nan
```

### Écrire une classe d'évaluation Meyer-Peter & Müller Charriage

Créez un nouveau script (par exemple `mpm.py`) et implémentez une classe `MPM` (**M**eyer-**P**eter & **M**üller) qui hérite de la classe `BedCore`. La méthode `__init__` de `MPM` devrait initialiser `BedCore` et écraser (rappeler {ref}`polymorphism`) les paramètres pertinents au calcul de {term}`bedload <Bedload>` selon Meyer-Peter & Müller (1948). En outre, l'initialisation d'un objet `MPM` devrait aller avec une vérification de la validité et le calcul du sans dimension {term}`bedload <Bedload>` transport $\Phi_b$ (voir ci-dessus {ref}`explanations of MPM <mpm>`):

```python
from bedload import *


class MPM(BedCore):
    def __init__(self, grain_size, Froude, water_depth,
                 velocity, Q, hydraulic_radius, slope):
        # initialize parent class
        BedCore.__init__(self)
        # assign parameters from arguments
        self.D = grain_size
        self.h = water_depth
        self.Q = Q
        self.Se = slope
        self.Rh = hydraulic_radius
        self.u = velocity
        self.check_validity(Froude)
        self.compute_phi()
```

Ajouter la méthode `check_validity` pour vérifier si les caractéristiques transversales fournies tombent dans la plage de validité de la formule Meyer-Peter & Müller (c.-à-d. pente, granulométrie, rapport de débit et profondeur de l'eau, et {term}`Froude number`):

```python
    def check_validity(self, Fr):
        if (self.Se < 0.0004) or (self.Se > 0.02):
            logging.warning('Warning: Slope out of validity range.')
        if (self.D < 0.0004) or (self.D > 0.0286):
            logging.warning('Warning: Grain size out of validity range.')
        if ((self.u * self.h) < 0.002) or ((self.u * self.h) > 2.0):
            logging.warning('Warning: Discharge out of validity range.')
        if (self.s < 0.25) or (self.s > 3.2):
            logging.warning('Warning: Relative grain density (s) out of validity range.')
        if (Fr < 0.0001) or (Fr > 639):
            logging.warning('Warning: Froude number out of validity range.')
```

```{note}
La méthode ici montrée `check_validity` prend le {term}`Froude number` comme argument d'entrée. Alternativement, assignez le {term}`Froude number` déjà dans `__init__` et utilisez `self.Fr`.
```

Pour calculer la méthode sans dimension {term}`bedload <Bedload>` transport $\Phi_b$ selon Meyer-Peter & Müller, implémenter une méthode `compute_phi` qui utilise la méthode `compute_tau_x` de `BedCore`:

```python
   def compute_phi(self):
        tau_x = self.compute_tau_x()
        try:
            if tau_x > self.tau_xcr:
                self.phi = 8 * (0.85 * tau_x - self.tau_xcr) ** (3 / 2)
            else:
                self.phi = 0.0
        except TypeError:
            logging.warning("Could not calculate PHI (result=%s)." % str(tau_x)
            self.phi = np.nan
```

Avec la classe `MPM` définie, nous pouvons maintenant remplir la fonction `calculate_mpm` dans le script `main.py`. La fonction devrait créer un cadre de données *pandas* avec des colonnes sans dimension {term}`bedload <Bedload>` transport $ \Phi $ et dimensionnel {term}`bedload <Bedload>` transport $Q_{b}$ associé à un profil de canal (`"River Sta"`) et un scénario de flux (`"Profile" > "Scenario"`).

Le bloc de code suivant illustre un exemple de la fonction `calculate_mpm` qui crée le cadre de données *pandas* à partir d'un {ref}`dict` (`mpm_dict`). La fonction d'illustration crée le *dictionnaire* avec des listes de valeurs nulles, extrait les données hydrauliques du cadre de données *HEC-RAS* et des boucles sur les entrées `"River Sta"`. La boucle vérifie si les entrées `"River Sta"` sont valides (c.-à-d. pas `"Nan"`) parce que les lignes vides que *HEC-RAS* ajoute automatiquement entre les profils de sortie ne doivent pas être analysées. Si la vérification a été réussie, la boucle ajoute le profil, le scénario et la décharge directement à `mpm_dict`. La section {term}`bedload <Bedload>` résultats de transport d'objets `MPM`. Après la boucle, la fonction retourne `mpm_dict` comme objet `pd.DataFrame`.

```python
# main.py
from ...
from ...
from mpm import *

...

def calculate_mpm(hec_df, D_char):
    # create dictionary with relevant information about bedload transport with void lists
    mpm_dict = {
            "River Sta": [],
            "Scenario": [],
            "Q (m3/s)": [],
            "Phi (-)": [],
            "Qb (kg/s)": []
    }

    # extract relevant hydraulic data from HEC-RAS output file
    Froude = hec_df["Froude # Chl"]
    h = hec_df["Hydr Depth"]
    Q = hec_df["Q Total"]
    Rh = hec_df["Hydr Radius"]
    Se = hec_df["E.G. Slope"]
    u = hec_df["Vel Chnl"]

    for i, sta in enumerate(list(hec_df["River Sta"]):
        if not str(sta).lower() == "nan":
            logging.info("PROCESSING PROFILE {0} FOR SCENARIO {1}".format(str(hec_df["River Sta"][i]), str(hec_df["Profile"][i]))
            mpm_dict["River Sta"].append(hec_df["River Sta"][i])
            mpm_dict["Scenario"].append(hec_df["Profile"][i])
            section_mpm = MPM(grain_size=D_char,
                              Froude=Froude[i],
                              water_depth=h[i],
                              velocity=u[i],
                              Q=Q[i],
                              hydraulic_radius=Rh[i],
                              slope=Se[i])
            mpm_dict["Q (m3/s)"].append(Q[i])
            mpm_dict["Phi (-)"].append(section_mpm.phi)
            b = hec_df["Flow Area"][i] / h[i]
            mpm_dict["Qb (kg/s)"].append(section_mpm.add_dimensions(b)
    return pd.DataFrame(mpm_dict)
```

Après avoir défini la fonction `calculate_mpm()`, l'appel à cette fonction à partir de la fonction `main()` devrait maintenant attribuer un cadre de données {ref}`pandas` à la variable `mpm_results`. Pour finaliser le script, écrivez `mpm_results` à un manuel (par exemple, `"bed_load_mpm.xlsx"`) dans la fonction `main()`:

```python
# main.py
import os
from ...

...

def calculate_mpm(hec_df, D_char):
    ...

@log_actions
def main():
    ...

    mpm_results = calculate_mpm(hec.hec_data, D_char)
    mpm_results.to_excel(os.path.abspath("..") + os.sep + "bed_load_mpm.xlsx")
```

## Lancement et débogage

Dans votre IDE, exécutez le script (par exemple, {ref}`pycharm`, faites un clic droit dans le script `main.py` et cliquez sur `> Run 'main'`). Si le script s'écrase ou soulève des messages d'erreur, retracez-les et corrigez les problèmes. Ajouter `try` - `except` déclarations si nécessaire et rappeler {ref}`debugging instructions <sec-pyerror>`.

```{note}
Le programme produit intentionnellement des messages d'avertissement parce que certaines caractéristiques de profil ne remplissent pas la plage de validité de la formule Meyer-Peter & Müller.
```

Une exécution réussie de `main.py` produit un fichier `bed_load_mpm.xlsx` qui ressemble à ceci:

Scénario Q (m3/s)
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
Q moyenne
HQ2.33.33.43.43.42.72291418.
HQ5 : 17 : 0.682792055 : 54.58338633 :
HQ10 de 1970 à 1970
HQ10025 0.90554296777.92848176
Q moyenne
HQ2.33 ,13 ,144406226 ,14,00424884
HQ5 : 17 : 0.203854633 : 20.40484039 :
HQ10: 19:0.29078172:0 23.1352098:0
QG10025 0.29776754631.25225316
- Oui.

Le fichier journal devrait ressembler à ceci:

```text
[20XX-XX-XX 14:08:22,900] PROCESSING PROFILE 1970.1 FOR SCENARIO Q mean
[20XX-XX-XX 14:08:22,900] Warning: Discharge out of validity range.
[20XX-XX-XX 14:08:22,901] PROCESSING PROFILE 1970.1 FOR SCENARIO HQ2.33
[20XX-XX-XX 14:08:22,901] Warning: Discharge out of validity range.
[20XX-XX-XX 14:08:22,901] PROCESSING PROFILE 1970.1 FOR SCENARIO HQ5
[20XX-XX-XX 14:08:22,902] Warning: Discharge out of validity range.
[20XX-XX-XX 14:08:22,902] PROCESSING PROFILE 1970.1 FOR SCENARIO HQ10
[20XX-XX-XX 14:08:22,902] Warning: Discharge out of validity range.
[20XX-XX-XX 14:08:22,902] PROCESSING PROFILE 1970.1 FOR SCENARIO HQ100
[20XX-XX-XX 14:08:22,903] Warning: Discharge out of validity range.
[20XX-XX-XX 14:08:22,903] PROCESSING PROFILE 1893.37 FOR SCENARIO Q mean
[20XX-XX-XX 14:08:22,903] Warning: Discharge out of validity range.
[20XX-XX-XX 14:08:22,903] PROCESSING PROFILE 1893.37 FOR SCENARIO HQ2.33
[20XX-XX-XX 14:08:22,903] Warning: Discharge out of validity range.
[20XX-XX-XX 14:08:22,904] PROCESSING PROFILE 1893.37 FOR SCENARIO HQ5
[20XX-XX-XX 14:08:22,904] Warning: Discharge out of validity range.
[20XX-XX-XX 14:08:22,904] PROCESSING PROFILE 1893.37 FOR SCENARIO HQ10
[20XX-XX-XX 14:08:22,904] Warning: Discharge out of validity range.
[...]
```


```{admonition} Closing remarks
:class: warning

Les calculs du transport des sédiments basés sur la moyenne des sections hydrauliques locales ont des taux d'erreur extrêmement élevés en raison des commandes plus élevées {cite}`schwindt2023metaanalysis`.

Enfin, il y a beaucoup de solutions possibles à cet exercice et toute solution qui donne le même résultat (manuel et fichier journal) est valide. Le défi clé est d'utiliser une approche orientée objet avec au moins une classe héritant d'une autre classe.
```

```{admonition} Homeworks
1. Implement the Parker-Wong correction {cite:p}`wong_reanalysis_2006` for the {cite:t}`meyer-peter_formulas_1948` formula:$\Phi_{b,pw} \approx 4.93 \cdot (\tau_{x} - \tau_{x,cr})^{1.6}$. Implement the formula in the `MPM` class either use an optional keyword argument in `compute_phi` or a new method.

2. Utilisez la bibliothèque `openpyxl` pour ajouter une couleur de fond aux en-têtes des tables de sortie.

3. Choisir et extraire 3 profils de `mpm_results` et tracer la dimensional {term}`bedload <Bedload>` transport $Q_{b}$ (axe-y) contre la décharge $q$ (axe-x).
```
