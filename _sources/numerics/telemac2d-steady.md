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

```fortran
/---------------------------------------------------------------------
/ TELEMAC2D Version v8p2
/ STEADY HYDRODYNAMICS TRAINING
/---------------------------------------------------------------------

/ steady2d.cas
/------------------------------------------------------------------/
/			COMPUTATION ENVIRONMENT
/------------------------------------------------------------------/
TITLE : '2d steady flow'
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

In addition, the `MASS-BALANCE : YES` setting will printout the mass fluxes and errors in the computation region, which is an important parameter for verifying the plausibility of the model. Note that this keyword only enables mass balance printouts and does not imply mass balance of the model, which must be achieved through a consistent model setup following this tutorial and the {{ tm2d }}.

````{admonition} Expand to recall GENERAL PARAMETERS in the cas file
:class: note, dropdown
```fortran
/ steady2d.cas
/------------------------------------------------------------------/
/			GENERAL PARAMETERS
/------------------------------------------------------------------/
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

Telemac2d comes with three solvers for approximating the depth-averaged {term}`Navier-Stokes Equation` (shallow water) {cite:p}`p. 262 in <kundu_fluid_2008>` that can be chosen by adding an **EQUATIONS** keyword:

* `EQUATIONS : SAINT-VENANT FE` is the **default** that make Telemac2d use a Saint-Venant finite element method,
* `EQUATIONS : SAINT-VENANT FV` makes Telemac2d use a Saint-Venant finite volume method, and
* `EQUATIONS : BOUSSINESQ` makes Telemac2d use the {term}`Boussinesq` approximations (constant density except in the vertical momentum equation).

In addition, a type of discretization has to be specified with the **DISCRETIZATIONS IN SPACE** keyword, which is a list of five integer values. The five list elements define spatial discretization scheme for (1) velocity, (2) depth, (3) tracers, (4) $k-\epsilon$ turbulence, and (5) $\tilde{\nu}$ advection (Spalart-Allmaras). The minimum length of the keyword list is 2 (for velocity and depth) and all other elements are optional. The list elements may take the following values defining spatial discretization:

* `11` (default) activates triangular discretization in space (i.e., 3-node triangles),
* `12` activates quasi-bubble discretization with 4-node triangles, and
* `13` activates quadratic discretization with 6-node triangles.

The {{ tm2d }} recommend using the default value of `DISCRETIZATIONS IN SPACE : 11;11` that assign a linear discretization for velocity and water depth (computationally fastest). The option `12;11` may be used to reduce free surface instabilities or oscillations (e.g., along with steep bathymetry gradients). The option `13;11` increase the accuracy of results, the computation time, memory usage, and it is currently not available in Telemac2d.

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

The **PROPAGATION** keyword (default: `YES`) affects the modelling of propagation and related phenomena. For instance, disabling propagation (`PROPAGATION : NO`) will also disable {term}`Diffusion`. The other way round, when propagation is enabled, {term}`Diffusion` can be disabled separately. Read more about {term}`Diffusion` in Telemac2d in the {ref}`turbulence <tm2d-turbulence>` section.

(tm2d-fe)=
### Numerical Parameters for Finite Elements

**The following descriptions refer to section 7.2.1 in the {{ tm2d }}.**

Telemac2d uses finite elements for iterative solutions to the {term}`Navier-Stokes Equation`. To this end, a **TREATMENT OF THE LINEAR SYSTEM** keyword enables replacing the original set of equations (option `1`) involved in TELEMAC's finite element solver with a generalized wave equation (option `2`). The replacement (i.e., the use of the **generalized wave equation**) is set to **default since v8p2** and decreases computation time, but smoothens the results. The default (`TREATMENT OF THE LINEAR SYSTEM : 2`) automatically activates mass lumping for depth and velocity, and implies explicit velocity diffusion.

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

**Without any SCHEME FOR ADVECTION ...** keyword, the **SUPG OPTION** (Streamline Upwind Petrov Galerkin) keyword can be used to define if upwinding applies and what type of upwinding applies. The `SUPG OPTION` is a list of four integers that may take the following values:

* `0` disables upwinding,
* `1` enables upwinding with a classical SUPG scheme (recommended when the {term}`CFL` condition is unknown), and
* `2` enables upwinding with a modified SUPG scheme, where upwinding equals the {term}`CFL` condition (recommended when the {term}`CFL` condition is small).

