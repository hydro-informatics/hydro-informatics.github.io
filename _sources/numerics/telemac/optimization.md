(telemac-opti)=
# Optimization

A numerical model calibration should yield a computationally functional, and physically, at least a reasonably accurate model. Model calibration has already been covered in the {ref}`results analysis section <tm2d-post-export>` of the steady Telemac2d tutorial. This chapter first provides more tips to increase the physical correctness of a model, especially regarding the conservation of mass, which can sometimes be challenging in Telemac. Additionally, advanced calibration methods that use supervised machine learning to improve physical model accuracy are presented.

```{admonition} Goals and requirements
This tutorial explains how a Telemac model can be refined by improving its computational stability, and physical correctness. Thus, it is relevant after setting up a Telemac model, as explained for a simple case in the {ref}`steady 2d chapter <telemac2d-steady>`.

```


## Computing Time

Some of the keywords in TELEMAC's steering (`*.cas`) file affect computation speed.

* Use the {ref}`ACCURACY and MAXIMUM ITERATION <tm2d-accuracy>` keywords to yield faster convergence.
* Deactivate `TIDAL FLATS`, even though deactivating {ref}`tidal flats <tm2d-tidal>` can not be recommended to yield physically meaningful and stable models.
* When using the GMRES solver (`SOLVER : 7`), varying the {ref}`solver options <tm2d-solver-pars>` may aid to reduce the total calculation time.
* Make sure to use the default `MATRIX STORAGE : 3` keyword.
* Use an earlier simulation (e.g., with a coarser mesh) to initiate the model with the `COMPUTATION CONTINUED : YES` and `PREVIOUS COMPUTATION FILE : *.slf` keywords (see section 4.1.3 in the {{ tm2d }}).

Moreover, Telemac2d provides a way to stop a simulation (step) when fluxes stabilize. To enable this feature, add the following block in the steering (`*.cas`) file:

```
/ steady state stop criteria in steering.cas
STOP IF A STEADY STATE IS REACHED : YES / default is NO
STOP CRITERIA : 1.E-3;1.E-3;1.E-3 / use list of three values - defaults are 1.E-4
```

However, stop criteria are not functional for non-stationary flows (e.g., {cite:t}`von_karman_mechanische_1930` vortex street downstream of bridge piers). Read more about the convergence stop criteria in the {{ tm2d }} (section 5.1).

```{admonition} More recommendations are in the user manual
:class: tip

The {{ tm2d }} provides more recommendations for computing time, stability, and model optimization, including the mesh, in section 16.
```

## Stability & Physical Correctness

### Mass conservation

The conservation of mass is a primary concern that has already been discussed in the analysis of the results in the steady 2d case by {ref}`verifying discharge convergence <verify-steady-tm2d>` at the liquid model boundaries.


* An initial steady state may take a considerable amount of time: make sure to run a numerical model long enough.
* Avoid `MASSING LUMPING ...` keywords: they introduce incorrect smoothing.
* Keep the default value for `H CLIPPING` because modifications impair mass conservation.
* The `MASS-BALANCE : YES` keyword only prints mass fluxes across liquid boundaries, but does not enforce mass conservation.
* Use the following combination of keywords to increase the mass conservation of a Telemac2d model using finite elements:

```fortran
OPTION FOR THE DIFFUSION OF VELOCITIES : 2 / only option to get mass conservation but can cause problems with tidal flats
SCHEME FOR ADVECTION OF VELOCITIES : 3 / use 3, also for FV - MATRIX STORAGE must be 3
SCHEME OPTION FOR ADVECTION OF VELOCITIES : 4 / overrides SUPG OPTION and OPTION FOR CHARACTERISTICS
NUMBER OF CORRECTIONS OF DISTRIBUTIVE SCHEMES : 2 / increase for higher accuracy and longer computing time, requires SCHEME OF ADVECTION 3,4,5, or 15 and OPTION 2,3,4
TYPE OF SOURCES : 2 / 2=Dirac is the only possibility for mass conservation, the default=1 means linear function and is not mass conservative
CONTINUITY CORRECTION : YES / particularly important when not only discharge but also depth is imposed at boundaries
```


