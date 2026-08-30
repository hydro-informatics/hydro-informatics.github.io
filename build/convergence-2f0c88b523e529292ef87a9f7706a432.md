---
description: Quantitative convergence analysis for TELEMAC simulations using mass-balance output and Python, covering flux diagnostics and cumulative flowrate verification for reliable river models.
---

(tm-convergence)=
# Convergence (Quantitative)

````{admonition} Requirements
:class: important, dropdown

* Complete the {ref}`Telemac steady 2d tutorial <telemac2d-steady>` (or an equivalent steady simulation).
* The steering (`.cas`) file must contain the keywords `MASS-BALANCE : YES` and/or `PRINTING CUMULATED FLOWRATES : YES`, which cause TELEMAC to report the mass fluxes across the liquid boundaries in the listing.
* The TELEMAC simulation must have been executed with the `-s` flag (details below):

```fortran
telemac2d.py [STUDY-NAME].cas -s
```

* A Python (&geq; 3.9) installation with the `numpy`, `pandas`, and `matplotlib` libraries ({ref}`see the Python installation guide <install-python>`); `flusstools` is not required.

**All simulation files used in this tutorial can be downloaded from the [hydro-informatics/telemac repository on GitHub](https://github.com/hydro-informatics/telemac/tree/main/steady2d-tutorial) (see details below).**
````

```{admonition} Goals & purpose
:class: note

This chapter presents a quantitative procedure for verifying the flux convergence of a **steady** TELEMAC simulation and for determining the minimum simulation duration (`NUMBER OF TIME STEPS`) required to attain a mass-balanced state. Such verification is recommended before a steady result is used to hotstart an {ref}`unsteady <chpt-unsteady>` or a {ref}`morphodynamic (sediment transport) <gaia-basics>` simulation, because calibrating or continuing from a non-converged state propagates a transient bias into all subsequent computations. The same procedure may also be applied to compare the travel times of flood waves between an upstream and a downstream boundary.

For remedies to a non-converging model, refer to the {ref}`spotlight chapter on mass conservation <tm-foc-mass>` and verify that the {ref}`liquid boundaries are well defined <tm-foc-bc>`.
```

This chapter uses the simulation files from the {ref}`Telemac steady 2d tutorial <telemac2d-steady>`, with a modified definition of the time step and printout periods:

```fortran
/ steady2d-conv.cas
TIME STEP : 1.
NUMBER OF TIME STEPS : 10000
GRAPHIC PRINTOUT PERIOD : 50
LISTING PRINTOUT PERIOD : 50
```

In addition, the simulation was re-executed with the `-s` flag, which writes the complete listing to a file named `[FILE-NAME].cas_YEAR-MM-DD-HHhMMminSSs.sortie` in the simulation directory:

```fortran
telemac2d.py steady2d-conv.cas -s
```

Both the steering `.cas` and the `.sortie` files can be downloaded from the hydro-informatics.com repositories:

* [download steady2d-conv.cas](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/steady2d-conv.cas)
* [download steady2d-conv.cas_2023-07-26-18h41min26s.sortie](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/steady2d-conv.cas_2023-07-26-18h41min26s.sortie)

(tm-flux-convergence)=
## Extract and Check Flux Data

```{admonition} Alternative: use control sections

This section derives the flux (flow) convergence directly from the TELEMAC listing with Python. Alternatively, boundary fluxes can be extracted by {ref}`defining control sections (read more in the unsteady tutorial) <tm-control-sections>`.
```

The TELEMAC Jupyter notebook templates (*HOMETEL/notebooks/* > *data_manip/extraction/\*.ipynb* or *workshops/exo_fluxes.ipynb*) provide guidance for extracting data from simulation results; however, the templates do not constitute a directly applicable framework for assessing mass convergence at the boundaries as a function of `NUMBER OF TIME STEPS`. For this purpose, hydro-informatics.com maintains the lightweight Python package [pythomac](https://pythomac.readthedocs.io) (version &geq; 3.0.0 is described herein). The package requires only `numpy`, `pandas`, and `matplotlib` ({ref}`see the Python installation guide <install-python>`) and runs outside the TELEMAC Python environment. Two installation options are available:

`````{tab-set}
````{tab-item} pip-install pythomac (recommended)

Install the *pythomac* package from the Python Package Index:

```
pip install pythomac
```
````

````{tab-item} editable install from source

For development purposes, clone the *pythomac* repository from [GitHub](https://github.com/hydro-informatics/pythomac) and install it in editable mode:

```
git clone https://github.com/hydro-informatics/pythomac.git
pip install -e pythomac
```

Note that since version 3.0.0, *pythomac* is a regular Python package with in-package imports; copying the `pythomac/pythomac/` folder next to a simulation (the pre-3.0 workflow) is no longer supported.
````
`````

The central function is `pythomac.extract_fluxes()`. It locates the most recent `.sortie` listing next to the steering file, parses the volume balance and the signed flux printed for every liquid boundary at each listing printout (both the classical `THERE IS n LIQUID BOUNDARIES` and the TELEMAC v9 `NUMBER OF LIQUID BOUNDARIES:` listing formats are recognized), and writes into the simulation directory:

* `extracted-fluxes.csv` - the time series of the volume in the domain and of the flux across every liquid boundary; and
* `flux-convergence.png` - a plot of the flux magnitudes over simulation time (optional, `plotting=True`).

The function returns the extracted series as a `pandas.DataFrame` indexed by simulation time; the working directory of the calling process is not modified. The implementation can be inspected in [flux_analyst.py on GitHub](https://github.com/hydro-informatics/pythomac/blob/main/pythomac/flux_analyst.py), and the complete API documentation is available at [https://pythomac.readthedocs.io](https://pythomac.readthedocs.io).

To apply the function, copy the following code into a new Python script called, for instance, `example_flux_convergence.py`, located in the directory where the dry-initialized steady2d simulation ran (or [download example_flux_convergence.py](https://github.com/hydro-informatics/pythomac/blob/main/example_flux_convergence.py)):

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

Run the Python script from a terminal (or Anaconda Prompt) in the simulation directory:

```
python example_flux_convergence.py
```

The script places in the simulation folder:

* the CSV file [extracted-fluxes.csv (download)](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/extracted_fluxes.csv); and
* the flux-convergence plot (*flux-convergence.png*) across the model boundaries (see {numref}`Fig. %s <steady-flux-convergence>`), which indicates qualitatively that the fluxes approached convergence after approximately 6000-7000 time steps.

```{figure} ../../img/telemac/flux-convergence.png
:alt: python telemac flux discharge convergence pythomac
:name: steady-flux-convergence

Flux magnitudes across the two liquid boundaries of the dry-initialized steady Telemac2d simulation over the simulated time, produced with the pythomac.extract_fluxes() function.
```

(tm-calculate-convergence)=
## Identify Convergence

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

The combination of the convergence rate (or order) $\iota$ and the convergence constant $c_{\varepsilon}$ indicates:

* linear convergence if $\iota$ = 1 **and** $c_{\varepsilon} \in ]0, 1[$;
* slow *sublinear* convergence if $\iota$ = 1 **and** $c_{\varepsilon}$ = 1;
* fast *superlinear* convergence if $\iota$ > 1 **and** $c_{\varepsilon} \in ]0, 1]$; and
* divergence if $\iota$ = 1 **and** $c_{\varepsilon}$ > 1, **or** $\iota$ < 1.

````{aside} Calculate $\varepsilon_{t+1}$

$\varepsilon_{t+1}$ (`epsilon_t1`) is obtained from $\varepsilon_{t}$ (`epsilon_t0`) by shifting the series by one element:

```python
epsilon_t0 = epsilon[:-1]  # cut off last element
epsilon_t1 = epsilon[1:]   # cut off element zero
```
````

The time at which a steady simulation may be considered to have attained a stable state is identified by the onset of sublinear convergence ($\iota$ = 1 and $c_{\varepsilon}$ = 1); that is, the time $t$ beyond which each additional step $t+1$ improves the model precision only insignificantly (the term *insignificant* is quantified in the {ref}`section below <tm-target-conv>`). Under the assumption that the model converges in some form, setting $c_{\varepsilon}$ = 1 yields $\iota(t)$ as a function of $\varepsilon_{t}$ and $\varepsilon_{t+1}$:

\begin{align}
\label{estimate_convergence}
\frac{\varepsilon_{t+1}}{\varepsilon^{\iota(t)}_{t}} &=c_{\varepsilon} & \Leftrightarrow \\
\iota(t) &=  \frac{1}{c_{\varepsilon}} \cdot \log_{\varepsilon_{t}}\varepsilon_{t+1} & \overbrace{\Longleftrightarrow }^{c_{\varepsilon} = 1}\\
\iota(t) &=  \log_{\varepsilon_{t}}\varepsilon_{t+1} &
\end{align}

These relations are implemented in the `pythomac.calculate_convergence()` function, which returns a `pandas.DataFrame` with the columns `"Relative imbalance"` ($\varepsilon_{t+1}$, Equation {eq}`error_rate`) and `"Convergence rate"` ($\iota(t)$), indexed by simulation time. Its core reads:

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

To compute $\iota(t)$ (Python variable name: `iota_t`) with the above function, amend the *example_flux_convergence.py* Python script as follows:

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
## Derive Optimum Simulation Time

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

With the convergence time established, the `NUMBER OF TIME STEPS` keyword in the `.cas` steering file can be reduced accordingly, for example:

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

## Troubleshoot Instabilities & Divergence

If a steady simulation fails to attain stable fluxes, or if the fluxes diverge, verify that all boundaries are robustly defined according to the spotlight section on {ref}`boundary conditions <tm-foc-bc>`, and consult the workflow in the section on {ref}`mass conservation <tm-foc-mass>`.
