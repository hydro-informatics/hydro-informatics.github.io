---
description: Objektorientierte Python-Übung für 1D Bettlast-Sedimenttransport mit der Meyer-Peter- und Müller-Formel, mit Pandas DataFrames, Excel-Arbeitsbüchern und Manning-Strickler-Hydraulik.
---

(ex-py-sediment)=
# 1d Sediment Transport

```{admonition} Goals
Diese Übung beinhaltet die Anwendung der Meyer-Peter & Müller (1948) {term}`bedload <Bedload>` Transportformel auf eine gültige Anwendung: 1d, Querschnitt gemittelte Hydraulik. Schreiben Sie objektorientierten Code mit benutzerdefinierten Klassen für maßgeschneiderte Interaktionen mit *xlsx* Arbeitsmappe. Die Hausaufgaben beinhalten integrierte Methoden von {ref}`pandas` DataFrames und Plotting.
```

```{admonition} Requirements
:class: attention
Lesen und verstehen Sie die Datenverarbeitung mit {ref}`numpy` und {ref}`pandas` sowie {ref}`ooc`.
```

Bereiten Sie sich durch Klonen des Übungs-Repository:

```
git clone https://github.com/Ecohydraulics/Exercise-SedimentTransport.git
```

```{figure} https://github.com/Ecohydraulics/media/raw/main/jpg/arbogne.jpg
:alt: arbogne Switzerland Fribourg
:name: arbogne

Der Arbogne River in der Schweiz (Quelle: Sebastian Schwindt 2013).
```


## Theorie

