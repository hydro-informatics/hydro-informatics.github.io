(chpt-unsteady)=
# Unsteady 2d Simulation

```{admonition} Requirements
This tutorial is designed for **advanced modelers** and before diving into this tutorial make sure to complete the {ref}`TELEMAC pre-processing <slf-prepro-tm>` and {ref}`Telemac2d steady hydrodynamic modeling <telemac2d-steady>` tutorials.


The case featured in this tutorial was established with the following software:
* {ref}`Notepad++ <npp>` text editor (any other text editor will do just as well.)
* TELEMAC v8p2r0 ({ref}`stand-alone installation <modular-install>`).
* {ref}`QGIS <qgis-install>` and the {ref}`PostTelemac plugin <tm-qgis-plugins>`.
* Debian Linux 10 (Buster) installed on a Virtual Machine (read more in the {ref}`software chapter <chpt-vm-linux>`).
```

## Get Started

The {ref}`steady 2d tutorial <telemac2d-steady>` hypothesizes that the discharge of a river is constant over time. However, the discharge of a river is never truly steady and varies slightly from second to second, even in flow-controlled rivers. Alas, the inherently unsteady flow regime of rivers cannot realistically be modeled in any numerical software. As a result, we must discretize time-dependent discharge (e.g., a flood hydrograph) in a numerical model as a series of steady discharges. {numref}`Figure %s <unsteady-hydrograph>` illustrates the discretization of a natural flood hydrograph into steps of steady flows, which will be used in this tutorial. Note that the hydrograph **starts at Time = 15000**, which is the result of using the steady2d simulation end state for model initialization. Note that the end time of T=15000 represents the end of the dry steady model initialization, as described in the {ref}`tm2d-dry` section (results can be downloaded, see below).

```{figure} ../img/telemac/unsteady-hydrograph.png
:alt: unsteady flow discharge quasi steady telemac telemac2d hydrodynamic
:name: unsteady-hydrograph

The discretization of a natural hydrograph into steps of steady flows (qualitative hydrograph for this tutorial).
```

This tutorial shows how such a quasi-steady discharge hydrograph can be created through the definition of an inflow sequence (red circles in {numref}`Fig. %s <unsteady-hydrograph>`) and implemented in a Telemac2d simulation. The tutorial builds on the steady simulation of a discharge of 35 m$^3$/s and requires the following data from the {ref}`pre-processing <slf-prepro-tm>` and {ref}`steady2d <telemac2d-steady>` tutorials, which can be downloaded by clicking on the filenames:

