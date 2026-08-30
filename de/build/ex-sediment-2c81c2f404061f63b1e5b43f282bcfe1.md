---
description: Objektorientierte Python-Übung für den 1D-Sedimenttransport mit der Meyer-Peter- und Müller-Formel mit Pandas DataFrames, Excel-Arbeitsmappen und Manning-Strickler-Hydraulik.
---

(ex-py-sediment)=
# 1d Sedimenttransport

```{admonition} Goals
This exercise features the application of the Meyer-Peter & Müller (1948) {term}`bedload <Bedload>` transport formulae to a valid application: 1d, cross-section averaged hydraulics. Write object-oriented code with custom classes for tailored interactions with *xlsx* workbooks. The homework involves built-in methods of {ref}`pandas` DataFrames and plotting.
```

```{admonition} Requirements
:class: attention
Read and understand data handling with {ref}`numpy` and {ref}`pandas` as well as {ref}`ooc`.
```

Machen Sie sich bereit, indem Sie das Übungsrepository klonen:

```
git clone https://github.com/Ecohydraulics/Exercise-SedimentTransport.git
```

```{figure} https://github.com/Ecohydraulics/media/raw/main/jpg/arbogne.jpg
:alt: arbogne Switzerland Fribourg
:name: arbogne

Die Arbogne in der Schweiz (Quelle: Sebastian Schwindt 2013).
```


## Theorie

