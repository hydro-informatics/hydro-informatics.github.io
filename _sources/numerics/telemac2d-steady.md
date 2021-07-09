(telemac2d-steady)=
# Steady 2d Simulation

```{admonition} Requirements
This tutorial is designed for **advanced beginners** and before diving into this tutorial make sure to complete the {ref}`TELEMAC pre-processing tutorial <slf-prepro-tm>`.

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

The steering file has the file ending `*.cas` (presumably derived from the French word *cas*, which means *case* in English). The `*.cas` file is the main simulation file with information about references to the two always mandatory files (i.e., the [SELAFIN / SERAFIN](https://gdal.org/drivers/vector/selafin.html) `*.slf` geometry and the `*.cli` boundary files) and optional files, as well as definitions of simulation parameters. The steering file can be created or edited with a basic text editor or advanced software such as {ref}`Fudaa PrePro <fudaa>` or {ref}`Blue Kenue <bluekenue>`. This tutorial uses {ref}`Notepad++ <npp>` as basic text editor to minimize the number of software involved.

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

```fortran
/---------------------------------------------------------------------
/ TELEMAC2D Version v8p2
/ STEADY HYDRODYNAMICS TRAINING
/---------------------------------------------------------------------

/ steady2d.cas
/------------------------------------------------------------------/
/			COMPUTATION ENVIRONMENT
/------------------------------------------------------------------/
TITLE : '2d steady'
/
BOUNDARY CONDITIONS FILE : boundaries.cli
GEOMETRY FILE            : qgismesh.slf
RESULTS FILE           : r2dsteady.slf
/
MASS-BALANCE : YES / activates mass balance printouts - does not enforce mass balance
VARIABLES FOR GRAPHIC PRINTOUTS : U,V,H,S,Q,F / Q enables boundary flux equilibrium controls
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
/ General solver parameters
DISCRETIZATIONS IN SPACE : 11;11
FREE SURFACE GRADIENT COMPATIBILITY : 0.1  / default 1.
ADVECTION : YES
/
/ STABILITY CONTROLS
PRINTING CUMULATED FLOWRATES : YES
DESIRED COURANT NUMBER : 0.9
/
/ FINITE ELEMENT SCHEME PARAMETERS
/------------------------------------------------------------------
TREATMENT OF THE LINEAR SYSTEM : 2 / default is 2 - use 1 to avoid smoothened results
SCHEME FOR ADVECTION OF VELOCITIES : 14 / alternatively keep 1
SCHEME FOR ADVECTION OF TRACERS : 5
SCHEME FOR ADVECTION OF K-EPSILON : 14
IMPLICITATION FOR DEPTH : 0.55 / should be between 0.55 and 0.6
IMPLICITATION FOR VELOCITY : 0.55 / should be between 0.55 and 0.6
IMPLICITATION FOR DIFFUSION OF VELOCITY : 1. / v8p2 default
IMPLICITATION COEFFICIENT OF TRACERS : 0.6 / v8p2 default
MASS-LUMPING ON H : 1.
MASS-LUMPING ON VELOCITY : 1.
MASS-LUMPING ON TRACERS : 1.
SUPG OPTION : 0;0;2;2 / classic supg for U and V
/
/ SOLVER
/------------------------------------------------------------------
INFORMATION ABOUT SOLVER : YES
SOLVER : 1
MAXIMUM NUMBER OF ITERATIONS FOR SOLVER : 200 / maximum number of iterations when solving the propagation step
MAXIMUM NUMBER OF ITERATIONS FOR DIFFUSION OF TRACERS : 60 / tracer diffusion
MAXIMUM NUMBER OF ITERATIONS FOR K AND EPSILON : 50 / diffusion and source terms of k-e
/
/ TIDAL FLATS
TIDAL FLATS : YES
CONTINUITY CORRECTION : YES / default is NO
OPTION FOR THE TREATMENT OF TIDAL FLATS : 1
TREATMENT OF NEGATIVE DEPTHS : 2 / value 2 or 3 is required with tidal flats - default is 1
/
/ MATRIX HANDLING
MATRIX STORAGE : 3 / default is 3
/
/ BOUNDARY CONDITIONS
/------------------------------------------------------------------
/ Friction
LAW OF BOTTOM FRICTION : 4 / 4-Manning
FRICTION COEFFICIENT : 0.03 / Roughness coefficient
/
/ Liquid boundaries
PRESCRIBED FLOWRATES  : 35.;35.
PRESCRIBED ELEVATIONS : 0.;371.33
/
/ Type of velocity profile can be 1-constant normal profile (default) 2-UBOR and VBOR in the boundary conditions file (cli) 3-vector in UBOR in the boundary conditions file (cli) 4-vector is proportional to the root (water depth, only for Q) 5-vector is proportional to the root (virtual water depth), the virtual water depth is obtained from a lower point at the boundary condition (only for Q)
VELOCITY PROFILES : 4;1
/
/ INITIAL CONDITIONS
/ ------------------------------------------------------------------
INITIAL CONDITIONS : 'CONSTANT DEPTH' / use ZERO DEPTH to start with dry model conditions
INITIAL DEPTH : 1 / INTEGER for speeding up calculations
/
/------------------------------------------------------------------/
/			TURBULENCE
/------------------------------------------------------------------/
/
DIFFUSION OF VELOCITY : YES / default is YES
TURBULENCE MODEL : 3