* The computational mesh in [qgismesh.slf](https://github.com/hydro-informatics/telemac/raw/main/bk-slf/qgismesh.slf).
* The boundary definitions in [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/boundaries.cli).
* The results of the steady 2d model run for 35 m$^3$/s in [r2dsteady.slf](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/r2dsteady.slf) (result of the {ref}`dry bonus run <tm2d-dry>` ending at `T=15000`).

Consider saving the files in a new folder, such as `/unsteady2d-tutorial/`.

```{admonition} Unsteady simulation file repository
The simulation files used in this tutorial are available at [https://github.com/hydro-informatics/telemac/tree/main/unsteady2d-tutorial/](https://github.com/hydro-informatics/telemac/tree/main/unsteady2d-tutorial/).
```

(prepro-unsteady)=
## Model Adaptations

The integration of unsteady flows requires the adaptation of keywords and additional keywords (e.g., for linking liquid boundary files) in the steering (`*.cas`) file from the steady2d tutorial ([download steady2d.cas](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/steady2d.cas)).

```{admonition} View the unsteady steering file
To view the integration of the unsteady simulation keywords in the steering file, the `unsteady2d.cas` file can be [downloaded here](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/unsteady2d.cas)
```

## Initial Conditions

**The following descriptions refer to section 4.1.3 in the {{ tm2d }}.**

To speed up the calculations and provide a well-converging baseline for the quasi-steady calculations, this tutorial re-uses the output of the steady 2d simulation with dry initial conditions (see the {ref}`tm2d-dry` section). To this end, the steady results file ([r2dsteady.slf](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/r2dsteady.slf)) needs to be defined as `PREVIOUS COMPUTATION FILE`:

```fortran
COMPUTATION CONTINUED : YES
PREVIOUS COMPUTATION FILE : r2dsteady.slf / results of 35 CMS steady simulation
/ INITIAL TIME SET TO ZERO : 0 / avoid restarting at 15000
```

The `INITIAL TIME SET TO ZERO` keyword may be additionally defined with its default of `0` to reset the time from the previous computation file from `15000` to `0`. However, this tutorial does not use this option and continues at timestep 15000.

## General Parameters

To simulate the hydrograph shown in {numref}`Fig. %s <unsteady-hydrograph>`, the simulation must run for at least 15000 time steps (i.e., from `T=15000` to `T=30000`). Since printing out (intermediate) results has a significant effect on computational speed, we reduce graphic print-out time steps to every `500` time steps (in lieu of `200` used for the steady simulation):

```fortran
TIME STEP : 1.
NUMBER OF TIME STEPS : 15000
GRAPHIC PRINTOUT PERIOD : 500
LISTING PRINTOUT PERIOD : 500
```

## Open Boundaries

With the upstream open (liquid) boundary type being `4 5 5` (prescribed Q) and the downstream open (liquid) boundary type being `5 5 5` (prescribed Q and H), a time-dependent flow hydrograph and a {term}`Stage-discharge relation` needs to be provided (recall the rationales behind the choice of boundary types from the {ref}`pre-processing tutorial <bk-liquid-bc>`).

### Quasi-steady Hydrograph
With the dry-initialized model ending at T=15000, the hydrograph needs to start at `15000`, even though the model start will represent time *zero* of the unsteady simulation. To implement the triangular-shaped hydrograph shown in {numref}`Fig. %s <unsteady-hydrograph>`, **create a new file called `inflows.liq`** in the simulation folder. Open the new `inflows.liq` file in a text editor and add the red-circled points in {numref}`Fig. %s <unsteady-hydrograph>` as time-dependent flow information at the **upstream (1)** and **downstream (2)** open (liquid) boundaries. In this file:

* Add a file header starting with `#` signs (out-commented lines ignored by TELEMAC).
* Implement 3 columns (for time **T**, upstream inflow rate **Q(1)**, and downstream outflow rate **Q(2)**).
* Separate the columns either with *spaces* or *tabs* .

```{admonition} How does TELEMAC count the indices of open (liquid) boundaries?
Recall the information provided in the comment box in the {ref}`steady2d tutorial <tm2d-bounds>`.
```

Thus, the `inflows.liq` file should look similar to this:

```python
# Inflow hydrograph
#
T	Q(1)	Q(2)
s	m3/s	m3/s
15000	35	35
16000	35	35
17000	50	50
19000	1130	1130
22000	101	101
25000	35	35
99000	35	35
```

### Stage-Discharge Relation
To activate the use of a {term}`Stage-discharge relation` for an open (liquid) boundary with the `STAGE-DISCHARGE CURVES` keyword needs to be added to the steering file. This keyword accepts the following integers:

* `0` is the **default** that deactivates the usage of stage discharge.
* `1` applies prescribed elevations as function of calculated flow rate (discharge).
* `2` applies prescribed flow rates (discharge) as function of calculated elevation.

The `STAGE-DISCHARGE CURVES` keyword is a list that assigns one of the three integer (i.e., either `0`, `1`, or `2`) to the open (liquid) boundaries. In this tutorial `STAGE-DISCHARGE CURVES : 0;1` actives the use of a {term}`Stage-discharge relation` for the downstream boundary only where the **upstream open boundary number 1** is set to `0` and the **downstream open boundary number 1** is set to `0`.

The form (curve) of the {term}`Stage-discharge relation` needs to be defined in a stage-discharge file ({term}`ASCII` text format). Such files typically apply to the downstream boundary of a model at control sections (e.g., a free overflow weir). This tutorial uses the following relation that is stored in a file called `ratingcurve.txt` ([download](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/ratingcurve.txt)):

```
# Downstream Rating Curve
#
Z(2)	Q(2)
m	m3/s
371.33	35
371.45	50
371.86	101
375.73	1130
379.08	2560
```

To define {term}`Stage-discharge relation`s for multiple open boundaries (e.g., at river diversions or tributaries), add the curves to the same file. TELEMAC automatically recognizes where the curves apply by the number given in parentheses after the parameter name in the column header. For instance, in the above example for this tutorial, the column headers `Z(2)` and `Q(2)` tell TELEMAC to use these values for the second (i.e., downstream) open boundary. The column order is not important because TELEMAC reads the curve type (i.e., either $Q(Z)$ or $Z(Q)$) from the `STAGE-DISCHARGE CURVES` keyword.

````{admonition} Expand to view an example for multiple stage-discharge curve definitions
:class: note, dropdown
The following file block would prescribe {term}`Stage-discharge relation`s to the upstream and downstream boundary conditions in this tutorial. However, the file cannot be used here unless the upstream boundary type is changed to `5 5 5` (prescribed H and Q) in the `boundaries.cli` file (read more in the {ref}`pre-processing tutorial <bk-liquid-bc>`).
```
#
# Downstream Rating Curve
#
Z(2)	Q(2)
m	m3/s
371.33	35
371.45	50
371.86	101
375.73	1130
379.08	2560
#
# Upstream Rating Curve
#
Q(1)  Z(1)
m3/s  m
35    371.33
50    371.45
101   371.86
1130  375.73
2560  379.08
```
````

To use a stage-discharge file, define the following keyword in the steering file:

```
/ steering.cas
STAGE-DISCHARGE CURVES : 1
STAGE-DISCHARGE CURVES FILE : YES
```

### Numerical Parameters

The predictor-corrector schemes (`SCHEME FOR ...` keywords defined with `3`, `4`, `5`, or `15` as explained in the {ref}`steady2d tutorial <tm2d-numerical>`) rely on a parameter defining the number of iterations at every timestep for convergence. For quasi-steady simulations, the developers recommend to set this parameter to `2` or slightly larger (section 7.2.1 in the {{ tm2d }}). Therefore, add the following line to the steering file:

```fortran
NUMBER OF CORRECTIONS OF DISTRIBUTIVE SCHEMES : 2
```

In addition, a minimum value for water depth can be set to define if a cell is wet or dry. While TELEMAC developers do not recommend using a minimum water depth for most simulations, they do recommend its usage for unsteady (quasi-steady) simulation. Defining a minimum water depth requires to set the `TREATMENT OF THE TIDAL FLATS` keyword to `2` (read more in the {ref}`steady2d tutorial <tm2d-tidal>`), which is not compatible with the parallelization routines, nor with the here used `SCHEME FOR ADVECTION ... : 14` settings. Thus, good results, but long non-parallelized quasi-steady calculations can be yielded with the following keywords in the steering file:

```fortran
OPTION FOR THE TREATMENT OF TIDAL FLATS : 2 / use segment-wise flux control
MINIMUM VALUE OF DEPTH : 0.1 / in meters
```

## Run Telemac2d Unsteady

Go to the configuration folder of the local TELEMAC installation (e.g., `~/telemac/v8p2/configs/`) and launch the environment (e.g., `pysource.openmpi.sh` - use the same as for compiling TELEMAC).

```
cd ~/telemac/v8p2/configs
source pysource.openmpi.sh
config.py
```

````{admonition} If you are using the Hydro-Informatics (Hyfo) Mint VM
:class: note, dropdown

If you are working with the {ref}`Mint Hyfo VM <hyfo-vm>`, load the TELEMAC environment as follows:

```
cd ~/telemac/v8p2/configs
source pysource.hyfo-dyn.sh
config.py
```
````

With the TELEMAC environment loaded, change to the directory where the above-created 3d-flume simulation lives (e.g., `/home/telemac/v8p2/mysimulations/unsteady2d-tutorial/`) and run the `*.cas` file by calling the **telemac2d.py** script.

```
cd ~/telemac/v8p2/mysimulations/unsteady2d-tutorial/
telemac2d.py unsteady2d.cas
```


As a result, a successful computation should end with the following lines (or similar) in *Terminal*:

```fortran
[...]
                    *************************************
                    *    END OF MEMORY ORGANIZATION:    *
                    *************************************

CORRECT END OF RUN

ELAPSE TIME :
                            10  MINUTES
                            32  SECONDS
... merging separated result files

... handling result files
       moving: r2dunsteady.slf
... deleting working dir

My work is done
```