### 1d Querschnitt gemittelte Hydrodynamik
Anhand der [Stufenentladung (*Manning-Strickler* Formel) exercise](https://github.com/Ecohydraulics/Exercise-ManningStrickler) erinnern wir uns an die Formel, um die Beziehung zwischen der Wassertiefe $h$ (inklusive des hydraulischen Radius $R_{h}$) und der Strömungsgeschwindigkeit $u$ zu berechnen:

$$
u = 1/n_m \cdot S_{e}^{1/2} \cdot R_{h}^{2/3}
$$

wo
* $n_m$ ist die [*Manning* coefficient](http://www.fsl.orst.edu/geowater/FX3/help/8_Hydraulic_Reference/Mannings_n_Tables.htm) in *fiktionalen* Einheiten von (s/m$^{1/3}$).
* $S_{e}$ ist die hypothetische Energieschrägheit (m/m) und entspricht der Kanalschrägheit für stetige, gleichmäßige Strömungsverhältnisse (in natürlichen Flüssen nicht vorhanden).
* hydraulic radius $R_{h} = A / P$, where (for a trapezoidal cross-section):
  - the wetted (trapezoidal) cross-section area is $A = h \cdot 0.5\cdot (b + B) = h \cdot (b + h\cdot m)$;
  - the wetted perimeter of a trapezoid is $P = b + 2h\cdot(m^2 + 1)^{1/2}$;
  - $b$ (channel base width) and $m$ (bank slope) are illustrated in the figure below to calculate the depth-dependent water surface width $B=b+2\cdot h\cdot m$.


```{figure} https://github.com/Ecohydraulics/media/raw/main/png/flow-cs.png
:alt: 1d hydraulics parameters
:name: cs-sed
```

This exercise uses one-dimensional (1d) cross-section averaged hydraulic data produced with the US Army Corps of Engineers HEC-RAS software {cite:p}`us_army_corps_of_engineeers_hydrologic_2016`, which solves the Manning-Strickler formula numerically for any flow cross-section shape. In this exercise, *HEC-RAS* provides the hydraulic data needed to determine the {term}`sediment transport <Sediment transport>` capacity of a channel cross-section, although no explanations for creating, running, and exporting data from *HEC-RAS* models are given.

### Sedimenttransport

Fluvial {term}`Sediment transport` can be distinguished into two modes: (1) {term}`suspended load <Suspended load>` and (2) {term}`bedload <Bedload>` (see {numref}`Fig. %s <transport-modes>`). Finer particles with a weight that can be carried by the fluid (water) are transported as {term}`suspended load <Suspended load>`. Coarser particles rolling, sliding, and jumping on the channel bed are transported as {term}`bedload <Bedload>`. There is another type of transport, the so-called wash load, which is finer than the coarse {term}`bedload <Bedload>`, but too heavy (large) to be transported in suspension {cite:p}`einstein_bed-load_1950`.

```{figure} https://github.com/Ecohydraulics/media/raw/main/png/sediment-transport.png
:alt: 1d sediment transport
:name: transport-modes

Zwei Arten des Sedimenttransports (Quelle: {cite:p}`schwindt_hydro-morphological_2017`).
```

In the following, we will look at the {term}`bedload <Bedload>` transport mode. In this case, a sediment particle located in or on the riverbed is mobilized by shear forces of the water as soon as they exceed a critical value (see figure below). In river hydraulics, the so-called dimensionless bed shear stress or *Shields* stress {cite:p}`shields_anwendung_1936` is often used as the threshold value for the mobilization of sediment from the riverbed (see {numref}`Fig. %s <bedload-uptake>`). This exercise uses one of the dimensionless bed shear stress approaches and the next section provides more explanations.

```{figure} https://github.com/Ecohydraulics/media/raw/main/png/sediment-uptake.png
:alt: sediment uptake mobilization
:name: bedload-uptake

Das Prinzip der Sedimentmobilisierung.
```

(mpm)=
### Die Meyer-Peter und Müller (1948) Formel

The {cite:t}`meyer-peter_formulas_1948` formula for estimating {term}`bedload <Bedload>` transport was published by Swiss researchers Eugen Meyer-Peter (founder of the [Laboratory of Hydraulics, Hydrology and Glaciology (VAW)](https://vaw.ethz.ch/en/) and Robert Müller. Their study began one year after the establishment of the VAW in 1931 when Robert Müller was appointed assistant to Eugen Meyer-Peter. The two scientists worked in collaboration with Henry Favre and Albert Einstein's son Hans Albert. In 1934, the laboratory published for the first time a formula for the calculation of {term}`bedload <Bedload>` transport and its fundamental relationship between observed $\tau_{x}$ and critical $\tau_{x,cr}$ dimensionless bed shear stresses is used until today. The dimensionless {term}`bedload <Bedload>` transport rate $\Phi_b$ according to {cite:t}`meyer-peter_formulas_1948` is:

$$
\Phi_b \approx 8 \cdot (\tau_{x} - \tau_{x,cr})^{3/2}
$$ (eq-py-mpm)

```{admonition} Bed shear stress
:name: taux
* $\tau_{x,cr}$ $\approx$ 0.047 (up to 0.07 in mountain rivers), and
* $\tau_{x}$= $R_{h} \cdot S_{e} / [(s - 1) \cdot D_{char}]$
```

Die übrigen Parameter sind:
* $s$ $\approx$ 2.68, the dimensionless ratio of sediment grain density $\rho_{s}$ ($\approx$ 2680 kg/m³) and water density $\rho_{w}$ ($\approx$ 1000 kg/m³);
* $D_{char}$, the characteristic grain size in (m). It can be assumed that $D_{char} \approx D_{84}$ (i.e., the grain diameter of which 84% of a sediment mixture is smaller) in line with the scientific literature (e.g., {cite:t}`rickenmann_evaluation_2011`).

The *Meyer-Peter & Müller* formula applies (like any other {term}`Sediment transport` formula) only to certain rivers that have the following characteristics (range of validity):
* 0.4 $\cdot$ 10$^{-3}$ m $< D_{char}$ < 28.6 $\cdot$ 10$^{-3}$ m
* 10$^{-4}$ m $< Fr <$ 639 ($Fr$ denotes the dimensionless [{term}`Froude number`](https://en.wikipedia.org/wiki/Froude_number))
* 0,0004 $< S_{e} <$0,02
* 0,0002 m$^3$/(s $\cdot$m) $< q <$ 2.0 m$^3$/(s $\cdot$m) ($q$ ist die Entladung der Einheit, d.h. $q=Q/[0. 5\cdot (b + B)]$)
* 0.25 $< s <$ 3.2

The dimensionless expression for {term}`bedload <Bedload>` $\Phi_b$ was used to enable information transfer between different channels across scales by preserving geometric, kinematic, and dynamic similarity. The set of dimensionless parameters used results from [Buckingham's $\Pi$ theorem](https://pint.readthedocs.io/en/stable/pitheorem.html) {cite:p}`buckingham_model_1915`.
Therefore, to add dimensions to $\Phi_b$, it needs to be multiplied with the same set of parameters used for deriving the dimensionless expression from *Meyer-Peter & Müller*. Their set of parameters involves the characteristic grain size $D_{char}$, the grain density $\rho_{s}$, and the gravitational acceleration $g$. Thus, the dimensional unit {term}`bedload <Bedload>` is (in kg/s and meter width, i.e., kg/(s$\cdot$m):

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

wobei $b_{eff}$ die hydraulisch aktive Kanalbreite des Strömungsquerschnitts ist (z. B. für ein Trapez $b_{eff} = 0.5 \cdot (b + B)$).


## Code

### Setzen Sie den Frame
Der objektorientierte Code verwendet benutzerdefinierte Klassen, die wir in einem **`main.py`** Skript aufrufen. Erstellen Sie die folgenden **zusätzlichen Skripte**, die die benutzerdefinierten Klassen und Funktionen zur Steuerung der Protokollierung enthalten.

* `fun.py` enthält Protokollierungsfunktionen.
* `hec.py` wird eine `HecSet` Klasse enthalten, um hydraulische Ausgabedaten von *HEC-RAS* als strukturierte Objekte zu lesen.
* `grains.py` wird eine `GrainReader` Klasse enthalten, um Informationen zur Korngrößenklasse als strukturierte Objekte zu lesen.
* `bedload.py` enthält die Klasse `BedCore` mit grundlegenden Elementen, die die meisten {term}`bedload <Bedload>` Formeln gemeinsam haben.
* `mpm.py` enthält die Klasse `MPM`, die von `BedCore` erbt und {term}`bedload <Bedload>` wie oben beschrieben berechnet (Meyer-Peter & Müller 1948).

Wir erstellen die Klassen und Funktionen in den angegebenen Skripten gemäß dem folgenden Flussdiagramm:

```{figure} https://github.com/Ecohydraulics/Exercise-SedimentTransport/raw/main/graphs/uml.png
:alt: sediment transport calculation python code structure
:name: structure
```

To start with the `main.py` script, add a `main` function as well as a `get_char_grain_size` and a `calculate_mpm` function. Moreover, make the script *stand-alone* executable:

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

### Protokollierungsfunktionen
Das `fun.py`Script enthält zwei Funktionen:

1. `start_logging` zum Einrichten von Protokollierungsformaten und eines Logdateinamens, wie im Abschnitt unter {ref}`logging <logging>` beschrieben, und
1. `log_actions`, das ist ein Funktions-Wrapper für die `main()` (`main.py`) Funktionen zum Protokollieren von Skriptausführungsnachrichten.

Die Funktion `start_logging` sollte so aussehen (ändern Sie den Namen der Logdatei, falls gewünscht):

```python
import logging


def start_logging():
    logging.basicConfig(filename="logfile.log", format="[%(asctime)s] %(message)s",
                        filemode="w", level=logging.DEBUG)
    logging.getLogger().addHandler(logging.StreamHandler()

```

Die Wrapper-Funktion `log_actions` folgt den Anweisungen von {ref}`functions theory section <wrappers>`:

```python
def log_actions(fun):
    def wrapper(*args, **kwargs):
        start_logging()
        fun(*args, **kwargs)
        logging.shutdown()
    return wrapper
```

To use the `log_actions` wrapper throughout the program, we will implement it at the highest level, which is the `main()` function in `main.py`:

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

Now, we can log messages at different levels (info, warning, error, or others) in all functions called within `main()` by using for example `logging.info("Message")`, `logging.warning("Message")`, or `logging.error("Message")` rather than the `print()` function.


### Lesen Sie Korngrößendaten

Sediment grain size classes (ranging from $D_{16}$ to $D_{max}$) are provided in the file [`grains.csv`](https://github.com/Ecohydraulics/Exercise-SedimentTransport/raw/main/grains.csv) (`delimiter=","`) and can be customized.

Write a `GrainReader` class that uses the `read_csv` method from {ref}`pandas` to read the grain size distribution from `grains.csv`. Write the class in a separate *Python* script (e.g., `grains.py` as indicated in the above figure):

```python
class GrainReader:
    def __init__(self, csv_file_name="grains.csv", delimiter=","):
        self.sep = delimiter
        self.size_classes = pd.DataFrame
        self.get_grain_data(csv_file_name)
```

The `get_grain_data` method should look like this for reading the provided grain size classes:

```python
    def get_grain_data(self, csv_file_name):
        self.size_classes = pd.read_csv(csv_file_name,
                                        names=["classes", "size"],
                                        skiprows=[0],
                                        sep=self.sep,
                                        index_col=["classes"])
```

```{admonition} Challenge
Add a `__call__()` method to the `GrainReader` class.
```

Implement the instantiation of a `GrainReader` object in the `main.py` script in the `get_char_grain_size` function. The function should receive the *string*-type arguments `file_name` (here: `"grains.csv"`) and `D_char` (i.e., the characteristic grain size to use from `grains.csv`). The `main()` function calls the `get_char_grain_size` function with the arguments `file_name=os.path.abspath("..") + "\\grains.csv"` and `D_char="D84"` (corresponds to the first column in `grains.csv`).

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


### Lesen Sie die HEC-RAS-Eingabedaten

The provided *HEC-RAS* dataset is stored in the *xlsx* workbook [`HEC-RAS/output.xlsx`](https://github.com/Ecohydraulics/Exercise-SedimentTransport/raw/main/HEC-RAS/output.xlsx) and contains the following output:

| **Col.No.** | **Alphabetic Col.** | **Variable** | **Type/Unit** |**Beschreibung** |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| Col. 01 | A | Reach | *string* | River (reach) name |
| Col. 02 | B | River Sta | [m] | Position auf der Längsachse des Flusses |
| Spalte 03 | C | Profile | *string* | Name of flow scenario profile (z. B. HQ2.33) |
| Spalte 04 | D | Q Total | [m3/s] | Flussableitung |
| Spalte 05 | E | Min Ch El | [m a.s.l.] | Mindesthöhe (Niveau) des Kanalquerschnitts |
| Col. 06 | F | W.S. Elev | [m a.s.l.] | Wasseroberflächenhöhe (Ebene) |
| Spalte 07 | G | Vel Chnl | [m] | Strömungsgeschwindigkeit Hauptkanal |
| Spalte 08 | H | Flow Area | [m2] | Benetzte Querschnittsfläche *A* (siehe oben) |
| Spalte 09 | I | Froude\# Chl | [-] | {term}`Froude number` des Kanals (wenn 1, Berechnungsfehler - nicht verwenden!) |
| Spalte 10 | J | Hydraulikradius | [m] | Hydraulikradius |
| Spalte 11 | K | Hydr Tiefe | [m] | Wassertiefe (aktiver Querschnittsmittelwert) |
| Spalte 12 | L | E.G. Slope | [m/m] | Energy Gradeline Hang |

Um *HEC-RAS*-Ausgabedaten zu laden, schreiben Sie eine benutzerdefinierte Klasse (in einem separaten Skript namens `hec.py`), die den Dateinamen als Eingabeargument annimmt und die *HEC-RAS*-Datei als *pandas*-Datenrahmen liest:

```python
class HecSet:
    def __init__(self, xlsx_file_name="output.xlsx"):
        self.hec_data = pd.DataFrame
        self.get_hec_data(xlsx_file_name)
```

The `get_hec_data` method should look (something) like this:
```python
    def get_hec_data(self, xlsx_file_name):
        self.hec_data = pd.read_excel(xlsx_file_name,
                                      skiprows=[1],
                                      header=[0])
```

Um ein `HecSet`-Objekt in der Funktion `main()` (`main.py`) zu erstellen, müssen wir es importieren und instanziieren, beispielsweise als `hec = HecSet(file_name)`. Darüber hinaus können wir bereits die Weitergabe der `pd.DataFrame` der *HEC-RAS*-Daten an die `calculate_mpm`-Funktion (auch in `main.py`) implementieren, die wir später abschließen werden.

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

### Erstellen einer Geschiebetransport Core Class

A `BedCore` class written in the `bedload.py` script provides variables and methods, which are relevant to many {term}`bedload <Bedload>` and {term}`Sediment transport` calculation formulae, such as the *Parker-Wong* correction {cite:p}`wong_reanalysis_2006` or the {cite:t}`smart_sedimenttransport_1983` ([direct download](https://ethz.ch/content/dam/ethz/special-interest/baug/vaw/vaw-dam/documents/das-institut/mitteilungen/1980-1989/064.pdf) ). Moreover, the `BedCore` class contains constants such as the gravitational acceleration $g$ (i.e., `self.g=9.81`), the ratio of sediment grain and water density $s$ (i.e., `self.s=2.68`), and the critical dimensionless bed shear stress $\tau_{x,cr}$ (i.e., `self.tau_xcr=0.047`, which may be re-defined by users). The header of the `BedCore` class should look (similar) like this:

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
Import `fun` (the script with logging functions) to enable the usage of `logging.warning(...)` messages in the methods of `BedCore` and its child classes.
```

Add a method to convert the dimensionless {term}`bedload <Bedload>` transport $\Phi_b$ into a dimensional value (kg/s). In addition to the variables defined in the `__init__` method, the `add_dimensions` method will require the effective channel width $b_{eff}$ ({ref}`recall the above calculus <qb>`):

```python
    def add_dimensions(self, b):
        try:
            return self.phi * b * np.sqrt((self.s - 1) * self.g * self.D ** 3) * self.rho_s
        except ValueError:
            logging.warning("Non-numeric data. Returning Qb=NaN.")
            return np.nan
```

Many {term}`bedload <Bedload>` transport formulae involve the dimensionless bed shear stress [$\tau_{x}$ (see above {ref}`definitions <taux>`) associated with a set of cross-section averaged hydraulic parameters. Therefore, implement the calculation method `compute_tau_x` in `BedCore`:

```python
    def compute_tau_x(self):
        try:
            return self.Se * self.Rh / ((self.s - 1) * self.D)
        except ValueError:
            logging.warning("Non-numeric data. Returning tau_x=NaN.")
            return np.nan
```

### Schreiben Sie eine Meyer-Peter & Müller Geschiebetransport Assessment Class

Create a new script (e.g., `mpm.py`) and implement an `MPM` class (**M**eyer-**P**eter & **M**üller) that inherits from the `BedCore` class. The `__init__` method of `MPM` should initialize `BedCore` and overwrite (recall {ref}`polymorphism`) relevant parameters to the calculation of {term}`bedload <Bedload>` according to Meyer-Peter & Müller (1948). Moreover, the initialization of an `MPM` object should go along with a check of the validity and the calculation of the dimensionless {term}`bedload <Bedload>` transport $\Phi_b$ (see above {ref}`explanations of MPM <mpm>`):

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

Fügen Sie die `check_validity`-Methode hinzu, um zu überprüfen, ob die bereitgestellten Querschnittsmerkmale in den Gültigkeitsbereich der Meyer-Peter & Müller-Formel fallen (z. B. Steigung, Korngröße, Verhältnis von Entladung und Wassertiefe und {term}`Froude number`):

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
The here shown `check_validity` method takes the {term}`Froude number` as input argument. Alternatively, assign the {term}`Froude number` already in `__init__` and use `self.Fr`.
```

Um den dimensionslosen {term}`bedload <Bedload>` transport $\Phi_b$ nach Meyer-Peter & Müller zu berechnen, implementieren Sie eine `compute_phi`-Methode, die die `compute_tau_x`-Methode von `BedCore` verwendet:

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

With the `MPM` class defined, we can now fill the `calculate_mpm` function in the `main.py` script. The function should create a *pandas* data frame with columns of dimensionless {term}`bedload <Bedload>` transport $ \Phi $ and dimensional {term}`bedload <Bedload>` transport $Q_{b}$ associated with a channel profile (`"River Sta"`) and flow scenario (`"Profile" > "Scenario"`).

The following code block illustrates an example of the `calculate_mpm` function that creates the *pandas* data frame from a {ref}`dict` (`mpm_dict`). The illustrative function creates the *dictionary* with void value lists, extracts hydraulic data from the *HEC-RAS* data frame, and loops over the `"River Sta"` entries. The loop checks if the `"River Sta"` entries are valid (i.e., not `"Nan"`) because empty rows that *HEC-RAS* automatically adds between output profiles should not be analyzed. If the check was successful, the loop appends the profile, scenario, and discharge directly to `mpm_dict`. The section-wise {term}`bedload <Bedload>` transport results from `MPM` objects. After the loop, the function returns `mpm_dict` as a `pd.DataFrame` object.

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

Nachdem die Funktion `calculate_mpm()` definiert wurde, sollte der Aufruf dieser Funktion aus der Funktion `main()` nun der Variablen `mpm_results` einen {ref}`pandas`-Datenrahmen zuweisen. Um das Skript abzuschließen, schreiben Sie `mpm_results` in eine Arbeitsmappe (z. B. `"bed_load_mpm.xlsx"`) in der Funktion `main()`:

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

## Launch und Debug

In your IDE, run the script (e.g., in {ref}`pycharm`, right-click in the `main.py` script and click `> Run 'main'`). If the script crashes or raises error messages, trace them back, and fix the issues. Add `try` - `except` statements where necessary and recall the {ref}`debugging instructions <sec-pyerror>`.

```{note}
Das Programm erzeugt absichtlich Warnmeldungen, da einige der Profileigenschaften den Gültigkeitsbereich der Meyer-Peter & Müller-Formel nicht erfüllen.
```

Ein erfolgreicher Lauf von `main.py` erzeugt eine `bed_load_mpm.xlsx`-Datei, die so aussieht:

| | River Sta | Szenario | Q (m3/s) | Phi (-) | Qb (kg/s) |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| 0 | 1970.1 | Q bedeuten | 1 | | |
| 1 | 1970.1 | HQ2.33 | 13 | 0.548377243 | 42.72291418
| 2 | 1970.1 | HQ5 | 17 | 0.682792055 | 54.58338633
| 3 | 1970.1 | HQ10 | 19 | 0.765834516 | 62.56010505 |
| 4 | 1970.1 | HQ100 | 25 | 0.905542967 | 77.92848176
| 5 | 1893.37 | Q bedeuten | 1 | 0.193642263 | 5.075423967
| 6 | 1893.37 | HQ2.33 | 13 | 0.144406226 | 14.00424884
| 7 | 1893.37 | HQ5 | 17 | 0.203854633 | 20.40484039
| 8 | 1893.37 | HQ10 | 19 | 0.229078172 | 23.1352098 |
| 9 | 1893.37 | HQ100 | 25 | 0.297767546 | 31.25225316 |
| ...| ... | ... | ...

Die Logfile sollte ähnlich aussehen:

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

Sediment transport calculations based on local cross-section averaged hydraulics have extremely high error rates because of higher-order controls {cite}`schwindt2023metaanalysis`.

Schließlich gibt es viele mögliche Lösungen für diese Übung und jede Lösung, die zum gleichen Ergebnis führt (Arbeitsmappe und Logfile), ist gültig. Die größte Herausforderung besteht darin, einen objektorientierten Ansatz zu verwenden, bei dem mindestens eine Klasse von einer anderen Klasse erbt.
```

```{admonition} Homeworks
1. Implement the Parker-Wong correction {cite:p}`wong_reanalysis_2006` for the {cite:t}`meyer-peter_formulas_1948` formula:$\Phi_{b,pw} \approx 4.93 \cdot (\tau_{x} - \tau_{x,cr})^{1.6}$. Implement the formula in the `MPM` class either use an optional keyword argument in `compute_phi` or a new method.

2. Use the `openpyxl` library to add a background color to the headers of output tables.

3. Choose and extract 3 profiles from `mpm_results` and plot the dimensional {term}`bedload <Bedload>` transport $Q_{b}$ (y-axis) against the discharge $q$ (x-axis).
```