### Accuracy

When the accuracy keywords are improperly defined, TELEMAC may not be able to end the simulation. In this case, make sure to comment out the accuracy keywords and let TELEMAC use its default values:

```fortran
/ SOLVER ACCURACY : 1.E-4
/ ACCURACY FOR DIFFUSION OF TRACERS : 1.E-4
/ ACCURACY OF K : 1.E-6
/ ACCURACY OF EPSILON : 1.E-6
/ ACCURACY OF SPALART-ALLMARAS : 1.E-6
```

### Variable Time-Steps and CFL Condition

Unstable simulations may occur when the {term}`CFL` condition is insufficiently fulfilled. To ensure that the {term}`CFL` condition is respected, enable variable timestep calculation and use the **DESIRED COURANT NUMBER** keyword (default value `1`), for example:

```fortran
TIME STEP : 5
VARIABLE TIME-STEP : YES
DURATION : 5000
DESIRED COURANT NUMBER : 0.9
```

Note that the **TIME STEP** is still required because the **GRAPHIC PRINTOUT PERIOD** is a multiple of the defined **TIME STEP**.

```{admonition} Use the DURATION keyword
A variable timestep calculation may run eternally. Assigning the **DURATION** keyword avoids such eternal runs.
```

### Implicitation
To increase model stability, modify the following variables or make sure that the variables are within reasonable ranges in the *CAS* file:

* `IMPLICITATION FOR DEPTH` should be between `0.5` and `0.6`.
* `IMPLICITATION FOR VELOCITIES` should be between `0.5` and `0.6`.
* `IMPLICITATION FOR DIFFUSION` should be `1.` or smaller.

### Surface Oscillations (Wiggles)
When physically non-meaningful gradients or oscillations occur at the water surface or the bathymetry has steep slopes, the following keyword settings may help:

* `FREE SURFACE GRADIENT` - default is `1.0`, but it can be reduced to `0.1` to achieve stability (nevertheless, start with going incrementally down, such as a value of `0.9`).
* `DISCRETIZATIONS IN SPACE : 12;11` - uses quasi-bubble spatial discretization with 4-node triangles for velocity.

### Residual Mass Errors
To reduce residual mass errors use in the steering file:

```fortran
CONTINUITY CORRECTION : YES
```

### Divergence

To limit divergence issues, use the `CONTROL OF LIMITS` and `LIMIT VALUES` keywords. The `LIMIT VALUES` keyword is a list of 8 integers for minimum and maximum values for H, U, V, and T (tracers). The implementation in the steering file looks like this:

```fortran
CONTROL OF LIMITS : YES / default is NO
LIMIT VALUES : -1000;9000;-1000;1000;-1000;1000;-1000;1000 / default mins and max for H, U, V, tracer
```

### Tidal Flats

Wetting and drying of grid cells, for instance, during a simulation of dam breaks or flood hydrographs, may lead to model instability. While the {ref}`tm2d-tidal` section in the Telemac2d steady modeling tutorial suggests physically and computationally meaningful keyword option combinations, section 16.5 in the {{ tm2d }} recommends using the following settings in the steering file as conservative choices from the BAW's Wesel example.

```fortran
VELOCITY PROFILES : 4;0
TURBULENCE MODEL : 1
VELOCITY DIFFUSIVITY : 2.
TIDAL FLATS : YES
OPTION FOR THE TREATMENT OF TIDAL FLATS : 1
TREATMENT OF NEGATIVE DEPTHS : 2
FREE SURFACE GRADIENT COMPATIBILITY : 0.9
H CLIPPING : NO
TYPE OF ADVECTION : 1;5
SUPG OPTION : 0;0
TREATMENT OF THE LINEAR SYSTEM : 2
SOLVER : 2
PRECONDITIONING : 2
SOLVER ACCURACY : 1.E-5
CONTINUITY CORRECTION : YES
```

