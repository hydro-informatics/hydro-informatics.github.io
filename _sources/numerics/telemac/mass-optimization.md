(tm-foc-mass)=
# Mass Conservation

```{admonition} Requirements

This tutorial does not require running code, but we recommend to at least setting up a Telemac model, such as described in the {ref}`steady 2d tutorial <telemac2d-steady>`, which eases the understanding of concepts and terms.
```


(tm-foc-mass-workflow)=
## Workflow for Mass Conservation

With the understanding of boundary conditions, a Telemac model can be robustly built according to the following workflow:

1. Make sure to {ref}`draw liquid boundaries according to the recommendations in the section on boundaries <tm-foc-draw-bc>`.
1. Use `4 5 5` upstream (prescribed Q) and a `5 4 4` downstream (prescribed H) boundaries in the `.cli` file to prescribe **steady** discharges through the `PRESCRIBED FLOWRATES` and `PRESCRIBED ELEVATIONS` keywords, respectively in the steering (`.cas`) file.
1. Use the following keywords to prescribe roughness coefficients at the boundaries that correspond to **measured {term}`stage-discharge relation <Stage-discharge relation>`** and back-calculated cross-section averaged hydraulics:
   * `LAW OF FRICTION ON LATERAL BOUNDARIES` (integer)
   * `ROUGHNESS COEFFICIENT OF BOUNDARIES` (float)
   * To back-calculate a roughness (friction) coefficient corresponding to a measured pair of water depth and discharge, take a look at the {ref}`Python exercise on 1-d hydraulics for solving the Manning-Strickler <ex-1d-hydraulics>` formula.
   * *<span style="color: #41C639 ">Note that **not using these keywords** will make any roughness calibration **affect the mass balance**.</span>*
1. Run steady simulations with `PRESCRIBED FLOWRATES` corresponding to discharges for which hydraulic (e.g., water depth and flow velocity) **measurements** are available to **calibrate the roughness** (i.e., `FRICTION`).
   * Any initial steady state simulation should run sufficiently long ($\geq$ 10$^4$ timesteps) to reach mass convergence, that is, close-to equal inflows and outflows written through the `MASS-BALANCE : YES` keyword.
   * The roughness should be preferably defined specifically for zones with equal terrain attributes (e.g., *cobble*, *sand bar*, or *vegetation*), as described in the spotlight focus on {ref}`defining roughness zones <tm-friction-zones>`. As a result, simulated and measured water depths (or water surface elevations) and flow velocities should be in similar ranges (not more than $\pm$0.10 m difference).
1. Use the calibrated model for your purposes with hotstart conditions:
   * The `PRESCRIBED FLOWRATES` keyword in the `.cas` file is sufficient to calculate physical {ref}`habitat suitability indices <hsi-def-ex>` for specific discharges.
   * Define unsteady inflows through a hydrograph file, such as `inflows.liq` used in the {ref}`unsteady 2d <tm2d-liq-file>` tutorial.


````{admonition} Finite volume solver
:class: tip
:name: fv-tip

Have a look at Telemac's finite volume scheme, which is better in preserving mass balance, and does not require dealing with `TIDAL FLATS`. It can be activated by setting the keyword:

```fortran
/ steering .cas file
EQUATIONS : 'SAINT-VENANT FV' / the apostrophes are strictly needed here
VARIABLE TIME-STEP : TRUE / use instead of the TIME STEP keyword
DURATION: 1000 / example value
DESIRED COURANT NUMBER : 0.6
/
/ additional FV recommendations
OPTION FOR THE DIFFUSION OF VELOCITIES : 2 / only option to get mass conservation but can cause problems with tidal flats
SCHEME FOR ADVECTION OF VELOCITIES : 3 / use 3, also for FV - MATRIX STORAGE must be 3
SCHEME OPTION FOR ADVECTION OF VELOCITIES : 4 / overrides SUPG OPTION and OPTION FOR CHARACTERISTICS
NUMBER OF CORRECTIONS OF DISTRIBUTIVE SCHEMES : 2 / increase for higher accuracy and longer computing time, requires SCHEME OF ADVECTION 3,4,5, or 15 and OPTION 2,3,4
TYPE OF SOURCES : 2 / 2=Dirac is the only possibility for mass conservation, the default=1 means linear function and is not mass conservative
CONTINUITY CORRECTION : YES / particularly important when not only discharge but also depth is imposed at boundaries
```

Read more about the finite volume scheme in section 7.2.2 of the {{ tm2d }}, and the malpasset example (`telemac/v8p4/examples/malpasset/`).

````

(tm-foc-mass-keywords)=
## Additional Steering File Keywords 

During a simulation, the mass balance can be observed by activating the `MASS BALANCE` keyword in the steering file, which, however, **does not enforce mass balance**:

```fortran
/ steering .cas file
MASS-BALANCE : YES
```

After the simulation, the conservation of mass can be verified as discussed in the analysis of the {ref}`results in the steady 2d tutorial <verify-steady-tm2d>`.

The priority that Telemac uses to yield mass balance can be defined with:

```fortran
/ steering .cas file
TREATMENT OF FLUXES AT THE BOUNDARIES : 1 / 1-priority of prescribed values, 2-priority of correct fluxes
```

Other keywords can be defined to not only observe but also improve the mass balance. For example, the default number of boundary nodes in a steering file is 30, which is quickly exceeded in a large model. Thus, if there are more than 30 boundary nodes, increase the maximum number of boundary nodes in the steering (`.cas`) file, for example to `50`:

```fortran
/ steering .cas file
MAXIMUM NUMBER OF BOUNDARIES : 50
```

Also, too small water depths can cause supercritical flows at liquid boundaries, which should be avoided, either by correctly defining the boundary nodes at the bottom of the riverbed only (recall the {ref}`recommendations to draw liquid boundaries <tm-foc-draw-bc>`) or by increasing the minimum water depth from its default value of 0.1 m to a higher value in the steering file, for example to 0.2 m:

```fortran
/ steering .cas file
MINIMUM DEPTH TO COMPUTE TIDAL VELOCITIES BOUNDARY CONDITIONS : 0.2
MINIMUM DEPTH TO COMPUTE TIDAL VELOCITIES INITIAL CONDITIONS : 0.2
```

In addition, the `MINIMUM VALUE OF DEPTH` keyword may be increased from its default value of `0.0`, but such increases might negatively effect on the mass balance.

To increase computing speed, some tutorials recommend using mass lumping, which, however, negatively affect mass conservation:

* Avoid `MASSING LUMPING ...` keywords: they introduce incorrect smoothing.
* Keep the default value for `H CLIPPING` because modifications impair mass conservation.
