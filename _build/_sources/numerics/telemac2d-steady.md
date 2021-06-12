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

### Overview of the CAS File

The below box shows the provided [steady2d.cas](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/steady2d.cas) file that can be used for running this tutorial.

````{admonition} Expand to view the complete .CAS file
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

```{admonition} What means &ETA?
:class: note
The `&ETA` keyword at the bottom of the `*.cas` template file makes TELEMAC printing out keyword and the values assigned to them when it runs its *Damocles* algorithm.
````

### General Parameters

The general parameters define the computation environment starting with a simulation title and the most important links to the two mandatory input files:

* `BOUNDARY CONDITIONS FILE` : `boundaries.cli` - with a *MED* file, use a *BND* boundary file
* `GEOMETRY FILE`: `qgismesh.slf`

The model **output** can be defined with the following keywords:

* `RESULTS FILE` : `r2dsteady.slf` - can be either a *MED* file or a *SLF* file
* `VARIABLES FOR GRAPHIC PRINTOUTS`:  `U,V,H,S,Q,F` - many more options can be found in section 1.317 (page 85) of the {{ tm2dref }}.

The velocities (`U` and `V`), the water depth (`H`), and the discharge (`Q`) are standard variables that should be used in every simulation. In particular, the discharge (`Q`) is required to check when a (steady) flow converges at the inflow and outflow boundaries. Moreover, the discharge (`Q`) enables to trace fluxes along any user-defined line in the model. The procedure for verifying and identify discharges is described in the {ref}`discharge verification <verify-steady-tm2d>` section in the post-processing.

The time variables (`TIME STEP` and `NUMBER OF TIME STEPS`) define the simulation length and the printout periods (`GRAPHIC PRINTOUT PERIOD` and `LISTING PRINTOUT PERIOD`) define the result output frequency. The **smaller the printout period**, **the longer will take the simulation** because writing results is one of the most time consuming processes in numerical modeling. The printout periods (frequencies) refer to a multiple of the `TIME STEPS` parameter and need to be a smaller number than the `NUMBER OF TIME STEPS`. Read more about time step parameters in the {{ tm2d }} in the sections 5 and 12.4.2.

````{admonition} Expand to recall GENERAL PARAMETERS in the cas file
:class: note, dropdown
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
````

### Numerical Parameters

The `SUPG OPTION` (Streamline Upwind Petrov Galerkin) keyword is a list of four integers that define if upwinding applies and what type of upwinding applies. The integers may take the following values:

* `0` disables upwinding,
* `1` enables upwinding with a classical SUPG scheme (recommended when the [Courant number](https://en.wikipedia.org/wiki/Courant-Friedrichs-Lewy_condition) is unknown), and
* `2` enables upwinding with a modified SUPG scheme, where upwinding corresponds to the Courant number.

The default is `SUPG OPTION : 1;0;1;1`, where the first list element refers to flow velocity (default `1`), the second to water depth (default `0`), the third to tracers (default `1`), and the last to the k-epsilon model (default `1`). Read more in section ??? of the {{ tm2d }}.

**Implication parameters** (`IMPLICITATION FOR DEPTH` and `IMPLICITATION FOR VELOCITIES`) should be set between 0.55 and 0.60 (default is 0.55 since *TELEMAC v8p1*) and can be considered as a degree of implicitation. `IMPLICITATION FOR DIFFUSION` is set to `1.0` by default. Read more in section ??? of the {{ tm2d }}.

The parameter `FREE SURFACE GRADIENT` can be used for increasing the stability of a model. Its default value is `1.0`, but it can be reduced to `0.1` to achieve stability.

* The `MASS-BALANCE : YES` setting will printout the mass fluxes and errors in the computation region, which is an important parameter for verifying the plausibility of the model.

Depending on the type of analysis, the solver-related parameters of `SOLVER`, `SOLVER OPTIONS`, `MAXIMUM NUMBER OF ITERATION FOR SOLVER`, and `TIDAL FLATS` may be modified.

````{admonition} Expand to recall NUMERICAL PARAMETERS in the cas file
:class: note, dropdown
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
````

### Boundary and Initial Conditions

Parameters for **Boundary Conditions** enable the definition of roughness laws and properties of liquid boundaries.

 To apply the *Manning* roughness coefficient to the bottom and the boundaries use:

* `LAW OF BOTTOM FRICTION`: `4`
* `LAW OF FRICTION ON LATERAL BOUNDARIES`: `4`, which can well be applied to model natural banks, or set to `0` (no-slip) for symmetry.<br>*Note that the friction on lateral boundaries in not defined in the provided *steady2d.cas* file.
* `FRICTION COEFFICIENT FOR THE BOTTOM`: `0.1` corresponds to 3 times a hypothetical *d90* (grain diameter of which 90% of the surface grain mixture are finer) according to [van Rijn](https://www.leovanrijn-sediment.com/).

The liquid boundary definitions for `PRESCRIBED FLOWRATES` and `PRESCRIBED ELEVATIONS` correspond to the definitions of the **downstream** boundary edge in line 2 and the **upstream** boundary edge in line 3 (see [boundary definitions section](#bnd-mod)). From the boundary file, *TELEMAC* will understand the **downstream** boundary as edge number **1** (first list element) and the **upstream** boundary as edge number **2** (second list element). Hence:

* The list parameter `PRESCRIBED FLOWRATES : 50.;50.` assigns a flow rate of 50 m<sup>3</sup>/s to the **downstream** and the **upstream** boundary edges.
* The list parameter `PRESCRIBED ELEVATIONS : 2.;0.` assigns an elevation (i.e., water depth) of two m to the **downstream** boundary and a water depth of 0.0 m to the **upstream** boundary.

The `0.` value for the water does physically not make sense at the upstream boundary, but because they do not make sense, and because the boundary file (`flume3d_bc.bnd`) only defines (*prescribes*) a flow rate (by setting `LIUBOR` and `LIVBOR` to `5`), *TELEMAC* will ignore the zero-water depth at the upstream boundary.

Instead of a list in the steering *CAS* file, the liquid boundary conditions can also be defined with a liquid boundary condition file in *ASCII* text format. For this purpose, a `LIQUID BOUNDARIES FILE` or a `STAGE-DISCHARGE CURVES FILE` (sections ??? and??? in the {{ tm2d }}, respectively can be defined. A liquid boundary file (*QSL*) may look like this:

```fortran
# quasi-unsteady2d.qsl
# time-dependent inflow upstream-discharge Q(2) and outflow downstream-depth SL(1)
T           Q(2)     SL(1)
s           m3/s     m
0.            0.     5.0
500.        100.     5.0
5000.       150.     5.0
```

With a prescribed flow rate, a horizontal and a vertical velocity profile can be prescribed for all liquid boundaries. With only a **downstream** and an **upstream** liquid boundary (in that order according to the above-defined boundary file), the velocity profile keywords are lists of two elements each, where the first entry refers to the **downstream** and the second element to **upstream** boundary edges:

* `VELOCITY PROFILES`: `1;1` is the default option for the **horizontal** profiles. If set to `2;2`, the velocity profiles will be read from the boundary condition file.

Read more about options for defining velocity profiles in section ??? of the {{ tm2d }}.

The **initial conditions** describe the condition at the beginning of the simulation. This tutorial uses a constant elevation (corresponding to a constant water depth) of `2.`, and enables using an initial guess for the water depth to speed up the simulation:

* `INITIAL CONDITIONS`: `'CONSTANT ELEVATION'` can alternatively be set to `'CONSTANT DEPTH'`
* `INITIAL ELEVATION`: `50.` may be used to define an initial water surface level of a lake, but this keyword should not be used with a river model. Therefore, it is not included in the provided *steady2d.cas* file.
* `INITIAL DEPTH`: `1` .

Read more about the initial conditions in section ??? of the {{ tm2d }}.

````{admonition} Expand to recall BOUNDARY and INITIAL CONDITIONS in the cas file
:class: note, dropdown
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
````

### Turbulence

Turbulence describes a seemingly random and chaotic state of fluid motion in the form of three-dimensional vortices (eddies). True turbulence is only present in 3d vorticity and when it occurs, it mostly dominates all other flow phenomena through increases in energy dissipation, drag, heat transfer, and mixing. The phenomenon of turbulence has been a mystery to science for a long time, since turbulent flows have been observed, but could not be directly explained by the systems of linear equations. Today, turbulence is considered a random phenomenon that can be accounted for in linear equations, for instance, by introducing statistical parameters. Not surprisingly, there are a variety of options for implementing turbulence in numerical models. The horizontal and vertical dimensions of turbulent eddies can vary greatly, especially in rivers and transitions to backwater zones (tidal flats), with large flow widths (horizontal dimension) compared to small water depths (vertical dimension). For these reasons, *TELEMAC* provides multiple turbulence models that can be applied in the vertical and horizontal dimensions.

In 2d, *TELEMAC* developers recommend using either the *k-&epsilon;* model (`3`) or the *Spalart-Allmaras* model (`5`) in lieu of the mixing length model (`2`):

* `HORIZONTAL TURBULENCE MODEL`: `3`
* `VERTICAL TURBULENCE MODEL`: `3`

If the `VERTICAL TURBULENCE MODEL` is set to `2` (`'MIXING LENGTH'`), a `MIXING LENGTH MODEL` can be assigned. The default is `1`, which is preferable for strong tidal influences and a value of `3` sets the length for computing vertical diffusivity to *Nezu and *Nakagawa*.

Read more about turbulence in *TELEMAC* in section ??? and the mixing length in section ??? of the {{ tm2d }}.

````{admonition} Expand to recall TURBULENCE in the cas file
:class: note, dropdown
```
/------------------------------------------------------------------/
/			TURBULENCE
/------------------------------------------------------------------/
/
TURBULENCE MODEL : 1
```
````




## Run Telemac2d

### Load environment and files

Go to the configuration folder of the local *TELEMAC* installation (e.g., `~/telemac/v8p2/configs/`) and configure the environment (e.g., `pysource.openmpi.sh` - use the same as for compiling *TELEMAC*).

```
cd ~/telemac/v8p1/configs
source pysource.openmpi.sh
config.py
```

To start a simulation, change to the directory (`cd`) where the simulation files live (see previous page) and ran the steering file (*cas*) with the **telemac2d.py** script:

```
cd /go/to/steady2d-tutorial/
telemac2d.py steady2d.cas
```


As a result, a successful computation should end with the following lines (or similar) in *Terminal*:

```fortran
[...]
BOUNDARY FLUXES FOR WATER IN M3/S ( >0 : ENTERING )
FLUX BOUNDARY      1                          :    -35.85411
FLUX BOUNDARY      2                          :     35.00000
--------------------------------------------------------------------------------
                FINAL MASS BALANCE
T =        5000.0000

--- WATER ---
INITIAL MASS                        :     2500000.
FINAL MASS                          :     100343.0
MASS LEAVING THE DOMAIN (OR SOURCE) :     2384217.
MASS LOSS                           :     15440.06

 END OF TIME LOOP

 EXITING MPI
                     *************************************STOP 0
                     *    END OF MEMORY ORGANIZATION:    *
                     *************************************

 CORRECT END OF RUN

 ELAPSE TIME :
                             44  SECONDS
... merging separated result files

... handling result files
        moving: r2dsteady.slf
... deleting working dir

My work is done
```

Thus, Telemac2d produced the file `r2dsteady.slf` that can now be analyzed in the {ref}`post-processing with QGIS <tm-steady2d-postpro>` or ParaView.


(tm-steady2d-postpro)=
# Post-processing

The post-processing of the steady 2d scenario only uses QGIS and the {ref}`PostTelemac plugin <tm-qgis-plugins>`.

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
