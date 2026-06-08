---
description: Quantitative Konvergenzanalyse für TELEMAC-Simulationen unter Verwendung von Massenbilanz und Python, die die Flussdiagnostik und die kumulative Flussrate-Verifikation für zuverlässige Flussmodelle abdeckt.
---

(tm-convergence)=
# Konvergenz (Quantitative)

````{admonition} Requirements
:class: important, dropdown

* Vervollständigen Sie die {ref}`Telemac steady 2d tutorial <telemac2d-steady>` (oder ähnliches).
* Die Schlüsselwörter `MASS-BALANCE : YES` und/oder `PRINTING CUMULATED FLOWRATES : YES` sind in der Steuerungsdatei (`.cas`) verwendet worden, um Massenflüsse über Flüssigkeitsgrenzen im Terminal zu drucken.
* Die Telemac-Simulation muss mit der `s`-Flagge ausgeführt sein (weitere Details unten):

```fortran
telemac2d.py [STUDY-NAME].cas -s
```

* Eine Installation von Python zusammen mit der `numpy`,`pandas` und `matplotlib` Bibliotheken ({ref}`see the Python installation guide <install-python>`), auch wenn `flusstools` nicht erforderlich ist.

**Alle benötigten Simulationsdateien für dieses Tutorial können vom [Hydro-informatics/telemac-Repository auf GitHub](https://github.com/hydro-informatics/telemac/tree/main/steady2d-tutorial)(siehe unten) heruntergeladen werden.**
````

```{admonition} Goals & purpose
:class: note

Dieses Tutorial beschreibt die Überprüfung der Flusskonvergenz, um die erforderliche Anzahl von Simulations-Zeitschritten (`NUMBER OF TIME STEPS`) eines **steady* zu optimieren. Telemac Simulation. Eine solche Konvergenzanalyse wird vor der Verwendung von stationären Simulationsergebnissen für den Hotstart einer {ref}`unsteady <chpt-unsteady>` oder einer {ref}`morphodynamic (sediment transport) <gaia-basics>`-Simulation empfohlen. Die hier gezeigten Skripte können aber auch zum Vergleich von Fahrtzeiten von von stromaufwärts zu einer stromabwärtigen Grenze laufenden Flutwellen dienen.

Wenn Sie nach Lösungen suchen, um ein nicht konvergierendes Modell zu beheben, wenden Sie sich bitte an die {ref}`spotlight chapter on mass conservation <tm-foc-mass>` und stellen Sie sicher, dass die {ref}`liquid boundaries are well defined <tm-foc-bc>`.
```

Dieses Kapitel verwendet die Simulationsdateien der {ref}`Telemac steady 2d tutorial <telemac2d-steady>`, aber mit einer etwas anderen Definition von Zeitschritten und Ausdruckzeiten:

```fortran
/ steady2d-conv.cas
TIME STEP : 1.
NUMBER OF TIME STEPS : 10000
GRAPHIC PRINTOUT PERIOD : 50
LISTING PRINTOUT PERIOD : 50
```

Zusätzlich wurde die Simulation mit der `-s`-Flagge wiederholt, die den Simulationszustand in einer Datei speichert, die ähnlich `[FILE-NAME].cas_YEAR-MM-DD-HHhMMminSSs.sortie` aufgerufen wird.

```fortran
telemac2d.py steady2d-conv.cas -s
```

Sowohl die Steuerung `.cas` als auch `.sortie` Dateien können von den hydro-informatics.com-Repositories heruntergeladen werden:

* [download station2d-conv.cas](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/steady2d-conv.cas)
* [download station2d-conv.cas 2023-07-26-18h41min26s.sortie](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/steady2d-conv.cas_2023-07-26-18h41min26s.sortie)

(tm-flux-convergence)=
## Daten extrahieren und überprüfen

```{admonition} Alternative: use control sections

Dieser Abschnitt enthält die Fluss- (Fluss-)Konvergenzanalyse direkt aus der Telemac-Nachrichtenprotokollierung mit Python. Alternativ können Flussmittel von {ref}`defining control sections (read more in the unsteady tutorial <tm-control-sections>` extrahiert werden.
```

The Telemac jupyter notebook templates (*HOMETEL/notebooks/* > *data_manip/extraction/\*.ipynb* or *workshops/exo_fluxes.ipynb*) provide some guidance for extracting data from simulation results, which can be tweaked into a generally applicable framework for observing mass convergence at the boundaries as a function of the defined `NUMBER OF TIME STEPS`. However, the notebook templates do not work straightforwardly, which is why the following paragraphs describe a simple, minimalist Python tweak called [pythomac](https://pythomac.readthedocs.io), developed by hydro-informatics.com. There are three options for working with our codes, and all of them require having an installation of Python along with the `numpy`, `pandas`, and `matplotlib` libraries ({ref}`see the Python installation guide <install-python>`):

`````{tab-set}
````{tab-item} pip-install pythomac

Pip-installieren Sie das *pythomac* Paket:

```
pip install pythomac
```
````

````{tab-item} clone pythomac

Binden Sie das *pythomac*-Repository von [GitHub](https://github.com/hydro-informatics/pythomac):

```
git clone https://github.com/hydro-informatics/pythomac.git
```

Kopieren Sie den Ordner `pythomac/pythomac/` in Ihr Simulationsverzeichnis. Das heißt, stellen Sie sicher, dass das Python-Skript `/HOME/pythomac/extract_fluxes.py` (u.a.) richtig liegt, neben `/HOME/your-simulation-dir/steady2d.cas`.
````

````{tab-item} download pythomac as zip

Laden Sie ein verzipptes Archiv des *pythomac*-Repositorys von [GitHub herunter (rechtsklicken Sie hier > speichern als...)](https://github.com/hydro-informatics/pythomac/archive/refs/heads/main.zip). Öffnen Sie das zip-Archiv > öffnen `pythomac-main` und extrahieren Sie die Inhalte des `pythomac`-Ordners (d.h.`pythomac-main/pythomac/`) neben Ihrem Simulationsverzeichnis. Das heißt, stellen Sie sicher, dass das Python-Skript `/HOME/pythomac/extract_fluxes.py` (u.a.) richtig liegt, neben `/HOME/your-simulation-dir/steady2d.cas`.
````
`````

````{admonition} Expand to see the code in the extract_fluxes.py Python script:
:class: tip, dropdown
:name: python-extract-fluxes-telemac

```python
""" Extract data from a Telemac simulation that has already been running.
The codes are inspired by the following jupyter notebook:
    HOMETEL/notebooks/data_manip/extraction/output_file_extraction.ipynb
 which uses the following example case:
    /examples/telemac2d/bump/t2d_bump_FE.cas
"""

# retrieve file paths - this script must be stored in the directory where the simulation lives
import sys
import os
# data processing
import pandas as pd
import numpy as np
# plotting
import matplotlib
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
# Telemac stuff
from parser_output import get_latest_output_files
from parser_output import OutputFileData


def extract_fluxes(
        model_directory="",
        cas_name="steady2d.cas",
        plotting=True
):
    """This function writes a .csv file and an x-y plot of fluxes across the boundaries of a Telemac2d model. It auto-
        matically place the .csv and .png plot files into the simulation directory (i.e., where the .cas file is).

    Notes:
        * The Telemac simulation must have been running with the '-s' flag (``telemac2d.py my.cas -s``).
        * Make sure to activate the .cas keyword ``PRINTING CUMULATED FLOWRATES : YES``
        * This script skips volume errors (search tags are not implemented).
        * Read more about this script at
            https://hydro-informatics.com/numerics/telemac/telemac2d-steady.html#verify-steady-tm2d

    :param str model_directory: the file directory where the simulation lives
    :param str cas_name: name of the .cas steering file (without directory)
    :param bool plotting: default (True) will place a figure called flux-convergence.png in the simulation directory
    :return pandas.DataFrame: time series of fluxes across boundaries (if Error int: -1)
    """

    # assign cas file name in the folder
    file_name = get_latest_output_files(
        os.path.join(model_directory,  # os.path.dirname(os.path.realpath(__file__))
                     cas_name
                     )
        )

    # go to working directory
    try:
        os.chdir(model_directory)
    except Exception as problem:
        print("ERROR: the provided directory {0} does not exist:\n{1}".format(str(model_directory), str(problem)))
        return -1

    try:
        out_file = OutputFileData(file_name[0])
    except Exception as e:
        print("CAS name: " + str(os.path.join(os.path.dirname(os.path.realpath(__file__)), cas_name)))
        print("ERROR in file {0}:\n{1}".format(str(file_name), str(e)))
        print("Recall: the simulation must run with the -s flags")
        return -1

    print("Found study with name: {}".format(out_file.get_name_of_study()))
    print("The simulation took: {} seconds".format(out_file.get_exec_time()))

    # extract total volume, fluxes, and volume error
    out_fluxes = out_file.get_value_history_output("voltotal;volfluxes;volerror")
    out_fluxes_dict = {}
    for e in out_fluxes:
        try:
            # differentiate between Time and Flux series with nested lists
            if not isinstance(e[0], tuple):
                out_fluxes_dict.update({e[0]: np.array(e[1])})
            else:
                for sub_e in e:
                    try:
                        if "volume" in str(sub_e[0]).lower():
                            # go here if ('Volumes (m3/s)', [volume(t)])
                            out_fluxes_dict.update({sub_e[0]: np.array(sub_e[1])})
                        if "fluxes" in str(sub_e[0]).lower():
                            for bound_i, bound_e in enumerate(sub_e[1]):
                                out_fluxes_dict.update({
                                    "Fluxes {}".format(str(bound_e)): np.array(sub_e[2][bound_i])
                                })
                    except Exception as problem:
                        print("ERROR in intended VOLUME tuple " + str(sub_e[0]) + ":\n" + str(problem))
        except Exception as problem:
            print("ERROR in " + str(e[0]) + ":\n" + str(problem))
            print("WARNING: Flux series seem empty. Verify:")
            print("         - did you run telemac2d.py sim.cas with the -s flag?")
            print("         - did your define all required VARIABLES FOR GRAPHIC PRINTOUTS (U,V,S,B,Q,F,H)?")

    try:
        df = pd.DataFrame.from_dict(out_fluxes_dict)
        df.set_index(list(df)[0], inplace=True)
    except Exception as problem:
        print("ERROR: could not convert dict to DataFrame because:\n" + str(problem))
        return -1

    export_fn = "extracted_fluxes.csv"
    print("* Exporting to {}".format(str(os.path.join(model_directory, export_fn))))
    df.to_csv(os.path.join(model_directory, export_fn))

    if plotting:
        font = {'size': 9}
        matplotlib.rc('font', **font)
        fig = plt.figure(figsize=(6, 3), dpi=400)
        axes = fig.add_subplot()
        colors = plt.cm.Blues(np.linspace(0, 1, len(df.columns)))
        markers = ("x", "o", "s", "+", "1", "D", "*", "CARETDOWN", "3", "^", "p", "2")
        for i, y in enumerate(list(df)):
            if "flux" in str(y).lower():
                axes.plot(df.index.values, df[y].abs(), color=colors[i], markersize=2, marker=markers[i], markerfacecolor='none',
                          markeredgecolor=colors[i], linestyle='-', linewidth=1.0, alpha=0.6, label=y)
        axes.set_xlim((np.nanmin(df.index.values), np.nanmax(df.index.values)))
        axes.set_ylim(bottom=0)
        axes.set_xlabel("Time (s)")
        axes.set_ylabel("Fluxes (m$^3$/s)")
        axes.legend(loc="best", facecolor="white", edgecolor="gray", framealpha=0.5)
        fig.tight_layout()
        fig.savefig(os.path.join(model_directory, "flux-convergence.png"))
        print("* Saved plot as " + str(os.path.join(model_directory, "flux-convergence.png")))
    return df
```
````

Detailed instructions for using the `extract_fluxes()` function through pythomac and its dependencies (`numpy`, `pandas`, and `matplotlib`) can be found at [https://pythomac.readthedocs.io](https://pythomac.readthedocs.io).

Um die in `pythomac` definierten Funktionen zu nutzen, kopieren Sie den folgenden Code in ein neues Python-Skript, das z.B. `example_flux_convergence.py` im Verzeichnis aufgerufen wird, in dem die trocken-initialisierte stationäre2d-Simulation lief (oder [download example flux convergence.py](https://github.com/hydro-informatics/pythomac/blob/main/example_flux_convergence.py)):


```python
# example_flux_convergence.py

from pathlib import Path
from pythomac import extract_fluxes

simulation_dir = str(Path(__file__).parents[1])
telemac_cas = "steady2d.cas"

fluxes_df = extract_fluxes(
    model_directory=simulation_dir,
    cas_name=telemac_cas,
    plotting=True
)
```

```{admonition} Got errors? Verify that the simulation directories are correct.
:class: error

Eine einfache `print(simulation_dir)`-Linie im obigen Codeblock hinzufügen könnte dazu beitragen, die Richtigkeit der Verzeichnisse zu überprüfen. Das heißt, der Python-Code sollte in der Lage sein, die Simulation zu verbessern.
```

Führen Sie das Python-Skript von Terminal (oder Anaconda Prompt) wie folgt aus (vergewissern Sie sich an `cd` in das Simulationsverzeichnis):

```
python example_flux_convergence.py
```

Das Skript wird im Simulationsordner platziert:

* eine CSV-Datei namens [extracted fluxes.csv (download)](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/extracted_fluxes.csv) und
* ein Diagramm der Flusskonvergenz (*flux-convergence.png*) über die Modellgrenzen hinweg (siehe {numref}`Fig. %s <steady-flux-convergence>`) zeigt qualitativ, dass die Flußmittel nach etwa 6000-7000 Zeitschritten Konvergenz erreichten.

```{figure} ../../img/telemac/flux-convergence.png
:alt: python telemac flux discharge convergence pythomac
:name: steady-flux-convergence

Flux Konvergenzdiagramm über die beiden Grenzen der trocken-initialisierten stationären Telemac2d-Simulation mit einer Gesamtsimulationszeit von Zeitschritten Sekunden, erstellt mit der pythomac.extract fluxes() Funktion.
```

(tm-calculate-convergence)=
## Konvergence identifizieren

Um zu testen, ob und wann die Flußmittel konvergiert werden, verfolgen wir das relative Flussungleichgewicht für jeden Zeitschritt $t$ als:

```{math}
:label: error_rate
Es handelt sich dabei um ein System, bei dem es sich um ein Produkt handelt.
```

where $Q_{i,t}$ and $Q_{j,t}$ are the outflow and inflow fluxes across the model boundaries at timestep $t$, respectively. The flux magnitudes $|\cdot|$ are used because Telemac reports boundary fluxes with a sign (inflow positive, outflow negative); mass balance then corresponds to $|Q_{i,t}| = |Q_{j,t}|$, so that $\varepsilon_{t} \to 0$ at convergence, and normalizing by the inflow $|Q_{j,t}|$ makes $\varepsilon_{t}$ dimensionless. In a stable steady simulation, the ratio of consecutive flux imbalances should converge toward a convergence constant $c_{\varepsilon}$ equal to unity with increasing time:

```{math}
:label: error_lim
In den Warenkorb
```

Die Kombination der Konvergenzrate (oder Bestellung) $\iota$ und der Konvergenzkonstante $c_{\varepsilon}$:

* lineare Konvergenz, wenn $\iota$ = 1 ** und**$c_{\varepsilon} \in ]0, 1[$
* langsam *sublinear* Konvergenz, wenn $\iota$ = 1 ** und**$c_{\varepsilon}$ = 1
* schnelle *superlinear* Konvergenz, wenn $\iota$ > 1 ** und ** $c_{\varepsilon} \in ]0, 1]$
* Divergenzkonvergenz, wenn$\iota$ = 1 ** und**$c_{\varepsilon}$ > 1; ** oder*$\iota$ < 1

````{aside} Calculate $\varepsilon_{t+1}$

Um $\varepsilon_{t+1}$ (`epsilon_t1`) von $\varepsilon_{t}$ (`epsilon_t0`) zu berechnen, rollen wir einfach $\varepsilon_{t}$ um ein Element in Python:

```python
epsilon_t0 = epsilon[:-1]  # cut off last element
epsilon_t1 = epsilon[1:]   # cut off element zero
```
````

Um den Zeitschritt zu bestimmen, bei dem eine stetige Simulation als stabiler Zustand betrachtet werden kann, möchten wir beobachten, wann $\iota$ = 1 und $c_{\varepsilon}$ = 1 die sublineare Konvergenz angeben. Das heißt, wir suchen den Zeitschritt $t$, über den jeder zusätzliche Zeitschritt $t+1$ nur unwesentlich die Modellpräzision verbessert (lesen Sie mehr über den Begriff *insignificant* in der {ref}`below section <tm-target-conv>`). Unter der Annahme, dass die Modellkonvergenz in jeder Form vorliegt, können wir $c_{\varepsilon}$ = 1 setzen, um $\iota (t)$ in Abhängigkeit von $\varepsilon_{t}$ und $\varepsilon_{t+1}$ zu berechnen:

\begin{align}
\label{estimate convergence}
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(c {\varepsilon} ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
\iota(t) &= \log {\varepsilon {t}\varepsilon {t+1} &
(Ausrichtung)

Diese Gleichung kann in einer Python-Funktion wie folgt implementiert werden:


```python
import numpy as np
import pandas as pd


def calculate_convergence(Q_in, Q_out, conv_constant=1.):
    # relative flux imbalance epsilon_t = ||Q_in| - |Q_out|| / |Q_in|; the magnitudes |.|
    #   are needed because Telemac reports outflow negative, so that balance -> epsilon -> 0
    epsilon = np.abs(np.abs(Q_in) - np.abs(Q_out)) / np.abs(Q_in)
    # derive epsilon at t and t+1
    epsilon_t0 = epsilon[:-1]  # cut off last element
    epsilon_t1 = epsilon[1:]   # cut off element zero
    # return the relative imbalance and the convergence rate iota as a pandas DataFrame
    return pd.DataFrame({
        "Relative imbalance": epsilon_t1,
        "Convergence rate": np.emath.logn(epsilon_t0, epsilon_t1) / conv_constant,
    })
```

````{admonition} Also this function is available in pythomac
:class: tip

```python
from pythomac import calculate_convergence
```
````

Um $\iota (t)$ (Python variabler Name: `iota_t`) mit der obigen Funktion zu berechnen, ändern Sie die *example flux convergence.py* Python Script:

```python
# example_flux_convergence.py

# ...
# add to header (alternatively copy-paste the above function into this script):
from pythomac import calculate_convergence

# calculate fluxes_df (see above code block)
fluxes_df = [...]

# calculate iota (t) with the calculate_convergence function
iota_t = calculate_convergence(
    fluxes_df["Fluxes Boundary 1"][1:],  # remove first zero-entry
    fluxes_df["Fluxes Boundary 2"][1:],  # remove first zero-entry
)
```

The resulting convergence rate $\iota (t)$ is plotted in {numref}`Fig. %s <tm-convergence-rate>` for the {ref}`steady 2d tutorial <telemac2d-steady>`, with the modified printout periods of `50` seconds and a total simulation time of `10000` seconds.

```{figure} ../../img/telemac/convergence-rate.png
:alt: convergence rate fluxes telemac boundaries
:name: tm-convergence-rate

Die Konvergenzrate $\iota$ als Funktion 10000 Simulations-Zeitschritte der stationären 2d-Simulation.
```

(tm-target-conv)=
## Abwechslungsreiche Simulationszeit

Um die Rechenzeit zu sparen, interessieren wir uns für den Zeitschritt, in dem die Zu- und Abflussströme konvergiert werden. Die in {numref}`Fig. %s <steady-flux-convergence>` aufgetragenen Flußmittel und die Konvergenzrate in {numref}`Fig. %s <tm-convergence-rate>` deuten qualitativ darauf hin, dass die Simulation nach etwa 6000 Sekunden stabil war (Zeitschritte). Die Stöße in beiden Figuren nach 4000 Zeitschritten geben gut an, dass der Fluss "Wellen" aus den vor- und nachgelagerten Grenzen kommt (siehe {ref}`animation in the steady 2d tutorial <telemac-flow-convergence-gif>`). Erst danach hat sich die Konvergenz gesetzt.

Die Definition der Konvergenz kann subjektiv sein. Um die Rechenzeit zu sparen, suchen wir nach dem kleinsten Zeitschritt $t$, über den das relative Flussungleichgewicht $\varepsilon_{t}$ (Equation {eq}`error_rate`) dauerhaft unter einer Zieltoleranz $\varepsilon_{tar}$ bleibt. Toleranzen von $\varepsilon_{tar}$ = 10$^{-4}$ sind für die Vorabkalibrierung in der Regel zulässig, während Validierung und Hotstart-Initialisierung kleinere Werte (10$^{-6}$ oder kleiner) garantieren. Wie {numref}`Fig. %s <tm-convergence-rate>` illustriert, kann das Ungleichgewicht kurz unter die Toleranz fallen und nach etwa 4000 Zeitschritten wieder ansteigen, wenn die vorgeschaltete "Welle" über die nachgeschaltete Grenze rollt; nur die letzte Dauerüberschreitung zählt. Deshalb wollen wir eine algorithmische Umsetzung, die den letzten Zeitschritt erkennt, an dem $\varepsilon_{t} \geq \varepsilon_{tar}$ den nächsten als Konvergenzzeit nimmt. Zu diesem Zweck können wir die oben gestartete *example flux convergence.py* hinzufügen. Python Script der folgende Code:

```python
# example_flux_convergence.py

# ...

# calculate fluxes_df (see above code block)
fluxes_df = [...]

# calculate iota_t with calculate_convergence (also returns a "Relative imbalance" column)
iota_t = [...]

# define a desired target tolerance (epsilon_tar) for the relative flux imbalance
target_convergence_precision = 1.0E-4

# get the relative flux imbalance epsilon_t (Delta_Q) from calculate_convergence
relative_imbalance = iota_t["Relative imbalance"].to_numpy()

# find the index of the last element that still exceeds the target tolerance and add +1
#   (i.e., the first element from which the imbalance stays permanently below the tolerance)
below_tolerance = relative_imbalance < target_convergence_precision
idx = np.flatnonzero(~below_tolerance)[-1] + 1

# print the timestep at which the desired convergence was achieved to the console
printout_period_in_cas = 50  # the printout period defined in the cas file
print("The simulation converged after {0} simulation seconds ({1}th printout).".format(
        str(printout_period_in_cas * idx), str(idx)))
```

```  
The simulation converged after 6000 simulation seconds (120th printout).
```

````{admonition} Bolster your code
:class: tip

Der Code zur Berechnung des Zeitschritts, bei dem ein Zielkonvergenzniveau erreicht wurde, wird auch in der `get_convergence_time()`-Funktion in `pythomac` umgesetzt:

```python
from pythomac import get_convergence_time
```

A full implementation with also a convenient way for retrieving the `printout_period_in_cas` variable can be found in [this version of example_flux_convergence.py](https://github.com/hydro-informatics/pythomac/blob/main/example_flux_convergence.py) with documentation on [https://pythomac.readthedocs.io](https://pythomac.readthedocs.io/en/latest/convergence.html).
````

Nun, da Sie wissen, wann Ihre Telemac-Simulation zufriedenstellend konvergiert, können Sie den `NUMBER OF TIME STEPS`-Parameter in der `.cas`Lenkdatei reduzieren, zum Beispiel:

```fortran
/ steady2d-conv.cas
TIME STEP : 1.
NUMBER OF TIME STEPS : 6000
GRAPHIC PRINTOUT PERIOD : 50
LISTING PRINTOUT PERIOD : 50
```

## Fehlerbehebung Instabilitäten & Divergenz

Wenn eine stetige Simulation niemals die Stabilität von Flußmitteln oder sogar Flussdivergenz erreicht, stellen Sie sicher, dass alle Grenzen nach dem Spotlight-Bereich auf {ref}`boundary conditions <tm-foc-bc>` robust definiert sind und einen Blick auf den Workflow im nächsten Abschnitt auf {ref}`mass conservation <tm-foc-mass>` haben.