### 1d Querschnitt Durchschnittliche Hydrodynamik
Aus der [State-Decharge (*Manning-Strickler*-Formel) Bewegung](https://github.com/Ecohydraulics/Exercise-ManningStrickler) wenden wir uns an die Formel, um die Beziehung zwischen Wassertiefe $h$ (in den Hydraulikradius $R_{h}$) und Fließgeschwindigkeit $u$ zu berechnen:

$$
u = 1/n_m \cdot S_{e}^{1/2} \cdot R_{h}^{2/3}
$$

wenn
* $n_m$ ist der [*Manning* Koeffizient](http://www.fsl.orst.edu/geowater/FX3/help/8_Hydraulic_Reference/Mannings_n_Tables.htm) in *fictional* Einheiten von (s/m$^{1/3}$.
* $S_{e}$ ist die hypothetische Energieneigung (m/m) und entspricht der Kanalneigung für stetige, gleichmäßige Strömungsbedingungen (nicht vorhanden in natürlichen Flüssen).
* Hydraulikradius $R_{h} = A / P$, wo (für einen trapezförmigen Querschnitt):
  - die benetzte (trapezoidale) Querschnittsfläche ist $A = h \cdot 0.5\cdot (b + B) = h \cdot (b + h\cdot m)$;
  - der benetzte Umfang eines Trapezes ist $P = b + 2h\cdot(m^2 + 1)^{1/2}$;
  - $b$ (Kanal-Basisbreite) und $m$ (Bankflanke) sind in der folgenden Abbildung dargestellt, um die tiefenabhängige Wasseroberflächenbreite $B=b+2\cdot h\cdot m$ zu berechnen.


```{figure} https://github.com/Ecohydraulics/media/raw/main/png/flow-cs.png
:alt: 1d hydraulics parameters
:name: cs-sed
```

This exercise uses one-dimensional (1d) cross-section averaged hydraulic data produced with the US Army Corps of Engineers HEC-RAS software {cite:p}`us_army_corps_of_engineeers_hydrologic_2016`, which solves the Manning-Strickler formula numerically for any flow cross-section shape. In this exercise, *HEC-RAS* provides the hydraulic data needed to determine the {term}`sediment transport <Sediment transport>` capacity of a channel cross-section, although no explanations for creating, running, and exporting data from *HEC-RAS* models are given.

### Sediment Transport

Fluvial {term}`Sediment transport` kann in zwei Modi unterschieden werden: (1) {term}`suspended load <Suspended load>` und (2) {term}`bedload <Bedload>` (siehe{numref}`Fig. %s <transport-modes>`). Finer-Partikel mit einem Gewicht, das von der Flüssigkeit (Wasser) getragen werden kann, werden als {term}`suspended load <Suspended load>` transportiert. Coarser-Partikel rollen, gleiten und springen auf dem Kanalbett werden als {term}`bedload <Bedload>` transportiert. Es gibt eine andere Art von Transport, die sogenannte Waschlast, die feiner ist als die grobe {term}`bedload <Bedload>`, aber zu schwer (groß) in Suspension zu transportieren{cite:p}`einstein_bed-load_1950`.

```{figure} https://github.com/Ecohydraulics/media/raw/main/png/sediment-transport.png
:alt: 1d sediment transport
:name: transport-modes

Zwei Arten des Sedimenttransports (Quelle: {cite:p}`schwindt_hydro-morphological_2017`).
```

Im Folgenden werden wir uns den Transportmodus {term}`bedload <Bedload>` anschauen. In diesem Fall wird ein im oder am Flussbett befindliches Sedimentpartikel durch Scherkräfte des Wassers mobilisiert, sobald sie einen kritischen Wert überschreiten (siehe Abbildung unten). In der Flusshydraulik wird oft der sogenannte dimensionslose Bettscherbeanspruchung oder *Shields* stress{cite:p}`shields_anwendung_1936` als Schwellenwert für die Mobilisierung von Sediment aus dem Flussbett verwendet (siehe {numref}`Fig. %s <bedload-uptake>`). Diese Übung verwendet eine der dimensionslosen Bettscherbeanspruchungen und der nächste Abschnitt gibt mehr Erläuterungen.

```{figure} https://github.com/Ecohydraulics/media/raw/main/png/sediment-uptake.png
:alt: sediment uptake mobilization
:name: bedload-uptake

Das Prinzip der Sedimentmobilisierung.
```

(mpm)=
### Die Meyer-Peter und Müller (1948) Formel

Die {cite:t}`meyer-peter_formulas_1948` Formel für die Schätzung {term}`bedload <Bedload>`Transport wurde von Schweizer Forschern Eugen Meyer-Peter (Gründer des [Laboratoriums für Hydraulik, Hydrologie und Glaciologie (VAW)](https://vaw.ethz.ch/en/) und Robert Müller) veröffentlicht. Ihre Studie begann ein Jahr nach der Gründung der VAW 1931, als Robert Müller zum Assistenten von Eugen Meyer-Peter ernannt wurde. Die beiden Wissenschaftler arbeiteten in Zusammenarbeit mit Henry Favre und Albert Einsteins Sohn Hans Albert. Im Jahr 1934 veröffentlichte das Labor erstmals eine Formel für die Berechnung von {term}`bedload <Bedload>`Transport und dessen grundlegende Beziehung zwischen beobachteten $\tau_{x}$ und kritischen $\tau_{x,cr}$ dimensionslosen Bettscherspannungen bis heute. Die dimensionslose {term}`bedload <Bedload>` Transportrate $\Phi_b$ laut {cite:t}`meyer-peter_formulas_1948` ist:

$$
\Phi_b \approx 8 \cdot (\tau_{x} - \tau_{x,cr})^{3/2}
$$ (eq-py-mpm)

```{admonition} Bed shear stress
:name: taux
* $\tau_{x,cr}$ $\approx$ 0.047 (up to 0.07 in mountain rivers), and
* $\tau_{x}$ = $R_{h} \cdot S_{e} / [(s - 1) \cdot D_{char}]$
```

Die anderen Parameter sind:
* $s$ $\approx$ 2.68, the dimensionless ratio of sediment grain density $\rho_{s}$ ($\approx$ 2680 kg/m³) and water density $\rho_{w}$ ($\approx$ 1000 kg/m³);
* $D_{char}$, die charakteristische Korngröße in (m). Es kann davon ausgegangen werden, dass $D_{char} \approx D_{84}$ (d.h. der Korndurchmesser, dessen 84% eines Sedimentgemisches kleiner ist) entsprechend der wissenschaftlichen Literatur (z.B. {cite:t}`rickenmann_evaluation_2011`) entspricht.

Die *Meyer-Peter & Müller*-Formel gilt (wie jede andere {term}`Sediment transport`-Formel) nur für bestimmte Flüsse, die folgende Eigenschaften haben (Validitätsbereich):
* $\cdot$10$^{-3}$m@m$< D_{char}$ < 28,6$\cdot$10$^{-3}$m
* 10$^{-4}$ m $< Fr <$ 639 ($Fr$ denotes the dimensionless [{term}`Froude number`](https://en.wikipedia.org/wiki/Froude_number))
* 0,0004$< S_{e} <$0,02
* 0,0002 m$^3$/(s $\cdot$m)$< q <$ 2.0 m$^3$/(s$\cdot$m) ($q$ ist die Einheitsentladung, d.h.$q=Q/[0. 5\cdot (b + B)]$)
* 0,25 $< s <$ 3.2

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

wobei $b_{eff}$ die hydraulisch aktive Kanalbreite des Strömungsquerschnitts ist (z.B. für einen Trapezoid $b_{eff} = 0.5 \cdot (b + B)$).


## Code

### Setzen Sie den Rahmen
Der objektorientierte Code verwendet benutzerdefinierte Klassen, die wir in einem **`main.py`* Script anrufen. Erstellen Sie die folgenden **zusätzlichen Skripte**, die die benutzerdefinierten Klassen und Funktionen enthalten, um das Protokoll zu steuern.

* `fun.py` enthält Protokollfunktionen.
* `hec.py` wird eine `HecSet`-Klasse enthalten, um hydraulische Ausgangsdaten von *HEC-RAS* als strukturierte Objekte zu lesen.
* `grains.py` wird eine `GrainReader`-Klasse enthalten, um Informationen zur Korngrößenklasse als strukturierte Objekte zu lesen.
* `bedload.py` enthält die Klasse `BedCore` mit den Grundelementen, die die meisten {term}`bedload <Bedload>` Formeln gemeinsam haben.
* `mpm.py` enthält die Klasse `MPM`, die von `BedCore` vererbt wird und wie oben beschrieben {term}`bedload <Bedload>` berechnet (Meyer-Peter & Müller 1948).

Wir erstellen die Klassen und Funktionen in den angegebenen Skripten nach dem folgenden Flussdiagramm:

```{figure} https://github.com/Ecohydraulics/Exercise-SedimentTransport/raw/main/graphs/uml.png
:alt: sediment transport calculation python code structure
:name: structure
```

Um mit dem `main.py`Script zu beginnen, fügen Sie eine `main`-Funktion sowie eine `get_char_grain_size` und eine `calculate_mpm`-Funktion hinzu. Außerdem machen Sie das Skript *stand-alone* ausführbar:

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

### Logging Funktionen
Das `fun.py`Script enthält zwei Funktionen:

1. `start_logging`, um Logging-Formate und einen Log-Dateinamen wie im Abschnitt unter {ref}`logging <logging>` beschrieben, und
1. `log_actions`, das ist ein Funktions-Wrapper für die `main()` (`main.py`) Funktionen, um Skriptausführungsnachrichten zu protokollieren.

Die `start_logging`-Funktion sollte so aussehen (gegebenenfalls den Log-Dateinamen ändern):

```python
import logging


def start_logging():
    logging.basicConfig(filename="logfile.log", format="[%(asctime)s] %(message)s",
                        filemode="w", level=logging.DEBUG)
    logging.getLogger().addHandler(logging.StreamHandler()

```

Die `log_actions`Wrapper-Funktion folgt den Anweisungen des {ref}`functions theory section <wrappers>`:

```python
def log_actions(fun):
    def wrapper(*args, **kwargs):
        start_logging()
        fun(*args, **kwargs)
        logging.shutdown()
    return wrapper
```

Um den `log_actions`packper im gesamten Programm zu nutzen, setzen wir ihn auf höchstem Niveau um, das ist die `main()`-Funktion in`main.py`:

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

Nun können wir Meldungen auf verschiedenen Ebenen (Info, Warnung, Fehler oder andere) in allen Funktionen, die unter `main()` aufgerufen werden, unter Verwendung von z.B. `logging.info("Message")`, `logging.warning("Message")` oder `logging.error("Message")` anstelle der `print()`-Funktion anmelden.


### Korngrößendaten lesen

Sediment grain size classes (ranging from $D_{16}$ to $D_{max}$) are provided in the file [`grains.csv`](https://github.com/Ecohydraulics/Exercise-SedimentTransport/raw/main/grains.csv) (`delimiter=","`) and can be customized.

Schreiben Sie eine `GrainReader`-Klasse, die die `read_csv`-Methode von {ref}`pandas` verwendet, um die Korngrößenverteilung von `grains.csv` zu lesen. Schreiben Sie die Klasse in einem separaten *Python*-Skript (z.B. `grains.py`, wie in der obigen Abbildung angegeben):

```python
class GrainReader:
    def __init__(self, csv_file_name="grains.csv", delimiter=","):
        self.sep = delimiter
        self.size_classes = pd.DataFrame
        self.get_grain_data(csv_file_name)
```

Die `get_grain_data`-Methode sollte so aussehen, um die bereitgestellten Korngrößenklassen zu lesen:

```python
    def get_grain_data(self, csv_file_name):
        self.size_classes = pd.read_csv(csv_file_name,
                                        names=["classes", "size"],
                                        skiprows=[0],
                                        sep=self.sep,
                                        index_col=["classes"])
```

```{admonition} Challenge
Fügen Sie eine `__call__()` Methode an die `GrainReader`Klasse.
```

Ergänzen Sie die Instantiation eines `GrainReader`Objekts im `main.py`Script in der `get_char_grain_size` Funktion. Die Funktion sollte die *string*-Argumente `file_name` (hier:`"grains.csv"`) und `D_char` (d.h. die charakteristische Korngröße von `grains.csv`) erhalten. Die `main()`-Funktion ruft die `get_char_grain_size`-Funktion mit den Argumenten `file_name=os.path.abspath("..") + "\\grains.csv"` und `D_char="D84"` auf (entspricht der ersten Spalte unter `grains.csv`).

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


### HEC-RAS Eingabedaten lesen

The provided *HEC-RAS* dataset is stored in the *xlsx* workbook [`HEC-RAS/output.xlsx`](https://github.com/Ecohydraulics/Exercise-SedimentTransport/raw/main/HEC-RAS/output.xlsx) and contains the following output:

| **Col.No.****Alphabetic Col.**********Variable**** Typ/Unit***** Beschreibung*** |
-----------------------------------------------------------------------------------------------------
| Col. 01 | A | Reach | *string* | River (Reach) Name |
| Col. 02 | B | River Sta | [m] | Position auf der Flusslängsachse |
| Col. 03 | C | Profil | *string* | Name des Flussszenarioprofils (z.B. HQ2.33) |
| Col. 04 | D | Q Total | [m3/s] | Flussentladung |
| Col. 05 | E | Min Ch El | [m a.s.l.] | Mindesthöhe (Ebene) des Kanalquerschnitts |
| Col. 06 | F | W.S. Elev | [m a.s.l] | Wasseroberflächenerhebung (Ebene) |
| Col. 07 | G | Vel Chnl | [m] | Strömungsgeschwindigkeit Hauptkanal |
| Col. 08 | H | Durchflussbereich | [m2] | Benetzter Querschnitt *A* (siehe oben) |
| Col. 09 | I | Froude\# Chl | [-] | {term}`Froude number` des Kanals (wenn 1, Berechnungsfehler - nicht verwenden!) |
| Col. 10 | J | Hydr Radius | [m] | Hydraulischer Radius |
| Col. 11 | K | Hydr Depth | [m] | Wassertiefe (aktive Querschnittsmittel) |
| Col. 12 | L | E.G. Slope | [m/m] | Energy Gradeline Pisten

Um *HEC-RAS* Ausgabedaten zu laden, schreiben Sie eine benutzerdefinierte Klasse (in einem separaten Skript namens `hec.py`), das den Dateinamen als Eingabeargument nimmt und die *HEC-RAS*-Datei als *pandas* Datenrahmen liest:

```python
class HecSet:
    def __init__(self, xlsx_file_name="output.xlsx"):
        self.hec_data = pd.DataFrame
        self.get_hec_data(xlsx_file_name)
```

Die `get_hec_data` Methode sollte so aussehen (etwas):
```python
    def get_hec_data(self, xlsx_file_name):
        self.hec_data = pd.read_excel(xlsx_file_name,
                                      skiprows=[1],
                                      header=[0])
```

Um ein `HecSet`-Objekt in der `main()` (`main.py`)-Funktion zu erstellen, müssen wir es z.B. als `hec = HecSet(file_name)` importieren und umgehen. Darüber hinaus können wir bereits die `pd.DataFrame` der *HEC-RAS*-Daten an die `calculate_mpm`-Funktion (auch unter `main.py`) weitergeben, die wir später abschließen werden.

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

### Erstellen Sie eine Geschiebetransport Core Class

Eine im `bedload.py`-Skript geschriebene `BedCore`-Klasse liefert Variablen und Methoden, die für viele {term}`bedload <Bedload>` und {term}`Sediment transport`Berechnungsformeln relevant sind, wie z.B. die *Parker-Wong*-Korrektur {cite:p}`wong_reanalysis_2006` oder die {cite:t}`smart_sedimenttransport_1983` ([direct download](https://ethz.ch/content/dam/ethz/special-interest/baug/vaw/vaw-dam/documents/das-institut/mitteilungen/1980-1989/064.pdf) ]. Darüber hinaus enthält die `BedCore`-Klasse Konstanten wie die Gravitationsbeschleunigung $g$ (d.h.`self.g=9.81`), das Verhältnis von Sedimentkorn und Wasserdichte $s$ (d.h. `self.s=2.68`) und den kritischen dimensionslosen Bettscherstress$\tau_{x,cr}$ (d.h.`self.tau_xcr=0.047`, die von den Nutzern neu definiert werden kann). Der Header der `BedCore`-Klasse sollte so aussehen (ähnlich):

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
Import `fun` (das Skript mit Logging-Funktionen) um die Nutzung von `logging.warning(...)`Nachrichten in den Methoden von `BedCore` und seinen Kinderklassen zu ermöglichen.
```

Fügen Sie eine Methode hinzu, um den dimensionslosen {term}`bedload <Bedload>` transport $\Phi_b$ in einen Maßwert umzuwandeln (kg/s). Neben den Variablen, die in der `__init__`-Methode definiert sind, benötigt die `add_dimensions`-Methode die effektive Kanalbreite $b_{eff}$ ({ref}`recall the above calculus <qb>`):

```python
    def add_dimensions(self, b):
        try:
            return self.phi * b * np.sqrt((self.s - 1) * self.g * self.D ** 3) * self.rho_s
        except ValueError:
            logging.warning("Non-numeric data. Returning Qb=NaN.")
            return np.nan
```

Viele {term}`bedload <Bedload>` Transportformeln beinhalten die dimensionslose Bettscherbeanspruchung [$\tau_{x}$ (siehe oben {ref}`definitions <taux>`) mit einem Satz von durchschnittenen hydraulischen Parametern. Deshalb die Berechnungsmethode `compute_tau_x` in `BedCore`:

```python
    def compute_tau_x(self):
        try:
            return self.Se * self.Rh / ((self.s - 1) * self.D)
        except ValueError:
            logging.warning("Non-numeric data. Returning tau_x=NaN.")
            return np.nan
```

### Schreibe eine Meyer-Peter & Müller Geschiebetransport Assessment Class

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

Fügen Sie die `check_validity`-Methode hinzu, um zu überprüfen, ob die bereitgestellten Querschnittseigenschaften in den Gültigkeitsbereich der Meyer-Peter & Müller-Formel fallen (d.h. Steigung, Korngröße, Austritts- und Wassertiefe und {term}`Froude number`):

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
Die hier dargestellte `check_validity` Methode nimmt die {term}`Froude number` als Eingabeargument an. Alternativ können Sie die {term}`Froude number` bereits unter`__init__` anordnen und `self.Fr` verwenden.
```

Um dimensionslose {term}`bedload <Bedload>` transport $\Phi_b$ nach Meyer-Peter & Müller zu berechnen, implementieren Sie eine `compute_phi` Methode, die die `compute_tau_x` Methode von `BedCore` verwendet:

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

Mit der definierten `MPM`-Klasse können wir nun die `calculate_mpm`-Funktion im `main.py`-Skript ausfüllen. Die Funktion sollte einen *pandas*-Datenrahmen mit spalten von dimensionslosen {term}`bedload <Bedload>` transport$ \Phi $ und dimensional{term}`bedload <Bedload>` transport$Q_{b}$ erstellen, der mit einem Kanalprofil (`"River Sta"`) und einem Flow-Szenario (`"Profile" > "Scenario"`) verbunden ist.

Der folgende Codeblock zeigt ein Beispiel der `calculate_mpm`-Funktion, die den *pandas*-Datenrahmen aus einem {ref}`dict` (`mpm_dict`) erstellt. Die illustrative Funktion erstellt das *dictionary* mit Leerwertlisten, extrahiert hydraulische Daten aus dem *HEC-RAS* Datenrahmen und Schleifen über die `"River Sta"`Einträge. Die Schleife überprüft, ob die `"River Sta"`-Einträge gültig sind (d.h. nicht `"Nan"`), da leere Zeilen, die *HEC-RAS* automatisch zwischen Ausgabeprofilen addiert, nicht analysiert werden sollten. Wenn die Prüfung erfolgreich war, fügt die Schleife das Profil, das Szenario und die Entladung direkt an `mpm_dict`. Der abschnittsweise {term}`bedload <Bedload>` transport ergibt sich aus `MPM`Objekten. Nach der Schleife gibt die Funktion `mpm_dict` als `pd.DataFrame`objekt zurück.

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

Nach der Definition der `calculate_mpm()`-Funktion sollte der Anruf an diese Funktion aus der `main()`-Funktion nun einen {ref}`pandas`-Datenrahmen an die `mpm_results`-Variable vergeben. Um das Skript abzuschließen, schreiben Sie `mpm_results` an ein Arbeitsbuch (z.B. `"bed_load_mpm.xlsx"`) in der `main()`-Funktion:

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

## Start und Debug

In your IDE, run the script (e.g., in {ref}`pycharm`, right-click in the `main.py` script and click `> Run 'main'`). If the script crashes or raises error messages, trace them back, and fix the issues. Add `try` - `except` statements where necessary and recall the {ref}`debugging instructions <sec-pyerror>`.

```{note}
Das Programm produziert absichtlich Warnmeldungen, da einige der Profileigenschaften den Gültigkeitsbereich der Meyer-Peter & Müller-Formel nicht erfüllen.
```

Ein erfolgreicher Lauf von `main.py` erzeugt eine `bed_load_mpm.xlsx`-Datei, die so aussieht:

| | River Sta | Scenario | Q (m3/s) | Phi (-) | Qb (kg/s) |
-------------------------------------------------------------
| 0 | 1970.1 | Q bedeuten | 1 | | | |
| 1 | 1970.1 | HQ2.33 | 13 | 0.548377243 | 42.72291418 |
| 2 | 1970.1 | HQ5 | 17 | 0.682792055 | 54.58338633 |
| 3 | 1970.1 | HQ10 | 19 | 0.765834516 | 62.560105 |
| 4 | 1970.1 | HQ100 | 25 | 0.905542967 | 77.92848176 |
| 5 | 1893.37 | Q mean | 1 | 0.193642263 | 5.075423967 |
| 6 | 1893.37 | HQ2.33 | 13 | 0.144406226 | 14.00424884 |
| 7 | 1893.37 | HQ5 | 17 | 0.203854633 | 20.40484039 |
| 8 | 1893.37 | HQ10 | 19 | 0.229078172 | 23.1352098 |
| 9 | 1893.37 | HQ100 | 25 | 0.297767546 | 31.25225316 |
...

Das Logfile sollte so ähnlich aussehen:

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

Sediment-Transportberechnungen auf der Basis lokaler Querschnittsmittelhydraulik haben aufgrund der übergeordneten Steuerungen {cite}`schwindt2023metaanalysis` extrem hohe Fehlerraten.

Schließlich gibt es viele mögliche Lösungen für diese Übung und jede Lösung, die zum gleichen Ergebnis führt (Arbeitsbuch und Logfile) ist gültig. Die zentrale Herausforderung besteht darin, einen objektorientierten Ansatz mit mindestens einer Klasse zu verwenden, die von einer anderen Klasse erbt wird.
```

```{admonition} Homeworks
1. Implementieren Sie die Parker-Wong-Korrektur {cite:p}`wong_reanalysis_2006` für die {cite:t}`meyer-peter_formulas_1948` Formel:$\Phi_{b,pw} \approx 4.93 \cdot (\tau_{x} - \tau_{x,cr})^{1.6}$. Ergänzen Sie die Formel in der `MPM` Klasse, verwenden Sie entweder ein optionales Keyword-Argument in `compute_phi` oder eine neue Methode.

2. Verwenden Sie die `openpyxl` Bibliothek, um den Headern der Ausgabetabellen eine Hintergrundfarbe hinzuzufügen.

3. Wählen und extrahieren Sie 3 Profile von `mpm_results` und legen Sie die Dimension {term}`bedload <Bedload>` transport$Q_{b}$ (y-axis) gegen die Entladung $q$ (x-Achse) auf.
```
