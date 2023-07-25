(chpt-telemac3d-slf)=
# Steady 3d (SLF - Selafin)

```{admonition} Tutorial under construction
:class: warning
This tutorial is still growing and provides currently only rough guidance to constructing a 3d steady, hydrodynamic model with TELEMAC.
```

```{admonition} Requirements
This tutorial is designed for **advanced beginners** and before diving into this tutorial make sure to complete the {ref}`TELEMAC pre-processing tutorial <slf-prepro-tm>`.

The case featured in this tutorial was established with the following software:
* {ref}`Notepad++ <npp>` text editor (any other text editor will do just as well.)
* TELEMAC v8p2r0 ({ref}`stand-alone installation <modular-install>`).
* {ref}`QGIS <qgis-install>` and the {ref}`PostTelemac plugin <tm-qgis-plugins>`.
* Debian Linux 10 (Buster) installed on a Virtual Machine (read more in the {ref}`software chapter <chpt-vm-linux>`).
```

This tutorial shows how a steady discharge can be simulated with Telemac3d using the SLF geometry format. **The tutorial builds on the steady2d simulation** of the 35-m$^3$/s discharge and requires the following data from the {ref}`pre-processing <slf-prepro-tm>` and {ref}`steady2d <telemac2d-steady>` tutorials, which can be downloaded by clicking on the filenames:

* The computational mesh in [qgismesh.slf](https://github.com/hydro-informatics/telemac/raw/main/bk-slf/qgismesh.slf).
* The boundary definitions in [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/boundaries.cli).
* The results of the {ref}`steady 2d model <tm2d-init-dry>` simulaton of 35 m$^3$/s in [r2dsteady.slf](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/r2dsteady.slf) (ending at `t=15000`).

Consider saving the files in a new folder, such as `/steady3d-tutorial/`.

```{admonition} 3d-steady simulation file repository
The simulation files used in this tutorial are available at [https://github.com/hydro-informatics/telemac/tree/main/steady3d-tutorial/](https://github.com/hydro-informatics/telemac/tree/main/steady3d-tutorial/).
```

(prepro-3dsteady-slf)=
## Re-use the 2d Model

The simulation of 3d flow phenomena flows requires the adaptation of keywords and additional keywords (e.g., for linking liquid boundary files) in the steering (`*.cas`) file from the steady2d tutorial ([download steady2d.cas](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/steady2d.cas)).

```{admonition} View the steady3d steering file
To view the integration of the steady3d simulation keywords in the steering file, the `steady3d.cas` file can be [downloaded here](https://github.com/hydro-informatics/telemac/raw/main/steady3d-tutorial/steady3d.cas).
```


## Steering File

This tutorial features a steady, hydrodynamic model with an inflow rate of 35 m$^3$/s (prescribed upstream flow rate boundary) and an outflow depth of 2 m (prescribed downstream elevation). The simulation uses 5 vertical layers that constitute a numerical grid of prisms. 3d outputs of *U* (*x*-direction), *V* (*y*-direction), and *W* (*z*-direction) velocities, as well as the elevation *Z*, are written to a file named `r3dsteady.slf`. 2d outputs of depth-averaged *U* velocity (*x*-direction), depth-averaged *V* velocity (*y*-direction), and water depth *h* are written to a file named `r2d3dsteady.slf`.

The below code block shows the steering file `t3d_flume.cas` and details for every parameter are provided after the code block. The slash `/` character comments out lines (i.e., TELEMAC will ignore anything in a line the `/` character). The `:` character separates `VARIABLE NAME` and `VALUE`s. Alternatively to the `:`, also a `=` sign may be used. The `&ETA` at the end of the file makes TELEMAC printing out a list of keywords applied (in the *DAMOCLES* routine).

```{tip}
To facilitate setting up the steering (CAS) file for this tutorial, [download the template](https://github.com/hydro-informatics/telemac/raw/main/steady3d-tutorial/steady3d.cas) (right-click on the link > *Save Link As...* > navigate to the local tutorial folder), which contains more descriptions and options for simulation parameters.
```

````{admonition} Expand to view the steady3d.cas steering file
:class: note, dropdown
```fortran
/ steady3d.cas
/------------------------------------------------------------------/
/			COMPUTATION ENVIRONMENT
/------------------------------------------------------------------/
/
TITLE : '3d steady'
MASS-BALANCE : YES
/
BOUNDARY CONDITIONS FILE : boundaries.cli
GEOMETRY FILE            : qgismesh.slf
3D RESULT FILE           : r3dsteady.slf
2D RESULT FILE           : r2d3dsteady.med
/ FILE FOR 2D CONTINUATION : r2dsteady.slf / sec. 3.1.1
/
VARIABLES FOR 2D GRAPHIC PRINTOUTS : U,V,H,S,Q,F / Q enables boundary flux equilibrium controls
VARIABLES FOR 3D GRAPHIC PRINTOUTS : Z,U,V,W
/
/------------------------------------------------------------------/
/			GENERAL PARAMETERS
/------------------------------------------------------------------/
/
/ 2D CONTINUATION : YES / enable to start off from 2d simulation
TIME STEP : 1.
NUMBER OF TIME STEPS : 8000
GRAPHIC PRINTOUT PERIOD : 500
LISTING PRINTOUT PERIOD : 200
/
/------------------------------------------------------------------/
/			VERTICAL
/------------------------------------------------------------------/
/ vertical cell height defined by initial condition x no. of levels
/ will be adapted for every time step
NUMBER OF HORIZONTAL LEVELS : 5 / default and minimum is 2, upward vertical direction
MESH TRANSFORMATION : 1 / 0-CALCOT (user defined) 1-SIGMA (default) 3-user defined
ELEMENT : 'PRISM' / default is 'PRISM' but preferably use 'TETRAHEDRON'
/
/------------------------------------------------------------------/
/			NUMERICAL PARAMETERS
/------------------------------------------------------------------/
/
/ ADVECTION-DIFFUSION
/------------------------------------------------------------------
SCHEME FOR ADVECTION OF VELOCITIES : 5
SCHEME FOR ADVECTION OF K-EPSILON : 5
SCHEME FOR ADVECTION OF TRACERS : 5
SCHEME OPTION FOR ADVECTION OF VELOCITIES : 4 / use 2 for without tidal flats for speed
SCHEME OPTION FOR ADVECTION OF K-EPSILON : 4
SCHEME OPTION FOR ADVECTION OF TRACERS : 4
/
MATRIX STORAGE : 3 / 1 (element-by-element), 3 (segment-wise faster)
SUPG OPTION : 2;2;2;2  / classic supg for U and V  see docs sec 6.2.2
/
/ PROPAGATION HEIGHT AND STABILITY
/ ------------------------------------------------------------------
IMPLICITATION FOR DEPTH : 0.55 / should be between 0.55 and 0.6
IMPLICITATION FOR VELOCITIES : 0.55 / should be between 0.55 and 0.6
IMPLICITATION FOR DIFFUSION : 1.
FREE SURFACE GRADIENT COMPATIBILITY : 0.1  / default 1.
/
/ MASS LUMPING - enable to fasten calculations (smoothens) - possibly avoid in 3d
/ ------------------------------------------------------------------
/ MASS-LUMPING FOR DIFFUSION : 1 / 1 is ON - 0 is OFF (default)
/ MASS-LUMPING FOR DEPTH : 1.  / VELOCITY has no effect
/ MASS-LUMPING FOR WEAK CHARACTERISTICS : 1
/
/------------------------------------------------------------------/
/			HYDRODYNAMICS
/------------------------------------------------------------------/
/
/ HYDRODYNAMIC SOLVER
/------------------------------------------------------------------
NON-HYDROSTATIC VERSION : YES
/ solver options are
/ 1-conjugate method 2-conjugate residual method 3-conjugate gradient
/ 4-minimum error 5-square conjugate gradient 6-stabilized conjugate gradient CGSTAB
/ 7-Generalised Minimum RESidual GMRES is the favorite for improperly conditioned systems - RECOMMENDED in 3d
/ 8-direct solver YSMP (Yale) is not working with parallel versions
SOLVER FOR DIFFUSION OF VELOCITIES : 1 / 1-default
SOLVER FOR PROPAGATION : 7 / 7-default
SOLVER FOR PPE : 7 / 7-default
/ SOLVER FOR DIFFUSION OF TRACERS : 1 / one value per tracer
SOLVER FOR DIFFUSION OF K-EPSILON : 1 / 1-default
/
/ Set OPTIONS for GMRES
/ Increasing values for precision, but also more memory consumption
OPTION OF SOLVER FOR DIFFUSION OF VELOCITIES : 5 / 5-default since v8
OPTION OF SOLVER FOR PROPAGATION : 5 / 5-default since v8
OPTION OF SOLVER FOR PPE : 5 / 5-default since v8
OPTION OF SOLVER FOR DIFFUSION OF K-EPSILON : 5 / 5-default since v8
/
/ Solver ACCURACY
ACCURACY FOR DIFFUSION OF VELOCITIES : 1.E-8 / default is 1.E-8
ACCURACY FOR PROPAGATION : 1.E-8 / default is 1.E-8
ACCURACY FOR PPE : 1.E-6 / default is 1.E-8
ACCURACY FOR DIFFUSION OF K-EPSILON : 1.E-8 / default is 1.E-8
/
/ Solver MAXIMUM ITERATIONS
MAXIMUM NUMBER OF ITERATIONS FOR DIFFUSION OF VELOCITIES : 100 / default is 60
MAXIMUM NUMBER OF ITERATIONS FOR PROPAGATION : 200 / default is 100
MAXIMUM NUMBER OF ITERATIONS FOR PPE : 100 / default is 100
MAXIMUM NUMBER OF ITERATIONS FOR DIFFUSION OF K-EPSILON : 150 / default is 200
/
/ PRECONDITIONING - DEFAULT Value is 2 for all
PRECONDITIONING FOR DIFFUSION OF VELOCITIES : 2
PRECONDITIONING FOR PROPAGATION : 2
PRECONDITIONING FOR PPE : 2
PRECONDITIONING FOR DIFFUSION OF TRACERS : 2
PRECONDITIONING FOR DIFFUSION OF K-EPSILON : 2
/
/ BOUNDARY CONDITIONS
/------------------------------------------------------------------
/ Use Nikuradse roughness law - all others are not 3D compatible
LAW OF BOTTOM FRICTION : 5
LAW OF FRICTION ON LATERAL BOUNDARIES : 5  / for natural banks - 0 for symmetry
FRICTION COEFFICIENT FOR THE BOTTOM : 0.1 / 3 times d90 according to van Rijn
/
/ Liquid boundaries - avoid Thompson (invalid in 3d)
PRESCRIBED FLOWRATES  : 35.;35.
PRESCRIBED ELEVATIONS : 0.;371.33
/
/ INITIAL CONDITIONS
/ ------------------------------------------------------------------
INITIAL CONDITIONS : 'CONSTANT DEPTH' / or CONSTANT DEPTH see docs sec. 4.2
INITIAL DEPTH : 0.1
INITIAL GUESS FOR DEPTH : 1 / INTEGER for speeding up calculations
/
/ Other
/------------------------------------------------------------------
VELOCITY VERTICAL PROFILES : 2;2 / 0 (user-defined), 1 (Constant), 2 (Log)
VELOCITY PROFILES : 1;1 / horizontal profile
/
/------------------------------------------------------------------/
/			TIDAL FLATS
/------------------------------------------------------------------/
TIDAL FLATS : YES / default is YES - disable for faster model runs
/ TREATMENT OF NEGATIVE DEPTHS : 2 / requires mass lumping for depth set to 1
TREATMENT ON TIDAL FLATS FOR TRACERS : 1 / ensure conservation
/ more in section docs 6.6
/
/------------------------------------------------------------------/
/			TURBULENCE
/------------------------------------------------------------------/
/ in 3d use k-epsilon model, alternatively Spalart-Allmaras (5) or
/  Smagorinsky (4) for highly non-linear flow
HORIZONTAL TURBULENCE MODEL : 3
VERTICAL TURBULENCE MODEL : 3
MIXING LENGTH MODEL : 3 / telemac docs sec. 5.2.2
COEFFICIENT FOR HORIZONTAL DIFFUSION OF VELOCITIES : 1.E-6 / is default
COEFFICIENT FOR VERTICAL DIFFUSION OF VELOCITIES   : 1.E-6 / is default
/
/------------------------------------------------------------------/
/			PARALLELISM
/------------------------------------------------------------------/
PARALLEL PROCESSORS : 0 / default is 0 - all others define number of processors
/ PARTIONING TOOL : METIS / default is METIS, others are SCOTCH, PARMETIS, PTSCOTCH
/
/ ENABLE COMMAND PRINTS IN TERMINAL
&ETA
```

````

(tm3d-slf-env)=
### Computation Environment

**The following descriptions refer to section 3 in the {{ tm3d }}.**

The computation environment defines a **Title** (e.g., `TELEMAC 3D FLUME`). The most important parameters involve the **input** files:

* `GEOMETRY FILE`: `qgismesh.slf` - alternatively, select a *serafin* (SLF) geometry file
* `Boundary conditions file`: `boundaries.cli` - with a *SLF* file, use a *CLI* boundary file

The **output** can be defined with the following keywords:

* `3D RESULT FILE`: `r3dsteady.slf` - can be either a *MED* file or a *SLF* file
* `2D RESULT FILE`: `r2d3dsteady.slf` - can be either a *MED* file or a *SLF* file
* `VARIABLES FOR 3D GRAPHIC PRINTOUTS`:  `U,V,H,S,Q,F` - many more options can be found in section 3.12 of the {{ tm3d }}
* `VARIABLES FOR 2D GRAPHIC PRINTOUTS`:  `U,V,H` - many more options can be found in section 3.13 of the {{ tm3d }}

In addition, the `MASS-BALANCE : YES` setting will printout the mass fluxes and errors in the computation region, which is an important parameter for verifying the plausibility of the model.

### General Parameters
**The following descriptions refer to section 3.2 in the {{ tm3d }}.**

The *General parameters* specify *time* and *location* settings for the simulation:

* **Location** can be used for geo-referencing of outputs (not to set in this tutorial).
* **Time**:
  + `TIME STEP`: `1.0` defines the time step as a multiple of graphic/listing printout periods.<br>*Use small enough and sufficient time steps to achieve/increase computational stability and increase to yield computational efficiency.*
  + `NUMBER OF TIME STEPS`: `8000` defines the overall simulation length. <br>*Limit the number of time steps to a minimum (e.g., until equilibrium conditions are reached in a steady simulation).*
  + `GRAPHIC PRINTOUT PERIOD` : `500` time step at which graphic variables are written,
  + `LISTING PRINTOUT PERIOD`: `500` time step multiplier at which listing variables are printed (in this example, listings are printed every `100` · `1` = 100 seconds)

Modify the time parameters to examine the effect in the simulation later.

```{attention}
Graphic printouts, just like all other data printouts, are time consuming and will slow down the simulation.
```

### Numerical Parameters

**The following descriptions refer to section 6 in the {{ tm3d }}.**

This section defines internal numerical parameters for the {term}`Advection` and  {term}`Diffusion` solvers.

In Telemac3d, it is recommended to use the so-called distributive predictor-corrector (PSI) scheme ([read more](https://henry.baw.de/bitstream/handle/20.500.11970/104314/13_Hervouet_2015.pdf?sequence=1&isAllowed=y) at the BAW's hydraulic engineering repository) with local implication for tidal flats (for velocity, tracers, and k-epsilon):

* Set the PSI scheme:
    + `SCHEME FOR ADVECTION OF VELOCITIES`: `5`
    + `SCHEME FOR ADVECTION OF K-EPSILON`: `5`
    + `SCHEME FOR ADVECTION OF TRACERS`: `5`
* Enable predictor-corrector with local implication:
    + `SCHEME OPTION FOR ADVECTION OF VELOCITIES`: `4`
    + `SCHEME OPTION FOR ADVECTION OF K-EPSILON`: `4`
    + `SCHEME OPTION FOR ADVECTION OF TRACERS`: `4`

These values (`5` for the scheme and `4` for the scheme option) are default values since *TELEMAC v8p1*, but it still makes sense to define these parameters for enabling backward compatibility of the steering file. If the occurrence of tidal flats can be excluded (note that already a little backwater upstream of a barrier can represent a tidal flat), the `SCHEME OPTIONS` can generally set to `2` for speeding up the simulation.

Similar to {term}`Advection`, the above keywords can be used to define {term}`Diffusion` steps (replace `ADVECTION` with `DIFFUSION` in the keywords), where a value of `0` can be used to override the default value of `1` and disable diffusion.

The `SUPG OPTION` (Streamline Upwind Petrov Galerkin) keyword is a list of four integers that define if upwinding applies and what type of upwinding applies. The integers may take the following values:

* `0` disables upwinding,
* `1` enables upwinding with a classical SUPG scheme (recommended when the {term}`CFL` condition is unknown), and
* `2` enables upwinding with a modified SUPG scheme, where upwinding corresponds to the Courant number.

The default is `SUPG OPTION : 1;0;1;1`, where the first list element refers to flow velocity (default `1`), the second to water depth (default `0`), the third to tracers (default `1`), and the last to the k-epsilon model (default `1`). Read more in section 6.2.2 of the {{ tm3d }}.

An additional option for speeding up is to enable mass lumping for diffusion, depth, and/or weak characteristics. Mass lumping results in faster convergence, but it introduces artificial dispersion in the results, which is why enabling mass lumping is discouraged by the TELEMAC developers. The provided [steady3d.cas](https://github.com/hydro-informatics/telemac/raw/main/steady3d-tutorial/steady3d.cas) includes the keywords for mass lumping, though they are disabled through the `/` at the beginning of the line.

**Implication parameters** (`IMPLICITATION FOR DEPTH` and `IMPLICITATION FOR VELOCITIES`) should be set between 0.55 and 0.60 (default is 0.55 since *TELEMAC v8p1*) and can be considered as a degree of implicitation. `IMPLICITATION FOR DIFFUSION` is set to `1.0` by default. Read more in section 6.4 of the {{ tm3d }}.

The parameter `FREE SURFACE GRADIENT` can be used for increasing the stability of a model. Its default value is `1.0`, but it can be reduced to `0.1` to achieve stability.

(tm3d-slf-vertical)=
### Vertical (3d) Parameters

**The following descriptions refer to section 4.1 in the {{ tm3d }}.**

Telemac3d will add *Horizontal levels* (i.e., layers) that correspond to copies of the 2d-mesh to build a 3d-mesh of prisms (default) or tetrahedrons. These parameters can be defined with:

* `NUMBER OF HORIZONTAL LEVELS`: `5` where the default and minimum is `2` and the horizontal levels point in upward vertical direction. The thickness of vertical layers results from the water depth, which can be user-defined through the `INITIAL ELEVATION` parameter (see the section on {ref}`3d initial conditions <tm3d-slf-init>`).
* `MESH TRANSFORMATION`: `1` is the kind of level for the distribution (default is `1`, a homogenous sigma distribution). For unsteady (quasi-steady) simulations, set this value to `2` (or `0` - calcot) and implement a `ZSTAR` array in a user Fortran file (`USER_MESH_TRANSFORM` subroutine).
* `ELEMENT`: `'PRISM'` (default) and prisms can optionally split into tetrahedrons by settings this parameter to `'TETRAHEDRON'` (can potentially crash the simulation).

```{admonition} Unsteady (quasi-steady) simulations
:class: tip
For unsteady simulations (time-variable inflow/outflow rates), pre-define the thickness of vertical layers with the `ZSTAR` parameter in a user Fortran file (subroutine) as described in section 4.1 of the {{ tm3d }}. Read more about setting up an unsteady simulation with TELEMAC in the {ref}`Telemac2d unsteady tutorial <chpt-unsteady>`.
```

To get started with writing subroutines (it is no magic neither), have a look at the **bottom_bc** example (`~/telemac/v8p2/examples/telemac3d/bottom_bc/`). In particular, examine the user fortran file `/user_fortran-source/user_mesh_transf.f` and its call in the steering file `t3d_bottom_source.cas` through the definition of the `FORTRAN FILE` keyword and setting of `MESH TRANSFORMATION : 2`.

(tm3d-slf-boundaries)=
### Open (Liquid) Boundaries

**The following descriptions refer to section 4.2 in the {{ tm3d }}.**

In river analyses, the non-hydrostatic version of TELEMAC should be used through the following keyword: `NON-HYDROSTATIC VERSION : YES`.

Depending on the type of analysis, the solver-related parameters of `SOLVER`, `SOLVER OPTIONS`, `MAXIMUM NUMBER OF ITERATION`, `ACCURACY`, and `PRECONDITIONING` may be modified. The provided [steady3d.cas](https://github.com/hydro-informatics/telemac/raw/main/steady3d-tutorial/steady3d.cas) includes solver keywords and comments for modifications, but the default options already provide a coherent a stable setup. Read more about solver parameters in section 6.5 of the {{ tm3d }}.

Parameters for **Boundary Conditions** enable the definition of roughness laws and properties of liquid boundaries.

With respect to roughness, TELEMAC developers recommend using the {cite:t}`nikuradse_stromungsgesetze_1933` roughness law in 3d (number `5`), because all others are not meaningful or not integrally implemented in the 3d version. To apply the {cite:t}`nikuradse_stromungsgesetze_1933` roughness law to the bottom and the boundaries use:

* `LAW OF BOTTOM FRICTION`: `5`
* `LAW OF FRICTION ON LATERAL BOUNDARIES`: `5`, which can well be applied to model natural banks, or set to `0` (no-slip) for symmetry.<br>*Note that the {ref}`boundary conditions file <bnd-mod>` sets the `LIUBOR` and `LIVBOR` for the `leftwall` and `rightwall` boundary edges to zero, to enable friction.
* `FRICTION COEFFICIENT FOR THE BOTTOM`: `0.1` corresponds to 3 times a hypothetical *d90* (grain diameter of which 90% of the surface grain mixture are finer) according to {cite:p}`vanrijn2019`.
* `FRICTION COEFFICIENT FOR LATERAL SOLID BOUNDARIES`: `0.1` corresponds to 3 times a hypothetical *d90*, similar as for the bottom.

The liquid boundary definitions for `PRESCRIBED FLOWRATES` and `PRESCRIBED ELEVATIONS` correspond to the definitions of the **downstream** boundary edge in line 2 and the **upstream** boundary edge in line 3 (see {ref}`boundary definitions section <bnd-mod>`). From the boundary file, TELEMAC will understand the **downstream** boundary as edge number **1** (first list element) and the **upstream** boundary as edge number **2** (second list element). Hence:

* The list parameter `PRESCRIBED FLOWRATES : 35.;35.` assigns a flow rate of 35 m$^3$/s to the **downstream** and the **upstream** boundary edges.
* The list parameter `PRESCRIBED ELEVATIONS : 0.;371.33` assigns no elevation to the **upstream** boundary (number 1) and an elevation of 371.3 m a.s.l. to the **downstream** boundary (number 2). To recall how TELEMAC counts open boundaries read the comment box in the {ref}`steady2d tutorial <tm2d-bounds>`.

The `0.` value for the water does physically not make sense at the upstream boundary, but because they do not make sense, and because the boundary file (`boundaries.cli`) only defines (*prescribes*) a flow rate (by setting `LIUBOR` and `LIVBOR` to `5`), TELEMAC will ignore the zero-water depth at the upstream boundary.

Instead of a list in the steering `*.cas` file, the liquid boundary conditions can also be defined with a liquid boundary condition file in *ASCII* text format. For this purpose, a `LIQUID BOUNDARIES FILE` or a `STAGE-DISCHARGE CURVES FILE` (sections 4.3.8 and 4.3.10 in the {{ tm3d }}, respectively can be defined. The [steady3d.cas](https://github.com/hydro-informatics/telemac/raw/main/steady3d-tutorial/steady3d.cas) file includes these keywords in the *COMPUTATION ENVIRONMENT* section, though they are disabled through the `/` character at the beginning of the line. A liquid boundary file (*QSL*) may look like this:

```fortran
# t3d_canal.qsl
# time-dependent inflow upstream-discharge Q(2) and outflow downstream-depth SL(1)
T           Q(2)     SL(1)
s           m3/s     m
0.            0.     374.0
500.        100.     375.0
5000.       150.     575.7
```

```{admonition} ELEVATION versus DEPTH
:class: note
The `ELEVATION` parameter in the `*.cas` file denotes water depth, while the `ELEVATION` keyword in an external liquid boundary file (e.g. stage-discharge curve) refers to absolute (geodetic) elevation (`Z` plus `H`).
```

With a prescribed flow rate, a horizontal and a vertical velocity profile can be prescribed for all liquid boundaries. With only a **downstream** and an **upstream** liquid boundary (in that order according to the above-defined boundary file), the velocity profile keywords are lists of two elements each, where the first entry refers to the **downstream** and the second element to **upstream** boundary edges:

* `VELOCITY PROFILES`: `1;1` is the default option for the **horizontal** profiles. If set to `2;2`, the velocity profiles will be read from the boundary condition file.
* `VELOCITY VERTICAL PROFILES`: `2;2` sets the **vertical** velocity profiles to logarithmic. The default is `1;1` (constant). Alternatively, a user-defined `USER_VEL_PROF_Z` subroutine can be implemented in a Fortran file.

Read more about options for defining velocity profiles in section 4.3.12 of the {{ tm3d }}.

(tm3d-slf-init)=
### Initial Conditions
The **initial conditions** describe the condition at the beginning of the simulation. This tutorial uses a constant elevation (corresponding to a constant water depth) of `2.`, and enables using an initial guess for the water depth to speed up the simulation:

* `INITIAL CONDITIONS`: `'CONSTANT ELEVATION'` can alternatively be set to `'CONSTANT DEPTH'`
* `INITIAL DEPTH`: `0.1` corresponds to water depth.
* `INITIAL GUESS FOR DEPTH`: `1` must be an **integer** value and speeds up the calculation (convergence).


### Turbulence

**The following descriptions refer to section 5.2 in the {{ tm3d }}.**

The fundamental principles of turbulence and its application to the {term}`Navier-Stokes equations` are explained in the {ref}`steady Telemac2d tutorial <tm2d-turbulence>`. In 3d, TELEMAC developers recommend using either the $k-\epsilon$ model (`3`) or the {cite:t}`spalart1992` model (`5`) in lieu of the mixing length model (`2`):

* `HORIZONTAL TURBULENCE MODEL`: `3`
* `VERTICAL TURBULENCE MODEL`: `3`

If the `VERTICAL TURBULENCE MODEL` is set to `2` (`'MIXING LENGTH'`), a `MIXING LENGTH MODEL` can be assigned. The default is `1`, which is preferable for strong tidal influences and a value of `3` sets the length for computing vertical diffusivity to {cite:t}`nezu1993`.



## Run Telemac3d

Go to the configuration folder of the local TELEMAC installation (e.g., `~/telemac/v8p2/configs/`) and launch the environment (e.g., `pysource.openmpi.sh` - use the same as for compiling TELEMAC).

```
cd ~/telemac/v8p2/configs
source pysource.openmpi.sh
```

````{admonition} If you are using the Hydro-Informatics (Hyfo) Mint VM
:class: note, dropdown

If you are working with the {ref}`Mint Hyfo VM <hyfo-vm>`, load the TELEMAC environment as follows:

```
cd ~/telemac/v8p2/configs
source pysource.hyfo-dyn.sh
```
````

With the TELEMAC environment loaded, change to the directory where the above-created 3d-flume simulation lives (e.g., `/home/telemac/v8p2/mysimulations/steady3d-tutorial/`) and run the `*.cas` file by calling the **telemac3d.py** script.

```
cd ~/telemac/v8p2/mysimulations/steady3d-tutorial/
telemac3d.py steady3d.cas
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
                            17  SECONDS
... merging separated result files

... handling result files
       moving: r3dsteady.slf
... deleting working dir

My work is done
```