The default is `SUPG OPTION : 2;2;2;2`, where

* the first list element refers to flow velocity (default `2`),
* the second to water depth (default `2` - set to `0` when `MATRIX STORAGE : 3`),
* the third to tracers (default `2`), and
* the last (forth) to the k-epsilon model (default `2`).

**Implicitation parameters** (`IMPLICITATION FOR DEPTH`, `IMPLICITATION FOR VELOCITIES`, and `IMPLICITATION FOR DIFFUSION OF VELOCITY`) apply to the semi-implicit time discretization used in Telemac2d. To enable cross-version compatibility, implicitation parameters should be defined in the `*.cas` file. For `DEPTH` and `VELOCITIES` use values between `0.55` and `0.60` (**default is `0.55` since v8p1**); for `IMPLICITATION FOR DIFFUSION OF VELOCITY` set the v8p2 default of `1.0`.

The default `TREATMENT OF THE LINEAR SYSTEM : 2` involves so-called **mass lumping**, which leads to a smoothening of results. Specific mass lumping keywords and values are required for the flux control option of the `TREATMENT OF NEGATIVE DEPTHS` keyword and the default value for the treatment of tidal flats. To this end, the mass lumping keywords should be defined as:

```fortran
MASS-LUMPING ON H : 1.
MASS-LUMPING ON VECLOCITY : 1.
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

All finite volume schemes are explicit and potentially subjected to instability. For this reason, a desired {term}`CFL` condition and a variable timestep should be defined through:

```fortran
DESIRED COURANT NUMBER : 0.9
VARIABLE TIME-STEP : YES / default is NO
```

The variable timestep will cause irregular listing outputs, while the graphic output frequency stems from the above-defined `TIME STEP`.

The **FINITE VOLUME SCHEME TIME ORDER** keyword defines the second order time scheme, which is by default set to *Euler explicit* (`1`). Setting the time scheme order to `2` makes Telemac2d using the Newmark scheme where an integration coefficient may be used to change the integration parameter (`NEWMARK TIME INTEGRATION COEFFICIENT : 1` corresponds to *Euler explicit*). To implement these options in the steering file, use the following settings:

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

The solver options vary between values of **`2` for a small mesh** and **`5` for a large mesh**. Integers between `2` and `5` can be used for medium-sized meshes. The {{ tm2d }} recommends to run simulations multiple times for finding an optimum value, where higher values (close to `5`) increase the time required for an iteration, but leads to faster convergence.

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

Telemac2d will printout warning messages when convergence could not be reached with the defined combination of accuracy and maximum iteration number keywords. The warning message printouts can be deactivated with the `INFORMATION ABOUT SOLVER` keyword, but deactivating convergence warnings is not recommended.

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
  * A float number keyword `THRESHOLD FOR NEGATIVE DEPTHS` (default `0.`) is available ony for this option.
  * Setting the threshold to, for instance, `-0.1` makes that negative water depths larger than -0.1 meters remain unchanged.
* `2` imposes a flux limitation that strictly ensures positive water depths.
* `3` acts similarly as `2` but for the ERIA {term}`Advection` scheme (set `SCHEME FOR ADVECTION OF TRACERS` to `4` or `5`). This option is appropriate for modelling conservative tracers.

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
````

### Matrix Handling

**The following descriptions refer to section 7.6 in the {{ tm2d }}.**

Telemac2d provides multiple options for matrix handling that need to be set up for particular solver schemes.

The **MATRIX STORAGE** keyword may be set to:

* `1` for using classic element-by-element matrix storage, or
* `3` for using edge-based matrix storage (default). This default is required when any `SCHEME FOR ADVECTION ...` keyword is set to `3`, `4`, `5`, `13`, `14`, or `15`, and when any direct `SOLVER` is set to `8`.

The additional **MATRIX-VECTOR PRODUCT** keyword may be used to switch between multiplication methods for the finite element scheme. However, the default value of `1` (vector multiplication by a non-assembled matrix) should currently **not be changed** because the only alternative (`2` for frontal assembled matrix multiplication) is not implemented for parallelism and quasi-bubble discretization.

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
Similar to the assignment of multiple friction coefficient values to multiple model regions featured in the {ref}`BASEMENT tutorial <bm-geometry>`, Telemac2d provides routines for domain-wise (or zonal) friction definitions. The Appendix E of the {{ tm2d }} provide detailed explanations for the implementation of such zonal friction values. The following tips may help to better understand the instructions in Appendix E:

* The proposed modification of the **FRICTION_USER** Fortran function (subroutine) is not mandatory. If the FRICTION_USER subroutines must be enabled anyway (e.g., to implement a new roughness law such as the {cite:t}`ferguson_flow_2007` equation):
  * The FICTION_USER subroutine can be found in `/telemac/v8p2/sources/telemac2d/friction_user.f`.
  * To use a modified version, copy `friction_user.f` to a new subfolder called `/user_fortran/` in your simulation case folder.
  * Modify and save edits in `/your/simulation/case/user_fortran/friction_user.f`.
  * Tell the steering (`*.cas`) file to use the modified FRICTION_USER Fortran file by adding the keyword `FORTRAN FILE : 'user_fortran'` (makes Telemac2d looking up Fortran files in the `/user_fortran/` subfolder).
* Useful examples are:
  * The BAW's Donau case study that lives in `/telemac/v8p2/examples/telemac2d/donau/` and features the usage of a `*.bfr` `ZONES FILE` and a `roughness.tbl` `FRICTION DATA FILE`, which are enabled through the `FRICTION DATA : YES` keyword in the `t2d_donau.cas` file. The donau examples was presented at the XXth Telemac-Mascaret user conference and the conference proceedings are available at the BAW's [HENRY portal](https://hdl.handle.net/20.500.11970/100418).
  * The [Baxter tutorial](http://www.opentelemac.org/index.php/component/jdownloads/summary/4-training-and-tutorials/185-telemac-2d-tutorial?Itemid=55) (look for the contribution *Reverse engineering of initial & boundary conditions with TELEMAC and algorithmic differentiation*).
* To assign zonal roughness values, use QGIS, Blue Kenue and a text editor:
  * Delineate zones with different roughness coefficients draw polygons (e.g., following landscapes characteristics on a basemap) in separate shapefiles with QGIS (see also the {ref}`pre-processing tutorial on QGIS <tm-qgis-prepro>`).
  * Import the separate polygons as closed lines in Blue Kenue (see also the {ref}`pre-processing tutorial on Blue Kenue <bk-tutorial>`).
  * Assign elevations to the polygons (closed lines) in Blue Kenue (requires {ref}`elevation information <bk-xyz>`).
  * Add a new variable to the {ref}`selafin <bk-create-slf>` geometry and call it BOTTOM FRICTION (this can be another `*.slf` file than the one where the computational mesh lives).
  * Use the {ref}`Map Object <bk-2dinterp>` function (*Tools* > *Map Object...*) to add the polygons (closed lines) to the BOTTOM FRICTION mesh variable.
  * Define zone numbers in Blue Kenue and save them (export) as `*.xyz` or `*.bfr` zones file (conversion to zones file may required opening the `*.xyz` file in a text editor and saving it form there as `*.bfr` file).
* In the `*.cas` file, make sure set a value for the FRICTION parameter according to the above descriptions and to set the `*.slf` file with the BOTTOM FRICTION variable for the `ZONES FILE` keyword.

```