````{admonition} How to find the Wesel example
:class: tip

This example is typically installed in the following directory:

```
/telemac/v8p4/examples/telemac2d/wesel/
```
````


### Discretization Scheme

The default setting of `DISCRETIZATIONS IN SPACE : 11;11` assigns a linear discretization for velocity and water depth, which is computationally fast but potentially unstable (read more in the section on {ref}`general Telemac2d parameters <tm2d-numerical>`). To overcome stability issues related to the discretization scheme, consider using `DISCRETIZATIONS IN SPACE : 12;11`. In addition, setting `FREE SURFACE GRADIENT COMPATIBILITY : 0.01` (i.e., close to zero) may aid in troubleshooting stability issues related to the discretization of velocity and depth.


### Exceeding Maximum Iterations
*This section is co-authored by {{ scolari }}*.

A simulation may print `EXCEEDING MAXIMUM ITERATIONS` warnings in the *Terminal*:

```fortran
GRACJG (BIEF) : EXCEEDING MAXIMUM ITERATIONS:    50 RELATIVE PRECISION:  0.7234532E-01
GRACJG (BIEF) : EXCEEDING MAXIMUM ITERATIONS:    50 RELATIVE PRECISION:  NaN
GRACJG (BIEF) : EXCEEDING MAXIMUM ITERATIONS:    50 RELATIVE PRECISION:  NaN
GRACJG (BIEF) : EXCEEDING MAXIMUM ITERATIONS:    50 RELATIVE PRECISION:  NaN
GRACJG (BIEF) : EXCEEDING MAXIMUM ITERATIONS:    50 RELATIVE PRECISION:  NaN
GRACJG (BIEF) : EXCEEDING MAXIMUM ITERATIONS:    50 RELATIVE PRECISION:  NaN
GRACJG (BIEF) : EXCEEDING MAXIMUM ITERATIONS:    50 RELATIVE PRECISION:  NaN
```

`EXCEEDING MAXIMUM ITERATIONS` warnings may occur when using **SCHEME FOR ADVECTION OF [...]** keywords with the values `3`, `4`, `5`, `13`, or `14`. The reason is that these schemes yield {term}`CFL` conditions of less than 1 by triggering iterative, adaptive timestepping. To troubleshoot `EXCEEDING MAXIMUM ITERATIONS` warnings, try the following options:

*	Decrease the timestep gradually.
*	Decrease the solver accuracy (e.g. from `1.E-8` to `1.E-6`).
* Use other values for `SCHEME FOR ADVECTION OF [...]`.
*	Increase the `MAXIMUM NUMBER OF ITERATIONS FOR SOLVER` keyword value, but do not exceed `200`.
*	Change the `VELOCITY PROFILE` type (read this eBook's instructions for {ref}`2d <tm2d-bounds>` or {ref}`3d  <tm3d-slf-boundaries>`).
*	Cold starts (i.e., {ref}`defining initial conditions with the INITIAL CONDITIONS keyword in the steering file <tm2d-init>`) may not converge. Therefore, either
    -	increase the `PRESCRIBED FLOWRATES` gradually (or in a {ref}`liquid boundary file <tm2d-liq-file>`), or
    -	{ref}`create an initial conditions Selafin file <bk-create-slf>`, assigning a water depth at the inlet nodes.




## Bayesian Calibration

```{admonition} Requirements
Be comfortable with {ref}`supervised learning concepts (read on hydro-informatics.com) <supervisedlearning>`, and familiarize with the required vocabulary.

```


```{admonition} This section is under construction

Until we have found the time to describe Bayesian calibration with the usual hydro-informatics.com quality, we invite you to take a look at our open-access publication on coupling Telemac with surrogate models for Bayesian optimizations: {cite:t}`mouris_stability_2023`. More information can also be found in {cite:t}`schwindt_bayesian_2023`, {cite:t}`mohammadi_bayesian_2018`, and {cite:t}`oladyshkin_bayesian3_2020`.

```

