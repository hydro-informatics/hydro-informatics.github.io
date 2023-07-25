(tm-convergence)=
# Convergence (Quantitative)

```{admonition} Requirements

* Complete the {ref}`Telemac steady 2d tutorial <telemac2d-steady>` (or similar).
* An installation of Python along with the `numpy`, `pandas`, and `matplotlib` libraries ({ref}`see the Python installation guide <install-python>`), even though `flusstools` is not required).
```

The convergence study featured in this study requires that the `MASS-BALANCE : YES` and/or `PRINTING CUMULATED FLOWRATES : YES`  keywords were used in the steering (`.cas`) file to print mass fluxes across liquid boundaries in the Terminal. Additionally, the simulation must have run with the `-s` flag, which saves the simulation state in a file called similar to `[FILE-NAME].cas_YEAR-MM-DD-HHhMMminSSs.sortie`.

```fortran
telemac2d.py steady2d.cas -s
```

## Extract Flux Data

The Telemac notebook examples (*HOMETEL/notebooks/* > *data_manip/extraction/\*.ipynb* or *workshops/exo_fluxes.ipynb*) provide some guidance for extracting data from simulation results, which can be tweaked into a generally applicable framework for observing mass convergence at the boundaries as a function of the defined timestep. However, the Python examples do not work straight forward, which is why the following paragraphs describe a simple, minimalist Python tweak called [pythomac](https://pythomac.readthedocs.io), developed by hydro-informatics.com. There are three options for working with our codes, all of them require having an installation of Python along with the `numpy`, `pandas`, and `matplotlib` libraries ({ref}`see the Python installation guide <install-python>`):

`````{tab-set}
````{tab-item} pip-install pythomac

Pip-install the *pythomac* package:

```
pip install pythomac
```
````

````{tab-item} clone pythomac

Clone the *pythomac* repository from [github.com](https://github.com/hydro-informatics/pythomac):

```
git clone https://github.com/hydro-informatics/pythomac.git
```

Copy-past the folder `pythomac/pythomac/` into your simulation directory. That is, make sure that the Python script `/dir/to/simulation/pythomac/extract_fluxes.py` (among others) is correctly located, next to `/dir/to/simulation/steady2d.cas`.
````

````{tab-item} download pythomac as zip

Download a zipped archive of the *pythomac* repository from [github.com (right-click here > save as...)](https://github.com/hydro-informatics/pythomac/archive/refs/heads/main.zip). Open the zip archive > open `pythomac-main`, and extract the contents of the `pythomac` folder (i.e., `pythomac-main/pythomac/`) into your simulation directory. That is, make sure that the Python script `/dir/to/simulation/pythomac/extract_fluxes.py` (among others) is correctly located, next to `/dir/to/simulation/steady2d.cas`.
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

@author: Sebastian Schwindt (July 2023)
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

Detailed instructions for using pythomac and its dependencies (`numpy`, `pandas`, and `matplotlib`) can be found at [https://pythomac.readthedocs.io](https://pythomac.readthedocs.io). To use the `extract_fluxes` functions from `pythomac.extract_fluxes`, copy the following code into a new Python script called, for instance, `steady2dconv.py` in the directory where the dry-initialized steady2d simulation ran ([download code here](https://github.com/hydro-informatics/pythomac/blob/main/example.py)):


```python
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

Run the Python script from Terminal (or Anaconda Prompt) as follows (make sure to `cd` into the simulation directory):

```
python steady2dconv.py
```

The script will have placed in the simulation folder:

* a CSV file called [extracted_fluxes.csv (download)](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/extracted_fluxes.csv), and
* a plot of flux convergences across the model boundaries (see {numref}`Fig. %s <steady-flux-convergence>`) show that the fluxes reached convergence after approximately 7000 timesteps.

```{figure} ../../img/telemac/steady-flux-convergence.png
:alt: python telemac flux discharge convergence pythomac
:name: steady-flux-convergence

Flux convergence plot across the two boundaries of the dry-initialized steady Telemac2d simulation, created with the pythomac.extract_fluxes() function.
```

(tm-calculate-convergence)=
## Identify Convergence

To test if the fluxes converge, we can calculate the differences between fluxes for each timestep $t$ as:

```{math}
:label: error_rate
\varepsilon_{t} = \|Q_i - Q_j\|
```

where $Q_i$ and $Q_j$ are the sum of the outflow and inflow fluxes across the model boundaries, respectively. The difference between inflows and outflows should converge to zero in a stable simulation; that is:

```{math}
:label: error_lim
\lim_{t\to \infty} \frac{\varepsilon_{t+1}}{\varepsilon^{\iota}_{t}} < c_{\varepsilon}
```

where $\iota$ is the convergence order, and $c_{\varepsilon}$ is a convergence constant indicating:

* linear convergence if $\iota$ = 1 **and** $c_{\varepsilon} \in ]0, 1[$
* slow *sublinear* convergence if $\iota$ = 1 **and** $c_{\varepsilon}$ = 1
* fast *superlinear* convergence if $\iota$ > 1 **and** $c_{\varepsilon} \in ]0, 1]$
* divergence convergence if $\iota$ = 1 **and** $c_{\varepsilon}$ > 1; **or** $\iota$ < 1

To determine the timestep at which a steady simulation can be considered to have reached a stable state, we want to observe when $\iota$ = 1 and $c_{\varepsilon}$ = 1 indicate sublinear convergence. That is, we look for the timestep $t$ above which each additional timestep $t+1$ does not significantly improve the model results. For this purpose we want to estimate $\iota$ by means of the slope of the convergence curve (Equation {eq}`error_lim`) as follows, :

```{math}
:label: estimate_convergence
\iota \approx \left[\ln\|\ln(\varepsilon_{t+1}/\varepsilon_t)\|\right]' = \left[\ln \|\ln \varepsilon_{t+1} - \ln \varepsilon_t\|\right]'

```

This approximation equation can be implemented into a Python function as follows: 


```python
def approx_convergence(series_1, series_2):
    """
    to do
    """
    epsilon = np.array(abs(series_1 - series_2))
```


## Troubleshoot Instabilities & Divergence

If a steady simulation never reaches stability of fluxes, or even flux divergence, make sure that all boundaries are robustly defined according to the spotlight section on {ref}`boundaries conditions <tm-foc-bc>`, and have a look at the workflow on mass balance in next section on the {ref}`optimization of mass conservation <tm-foc-mass>`.
