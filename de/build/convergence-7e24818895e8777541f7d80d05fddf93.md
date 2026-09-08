---
description: Quantitative Konvergenzanalyse für TELEMAC-Simulationen mit Massenbilanz-Output und Python, einschließlich Flussdiagnose und Überprüfung der kumulativen Durchflussrate für zuverlässige Flussmodelle.
---

(tm-convergence)=
# Konvergenz (quantitativ)

````{admonition} Requirements
:class: important, dropdown

* Complete the {ref}`Telemac steady 2d tutorial <telemac2d-steady>` (or an equivalent steady simulation).
* Die Steuerungsdatei (`.cas`) muss die Schlüsselwörter `MASS-BALANCE : YES` und/oder `PRINTING CUMULATED FLOWRATES : YES` enthalten, die TELEMAC veranlassen, die Massenflüsse über die Flüssigkeitsgrenzen in der Auflistung zu melden.
* Die TELEMAC-Simulation muss mit dem `-s`-Flag ausgeführt worden sein (Details unten):

```fortran
telemac2d.py [STUDY-NAME].cas -s
```

* Eine Python-Installation (&geq; 3.9) mit den Bibliotheken `numpy`, `pandas` und `matplotlib` ({ref}`see the Python installation guide <install-python>`); `flusstools` ist nicht erforderlich.

** Alle in diesem Tutorial verwendeten Simulationsdateien können aus dem [Hydroinformatik / Telemac-Repository unter GitHub](https://github.com/hydro-informatics/telemac/tree/main/steady2d-tutorial) (siehe Details unten)] heruntergeladen werden.**
````

```{admonition} Goals & purpose
:class: note

This chapter presents a quantitative procedure for verifying the flux convergence of a **steady** TELEMAC simulation and for determining the minimum simulation duration (`NUMBER OF TIME STEPS`) required to attain a mass-balanced state. Such verification is recommended before a steady result is used to hotstart an {ref}`unsteady <chpt-unsteady>` or a {ref}`morphodynamic (sediment transport) <gaia-basics>` simulation, because calibrating or continuing from a non-converged state propagates a transient bias into all subsequent computations. The same procedure may also be applied to compare the travel times of flood waves between an upstream and a downstream boundary.

Für Abhilfen für ein nicht-konvergierendes Modell, beziehen Sie sich auf die {ref}`spotlight chapter on mass conservation <tm-foc-mass>` und überprüfen Sie, dass die {ref}`liquid boundaries are well defined <tm-foc-bc>`.
```

This chapter uses the simulation files from the {ref}`Telemac steady 2d tutorial <telemac2d-steady>`, with a modified definition of the time step and printout periods:

```fortran
/ steady2d-conv.cas
TIME STEP : 1.
NUMBER OF TIME STEPS : 10000
GRAPHIC PRINTOUT PERIOD : 50
LISTING PRINTOUT PERIOD : 50
```

Darüber hinaus wurde die Simulation mit dem Flag `-s` erneut ausgeführt, das die vollständige Auflistung in eine Datei namens `[FILE-NAME].cas_YEAR-MM-DD-HHhMMminSSs.sortie` in das Simulationsverzeichnis schreibt:

```fortran
telemac2d.py steady2d-conv.cas -s
```

Sowohl die Steuerung `.cas` als auch die `.sortie`-Dateien können aus den hydro-informatics.com-Repositories heruntergeladen werden:

* [Download steady2d-conv.cas](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/steady2d-conv.cas)]
* [Download steady2d-conv.cas 2023-07-26-18h41min26s.sortie](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/steady2d-conv.cas_2023-07-26-18h41min26s.sortie)]

(tm-flux-convergence)=
## Extrahieren und Überprüfen von Flussdaten

```{admonition} Alternative: use control sections

This section derives the flux (flow) convergence directly from the TELEMAC listing with Python. Alternatively, boundary fluxes can be extracted by {ref}`defining control sections (read more in the unsteady tutorial) <tm-control-sections>`.
```

