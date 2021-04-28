# One-dimensional (1d) Cross-section Averaged Sediment Transport

```{admonition} Goals
This exercise features the application of the Meyer-Peter & Müller (1948) bed load transport formulae to a valid application: 1D, cross-section averaged hydraulics. Write object-oriented code with custom classes for tailored interactions with *xlsx* workbooks. The homework involves using built-in methods of *pandas* data frames and plotting.
```

```{admonition} Requirements
*Python* libraries: *numpy* and *pandas*. Read and understand the [data handling with *numpy* and *pandas*](../python-basics/pynum), as well as [object orientation](../python-basics/classes).
```

Get ready by cloning the exercise repository:

```
git clone https://github.com/Ecohydraulics/Exercise-SedimentTransport.git
```

```{figure} https://github.com/Ecohydraulics/media/raw/master/jpg/arbogne.jpg
:alt: arbogne Switzerland Fribourg
:name: arbogne

The Arbogne River in Switzerland (source: Sebastian Schwindt 2013).
```


## Theory

### 1d Cross-section Averaged Hydrodynamics
From the [stage-discharge (*Manning-Strickler* formula) exercise](https://github.com/Ecohydraulics/Exercise-ManningStrickler), we recall the formula to calculate the relationship between water depth *h* (incorporated in the hydraulic radius *R<sub>h</sub>*) and flow velocity *u*:
*u = 1/n · S<sub>e</sub><sup>1/2</sup> · R<sub>h</sub><sup>2/3</sup>*

where
* *n* is the [*Manning* coefficient](http://www.fsl.orst.edu/geowater/FX3/help/8_Hydraulic_Reference/Mannings_n_Tables.htm) in *fictional* units of (s/m<sup>1/3</sup>).
* *S<sub>e</sub>* is the hypothetical energy slope (m/m) and corresponds to the channel slope for steady, uniform flow conditions (non-existing in natural rivers).
* the hydraulic radius *R<sub>h</sub>* = *A / P*, where (for a trapezoidal cross-section):
    - the wetted (trapezoidal) cross-section area is *A = h · 0.5·(b + B) = h · (b + h·m)*;
    - the wetted perimeter of a trapezoid is *P = b + 2h·(m² + 1)<sup>1/2</sup>*;
    - *b* (channel base width) and *m* (bank slope) are illustrated in the figure below to calculate the depth-dependent water surface width *B*=*b+2·h·m*.


```{figure} https://github.com/Ecohydraulics/media/raw/master/png/flow-cs.png
:alt: 1d hydraulics parameters
:name: cs-sed
```

This exercise uses one-dimensional (1D) cross-section averaged hydraulic data produced with the US Army Corps of Engineers' [*HEC-RAS*](https://www.hec.usace.army.mil/software/hec-ras/) software, which solves the Manning-Strickler formula numerically for any flow cross-section shape. In this exercise, *HEC-RAS* provides the hydraulic data needed to determine the sediment transport capacity of a channel cross-section, although no explanations for creating, running, and exporting data from *HEC-RAS* models are given.

### Sediment transport

Fluvial sediment transport can be distinguished into two modes: (1) suspended load and (2) bed load (see figure below). Finer particles with a weight that can be carried by the fluid (water) are transported as suspended load. Coarser particles rolling, sliding, and jumping on the channel bed are transported as bed load. There is another type of transport, the so-called wash load, which is finer than the coarse bed load, but too heavy (large) to be transported in suspension ([Einstein 1950](http://dx.doi.org/10.22004/ag.econ.156389)).

```{figure} https://github.com/Ecohydraulics/media/raw/master/png/sediment-transport.png
:alt: 1d sediment transport
:name: transport
```

In the following, we will look at the bed load transport mode. In this case, a sediment particle located in or on the riverbed is mobilized by shear forces of the water as soon as they exceed a critical value (see figure below). In river hydraulics, the so-called dimensionless bed shear stress or *Shields* stress ([Shields 1936](http://resolver.tudelft.nl/uuid:61a19716-a994-4942-9906-f680eb9952d6) is often used as the threshold value for the mobilization of sediment from the riverbed. This exercise uses one of the dimensionless bed shear stress approaches and the next section provides more explanations.

```{figure} https://github.com/Ecohydraulics/media/raw/master/png/sediment-uptake.png
:alt: sediment uptake mobilization
:name: uptake
```



### The Meyer-Peter and Müller (1948) formula <a name="mpm"></a>

The [Meyer-Peter & Müller (1948)](http://resolver.tudelft.nl/uuid:4fda9b61-be28-4703-ab06-43cdc2a21bd7) formula for estimating bed load transport was published by Swiss researchers Eugen Meyer-Peter (founder of the famous [*Laboratory of Hydraulics, Hydrology and Glaciology (VAW)*](https://vaw.ethz.ch/en/) and Robert Müller. Their study began one year after the establishment of the *VAW* in 1931 when Robert Müller was appointed assistant to Eugen Meyer-Peter. The two scientists worked in collaboration with Henry Favre and Albert Einstein's son Hans Albert. In 1934, the laboratory published for the first time a formula for the calculation of bed load transport and its fundamental relationship between observed *&tau;<sub>x</sub>* and critical *&tau;<sub>x,cr</sub>* dimensionless bed shear stresses is used until today. The dimensionless bed load transport rate *&Phi;* according to [Meyer-Peter & Müller (1948)](http://resolver.tudelft.nl/uuid:4fda9b61-be28-4703-ab06-43cdc2a21bd7) is: <a name="phi"></a>

 *&Phi; &asymp; 8 · (&tau;<sub>x</sub> - &tau;<sub>x,cr</sub>)<sup>3/2</sup>*

where <a name="taux"></a>
* *&tau;<sub>x,cr</sub>* &asymp; 0.047 (up to 0.07 in mountain rivers), and
* *&tau;<sub>x</sub>* = *R<sub>h</sub> · S<sub>e</sub> / [(s - 1) · D<sub>char</sub>]*

The other parameters are:
* *s* &asymp; 2.68, the dimensionless ratio of sediment grain density *&rho;<sub>s</sub>* (&asymp; 2680 kg/m³) and water density *&rho;<sub>w</sub>* (&asymp; 1000 kg/m³);
* *D<sub>char</sub>*, the characteristic grain size in (m). It can be assumed that *D<sub>char</sub> &asymp; D<sub>84</sub>* (i.e., the grain diameter of which 84% of a sediment mixture is smaller) in line with the scientific literature (e.g., [Rickenmann and Recking 2011](https://doi.org/10.1029/2010WR009793)).

The *Meyer-Peter & Müller* formula applies (like any other sediment transport formula) only to certain rivers that have the following characteristics (range of validity):
* 0.4·10<sup>-3</sup>m < *D<sub>char</sub>* < 28.6·10<sup>-3<sup>m
* 10<sup>-4</sup>m < *Fr* < 639 (*Fr* denotes the dimensionless [*Froude* number](https://en.wikipedia.org/wiki/Froude_number)
* 0.0004 < *S<sub>e</sub>* < 0.02
* 0.0002 m³/(s·m) < *q* < 2.0 m³/(s·m) (*q* is the unit discharge, i.e., *q=Q/(0.5·(b + B)*)
* 0.25 < *s* < 3.2

The dimensionless expression for bed load *&Phi;* was used to enable information transfer between different channels across scales by preserving geometric, kinematic and dynamic similarity. The set of dimensionless parameters used results from  [Buckingham's *&Pi;* theorem](https://pint.readthedocs.io/en/stable/pitheorem.html).
Therefore, to add dimensions to *&Phi;*, it needs to be multiplied with the same set of parameters used for deriving the dimensionless expression from *Meyer-Peter & Müller*. Their set of parameters involves the characteristic grain size *D<sub>char</sub>*, the grain density *&rho;<sub>s</sub>*, and the gravitational acceleration *g*. Thus, the dimensional unit bed load is (in kg/s and meter width, i.e., kg/(s·m): <a name="qb"></a>

*q<sub>b</sub> = &Phi; · ((s-1) · g · D<sub>char</sub><sup>3</sup>)<sup>1/2</sup> · &rho;<sub>s</sub>*

The cross-section averaged bed load *Q<sub>b</sub>* (kg/s) is then:

*Q<sub>b</sub> = b<sub>eff</sub> · q<sub>b</sub> = b<sub>eff</sub> · &Phi; · [(s-1) · g · D<sub>char</sub><sup>3</sup>]<sup>1/2</sup> · &rho;<sub>s</sub>*

where *b<sub>eff</sub>* is the hydraulically active channel width of the flow cross-section (e.g., for a trapezoid *b<sub>eff</sub> = 0.5 · (b + B)*)


## Code

### Set the frame
The object-oriented code will use custom classes that we will call within a **`main.py`** script. Create the following **additional scripts**, which will contain the custom classes and functions to control logging.

* `fun.py` will contain logging functions.
* `hec.py` will contain a `HecSet` class to read hydraulic output data from *HEC-RAS* as structured objects.
* `grains.py` will contain a `GrainReader` class to read grain size class information as structured objects.
* `bedload.py` will contain the class `BedCore` with basic elements that most bed load formulae have in common.
* `mpm.py` will contain the class `MPM`, which inherits from `BedCore` and calculates bed load as above described (Meyer-Peter & Müller 1948).

We will create the classes and functions in the indicated scripts according to the following flow chart:

```{figure} https://github.com/Ecohydraulics/Exercise-SedimentTransport/raw/master/graphs/uml.png
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

### Logging functions
The `fun.py` script will contain two functions:

1. `start_logging` to setup logging formats and a log file name as described on the [debugging page](../python-basics/pypyerror.html#logging), and
1. `log_actions`, which is a function wrapper for the `main()` (`main.py`) functions to log script execution messages.

The `start_logging` function should look like this (change the log file name if desired):

```python
import logging


def start_logging():
    logging.basicConfig(filename="logfile.log", format="[%(asctime)s] %(message)s",
                        filemode="w", level=logging.DEBUG)
    logging.getLogger().addHandler(logging.StreamHandler()

```

The `log_actions` wrapper function follows the instructions from the [functions page](../python-basics/pypyfun.html#wrappers):

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


### Read grain size data

Sediment grain size classes (ranging from *D<sub>16</sub>* to *D<sub>max</sub>*) are provided in the file [`grains.csv`](https://github.com/Ecohydraulics/Exercise-SedimentTransport/raw/master/grains.csv) (`delimiter=","`) and can be customized.

Write a `GrainReader` class that uses *pandas*' `read_csv` method to read the grain size distribution from `grains.csv`. Write the class in a separate *Python* script (e.g., `grains.py` as indicated in the above figure):

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


### Read HEC-RAS input data

The provided *HEC-RAS* dataset is stored in an *xlsx* workbook ([`HEC-RAS/output.xlsx`](https://github.com/Ecohydraulics/Exercise-SedimentTransport/raw/master/HEC-RAS/output.xlsx) and contains the following output:

| **Col.No.** | **Alphabetic Col.** | **Variable** | **Type** | **Description**                                 |
|-------------|---------------------|--------------|----------|-------------------------------------------------|
| Col. 01     | A  | Reach          | [string]       | River (reach) name         |
| Col. 02 | B  | River Sta  | [m]  | Position on the longitudinal river axis          |
| Col. 03 | C  | Profile    | [string]       | Name of flow scenario profile (e.g., HQ2.33)    |
| Col. 04 | D  | Q Total    | [m³/s]  | River discharge    |
| Col. 05 | E  | Min Ch El  | [m a.s.l.]  | Minimum elevation (level) of channel cross-section           |
| Col. 06 | F  | W.S. Elev  | [m a.s.l.]  | Water surface elevation (level)           |
| Col. 07 | G  | Vel Chnl   | [m]  | Flow velocity main channel   |
| Col. 08 | H  | Flow Area   | [m²]  | Wetted cross section area *A* (see above)   |
| Col. 09 | I  | Froude\# Chl    | [-] | *Froude number* of the channel (if 1, computation error do not use!) |
| Col. 10 | J  | Hydr Radius        | [m]  | Hydraulic radius  |
| Col. 11 | K  | Hydr Depth        | [m]  | Water depth (active cross-section average)   |
| Col. 12 | L  | E.G. Slope          | [m/m]    | Energy Gradeline slope  |

To load *HEC-RAS* output data, write a custom class (in a separate script called `hec.py`) that takes the file name as input argument and reads the *HEC-RAS* file as *pandas* data frame:

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

To create a `HecSet` object in the `main()` (`main.py`) function, we need to import and instantiate it for example as `hec = HecSet(file_name)`. In addition, we can already implement passing the `pd.DataFrame` of the *HEC-RAS* data to the `calculate_mpm` function (also in `main.py`) that we will complete later on.

```python
# main.py
import os
from ...
from hec import HecSet

...

@log_actions
def main():
    D_char = ...

    hec_file = os.path.abspath("..") + "\\HEC-RAS\\output.xlsx"
    hec = HecSet(hec_file)
```

### Create a bed load core class

A `BedCore` class written in the `bedload.py` script provides variables and methods, which are relevant to many bed load and sediment transport calculation formulae (e.g., the *Parker-Wong* correction or the [Smart & Jaeggi 1983](https://ethz.ch/content/dam/ethz/special-interest/baug/vaw/vaw-dam/documents/das-institut/mitteilungen/1980-1989/064.pdf) formula). Moreover, the `BedCore` class contains constants such as the gravitational acceleration *g* (i.e., `self.g=9.81`), the ratio of sediment grain and water density *s* (i.e., `self.s=2.68`), and the critical dimensionless bed shear stress *&tau;<sub>x,cr</sub>* (i.e., `self.tau_xcr=0.047`, which may be re-defined by users). The header of the `BedCore` class should look (similar) like this:

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
        self.phi = np.nan  # dimensionless bed load
        self.Q = np.nan  # discharge (m3/s)
        self.Rh = np.nan  # hydraulic radius (m)
        self.u = np.nan  # flow velocity (m/s)
```

```{note}
Import `fun` (the script with logging functions) to enable the usage of `logging.warning(...)` messages in the methods of `BedCore` and its child classes.
```

Add a method to convert the dimensionless bed load transport *&Phi;* into a dimensional value (kg/s). In addition to the variables defined in the `__init__` method, the `add_dimensions` method will require the effective channel width *b<sub>eff</sub>* ([recall the above descriptions](#qb):

```python
    def add_dimensions(self, b):
        try:
            return self.phi * b * np.sqrt((self.s - 1) * self.g * self.D ** 3) * self.rho_s
        except ValueError:
            logging.warning("Non-numeric data. Returning Qb=NaN.")
            return np.nan
```

Many bed load transport formulae involve the dimensionless bed shear stress [*&tau;<sub>x</sub>* (see above formula)](#taux) associated with a set of cross-section averaged hydraulic parameters. Therefore, implement the calculation method `compute_tau_x` in `BedCore`:

```python
    def compute_tau_x(self):
        try:
            return self.Se * self.Rh / ((self.s - 1) * self.D)
        except ValueError:
            logging.warning("Non-numeric data. Returning tau_x=NaN.")
            return np.nan
```

### Write a Meyer-Peter & Müller bed load assessment class

Create a new script (e.g., `mpm.py`) and implement a `MPM` class (**M**eyer-**P**eter & **M**üller) that inherits from the `BedCore` class. The `__init__` method of `MPM` should initialize `BedCore` and overwrite (recall [Polymorphism](python-basics/pyclasses.html#polymorphism) relevant parameters to the calculation of bed load according to Meyer-Peter & Müller (1948). Moreover, the initialization of an `MPM` object should go along with a check of the validity and the calculation of the dimensionless bed load transport *&Phi;* ([see above explanations](#mpm):

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

Add the `check_validity` method to verify if the provided cross-section characteristics fall into the range of validity of the Meyer-Peter & Müller formula (i.e., slope, grain size, ratio of discharge and water depth, and *Froude* number):

```python
    def check_validity(self, Fr):
        if (self.Se < 0.0004) or (self.Se > 0.02):
            logging.warning('Warning: Slope out of validity range.')
        if (self.D < 0.0004) or (self.D > 0.0286):
            logging.warning('Warning: Grain size out of validity range.')
        if (self.Q / self.h < 0.002) or (self.Q / self.h > 2.0):
            logging.warning('Warning: Discharge out of validity range.')
        if (self.s < 0.25) or (self.s > 3.2):
            logging.warning('Warning: Relative grain density (s) out of validity range.')
        if (Fr < 0.0001) or (Fr > 639):
            logging.warning('Warning: Froude number out of validity range.')
```

```{note}
The here shown `check_validity` method takes the *Froude* number as input argument. Alternatively, assign the *Froude* number already in `__init__` and use `self.Fr`.
```

To calculate dimensionless bed load transport *&Phi;* according to Meyer-Peter & Müller, implement a `compute_phi` method that uses the `compute_tau_x` method from `BedCore`:

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

With the `MPM` class defined, we can now fill the `calculate_mpm` function in the `main.py` script. The function should create a *pandas* data frame with columns of dimensionless bed load transport *&Phi;* and dimensional bed load transport *Q<sub>b</sub>* associated with a channel profile (`"River Sta"`) and flow scenario (`"Profile" > "Scenario"`).

The following code block illustrates an example for the `calculate_mpm` function that creates the *pandas* data frame from a *dictionary* (`mpm_dict`). The illustrative function creates the *dictionary* with void value lists, extracts hydraulic data from the *HEC-RAS* data frame, and loops over the `"River Sta"` entries. The loop checks if the `"River Sta"` entries are valid (i.e., not "Nan") because empty rows that *HEC-RAS* automatically adds between output profiles should not be analyzed. If the check was successful, the loop appends the profile, scenario, and discharge directly to `mpm_dict`. The section-wise bed load transport results from `MPM` objects. After the loop, the function returns `mpm_dict` as a `pd.DataFrame` object.

```python
# main.py
from ...
from ...
from mpm import *

...

def calculate_mpm(hec_df, D_char):
    # create dictionary with relevant information about bed load transport with void lists
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

Having defined the `calculate_mpm()` function, the call to that function from the `main()` function should now assign a *pandas* data frame to the `mpm_results` variable. To finalize the script, write `mpm_results` to a workbook (e.g., `"bed_load_mpm.xlsx"`) in the `main()` function:

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
    mpm_results.to_excel(os.path.abspath("..") + "\\bed_load_mpm.xlsx")
```

## Launch and debug

Using [PyCharm](../get-started/ide.html#pycharm), right-click in the `main.py` script and click `> Run 'main'`. If the script crashes or raises error messages, trace them back, and fix the issues. Add `try` - `except` statements where necessary and recall the [debugging instructions](../python-basics/pyerror).

```{note}
The program intentionally produces warning messages because some of the profile characteristics do not fulfill the Meyer-Peter & Müller formula's validity range.
```

A successful run of `main.py` produces a `bed_load_mpm.xlsx` file that looks like this:

|    | River Sta | Scenario | Q (m3/s) | Phi (-)     | Qb (kg/s)   |
|----|-----------|----------|----------|-------------|-------------|
| 0  | 1970.1    | Q mean   | 1        |             |             |
| 1  | 1970.1    | HQ2.33   | 13       | 0.548377243 | 42.72291418 |
| 2  | 1970.1    | HQ5      | 17       | 0.682792055 | 54.58338633 |
| 3  | 1970.1    | HQ10     | 19       | 0.765834516 | 62.56010505 |
| 4  | 1970.1    | HQ100    | 25       | 0.905542967 | 77.92848176 |
| 5  | 1893.37   | Q mean   | 1        | 0.193642263 | 5.075423967 |
| 6  | 1893.37   | HQ2.33   | 13       | 0.144406226 | 14.00424884 |
| 7  | 1893.37   | HQ5      | 17       | 0.203854633 | 20.40484039 |
| 8  | 1893.37   | HQ10     | 19       | 0.229078172 | 23.1352098  |
| 9  | 1893.37   | HQ100    | 25       | 0.297767546 | 31.25225316 |
| ...| ...   | ...   | ...        | ...           | ...           |

The logfile should look similar to this:

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


```{note}
There are many possible solutions to this exercise and any solution that results in the same outcome (workbook and logfile) is valid. The key challenge is to use an object-oriented approach with at least one class inheriting from another class.
```

```{admonition} Homework
**HOMEWORK 1:**  Implement the [*Parker-Wong*](https://doi.org/10.1061/(ASCE)0733-9429(2006)132:11(1159) correction for the *Meyer-Peter & Müller* formula: *&Phi;<sub>pw</sub> &asymp; 4.93 · (&tau;<sub>x</sub> - &tau;<sub>x,cr</sub>)<sup>1.6</sup>*. Implement the formula in the `MPM` class either use an optional keyword argument in `compute_phi` or a new method.
**HOMEWORK 2:**  Use the `openpyxl` library to add a background color to the headers of output tables.
**HOMEWORK 3:**  Choose and extract 3 profiles from `mpm_results` and plot the dimensional bed load transport *Q<sub>b</sub>* (y-axis) against the discharge *Q* (x-axis).
```