&ETA
```

```{admonition} What means &ETA?
:class: note
The `&ETA` keyword at the bottom of the `*.cas` template file makes TELEMAC printing out keywords and the values assigned to them when it runs its *Damocles* algorithm.
```
````

### General Parameters

The general parameters define the computation environment starting with a simulation title and the most important links to the two mandatory input files:

* `BOUNDARY CONDITIONS FILE` : `boundaries.cli` - with a *MED* file, use a *BND* boundary file
* `GEOMETRY FILE`: `qgismesh.slf`

The model **output** can be defined with the following keywords:

* `RESULTS FILE` : `r2dsteady.slf` - can be either a *MED* file or a *SLF* file
* `VARIABLES FOR GRAPHIC PRINTOUTS`:  `U,V,H,S,Q,F` - many more options can be found in section 1.317 (page 85) of the {{ tm2dref }}.

The velocities (`U` and `V`), the water depth (`H`), and the discharge (`Q`) are standard variables that should be used in every simulation. In particular, the discharge (`Q`) is required to check when a (steady) flow converges at the inflow and outflow boundaries. Moreover, the discharge (`Q`) enables to trace fluxes along any user-defined line in the model. The procedure for verifying and identify discharges is described in the {ref}`discharge verification <verify-steady-tm2d>` section in the post-processing.

The time variables (`TIME STEP` and `NUMBER OF TIME STEPS`) define the simulation length and the printout periods (`GRAPHIC PRINTOUT PERIOD` and `LISTING PRINTOUT PERIOD`) define the result output frequency. The **smaller the printout period**, **the longer will take the simulation** because writing results is one of the most time-consuming processes in numerical modeling. The printout periods (frequencies) refer to a multiple of the `TIME STEPS` parameter and need to be a smaller number than the `NUMBER OF TIME STEPS`. Read more about time step parameters in the {{ tm2d }} in sections 5 and 12.4.2.

In addition, the `MASS-BALANCE : YES` setting will print out the mass fluxes and errors in the computation region, which is an important parameter for verifying the plausibility of the model. Note that this keyword only enables mass balance printouts and does not imply mass balance of the model, which must be achieved through a consistent model setup following this tutorial and the {{ tm2d }}.

````{admonition} Expand to view the GENERAL PARAMETERS used in this tutorial
:class: note, dropdown
```fortran
TITLE : '2d steady flow'
/
BOUNDARY CONDITIONS FILE : boundaries.cli
GEOMETRY FILE : qgismesh.slf
RESULTS FILE : r2dsteady.slf
/
MASS-BALANCE : YES / activates mass balance printouts - does not enforce mass balance
VARIABLES FOR GRAPHIC PRINTOUTS : U,V,H,S,Q,F / Q enables boundary flux equilibrium controls
/
TIME STEP : 1.
NUMBER OF TIME STEPS : 8000
GRAPHIC PRINTOUT PERIOD : 100
LISTING PRINTOUT PERIOD : 100
```
````

(tm2d-numerical)=
### General Numerical Parameters

**The following descriptions refer to section 7.1 in the {{ tm2d }}.**

Telemac2d comes with three solvers for approximating the depth-averaged {term}`Navier-Stokes equations` (shallow water) {cite:p}`p. 262 in <kundu_fluid_2008>` that can be chosen by adding an **EQUATIONS** keyword:

* `EQUATIONS : SAINT-VENANT FE` is the **default** that make Telemac2d use a Saint-Venant finite element method,
* `EQUATIONS : SAINT-VENANT FV` makes Telemac2d use a Saint-Venant finite volume method, and
* `EQUATIONS : BOUSSINESQ` makes Telemac2d use the {term}`Boussinesq` approximations (constant density except in the vertical momentum equation).

In addition, a type of discretization has to be specified with the **DISCRETIZATIONS IN SPACE** keyword, which is a list of five integer values. The five list elements define spatial discretization scheme for (1) velocity, (2) depth, (3) tracers, (4) $k-\epsilon$ turbulence, and (5) $\tilde{\nu}$ advection (Spalart-Allmaras). The minimum length of the keyword list is 2 (for velocity and depth) and all other elements are optional. The list elements may take the following values defining spatial discretization:

* `11` (default) activates triangular discretization in space (i.e., 3-node triangles),
* `12` activates quasi-bubble discretization with 4-node triangles, and
* `13` activates quadratic discretization with 6-node triangles.

The {{ tm2d }} recommend using the default value of `DISCRETIZATIONS IN SPACE : 11;11` that assign a linear discretization for velocity and water depth (computationally fastest). The option `12;11` may be used to reduce free surface instabilities or oscillations (e.g., along with steep bathymetry gradients). The option `13;11` increases the accuracy of results, the computation time, memory usage, and it is currently not available in Telemac2d.

In addition, the **FREE SURFACE GRADIENT** keyword can be defined for increasing the stability of a model. Its default value is `1.0`, but it can be reduced close to zero to achieve stability. The developers propose a minimum value of `0.`, but this would lead to non-meaningful results and this is why this eBook recommends a value slightly higher than zero. For instance, the following keyword combination may reduce surface instabilities (also referred to as *wiggles* or *oscillations*):

```fortran
DISCRETIZATIONS IN SPACE : 12;11
FREE SURFACE GRADIENT : 0.03
```

By default {term}`Advection` is activated through the keyword `ADVECTION : YES` and it can be deactivated for particular terms only:

```fortran
ADVECTION OF H : NO / deactivates depth advection
ADVECTION OF U AND V : NO / deactivates velocity advection
ADVECTION OF K AND EPSILON : NO / deactivates turbulent energy and dissipation (k-e model) or the Spalart-Allmaras advection
ADVECTION OF TRACERS : NO / deactivates tracer advection
```

The **PROPAGATION** keyword (default: `YES`) affects the modeling of propagation and related phenomena. For instance, disabling propagation (`PROPAGATION : NO`) will also disable {term}`Diffusion`. The other way round, when propagation is enabled, {term}`Diffusion` can be disabled separately. Read more about {term}`Diffusion` in Telemac2d in the {ref}`turbulence <tm2d-turbulence>` section.

(tm2d-fe)=
### Numerical Parameters for Finite Elements

**The following descriptions refer to section 7.2.1 in the {{ tm2d }}.**

Telemac2d uses finite elements for iterative solutions to the {term}`Navier-Stokes equations`. To this end, a **TREATMENT OF THE LINEAR SYSTEM** keyword enables replacing the original set of equations (option `1`) involved in TELEMAC's finite element solver with a generalized wave equation (option `2`). The replacement (i.e., the use of the **generalized wave equation**) is set to **default since v8p2** and decreases computation time, but smoothens the results. The default (`TREATMENT OF THE LINEAR SYSTEM : 2`) automatically activates mass lumping for depth and velocity, and implies explicit velocity diffusion.

```{admonition} Use SCHEME FOR ADVECTION in lieu of TYPE OF ADVECTION
:class: note, dropdown
The **TYPE OF ADVECTION** keyword is a list of four integers that define the advection schemes for (1) velocities (both $u$ and $v$), (2) water depth $h$, (3) tracers, and (4) turbulence ($k-\epsilon$ or $\tilde{\nu}$). The value provided for (2) depth is ignored since v6p0 and a list of two values is sufficient in the absence of (3) tracers and a specific (4) turbulence model. Thus, in lieu of `TYPE OF ADVECTION`, the `SCHEME FOR ADVECTION OF VELOCITIES` keyword may be used. The default is `TYPE OF ADVECTION : 1;5;1;1` (where the `5` for depth refers to an older Telemac2d version and does not trigger the PSI scheme). **The {{ tm2d }} state that the TYPE OF ADVECTION keyword will be deprecated in future releases.**
```

The {{ tm2d }} state that the following scalar **SCHEME FOR ADVECTION** keywords apply instead of the soon deprecated TYPE OF ADVECTION list:

```fortran
SCHEME FOR ADVECTION OF VELOCITIES : 1 / default
SCHEME FOR ADVECTION OF TRACERS : 1 / default
SCHEME FOR ADVECTION OF K-EPSILON : 1 / default
```

The three `SCHEME FOR ADVECTION` scalar keywords values may take the following values:

* `1` sets a not mass-conservative method of characteristics (default for all);
* `2` sets a semi-implicit scheme and activates the Streamline Upwind Petrov Galerkin (SUPG - see below);
* `3`, `4`, `13`, and `14` activate the so-called NERD scheme (these numbers activate different schemes in 3d only);
* `5` sets a mass-conservative PSI distributive scheme; and
* `15` sets the mass-conservative ERIA scheme that works with tidal flats.

Options `4` and `5` require that the {term}`CFL` condition is smaller than 1.

````{admonition} Recommended SCHEME OF ADVECTION ... keywords
:class: tip
The {{ tm2d }} recommend specific combinations depending on the simulation scenario.

For models **without any dry zones** use:
```fortran
SCHEME FOR ADVECTION OF VELOCITIES : 4 / alternatively keep 1
SCHEME FOR ADVECTION OF TRACERS : 5
SCHEME FOR ADVECTION OF K-EPSILON : 4
```

For models with **tidal flats** use (like in this tutorial):
```fortran
SCHEME FOR ADVECTION OF VELOCITIES : 14 / alternatively keep 1
SCHEME FOR ADVECTION OF TRACERS : 5
SCHEME FOR ADVECTION OF K-EPSILON : 14
```
````

**Without any SCHEME FOR ADVECTION ...** keyword, the **SUPG OPTION** (Streamline Upwind Petrov Galerkin) keyword defines if upwinding applies and what type of upwinding applies. The `SUPG OPTION` is a list of four integers that may take the following values:

* `0` disables upwinding,
* `1` enables upwinding with a classical SUPG scheme (recommended when the {term}`CFL` condition is unknown), and
* `2` enables upwinding with a modified SUPG scheme, where upwinding equals the {term}`CFL` condition (recommended when the {term}`CFL` condition is small).

The default is `SUPG OPTION : 2;2;2;2`, where

* the first list element refers to flow velocity (default `2`),
* the second to water depth (default `2` - set to `0` when `MATRIX STORAGE : 3`),
* the third to tracers (default `2`), and
* the last (fourth) to the k-epsilon model (default `2`).

Note that the `SUPG OPTION` keyword **is not optional** for many keyword combinations and this tutorial uses `SUPG OPTION : 0;0;2;2`.

**Implicitation parameters** (`IMPLICITATION FOR DEPTH`, `IMPLICITATION FOR VELOCITIES`, and `IMPLICITATION FOR DIFFUSION OF VELOCITY`) apply to the semi-implicit time discretization used in Telemac2d. To enable cross-version compatibility, implicitation parameters should be defined in the `*.cas` file. For `DEPTH` and `VELOCITIES` use values between `0.55` and `0.60` (**default is `0.55` since v8p1**); for `IMPLICITATION FOR DIFFUSION OF VELOCITY` set the v8p2 default of `1.0`.

The default `TREATMENT OF THE LINEAR SYSTEM : 2` involves so-called **mass lumping**, which leads to a smoothening of results. Specific mass lumping keywords and values are required for the flux control option of the `TREATMENT OF NEGATIVE DEPTHS` keyword and the default value for the treatment of tidal flats. To this end, the mass lumping keywords should be defined as:

```fortran
MASS-LUMPING ON H : 1.
MASS-LUMPING ON VELOCITY : 1.
MASS-LUMPING ON TRACERS : 1.
```

In addition, `MASS-LUMPING FOR WEAK CHARACTERISTICS : 1.` may be defined, which will make Telemac2d using weak characteristics (see below). The default value of any `MASS-LUMPING ...` keyword is `0.` and the maximum value is `1.`, which makes mass matrices diagonal.

The **OPTION OF CHARACTERISTICS** keyword defines the method of characteristics that can take a **strong (default of `1`)** or a **weak (`2`)** form. A weak form decreases {term}`Diffusion`, is more conservative, and increases computation time. Telemac2d automatically switches from the default strong (`1`) to the weak (`2`) form when

* the `TYPE OF ADVECTION` is set to `1`,
* any `SCHEME FOR ADVECTION ...` is set to `1`, or
* any `SCHEME OPTION FOR ADVECTION OF ...` is set to `2`.

None of these options should be used with tracers because they are not mass-conservative.

### Numerical Parameters for Finite Volumes

The finite volume method is mentioned here for completeness and detailed descriptions are available in section 7.2.2 of the {{ tm2d }}.

The finite volume method involves the definition of a scheme through the **FINITE VOLUME SCHEME** keyword that can take integer values:

* `0` enables the {cite:t}`roe1981ars` scheme ,
* `1` is the **default** and enables the kinetic scheme {cite:p}`audusse2000`,
* `3` enables the {cite:t}`zokagoa2010` scheme that is incompatible with tidal flats,
* `4` enables the {cite:t}`tchamen1998` scheme for modelling wetting and drying of a complex bathymetry,
* `5` enables the frequently use Harten Lax Leer-Contact (HLLC) scheme {cite:p}`toro2009a`, and
* `6` enables the Weighted Average Flux (WAF) {cite:p}`ata2012` scheme where parallelism is currently not implemented.

All finite volume schemes are explicit and potentially subjected to instability. For this reason, a desired {term}`CFL` condition and a variable timestep are recommended to be defined:

```fortran
DESIRED COURANT NUMBER : 0.9
VARIABLE TIME-STEP : YES / default is NO
```

The variable timestep will cause irregular listing outputs, while the graphic output frequency stems from the above-defined `TIME STEP`. Note that **this tutorial uses VARIABLE TIME-STEP : NO** because it uses finite elements.

The **FINITE VOLUME SCHEME TIME ORDER** keyword defines the second-order time scheme, which is by default set to *Euler explicit* (`1`). Setting the time scheme order to `2` makes Telemac2d using the Newmark scheme where an integration coefficient may be used to change the integration parameter (`NEWMARK TIME INTEGRATION COEFFICIENT : 1` corresponds to *Euler explicit*). To implement these options in the steering file, use the following settings:

```fortran
FINITE VOLUME SCHEME TIME ORDER : 2 / default is 1 - Euler explicit
NEWMARK TIME INTEGRATION COEFFICIENT : 0.5 / default is 0.5
```

Depending on the type of analysis, the solver-related parameters of `SOLVER`, `SOLVER OPTIONS`, `MAXIMUM NUMBER OF ITERATION FOR SOLVER`, and `TIDAL FLATS` may be modified.

(tm2d-solver-pars)=
### Numerical Solver Parameters

**The following descriptions refer to section 7.3.1 in the {{ tm2d }}.**

The solver can be selected and specified with the **SOLVER**, **SOLVER FOR DIFFUSION OF TRACERS**, and **SOLVER FOR K-EPSILON MODEL** keywords where the following settings are recommended values:

```fortran
SOLVER : 1 / default is 3
SOLVER FOR DIFFUSION OF TRACERS : 1
SOLVER FOR K-EPSILON MODEL : 1
```

Setting the `SOLVER` to `1` instead of the default value of `3` is recommended with `TREATMENT OF THE LINEAR SYSTEM : 2` (i.e., the default since v8p2) to write consistent and backward-compatible steering files.

Every solver keyword can take an integer value between `1` and `8`, where `1`-`6` use conjugate gradient methods:

* `1` sets the conjugate gradient method for symmetric matrices,
* `2` sets the conjugate residual method,
* `3` sets the conjugate gradient on normal equation method,
* `4` sets the minimum error method,
* `5` sets the squared conjugate gradient method,
* `6` sets the stabilized biconjugate gradient (BICGSTAB) method,
* `7` sets the Generalised Minimum RESidual (**GMRES**) method, and
* `8` set the Yale university direct solver (YSMP) that does not work with parallelism.

The **GMRES method may be enabled with the finite element scheme**, where the following solver options for the {term}`Krylov space`:

```fortran
SOLVER OPTION : 2 / hydrodynamic propagation
SOLVER OPTION FOR TRACERS DIFFUSION : 2 / tracer diffusion
OPTION FOR THE SOLVER FOR K-EPSILON MODEL : 2 /  k-e or Spalart-Allmaras
```

The solver options vary between values of **`2` for a small mesh** and **`5` for a large mesh**. Integers between `2` and `5` can be used for medium-sized meshes. The {{ tm2d }} recommends running simulations multiple times for finding an optimum value, where higher values (close to `5`) increase the time required for an iteration but lead to faster convergence.

(tm2d-accuracy)=
### Numerical Accuracy

**The following descriptions refer to section 7.3.2 in the {{ tm2d }}.**

The accuracy keywords make Telemac2d stop an iteration when two consecutive solutions for the same element vary by less than an **ACCURACY** threshold. To this end, the following default accuracy thresholds may be varied (Telemac2d ignores non-relevant parameters):

```fortran
SOLVER ACCURACY : 1.E-4 / propagation steps
ACCURACY FOR DIFFUSION OF TRACERS : 1.E-6 / tracer diffusion
ACCURACY OF K : 1.E-9 / diffusion and source terms of turbulent energy transport
ACCURACY OF EPSILON : 1.E-9 / diffusion and source terms of turbulent dissipation transport
ACCURACY OF SPALART-ALLMARAS : 1.E-9 / diffusion and source terms of the Spalart-Allmaras equation
```

In experience, the solver accuracy should not be larger than `1.E-3` (10$^{-3}$). In contrast, very small accuracies will lead to longer computation times. In addition or alternatively to the accuracy keywords, the following default numbers of iterations can be modified to speed up calculations:

```fortran
MAXIMUM NUMBER OF ITERATIONS FOR SOLVER : 100 / maximum number of iterations when solving the propagation step
MAXIMUM NUMBER OF ITERATIONS FOR DIFFUSION OF TRACERS : 60 / tracer diffusion
MAXIMUM NUMBER OF ITERATIONS FOR K AND EPSILON : 50 / diffusion and source terms of k-e or Spalart-Allmaras
```

Telemac2d will print out warning messages when convergence could not be reached with the defined combination of accuracy and maximum iteration number keywords. The warning message printouts can be deactivated with the `INFORMATION ABOUT SOLVER` keyword, but deactivating convergence warnings is not recommended.

(tm2d-tidal)=
### Tidal Flats

**The following descriptions refer to section 7.5 in the {{ tm2d }}.**

The **TIDAL FLATS (default: YES)** keyword applies to the **finite elements scheme only ({ref}`EQUATIONS keyword <tm2d-numerical>`)** and can be ignored with finite volumes. The term *tidal* may be slightly confusing because tidal flats can occur beyond coastal regions. Tidal flats occur wherever there are flow transitions, such as when fast-flowing water enters a backwater zone. Flow transitions occur in almost all environments more complex than a square-like flume, and therefore, the activation of tidal flats in Telemac2d models is highly recommended. Though activating tidal flats leads to longer computation times, in most cases only with tidal flats physically reasonable results and stable models can be achieved.

The `TIDAL FLATS` keyword is linked with a couple of other Telemac2d keywords driving model stability and physical meaningfulness. The following keyword setups may be generally applied to (quasi) steady, real-world rivers and channels (as opposed to lab flumes):

```fortran
TIDAL FLATS : YES
CONTINUITY CORRECTION : YES / default is NO
OPTION FOR THE TREATMENT OF TIDAL FLATS : 1
TREATMENT OF NEGATIVE DEPTHS : 2 / value 2 or 3 is required with tidal flats
```

The **OPTION FOR THE TREATMENT OF TIDAL FLATS** accepts integer values between `1` and `3` to select one of the following schemes:

* `1` detects tidal flats and corrects the free surface gradient.
* `2` removes tidal flat elements by using a masking table that eliminates any contribution of concerned mesh elements. This option may affect the mass conservation of the model.
* `3` resembles `1` and adds a porosity term to half-dry mesh elements. This affects the amount of water in the model, which here equals the depth integral multiplied by the porosity. A user Fortran file may be used to modify the porosity term in the `USER_CORPOR` subroutine.

The **TREATMENT OF NEGATIVE DEPTHS (default: 1)** keyword defines an approach for eliminating negative water depth values where the following integer numbers can be used:

* `0` disables any treatment of negative water depths.
* `1` conservatively smoothens negative water depths (**default**).
  * A float number keyword `THRESHOLD FOR NEGATIVE DEPTHS` (default `0.`) is available only for this option.
  * Setting the threshold to, for instance, `-0.1` makes that negative water depths larger than -0.1 meters remain unchanged.
* `2` imposes a flux limitation that strictly ensures positive water depths.
* `3` acts similarly as `2` but for the ERIA {term}`Advection` scheme (set `SCHEME FOR ADVECTION OF TRACERS` to `4` or `5`). This option is appropriate for modeling conservative tracers.

````{admonition} TIDAL FLATS options require particular keyword combinations
:class: tip
The `SCHEME FOR ADVECTION ...` keywords (see the {ref}`finite element parameters <tm2d-fe>` section) must be set for `TRACERS` to LIPS (either `4` or `5`) and for all others either to a NERD (`13` or `14`) or ERIA (`15`) scheme.

When using LIPS (`4` or `5`) with NERD (`13` or `14`) use the following combination (**used in this tutorial**):
```fortran
TIDAL FLATS : YES
OPTION FOR THE TREATMENT OF TIDAL FLATS : 1
TREATMENT OF NEGATIVE DEPTHS : 2
```

When using LIPS (`4` or `5`) with ERIA (`15`) use the following combination:
```fortran
TIDAL FLATS : YES
OPTION FOR THE TREATMENT OF TIDAL FLATS : 1
TREATMENT OF NEGATIVE DEPTHS : 3
```

Read more about viable and trouble-making parameter combinations for tidal flats in section 16.5 in the {{ tm2d }}.
````

### Matrix Handling

**The following descriptions refer to section 7.6 in the {{ tm2d }}.**

Telemac2d provides multiple options for matrix handling that need to be set up for particular solver schemes.

The **MATRIX STORAGE** keyword may be set to:

* `1` for using classic element-by-element matrix storage, or
* `3` for using edge-based matrix storage (default). This default is required when any `SCHEME FOR ADVECTION ...` keyword is set to `3`, `4`, `5`, `13`, `14`, or `15`, and when any direct `SOLVER` is set to `8`.

The additional **MATRIX-VECTOR PRODUCT** keyword may be used to switch between multiplication methods for the finite element scheme. However, the default value of `1` (vector multiplication by a non-assembled matrix) should currently **not be changed** because the only alternative (`2` for frontal assembled matrix multiplication) is not implemented for parallelism and quasi-bubble discretization.

(tm2d-friction)=
### Friction Boundary Conditions

Parameters for **Boundary Conditions** enable the definition of roughness laws and properties of liquid boundaries.

**The following descriptions of friction parameters refer to section 6.1 in the {{ tm2d }}.**
The **LAW OF BOTTOM FRICTION** keyword defines a friction law for topographic boundaries, which can be set to:

* `0` for no friction.
* `1` for the {cite:t}`haaland1983` equation, which is an implicit form of the {cite:t}`colebrook1937` equation that builds on the Darcy-Weisbach friction factor $f_D$. This law involves a high degree of uncertainty that stems from the underlying experimental dataset.
* `2` for the {cite:t}`chezy_formula_1776` roughness, that can be similarly used as `3` and `4`.
* `3` for {cite:t}`strickler_beitrage_1923` roughness $k_{st}$ (read more in the {ref}` 1d hydraulics exercise <ex-1d-hydraulics>`), which is the inverse of $n_m$ (`4`).
* `4` for {cite:t}`manning_transactions_1891` roughness $n_m$ (read more in the {ref}` 1d hydraulics exercise <ex-1d-hydraulics>`), which is the inverse of $k_{st}$ (`3`).
* `5` for the {cite:t}`nikuradse_stromungsgesetze_1933` roughness law, which should correspond to 3 $\cdot D_{90}$ according to {cite:t}`vanrijn2019`.
* `6` for the logarithmic law of the wall for turbulent flows assuming that the average flow velocity is a logarithmic function of the distance from the wall beyond the viscous and buffer layers. The thickness of these layers is a function of wall roughness length {cite:p}`von_karman_mechanische_1930`.
* `7` for the {cite:t}`colebrook1937` equation that calculates the Darcy-Weisbach friction factor $f_D$ for turbulent flows in smooth pipes.

With respect to the 2d applications in this eBook, the most relevant bottom friction laws are `3` {cite:p}`strickler_beitrage_1923`, `4` {cite:p}`manning_transactions_1891`, and `6` (log law). The {cite:t}`nikuradse_stromungsgesetze_1933` roughness law (`5`) is recommended for 3d simulations (see the {ref}`Telemac3d tutorial <tm3d-hydrodynamics>`).

The **FRICTION COEFFICIENT FOR THE BOTTOM** keyword sets the value for a characteristic roughness coefficient. For instance, when the friction law keyword is set to `3` {cite:p}`strickler_beitrage_1923`, the friction corresponds to the Strickler roughness coefficient $k_{st}$ (in fictive units of m$^{1/3}$ s$^{-1}$). For rough channels (e.g., mountain rivers) $k_{st} \approx 20$ m$^{1/3}$ s$^{-1}$ and for smooth concrete-lined channels $k_{st} \approx 75$ m$^{1/3}$ s$^{-1}$. In fully turbulent flows, the Strickler roughness can be approximated as $k_{st} \approx \frac{26}{D_{90}^{1/6}}$ {cite:p}`meyer-peter_formulas_1948` where $D_{90}$ is the grain diameter of which 90% of the surface grain mixture are finer.
This tutorial features the application of the *Manning* roughness coefficient $n_m$, which is the inverse of $k_{st}$ and implemented with:

```fortran
LAW OF BOTTOM FRICTION : 4 / 4-Manning
FRICTION COEFFICIENT : 0.03 / Roughness coefficient
```

````{admonition} Expand to see exemplary values for Manning roughness
:class: tip, dropdown

{numref}`Table %s <tab-mannings-n>` lists exemplary values for the Manning roughness coefficient $n_m$ based on {cite:t}`usgs1973_n` and {cite:t}`usgs1989_n`.

```{list-table} Exemplary values for Manning roughness for straight uniform channels.
:header-rows: 1
:name: tab-mannings-n

