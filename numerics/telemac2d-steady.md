(telemac2d-steady)=
# Steady 2d Simulation

```{admonition} Requirements
This tutorial is designed for **advanced beginners** and before diving into this tutorial make sure to do the {ref}`TELEMAC pre-processing tutorial <slf-prepro-tm>`.

The case featured in this tutorial was established with the following software:
* {ref}`Notepad++ <npp>` text editor (any other text editor will do just as well.)
* TELEMAC v8p2r0 ({ref}`stand-alone installation <modular-install>`).
* {ref}`QGIS <qgis-install>` and the {ref}`PostTelemac plugin <tm-qgis-plugins>`.
* Debian Linux 10 (Buster) installed on a Virtual Machine (read more in the {ref}`software chapter <chpt-vm-linux>`).
```

## Get Started

This section builds on the SELAFIN (`*.slf`) and Conlim (`*.cli`) boundary condition files that result from the {ref}`TELEMAC pre-processing tutorial <slf-prepro-tm>`. Both files can also be downloaded from the supplemental materials repository of this eBook:

* [Download qgismesh.slf](https://github.com/hydro-informatics/telemac/raw/main/bk-slf/qgismesh.slf).
* [Download boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/bk-slf/boundaries.cli).

Consider saving both files in a new folder, such as `/steady2d-tutorial/` that will contain all model files.

```{admonition} Download simulation files
All simulation files used in this tutorial are available at [https://github.com/hydro-informatics/telemac/tree/main/steady2d-tutorial/](https://github.com/hydro-informatics/telemac/tree/main/steady2d-tutorial/).
```

## Steering File (CAS)

The steering file has the file ending `*.cas` (presumably derived from the French word *cas*, which means *case* in English). The `*.cas` file is the main simulation file with information about references to the two always mandatory files (i.e., the [SELAFIN / SERAFIN](https://gdal.org/drivers/vector/selafin.html) `*.slf` geometry and the `*.cli` boundary files) and optional files, as well as definitions of simulation parameters. The steering file can be created or edited with a basic text editor or advanced software such as {ref}`Fudaa PrePro <fudaa>` or {ref}`Blue Kenue <bluekenue>`. This tutorial uses {ref}`Notepad++ <npp>` as a basic text editor to minimize the number of software involved.

```{admonition} Fudaa PrePro
*Fudaa PrePro* comes with variable descriptions that facilitate the definition of boundaries, initial conditions, and numerical parameters in the steering file. However, Fudaa PrePro refers to the platform system to reference simulation files (`\` on Windows and `/` on Linux) and writes absolute file paths to the `*.cas` file, which often require manual correction (e.g., if Fudaa PrePro is used for setting up a `*.cas` file on Windows for running a TELEMAC simulation on Linux). For working with Fudaa PrePro, follow the download instructions in the {ref}`software chapter <fudaa>`. To launch Fudaa Prepro, open *Terminal* (Linux) or *Command Prompt* (Windows) and tap:

* `cd` to the installation (download) directory of Fudaa PrePro
* Start the GUI (requires java):
  * *Linux*: `sh supervisor.sh`
  * *Windows*: `supervisor.bat`
```

For this tutorial, **create a new text file** in the same folder where `qgismesh.slf` and `boundaries.cli` live and name it, for instance, `steady2d.cas` (e.g., `/steady2d-tutorial/steady2d.cas`). The next sections guide through variable definitions that stem from the {{ tm2d }}. The final steering file can be downloaded from the supplemental materials repository ([download steady2d.cas](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/steady2d.cas)).


### General Parameters

The general parameters define the computation environment starting with a simulation title and the most important links to the two mandatory input files:

* `BOUNDARY CONDITIONS FILE` : `boundaries.cli` - with a *MED* file, use a *BND* boundary file
* `GEOMETRY FILE`: `qgismesh.slf`

The model **output** can be defined with the following keywords:

* `RESULTS FILE` : `r2dsteady.slf` - can be either a *MED* file or a *SLF* file
* `VARIABLES FOR GRAPHIC PRINTOUTS`:  `U,V,H,S,Q,F` - many more options can be found in section 1.317 (page 85) of the {{ tm2dref }}.

The velocities (`U` and `V`), the water depth (`H`), and the discharge (`Q`) are standard variables that should be used in every simulation. In particular, the discharge (`Q`) is required to check when a (steady) flow converges at the inflow and outflow boundaries. Moreover, the discharge (`Q`) enables to trace fluxes along any user-defined line in the model. The procedure for verifying and identify discharges is described in the {ref}`discharge verification <verify-steady-tm2d>` section in the post-processing.

The time variables (`TIME STEP` and `NUMBER OF TIME STEPS`) define the simulation length and the printout periods (`GRAPHIC PRINTOUT PERIOD` and `LISTING PRINTOUT PERIOD`) define the result output frequency. The **smaller the printout period**, **the longer will take the simulation** because writing results is one of the most time consuming processes in numerical modeling. The printout periods (frequencies) refer to a multiple of the `TIME STEPS` parameter and need to be a smaller number than the `NUMBER OF TIME STEPS`. Read more about time step parameters in the {{ tm2d }} in the sections 5 and 12.4.2.

```
/ steady2d.cas
/------------------------------------------------------------------/
/			GENERAL PARAMETERS
/------------------------------------------------------------------/
TITLE : 'TELEMAC 3D FLUME'
/
BOUNDARY CONDITIONS FILE : boundaries.cli
GEOMETRY FILE            : qgismesh.slf
RESULTS FILE           : r2dsteady.slf
/
VARIABLES FOR GRAPHIC PRINTOUTS : U,V,H,S,Q,F
/
TIME STEP : 1.
NUMBER OF TIME STEPS : 8000
GRAPHIC PRINTOUT PERIOD : 100
LISTING PRINTOUT PERIOD : 100
```


### Numerical Parameters

* The `MASS-BALANCE : YES` setting will printout the mass fluxes and errors in the computation region, which is an important parameter for verifying the plausibility of the model.

```
/------------------------------------------------------------------/
/			NUMERICAL PARAMETERS
/------------------------------------------------------------------/
/
/ CONVECTION-DIFFUSION
/------------------------------------------------------------------
DISCRETIZATIONS IN SPACE : 11;11
TYPE OF ADVECTION : 1;5;1;1
ADVECTION : YES
/
SUPG OPTION : 0;0;2;2  / classic supg for U and V  see docs sec 6.2.2
/
/ PROPAGATION HEIGHT AND STABILITY
/ ------------------------------------------------------------------
IMPLICITATION FOR DEPTH : 0.55 / should be between 0.55 and 0.6
IMPLICITATION FOR VELOCITY : 0.55 / should be between 0.55 and 0.6
FREE SURFACE GRADIENT COMPATIBILITY : 0.1  / default 1.
CONTINUITY CORRECTION : YES
TREATMENT OF THE LINEAR SYSTEM : 2
MASS-BALANCE : YES
MASS-LUMPING ON H : 1
/ MATRIX STORAGE : 3
/
/ HYDRODYNAMIC SOLVER
/------------------------------------------------------------------
INFORMATION ABOUT SOLVER : YES
SOLVER : 1
MAXIMUM NUMBER OF ITERATIONS FOR SOLVER = 200
TIDAL FLATS : YES
```

### Boundary and Initial Conditions

```
/ BOUNDARY CONDITIONS
/------------------------------------------------------------------
LAW OF BOTTOM FRICTION : 4 / 4-Manning
FRICTION COEFFICIENT : 0.03 / Roughness coefficient
/
/ Liquid boundaries
PRESCRIBED FLOWRATES  : 35.;35.
PRESCRIBED ELEVATIONS : 0.;371.33
/
/ INITIAL CONDITIONS
/ ------------------------------------------------------------------
INITIAL CONDITIONS : 'CONSTANT DEPTH'
INITIAL DEPTH : 1 / INTEGER for speeding up calculations
/
/ Type of velocity profile can be 1-constant normal profile (default) 2-UBOR and VBOR in the boundary conditions file (cli) 3-vector in UBOR in the boundary conditions file (cli) 4-vector is proportional to root (water depth, only for Q) 5-vector is proportional to root (virtual water depth), the virtual water depth is obtained from a lower point at the boundary condition (only for Q)
VELOCITY PROFILES : 4;1
/
```

### Turbulence

```
/------------------------------------------------------------------/
/			TURBULENCE
/------------------------------------------------------------------/
/
TURBULENCE MODEL : 1
```

### CAS Summary

````{admonition} Uncollapse to view the complete .CAS file
:class: note, dropdown

```
/---------------------------------------------------------------------
/ TELEMAC2D Version v8p2 Dec 18, 2022
/ STEADY HYDRODYNAMICS TRAINING
/---------------------------------------------------------------------

/ steady2d.cas
/------------------------------------------------------------------/
/			COMPUTATION ENVIRONMENT
/------------------------------------------------------------------/
TITLE : 'TELEMAC 3D FLUME'
/
BOUNDARY CONDITIONS FILE : boundaries.cli
GEOMETRY FILE            : qgismesh.slf
RESULTS FILE           : r2dsteady.slf
/
VARIABLES FOR GRAPHIC PRINTOUTS : U,V,H,S,Q,F
/
/------------------------------------------------------------------/
/			GENERAL PARAMETERS
/------------------------------------------------------------------/
TIME STEP : 1.
NUMBER OF TIME STEPS : 8000
GRAPHIC PRINTOUT PERIOD : 100
LISTING PRINTOUT PERIOD : 100
/
/------------------------------------------------------------------/
/			NUMERICAL PARAMETERS
/------------------------------------------------------------------/
/
/ CONVECTION-DIFFUSION
/------------------------------------------------------------------
DISCRETIZATIONS IN SPACE : 11;11
TYPE OF ADVECTION : 1;5;1;1
ADVECTION : YES
/
SUPG OPTION : 0;0;2;2  / classic supg for U and V  see docs sec 6.2.2
/
/ PROPAGATION HEIGHT AND STABILITY
/ ------------------------------------------------------------------
IMPLICITATION FOR DEPTH : 0.55 / should be between 0.55 and 0.6
IMPLICITATION FOR VELOCITY : 0.55 / should be between 0.55 and 0.6
FREE SURFACE GRADIENT COMPATIBILITY : 0.1  / default 1.
CONTINUITY CORRECTION : YES
TREATMENT OF THE LINEAR SYSTEM : 2
MASS-BALANCE : YES
MASS-LUMPING ON H : 1
/ MATRIX STORAGE : 3
/
/ HYDRODYNAMIC SOLVER
/------------------------------------------------------------------
INFORMATION ABOUT SOLVER : YES
SOLVER : 1
MAXIMUM NUMBER OF ITERATIONS FOR SOLVER = 200
TIDAL FLATS : YES
/
/ BOUNDARY CONDITIONS
/------------------------------------------------------------------
LAW OF BOTTOM FRICTION : 4 / 4-Manning
FRICTION COEFFICIENT : 0.03 / Roughness coefficient
/
/ Liquid boundaries
PRESCRIBED FLOWRATES  : 35.;35.
PRESCRIBED ELEVATIONS : 0.;371.33
/
/ INITIAL CONDITIONS
/ ------------------------------------------------------------------
INITIAL CONDITIONS : 'CONSTANT DEPTH'
INITIAL DEPTH : 1 / INTEGER for speeding up calculations
/
/ Type of velocity profile can be 1-constant normal profile (default) 2-UBOR and VBOR in the boundary conditions file (cli) 3-vector in UBOR in the boundary conditions file (cli) 4-vector is proportional to root (water depth, only for Q) 5-vector is proportional to root (virtual water depth), the virtual water depth is obtained from a lower point at the boundary condition (only for Q)
VELOCITY PROFILES : 4;1
/
/------------------------------------------------------------------/
/			TURBULENCE
/------------------------------------------------------------------/
/
TURBULENCE MODEL : 1

&ETA
```
````

The `&ETA` keyword at the bottom of the `*.cas` template file makes TELEMAC printing out keyword and the values assigned to them when it runs its *Damocles* algorithm.

## Run Telemac2d

### Load environment and files

Load the TELEMAC environment and run the configuration:

```
cd ~/telemac/v8p1/configs
source pysource.openmpi.sh
config.py
```


To start a simulation, `cd` to the directory where the simulation files live (see previous page) and launch the steering file (*cas*) with *telemac2d.py*:

```
cd /go/to/steady2d-tutorial/
telemac2d.py steady2d.cas
```

(tm-steady2d-postpro)=
# Post-processing

(verify-steady-tm2d)=
## Verify Discharge Convergence

The diagram in {numref}`Fig. %s <convergence-diagram-tm2d>` plots inflow and outflow for the simulation setup in this tutorial. The diagram suggests that the model reaches stability after the 55th output listing (simulation time $t \leq 5500$). Thus, the simulation time could be limited to $t = 6000$, but a simulation time of $t = 5000$ would be too short.

```{figure} ../img/telemac/convergence-diagram-tm.png
:alt: telemac2d convergence steady model simulation discharge verification validation
:name: convergence-diagram-tm2d

Convergence of inflow and outflow at the model boundaries.
```

Note the difference between the convergence duration in this steady simulation with Telemac2d that starts with an initial condition of 1.0 m water depth (plot in {numref}`Fig. %s <convergence-diagram-tm2d>`) compared to the longer convergence duration in the BASEMENT tutorial (plot in {numref}`Fig. %s <convergence-diagram-bm>`) that starts with a dry model. This difference mainly stems from the type of initial conditions (initial depth versus dry channel) that also reflects in an outflow surplus that is visible in the Telemac2d simulation and a zero-outflow in the BASEMENT simulation at the beginning of the simulations.

Telemac2d provides an efficient way to stop a simulation (step) when the mass fluxes stabilize. To enable this feature, add the following block in the steering (`*.cas`) file:

```
/ steady state stop criteria in steering.cas
STOP IF A STEADY STATE IS REACHED : YES / default is NO
STOP CRITERIA : 1.E-3 /  default is 1.E-4
```

Read more about the convergence stop criteria in the {{ tm2d }} (section 5.1).