### Liquid Boundary and Initial Conditions
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

(tm2d-turbulence)=
### Turbulence

**The following descriptions refer to section 6.2 in the {{ tm2d }}.**

Turbulence describes a seemingly random and chaotic state of fluid motion in the form of three-dimensional vortices (eddies). True turbulence is only present in 3d vorticity and when it occurs, it mostly dominates all other flow phenomena through increases in energy dissipation, drag, heat transfer, and mixing. The phenomenon of turbulence has been a mystery to science for a long time, since turbulent flows have been observed, but could not be directly explained by the systems of linear equations. Today, turbulence is considered a random phenomenon that can be accounted for in linear equations, for instance, by introducing statistical parameters. Not surprisingly, there are a variety of options for implementing turbulence in numerical models. The horizontal and vertical dimensions of turbulent eddies can vary greatly, especially in rivers and transitions to backwater zones (tidal flats), with large flow widths (horizontal dimension) compared to small water depths (vertical dimension). For these reasons, *TELEMAC* provides multiple turbulence models that can be applied in the vertical and horizontal dimensions.

In 2d, *TELEMAC* developers recommend using either the $k-\epsilon$ model (`3`) or the *Spalart-Allmaras* model (`5`) in lieu of the mixing length model (`2`):

```
DIFFUSION OF VELOCITY : YES / enabled by default
TURBULENCE MODEL : 3
```



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