* - Surface type
  - Material diameter (10$^{-3}$m)
  - $n_m$ (m$^{-1/3}$s)

* - Concrete
  - $-$
  - 0.012-0.018

* - Firm soil
  - $-$
  - 0.025-0.032

* - Coarse sand
  - 1-2
  - 0.026-0.035

* - Gravel
  - 2-64
  - 0.028-0.035

* - Cobble
  - 64-256
  - 0.030-0.050

* - Boulder
  - $>$ 256
  - 0.040-0.070
```

````

```{admonition} Friction zones (regional friction values)
:class: tip, dropdown
Similar to the assignment of multiple friction coefficient values to multiple model regions featured in the {ref}`BASEMENT tutorial <bm-geometry>`, Telemac2d provides routines for domain-wise (or zonal) friction definitions. Appendix E of the {{ tm2d }} provides detailed explanations for the implementation of such zonal friction values. The following tips may help to better understand the instructions in Appendix E:

* The proposed modification of the **FRICTION_USER** Fortran function (subroutine) is not mandatory. If the FRICTION_USER subroutines must be enabled anyway (e.g., to implement a new roughness law such as the {cite:t}`ferguson_flow_2007` equation):
  * The FICTION_USER subroutine can be found in `/telemac/v8p2/sources/telemac2d/friction_user.f`.
  * To use a modified version, copy `friction_user.f` to a new subfolder called `/user_fortran/` in your simulation case folder.
  * Modify and save edits in `/your/simulation/case/user_fortran/friction_user.f`.
  * Tell the steering (`*.cas`) file to use the modified FRICTION_USER Fortran file by adding the keyword `FORTRAN FILE : 'user_fortran'` (makes Telemac2d looking up Fortran files in the `/user_fortran/` subfolder).