Die TELEMAC Jupyter Notebook-Vorlagen (*HOMETEL/notebooks/* > *data manip/extraction/\*.ipynb* oder *workshops/exo fluxes.ipynb*) bieten Anleitungen zum Extrahieren von Daten aus Simulationsergebnissen; die Vorlagen stellen jedoch keinen direkt anwendbaren Rahmen für die Bewertung der Massenkonvergenz an den Grenzen in Abhängigkeit von `NUMBER OF TIME STEPS` dar. Zu diesem Zweck unterhält hydro-informatics.com das leichte Python-Paket [pythomac](https://pythomac.readthedocs.io) (Version &geq; 3.0.0 wird hier beschrieben). Das Paket benötigt nur `numpy`, `pandas` und `matplotlib` ({ref}`see the Python installation guide <install-python>`) und läuft außerhalb der TELEMAC Python-Umgebung. Es stehen zwei Installationsoptionen zur Verfügung:

`````{tab-set}
````{tab-item} pip-install pythomac (recommended)

Installieren Sie das Paket *pythomac* aus dem Python Package Index:

```
pip install pythomac
```
````

````{tab-item} editable install from source

Zu Entwicklungszwecken klonen Sie das *pythomac*-Repository aus [GitHub](https://github.com/hydro-informatics/pythomac)] und installieren Sie es im editierbaren Modus:

```
git clone https://github.com/hydro-informatics/pythomac.git
pip install -e pythomac
```

Beachten Sie, dass *pythomac* seit Version 3.0.0 ein reguläres Python-Paket mit Paketimporten ist; das Kopieren des `pythomac/pythomac/`-Ordners neben einer Simulation (der Pre-3.0-Workflow) wird nicht mehr unterstützt.
````
`````

Die zentrale Funktion ist `pythomac.extract_fluxes()`. Es sucht die neueste `.sortie`-Liste neben der Steuerungsdatei, analysiert die Volumenbilanz und den signierten Fluss, der für jede Flüssigkeitsgrenze bei jedem Listenausdruck gedruckt wird (sowohl das klassische `THERE IS n LIQUID BOUNDARIES` als auch das TELEMAC v9 `NUMBER OF LIQUID BOUNDARIES:`Listing-Format werden erkannt) und schreibt in das Simulationsverzeichnis:

* `extracted-fluxes.csv` - die Zeitreihe des Volumens in der Domäne und des Flusses über jede Flüssigkeitsgrenze; und
* `flux-convergence.png` - ein Diagramm der Flussgrößen über die Simulationszeit (optional, `plotting=True`).

The function returns the extracted series as a `pandas.DataFrame` indexed by simulation time; the working directory of the calling process is not modified. The implementation can be inspected in [flux_analyst.py on GitHub](https://github.com/hydro-informatics/pythomac/blob/main/pythomac/flux_analyst.py), and the complete API documentation is available at [https://pythomac.readthedocs.io](https://pythomac.readthedocs.io).

Um die Funktion anzuwenden, kopieren Sie den folgenden Code in ein neues Python-Skript mit dem Namen `example_flux_convergence.py`, das sich in dem Verzeichnis befindet, in dem die trocken-initialisierte steady2d-Simulation ausgeführt wurde (oder [download example flux convergence.py](https://github.com/hydro-informatics/pythomac/blob/main/example_flux_convergence.py)]):

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

```{admonition} Errors? Verify the simulation directory.
:class: error

A `print(simulation_dir)` statement in the above code block indicates whether the assigned path resolves to the directory that contains the steering and `.sortie` files. Adjust `simulation_dir` if the script resides at a different level relative to the simulation.
```

Führen Sie das Python-Skript von einem Terminal (oder Anaconda Prompt) im Simulationsverzeichnis aus:

```
python example_flux_convergence.py
```

Das Skript platziert sich im Simulationsordner:

* die CSV-Datei [extracted-fluxes.csv (Download)](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/extracted_fluxes.csv)] und
* das Fluss-Konvergenz-Plot (*flux-convergence.png*) über die Modellgrenzen hinweg (siehe {numref}`Fig. %s <steady-flux-convergence>`), das qualitativ anzeigt, dass sich die Flüsse nach etwa 6000-7000 Zeitschritten der Konvergenz näherten.

```{figure} ../../img/telemac/flux-convergence.png
:alt: python telemac flux discharge convergence pythomac
:name: steady-flux-convergence

Flussgrößen über die beiden Flüssigkeitsgrenzen der trockeninitialisierten stationären Telemac2d-Simulation über die simulierte Zeit, erzeugt mit der Funktion pythomac.extract fluxes().
```

(tm-calculate-convergence)=
## Identifizieren von Konvergenz

To assess whether and when the boundary fluxes converged, the relative flux imbalance is evaluated at every printout time $t$ as:

```{math}
:label: error_rate
\varepsilon_{t} = \frac{\left| |Q_{i,t}| - |Q_{j,t}| \right|}{|Q_{j,t}|}
```

where $Q_{i,t}$ and $Q_{j,t}$ = the outflow and inflow fluxes across the model boundaries at time $t$, respectively. The flux magnitudes $|\cdot|$ are required because TELEMAC reports boundary fluxes with a sign convention (inflow positive, outflow negative); mass balance therefore corresponds to $|Q_{i,t}| = |Q_{j,t}|$, so that $\varepsilon_{t} \to 0$ at convergence, and normalization by the inflow $|Q_{j,t}|$ renders $\varepsilon_{t}$ dimensionless. In a stable steady simulation, the ratio of consecutive flux imbalances approaches a convergence constant $c_{\varepsilon}$ equal to unity with increasing time:

```{math}
:label: error_lim
\lim_{t\to \infty} \frac{\varepsilon_{t+1}}{\varepsilon^{\iota}_{t}} = c_{\varepsilon}
```

Die Kombination der Konvergenzrate (oder Ordnung) $\iota$ und der Konvergenzkonstanten $c_{\varepsilon}$ zeigt an:

* lineare Konvergenz, wenn $\iota$ = 1 **und $c_{\varepsilon} \in ]0, 1[$
* langsame *sublineare* Konvergenz, wenn $\iota$ = 1 **und $c_{\varepsilon}$ = 1
* schnelle *superlineare* Konvergenz, wenn $\iota$ > 1 **und $c_{\varepsilon} \in ]0, 1]$ und
* Divergenz wenn $\iota$ = 1 **und $c_{\varepsilon}$ > 1, **oder $\iota$ < 1.

````{aside} Calculate $\varepsilon_{t+1}$

$\varepsilon_{t+1}$ (`epsilon_t1`) wird von $\varepsilon_{t}$ (`epsilon_t0`) erhalten, indem die Reihe um ein Element verschoben wird:

```python
epsilon_t0 = epsilon[:-1]  # cut off last element
epsilon_t1 = epsilon[1:]   # cut off element zero
```
````

Der Zeitpunkt, zu dem eine stationäre Simulation als stabil angesehen werden kann, wird durch den Beginn der sublinearen Konvergenz ($\iota$ = 1 und $c_{\varepsilon}$ = 1) identifiziert, dh der Zeitpunkt $t$, ab dem jeder weitere Schritt $t+1$ die Modellpräzision nur unwesentlich verbessert (der Begriff *unwesentlich* wird im {ref}`section below <tm-target-conv>` quantifiziert). Unter der Annahme, dass das Modell in irgendeiner Form konvergiert, ergibt die Einstellung $c_{\varepsilon}$ = 1 $\iota(t)$ als Funktion von $\varepsilon_{t}$ und $\varepsilon_{t+1}$:

\begin{align}
\label{estimate convergence}
\frac{\varepsilon {t+1}}{\varepsilon^{\iota(t)} {t}} &=c {\varepsilon} & \Leftrightarrow \\
\iota(t) &= \frac{1}{c {\varepsilon}} \cdot \log {\varepsilon {t}}\varepsilon {t+1} & \overbrace{\Longleftrightarrow }^{c {\varepsilon} = 1}\\\
\iota(t) &= \log {\varepsilon {t}}\varepsilon {t+1} &
\end{align}

Diese Beziehungen werden in der Funktion `pythomac.calculate_convergence()` implementiert, die ein `pandas.DataFrame` mit den Spalten `"Relative imbalance"` ($\varepsilon_{t+1}$, Gleichung {eq}`error_rate`) und `"Convergence rate"` ($\iota(t)$) zurückgibt, indiziert nach Simulationszeit. Sein Kern lautet:

```python
import numpy as np
import pandas as pd


def calculate_convergence(series_1, series_2, conv_constant=1.):
    # relative flux imbalance epsilon_t = ||Q_in| - |Q_out|| / |Q_in|; the magnitudes |.|
    #   are needed because Telemac reports outflow negative, so that balance -> epsilon -> 0
    epsilon = np.abs(np.abs(series_1) - np.abs(series_2)) / np.abs(series_1)
    # derive epsilon at t and t+1
    epsilon_t0 = epsilon[:-1]  # cut off last element
    epsilon_t1 = epsilon[1:]   # cut off element zero
    # return the relative imbalance and the convergence rate iota as a pandas DataFrame
    return pd.DataFrame({
        "Relative imbalance": epsilon_t1,
        "Convergence rate": np.emath.logn(epsilon_t0, epsilon_t1) / conv_constant,
    })
```

````{admonition} This function is available in pythomac
:class: tip

```python
from pythomac import calculate_convergence
```

The packaged implementation additionally accepts `cas_timestep` (the printout spacing in simulation seconds, used to scale the index) and `plot_dir` (if provided, a `convergence-rate.png` plot is written to that directory).
````

Um $\iota(t)$ (Python-Variablenname: `iota_t`) mit der obigen Funktion zu berechnen, ändern Sie die *beispiel flux convergence.py * Python Skript wie folgt:

```python
# example_flux_convergence.py

# ...
# add to header:
from pythomac import calculate_convergence

# calculate fluxes_df (see above code block)
fluxes_df = [...]

# back-calculate the printout spacing (in simulation seconds) from the flux index
timestep_in_cas = int(max(fluxes_df.index.values) / (len(fluxes_df.index.values) - 1))

# calculate iota (t) with the calculate_convergence function
iota_t = calculate_convergence(
    series_1=fluxes_df["Fluxes Boundary 1"][1:],  # remove first zero-entry
    series_2=fluxes_df["Fluxes Boundary 2"][1:],  # remove first zero-entry
    cas_timestep=timestep_in_cas,
    plot_dir=simulation_dir,
)
```

The resulting convergence rate $\iota(t)$ is plotted in {numref}`Fig. %s <tm-convergence-rate>` for the {ref}`steady 2d tutorial <telemac2d-steady>` with the modified printout periods of `50` seconds and a total simulation time of `10000` seconds.

```{figure} ../../img/telemac/convergence-rate.png
:alt: convergence rate fluxes telemac boundaries
:name: tm-convergence-rate

The convergence rate $\iota$ as a function of the 10000 simulation time steps of the steady 2d simulation.
```

(tm-target-conv)=
## Ableitung der optimalen Simulationszeit

To economize computing time, the time step at which the inflow and outflow fluxes converged is of practical interest. The fluxes plotted in {numref}`Fig. %s <steady-flux-convergence>` and the convergence rate in {numref}`Fig. %s <tm-convergence-rate>` suggest qualitatively that the simulation stabilized after approximately 6000 seconds (time steps). The local extrema in both figures near 4000 time steps mark the interaction of the wetting fronts propagating from the upstream and downstream boundaries (see the {ref}`animation in the steady 2d tutorial <telemac-flow-convergence-gif>`); monotonic convergence sets in only thereafter.

Because a purely visual judgment of convergence is subjective, an objective criterion is adopted: the optimum simulation length is the smallest time $t$ beyond which the relative flux imbalance $\varepsilon_{t}$ (Equation {eq}`error_rate`) remains permanently below a target tolerance $\varepsilon_{tar}$. Tolerances of $\varepsilon_{tar}$ = 10$^{-4}$ are typically acceptable for preliminary calibration runs, whereas validation and hotstart-initialization runs warrant smaller values (10$^{-6}$ or smaller). As {numref}`Fig. %s <tm-convergence-rate>` illustrates, the imbalance may temporarily drop below the tolerance and rise again (here near 4000 time steps, when the upstream front passes the downstream boundary); only the final, permanent crossing is relevant. The algorithmic implementation therefore detects the last time at which $\varepsilon_{t} \geq \varepsilon_{tar}$ and designates the subsequent printout as the convergence time. This criterion is implemented in `pythomac.get_convergence_time()`, which returns the printout index of the permanent crossing, or `numpy.nan` (with a warning) if the tolerance is never sustained. Amend the *example_flux_convergence.py* script as follows:

```python
# example_flux_convergence.py

# ...
# add to header:
from pythomac import get_convergence_time

# calculate fluxes_df and iota_t (see above code blocks)
fluxes_df = [...]
iota_t = [...]

# identify the printout index from which the relative flux imbalance stays
# permanently below the target tolerance (epsilon_tar)
convergence_time_iteration = get_convergence_time(
    relative_imbalance=iota_t["Relative imbalance"],
    convergence_precision=1.0E-4
)

if not str(convergence_time_iteration).lower() == "nan":
    print("The simulation converged after {0} simulation seconds ({1}th printout).".format(
            str(timestep_in_cas * convergence_time_iteration), str(convergence_time_iteration)))
```

```  
The simulation converged after 6000 simulation seconds (120th printout).
```

````{admonition} Full example script
:class: tip

A complete implementation, including the retrieval of the `timestep_in_cas` variable and the export of the convergence table to `convergence-rate.csv`, is provided in [example_flux_convergence.py](https://github.com/hydro-informatics/pythomac/blob/main/example_flux_convergence.py), with documentation at [https://pythomac.readthedocs.io](https://pythomac.readthedocs.io/en/latest/convergence.html).
````

Mit der festgelegten Konvergenzzeit kann das Schlüsselwort `NUMBER OF TIME STEPS` in der Steuerungsdatei `.cas` entsprechend reduziert werden, zum Beispiel:

```fortran
/ steady2d-conv.cas
TIME STEP : 1.
NUMBER OF TIME STEPS : 6000
GRAPHIC PRINTOUT PERIOD : 50
LISTING PRINTOUT PERIOD : 50
```

```{admonition} Variable time steps require a duration-based criterion
:class: note

If the steering file activates `VARIABLE TIME-STEP : YES` (a CFL-controlled adaptive step), the number of time steps is not known a priori and `NUMBER OF TIME STEPS` does not bound the simulated time; the run is then capped by `DURATION`, and the convergence time identified above should be interpreted in simulation seconds rather than in time steps.
```

## Fehlersuche bei Instabilitäten und Divergenzen

If a steady simulation fails to attain stable fluxes, or if the fluxes diverge, verify that all boundaries are robustly defined according to the spotlight section on {ref}`boundary conditions <tm-foc-bc>`, and consult the workflow in the section on {ref}`mass conservation <tm-foc-mass>`.