* Useful examples are:
  * The BAW's Donau case study that lives in `/telemac/v8p2/examples/telemac2d/donau/` and features the usage of a `*.bfr` `ZONES FILE` and a `roughness.tbl` `FRICTION DATA FILE`, which are enabled through the `FRICTION DATA : YES` keyword in the `t2d_donau.cas` file. The Donau example was presented at the XXth Telemac-Mascaret user conference and the conference proceedings are available at the BAW's [HENRY portal](https://hdl.handle.net/20.500.11970/100418).
  * The [Baxter tutorial](http://www.opentelemac.org/index.php/component/jdownloads/summary/4-training-and-tutorials/185-telemac-2d-tutorial?Itemid=55) (look for the contribution *Reverse engineering of initial & boundary conditions with TELEMAC and algorithmic differentiation*).
* To assign zonal roughness values, use QGIS, Blue Kenue, and a text editor:
  * Delineate zones with different roughness coefficients draw polygons (e.g., following landscapes characteristics on a basemap) in separate shapefiles with QGIS (see also the {ref}`pre-processing tutorial on QGIS <tm-qgis-prepro>`).
  * Import the separate polygons as closed lines in Blue Kenue (see also the {ref}`pre-processing tutorial on Blue Kenue <bk-tutorial>`).
  * Assign elevations to the polygons (closed lines) in Blue Kenue (requires {ref}`elevation information <bk-xyz>`).
  * Add a new variable to the {ref}`Selafin <bk-create-slf>` geometry and call it BOTTOM FRICTION (this can be another `*.slf` file than the one where the computational mesh lives).
  * Use the {ref}`Map Object <bk-2dinterp>` function (*Tools* > *Map Object...*) to add the polygons (closed lines) to the BOTTOM FRICTION mesh variable.
  * Define zone numbers in Blue Kenue and save them (export) as `*.xyz` or `*.bfr` zones file (conversion to zones file may require opening the `*.xyz` file in a text editor and saving it from there as `*.bfr` file).
* In the `*.cas` file, make sure to set a value for the FRICTION parameter according to the above descriptions and to set the `*.slf` file with the BOTTOM FRICTION variable for the `ZONES FILE` keyword.

```

(tm2d-bounds)=
### Liquid Boundary Conditions

**The following descriptions of friction parameters refer to section 4.2 in the {{ tm2d }}.**

Liquid boundary keywords assign hydraulic properties to the spatially defined upstream and downstream liquid boundary lines in the conlim (`*.cli`) file {ref}`created with Blue Kenue <bk-liquid-bc>`. This tutorial features the assignment of steady liquid boundaries for one discharge of 35 m$^3$/s. To this end, the upstream boundary condition is set to a steady target inflow rate (*Open boundary with prescribed Q*) and the downstream boundary condition gets a {term}`Stage-discharge relation` (*Open boundary with prescribed Q and H*) assigned (recall {numref}`Fig. %s <bk-bc-types>`). Thus, for running this tutorial add the following keywords to the steering (`*.cas`) file:

* The keyword `PRESCRIBED FLOWRATES : 35.;35.` assigns a flowrate of 35 m$^3$/s to the **downstream** and the **upstream** boundary edges.
* The keyword `PRESCRIBED ELEVATIONS : 0.;371.33` assigns a water surface elevation $wse$ (or H in Telemac) of 371.33 m a.s.l. (above sea level) to the **downstream** boundary. The upstream $wse$ prescription of 0.0 makes Telemac2d ignore this value corresponding to the assigned upstream boundary type (prescribed flowrate only).

The order of prescribed flowrates (Q) and $wse$ (H) values depends on the order of the definition of the boundaries. Thus, the first list element defines values for the upstream and the second list element for the downstream open boundary.

````{admonition} How to find out the order of boundary conditions?
:class: tip
The order of open boundaries can be read from the `*.cli` file. The first open boundary that is listed in the `*.cli` file corresponds to the first list element in any `PRESCRIBED ...` keyword. An open boundary node in the `*.cli` file is characterized by the line beginning with something like `4 5 5` or `5 5 5` (i.e., anything but `2 2 2`, which corresponds to a closed wall boundary node) and BlueKenue also marks the names of open boundaries at the line ends (after the hashtag). {numref}`Figure %s <boundary-cli>` illustrates the [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/bk-slf/boundaries.cli) file used in this tutorial where the `upstream` open boundary is defined at line 7, before the definition of the downstream open boundary starting at line 313.

```{figure} ../img/telemac/boundary-cli.png
:alt: telemac 2d cli boundary conditions order cas steering file prescribed prescription
:name: boundary-cli

The [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/bk-slf/boundaries.cli) file used in this tutorial starts with the upstream boundary defined in line 7. To find the downstream boundary scroll down to line 313.
```
````

Liquid boundary conditions may be assigned to any open boundary in the `*.cli` file.

````{admonition} External files instead of PRESCRIBED-keywords
:class: note, dropdown
Instead of a list of semi-colon separated numbers in the steering file, liquid boundary conditions can also be defined with a liquid boundary condition file in *ASCII* text format. For this purpose, the `LIQUID BOUNDARIES FILE` and/or `STAGE-DISCHARGE CURVES FILE` keywords need to be defined in the steering file. External files are required for the simulation of quasi-unsteady flows (e.g., a flood hydrograph or low flow sequences for habitat conditions) and more details can be found in sections 4.2.5 and 4.2.6 in the {{ tm2d }} or the {ref}`unsteady tutorial <chpt-unsteady>`.
````

A velocity profile type can be assigned to any prescribed Q (flowrate) or prescribed U (velocity) open boundary in the form of a list that has the same element order as the above-defined `PRESCRIBED ...` keywords. For this purpose, upstream and downstream velocity profiles can be defined with the `VELOCITY PROFILES` keyword that accepts the following values:

* `1` is the default option that defines the flow velocity direction at the boundary nodes normal to their edges. This option assigns a length of $1$ to the vector and multiplies it with a numeric factor to yield a target flowrate.
* `2` reads U and V velocity profiles from the boundary conditions (`*.cli`) file, which are multiplied with a constant to yield a target flowrate.
* `3` imposes the velocity vector direction normal to the boundary and reads the value (UBOR) from the `*.cli` file, which is then multiplied by a constant to yield a target flowrate.
* `4` imposes the velocity vector direction normal to the boundary and calculates the value's norm proportional to the square root of the water depth. This option can only be used with a prescribed Q open boundary.
* `5` imposes the velocity vector direction normal to the boundary and calculates the value's norm proportional to the square root of a virtual water depth.

With the upstream boundary being a *prescribed Q* boundary, this tutorial uses `VELOCITY PROFILES : 4;1` in the steering file. Read more about options for defining velocity profiles in section 4.2.8 of the {{ tm2d }}.

(tm2d-init)=
### Initial Conditions

**The following descriptions refer to section 4.1 in the {{ tm2d }}.**

The initial conditions describe the state of the model at the beginning of a simulation. Telemac2d recognizes the following types of initial conditions, which can be defined in the steering file with the keyword `INITIAL CONDITIONS : 'TYPE'`:

* `ZERO ELEVATION` initializes the free surface elevation at 0 (**default**). Thus, the initial water depths correspond to the bottom elevation.
* `CONSTANT ELEVATION` initializes the free surface elevation at a value defined with an `INITIAL ELEVATION` keyword that has a default value of `0.`. Thus, the initial water depths correspond to the subtraction of the bottom elevation from the water surface elevation $wse$. The initial water depth is set to zero at nodes where the bottom elevation is higher than defined b the `INITIAL ELEVATION` keyword.
* `ZERO DEPTH` initializes the simulation with `0` (i.e., $wse$ corresponds to bottom elevation). Thus, the model starts with dry conditions, similar as in the {ref}`BASEMENT <basement2d>` tutorial.
* `CONSTANT DEPTH` initializes the water depths at a value defined by an INITIAL DEPTH keyword that has a default value of `0.`.
* `TPXO SATELLITE ALTIMETRY` initializes the model using the information provided from a user-defined database (e.g., the [OSU TPXO model for ocean tides](http://g.hyyb.org/archive/Tide/TPXO/TPXO_WEB/global.html)). Read more in section 4.2.12 of the {{ tm2d }} on modeling marine systems.

This tutorial uses a constant water depth initial condition of `1` (integer to speed up calculations), which corresponds to a flooded initial model state (i.e., water volume surplus):

```fortran
INITIAL CONDITIONS : 'CONSTANT DEPTH'
INITIAL DEPTH : 1
```

The simulation speed can be significantly increased when the model has already been running once at the same discharge. The result of an earlier simulation can be used for the initial condition with the `COMPUTATION CONTINUED : YES` (default is `NO`) and `PREVIOUS COMPUTATION FILE : *.slf` (provide the name of a `*.slf` file) keywords. Section 4.1.3 in the {{ tm2d }} has detailed descriptions for continuing calculations.

(tm2d-turbulence)=
### Turbulence

**The following descriptions refer to section 6.2 in the {{ tm2d }}.**

Turbulence describes a seemingly random and chaotic state of fluid motion in the form of three-dimensional vortices (eddies). True turbulence is only present in 3d vorticity and when it occurs, it mostly dominates all other flow phenomena through increases in energy dissipation, drag, heat transfer, and mixing {cite:p}`kundu_fluid_2008`. The phenomenon of turbulence has been a mystery to science for a long time, since turbulent flows have been observed, but could not be directly explained by the systems of linear equations. Today, turbulence is considered a random phenomenon that can be accounted for in linear equations, for instance, by introducing statistical parameters. For instance, when turbulence applies to the {term}`Navier-Stokes equations` a numerical solution for a quantity (e.g., flow velocity) corresponds to $value = \overline{mean value} + value fluctuation'$. For this purpose, there are a variety of options for implementing turbulence in numerical models {cite:p}`nezu1993`.

The horizontal and vertical dimensions of turbulent eddies can vary greatly, especially in rivers and transitions to backwater zones (tidal flats) where the large horizontal flow dimension (river width) is significantly larger than the vertical flow dimension (water depth). Telemac2d provides multiple turbulence models that can be applied to the vertical and horizontal dimensions and defined with the `TURBULENCE MODEL` keyword being an integer number for one of the following options:

* `1` to use a constant viscosity coefficient (**default**) for turbulent viscosity, molecular viscosity, and {term}`Diffusion`. This closure option should not be used with {term}`Stage-discharge relation` open boundaries (i.e., do not use with prescribed Q and H) {cite:p}`wilson2002`.
* `2` to use the Elder formula for the {term}`Diffusion` coefficient $D$. The Elder turbulence closure also yields small errors for {term}`Stage-discharge relation` open boundaries (i.e., do not use with prescribed Q and H) {cite:p}`wilson2002`.
* `3` to use the $k-\epsilon$ two-equation model solving the {term}`Navier-Stokes equations`. The first equation represents a turbulence closure for the turbulent energy $k$; the second equation is a turbulence closure for the turbulent dissipation $\epsilon$. Both equations express that the sum of change of $k$/$\epsilon$ in time and {term}`Advection` transport of $k$/$\epsilon$ equal the sum of {term}`Diffusion` transport of $k$/$\epsilon$, the production rate of $k$/$\epsilon$, and the destruction rate of $k$/$\epsilon$ {cite:p}`launder1974`. The $k-\epsilon$ model is a generalization of the mixing length model (see option `5`) and assumes that the turbulent viscosity is isotropic (valid for many river applications, but not for circular-rotating or groundwater flows) {cite:p}`bradshaw1987`. Thus, the $k-\epsilon$ model introduces two additional equations and requires a finer mesh than the constant viscosity option `1`, which leads to a longer computation time. Yet, the $k-\epsilon$ model generally yields accurate results and small errors with {term}`Stage-discharge relation` open boundaries (i.e., do not use with prescribed Q and H) {cite:p}`wilson2002`. The following default keywords are associated with the $k-\epsilon$ model:
  * `VELOCITY DIFFUSIVITY : 1.E-6` corresponding to the kinematic viscosity $\nu$ of water (10$^{-6}$ m$^2$/s).
  * `TURBULENCE REGIME FOR SOLID BOUNDARIES : 2` **for rough walls** of closed boundaries to apply the value chosen for the `LAW OF BOTTOM FRICTION` and `ROUGHNESS COEFFICIENT OF BOUNDARIES` keywords (recall section {ref}`tm2d-friction`). For **smooth closed boundary walls** set `TURBULENCE REGIME FOR SOLID BOUNDARIES : 1`.
  * `INFORMATION ABOUT K-EPSILON MODEL : YES` enables console output of information on the $k-\epsilon$ closure solution.
* `4` to use the {cite:t}`smagorinsky1963` (also known as *general circulation*) model, which stems from climate modeling and is appropriate for modeling maritime systems with large eddies. The {cite:t}`smagorinsky1963` model does not account for {term}`Diffusion`.
* `5` to use a mixing length model according to Prandtl's theory that a fluid quantity conserves its properties for a characteristic length before it mixes with the bulk flow {cite:p}`bradshaw1974`.
* `6` to use the {cite:t}`spalart1992` (also referred to as *Spalart-Allmaras*) model that solves the {term}`Continuity equation` for a viscosity-like, kinematic eddy turbulent viscosity. The *Spalart-Allmaras* model was originally developed for aerodynamic flows with low {term}`Reynolds number` and it has also shown good results for other applications.

This tutorial uses the $k-\epsilon$ model (`3`) because of its low error rate and wide applicability (compared to other turbulence closures).

```
DIFFUSION OF VELOCITY : YES / enabled by default
TURBULENCE MODEL : 3
```

(tm2d-run)=
## Run Telemac2d

With the steering (`*.cas`) file, the last necessary ingredient for running a steady hydrodynamic 2d simulation with Telemac2d is available. Make sure to put all required files in one simulation folder (e.g., `~/telemac/v8p2/mysimulations/steady2d-tutorial/`). The required files can also be downloaded from this eBook's [steady2d tutorial repository](https://github.com/hydro-informatics/telemac/tree/main/steady2d-tutorial/) and include:

* [qgismesh.slf](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/qgismesh.slf)
* [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/boundaries.cli)
* [steady2d.cas](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/steady2d.cas)

With these files prepared, load the TELEMAC environment and run Telemac2d following the explanations in the next sections.

### Load environment and files

Go to the configuration folder of the TELEMAC installation (e.g., `~/telemac/v8p2/configs/`) and configure the environment (e.g., `pysource.openmpi.sh` - use the same as for compiling TELEMAC.

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

To start a simulation, change to the directory (`cd`) where the simulation files live and run the steering file (`*.cas`) with the **telemac2d.py** script:

```
cd ~/telemac/v8p2/mysimulations/steady2d-tutorial/
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
T =        8000.0000

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

The post-processing of the steady 2d scenario uses QGIS only and the {ref}`PostTelemac plugin <tm-qgis-plugins>`. Alternatively, TELEMAC results can also be visualized with [ParaView](https://www.paraview.org).

## Load Results

Launch QGIS, {ref}`create a new QGIS project <qgis-project>`, set the project {term}`CRS` to `UTM zone 33N`, add a satellite imagery basemap, and save the project (e.g., as `tm2d-postpro.qgis`) in the same folder where the Telemac2d simulation results file (*r2dsteady.slf* is located), similar to the descriptions in the {ref}`pre-processing tutorial <tm-qgis-prepro>`. Then, open the PostTelemac plugin as indicated in {numref}`Fig. %s <open-post-tm>`.

```{figure} ../img/telemac/load-tm-plugin.png
:alt: qgis load open PostTelemac plugin
:name: open-post-tm

Open the PostTelemac plugin in QGIS.
```

The PostTelemac plugin typically opens as a frame at the bottom-right of the QGIS windows (sometimes hard to find). Detach the PostTelemac plugin from the main QGIS window by clicking on the resize window button in the top-right corner of the PostTelemac plugin frame (next to the *close* cross). In the detached window load the model results as follows (also indicated in {numref}`Fig. %s <post-tm>`):

* Click on the **File ...** button, navigate to the location where the simulation lives and select `r2dsteady.slf`.
* **Move the Time slider** to the last time step (e.g., `8000`) and observe the main window, which will show by default the VELOCITY U parameter in this tutorial (depends on the variables defined with the `VARIABLES FOR GRAPHIC PRINTOUTS` keyword).
* Familiarize with the PostTelemac plugin by modifying the display **Parameter** and the **Color gradient**.

```{figure} ../img/telemac/post-telemac.png
:alt: qgis load simulation results slf PostTelemac plugin
:name: post-tm

Load the Telemac2d simulation results file in the detached PostTelemac plugin window.
```

```{admonition} Find the r2dsteady layer in the QGIS *Layers* panel
:class: tip
Once imported, the *r2dsteady* layer is listed in the *Layers* panel of QGIS (typically in the bottom-left of the window). Double-clicking on the *r2dsteady* layer will re-open the PostTelemac plugin when it was closed (e.g., after restarting QGIS). Structurally, the *r2dsteady* layer is a mesh with a particular format and QGIS needs the PostTelemac plugin to properly read the data from this selafin-type mesh.
```

(tm2d-post-export)=
## Analyze Results

The PostTelemac plugin enables to export simulation results in the form of multiple formats including {term}`GeoTIFF` rasters of simulation output variables or data along nodes. In addition, the evolution of a parameter over the simulation time can be exported to a video. To export or animate results, go to the **Tools** tab (light blue box in {numref}`Fig. %s <post-tm>`).

### Export GeoTIFF

This example features the export of a flow velocity raster at the modeling end time (8000). For this purpose, click on the **RasterCreation** entry of the **Export** menu in the **Tools** tab. To export a flow velocity {term}`GeoTIFF` raster:

* Set the **time step** to `8000` (use the field indicated in {numref}`Fig. %s <posttm-export-tif>`).
* Select `6 : VITESSE` for **Parameter**.
  * *Vitesse* is French for *velocity* and it is calculated as $VITESSE = \sqrt{(VELOCITY\ U)^2 + (VELOCITY\ V)^2}$
  * Do not use `VELOCITY U` nor `VELOCITY V` because those are the flow velocities in $x$ and $y$ directions only and respectively.
* Set in the **Group** frame:
  * **Cell size** to `1`, and
  * **Extent** to `Full Extent`.
* Start the export by clicking on **Create raster**.

The processing frame can be found at the bottom of the window (scroll down by clicking on the dotted circle indicated in {numref}`Fig. %s <posttm-export-tif>`) and informs about the progress.

```{figure} ../img/telemac/posttm-export-tif.png
:alt: qgis export simulation results slf PostTelemac raster geotiff tif
:name: posttm-export-tif

Export a flow velocity raster of simulation results with the PostTelemac plugin.
```

The successful raster creation results in a new layer called **r2dsteady_raster_VITESSE**, which is automatically saved as a {term}`GeoTIFF` raster in the same folder where the QGIS project (`*.qgz`) and the `r2dsteady.slf` files are located.

{numref}`Figure %s <exported-tif>` shows the exported flow velocity raster in QGIS with a *Magma* color map (select in the layer symbology).

```{figure} ../img/telemac/qgis-exported-tif.png
:alt: qgis flow velocity vitesse results slf PostTelemac raster geotiff tif
:name: exported-tif

The exported flow velocity (VITESSE) GeoTIFF raster in QGIS.
```

```{admonition} How reasonable are the results?
:class: important
The flow velocity raster in {numref}`Fig. %s <exported-tif>` shows some non-zero pixels on the floodplains, beyond the riverbanks. However, because the modeled discharge of 35 m$^3$/s corresponds to low baseflow conditions, there should not be any water on the floodplains. These apparently wrongly modeled pixels are an artifact of the wet initial conditions that put a 1-m deep water layer all over the model. In local swales (i.e., hollows or small terrain depressions) beside the main channel, the water cannot run off and remains here until the end of the simulation. To avoid the unrealistic disconnected swales, use `INITIAL DEPTH : 0` or `INITIAL CONDITIONS : ZERO DEPTH`, which corresponds to dry initial conditions (see the {ref}`initial conditions <tm2d-init>` section). Note that initializing the model with zero depths (dry) will require open (liquid) boundary conditions of the type `PRESCRIBED Q AND H`. Thus, for starting this tutorial with dry conditions, go back to the pre-processing section on creating {ref}`Conlim Boundary Conditions <bk-bc>` and assign prescribed Q and H to both upstream and downstream open boundaries (i.e., not only at the downstream open boundary). Alternatively, set the initial depth to a very small value such as `INITIAL DEPTH : 0.01`.
```

```{admonition} Export to shapefile or mesh
:class: tip
The PostTelemac plugin also enables exporting to other geodata types such as vector shapefiles or meshes.
```

(verify-steady-tm2d)=
### Verify Discharge Convergence

The discharge convergence can be observed during the simulation in the Terminal running Telemac2d with the `PRINTING CUMULATED FLOWRATES : YES` keyword, and also later to make sure fluxes are correctly entering and leaving the model. Furthermore, it can be determined at which time step inflows and outflows converge to each other, which enables the simulation to be shortened to this moment of convergence in steady simulations.

To export flowrates along any line or at any node of the mesh, make sure that `Q` is in the list of the `VARIABLES FOR GRAPHIC PRINTOUTS` keyword. Then, go to the **Tools** tab of the PostTelemac plugin in QGIS ({numref}`Fig. %s <draw-flow-controls>`) and:

* Click on the **Flow** ribbon.
* In the **Selection** frame select **Temporary polyline** and move the mouse cursor on the map viewport where the cursor should turn into a black cross that enables drawing a (green) thick line anywhere in the mesh layer (*r2dsteady*). If the cursor does not enable drawing, go somewhere else in the PostTelemac plugin (e.g., to the *Samplingtool* ribbon), then go back to the *Flow* ribbon, click in the *Selection* frame, and re-try. To draw a line for exporting associated flows:
  * left-click with the mouse cursor somewhere on the *r2dsteady* mesh on the map (e.g., the left bank at the inflow open boundary indicated in {numref}`Fig. %s <draw-flow-controls>`), and
  * double left-click on another point on the *r2dsteady* mesh (e.g., the right bank at the inflow open boundary indicated in {numref}`Fig. %s <draw-flow-controls>`).
  * The PostTelemac plugin then automatically draws the shortest path between the two points along the mesh nodes.
* The flow rate across the green line is now plotted in the graph of the PostTelemac plugin for the simulation time (e.g., timesteps `0` to `8000` in {numref}`Fig. %s <draw-flow-controls>`).
* To save the values for comparison at another line, click on **Copy to clipboard** and paste the values in a spreadsheet office software, such as {ref}`Libre Office <lo>`.

**Repeat** the procedure **at the downstream open boundary** and paste the values in another column of the spreadsheet used for the upstream open boundary.

```{figure} ../img/telemac/flow-control-us.png
:alt: qgis flow rate discharge control section Post Telemac convergence
:name: draw-flow-controls

Draw polylines along mesh nodes and export associated flows (Copy to clipboard).
```

```{admonition} A more consistent way to export fluxes along lines...
A more consistent way to verify fluxes at open boundaries or other particular lines (e.g., tributary inflows or diversions) is to use the `CONTROL SECTIONS` keyword. A control section is defined by a sequence of neighboring node numbers and the {{ tm2d }} provides detailed explanations in section 5.2.
```

The diagram in {numref}`Fig. %s <convergence-diagram-tm2d>` plots the two columns of flows at the upstream and downstream open boundaries over time for the simulation setup in this tutorial. The diagram suggests that the model reaches stability after the 55th output listing (simulation time $t \leq 5500$). Thus, the simulation time could be limited to $t = 6000$, but a simulation time of $t = 5000$ would be too short.

```{figure} ../img/telemac/convergence-diagram-tm.png
:alt: telemac2d convergence steady model simulation discharge verification validation
:name: convergence-diagram-tm2d

Convergence of inflow (upstream) and outflow (downstream) at the open model boundaries.
```

Note the difference between the convergence duration in this steady simulation with Telemac2d that starts with an initial condition of 1.0 m water depth (plot in {numref}`Fig. %s <convergence-diagram-tm2d>`) compared to the longer convergence duration in the BASEMENT tutorial (plot in {numref}`Fig. %s <convergence-diagram-bm>`) that starts with a dry model. This difference mainly stems from the type of initial conditions (initial depth versus dry channel) that also reflects in an outflow surplus of the Telemac2d simulation and a zero-outflow in the BASEMENT simulation at the beginning of the simulations. However, the faster convergence is at the cost of unrealistically wetted hollows in the Telemac2d simulation - read more in the above comment: *How reasonable are the results?*

(tm2d-dry)=
## Initialize Dry
For comparison, try running the Telemac2d simulation with initial dry conditions. To this end, change the upstream boundary type to `5 5 5` (prescribed H and Q) in the  {ref}`boundaries.cli <bk-liquid-bc>` file. For making this modification, it is sufficient to **open boundaries.cli in any text editor** and use its **find-and-replace** function (e.g., `CTRL` + `H` keys in {ref}`npp`, or `CTRL` + `F` keys in {ref}`install-atom`):

 * In the **Find** field type `4 5 5`.
 * In the **Replace with** field type `5 5 5`.
 * Click on **Replace ALL**.
 * Save and close **boundaries.cli**.

In the Telemac2d steering (`*.cas`) file comment out the `INITIAL DEPTH` keyword, change the `INITIAL CONDITIONS` keyword to `ZERO DEPTH`, and change the `PRESCRIBED ELEVATIONS` keyword to `374.80565;371.33` (in lieu of `0.;371.33`). So the steering file should involve now:

```fortran
/ ... header
PRESCRIBED ELEVATIONS : 374.80565;371.33
/ ...
INITIAL CONDITIONS : 'ZERO DEPTH'
/ INITIAL DEPTH : 1
/ ... footer
```

Alternatively, download the modified files:

* [boundaries-555.cli](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/boundaries-555.cli)
* [steady2d-initdry.cas](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/steady2d-initdry.cas)

Re-{ref}`run Telemac2d <tm2d-run>` and open the resulting `r2d...slf` file in QGIS with the PostTelemac plugin. Compare the results of the dry and wetted initial condition simulations with regards to the following questions:

* How does the mass balance evolve during the simulation?
* How long did the simulations take to converge and did you need to modify the `NUMBER OF TIME STEPS`?
* How reasonable are the results?
* Which of the two initial conditions would you use in practice to show that your simulation is correct?
