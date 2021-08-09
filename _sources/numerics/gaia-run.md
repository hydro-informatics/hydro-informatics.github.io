
(gaia-run)=
# Run and Analyze

## Run Gaia

Make sure that the simulation folder (e.g., `/gaia-tutorial/`) contains at least the following files (or similar, depending on the simulation case):

* A computational mesh, for example, in the form of [qgismesh.slf](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/qgismesh.slf).
* A hydrodynamic boundary definitions, for example, in the form of [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/boundaries.cli).
* A Gaia boundary definitions, for example, in the form of [boundaries-gaia.cli](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/boundaries-gaia.cli).
* A results file of a Telemac2d/3d simulation, for example, for 35 m$^3$/s in the form of [r2dsteady.slf](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/r2dsteady.slf) (result of the {ref}`dry bonus run <tm2d-dry>` ending at `T=15000`).
* A Telemac2d steering file, such as [steady2d-gaia.cas](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/steady2d-gaia.cas).
* A Gaia steering file, such as [gaia-morphodynamics.cas](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/gaia-morphodynamics.cas)e.

With all these files available, open *Terminal*, go to the TELEMAC configuration folder (e.g., `~/telemac/v8p2/configs/`), and launch the environment (e.g., `pysource.openmpi.sh` - use the same as for compiling TELEMAC).

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

With the TELEMAC environment loaded, change to the directory where the above-created 3d-flume simulation lives (e.g., `/home/telemac/v8p2/mysimulations/gaia2d-tutorial/`) and run the `*.cas` file by calling the **telemac2d.py** script (it will automatically know that it needs to use Gaia when it reads the line containing `COUPLING WITH : 'GAIA'`).

```
cd ~/telemac/v8p2/mysimulations/gaia2d-tutorial/
telemac2d.py steady2d-gaia.cas
```

````{admonition} Speed up
With {ref}`parallelism <mpi>` enabled (e.g., in the {ref}`Mint Hyfo Virtual Machine <hyfo-vm>`), speed up the calculation by using multiple CPUs through the `--ncsize=N` flag. For instance, the following line runs the unsteady simulation on `N=2` CPUs:

```
telemac2d.py steady2d-gaia.cas --ncsize=2
```
````
A successful computation should end with the following lines (or similar) in *Terminal*:

```fortran
[...]
                    *************************************
                    *    END OF MEMORY ORGANIZATION:    *
                    *************************************

CORRECT END OF RUN

ELAPSE TIME :
                            14  MINUTES
                            25  SECONDS
... merging separated result files

... handling result files
       moving: r2dsteady-gaia.slf
       moving: rGaia-steady2d.slf
... deleting working dir

My work is done
```

Telemac2d will write the files *r2dsteady-gaia.slf* and *rGaia-steady2d.slf*. Both result files are also available in the modelling repository to enable accomplishing the post-processing tutorial:

* [get r2dunsteady.slf](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/r2dsteady-gaia.slf), and
* [get r-control-sections.txt](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/rGaia-steady2d.txt).

## Post-processing in QGIS

### Open Boundary Fluxes

The above-defined {ref}`control sections <tm-control-sections>` enable insights into the correct adaptation of the flow at the upstream inflow boundary (`prescribed Q` through *inflows.liq*) and the downstream outflow boundary (`prescribed H` through *ratingcurve.txt*). {numref}`Figure %s <res-unsteady-hydrograph>` shows the modeled flow rates where the *Inflow_boundary* shows perfect agreement with *inflows.liq* and the *Outflow_boundary* reflects the flattening of the discharge curve in the modeled meandering gravel-cobble bed river.

```{figure} ../img/telemac/res-unsteady-hydrograph.png
:alt: result unsteady flow discharge telemac2d hydrodynamic inflow outflow control sections
:name: res-gaia-hydrograph

The simulated flows over the upstream *Inflow_boundary* and the downstream *Outflow_boundary* control sections.
```

The peak inflow corresponds to the specified 1130 m$^3$/s while the outflow peak discharge is only 889 m$^3$/s and the peak takes about 1070 seconds (inflow at $T=19000$ and outflow at $T\approx 20070$) to travel through the section.

(bl-calibration)=
## Calibration Parameters

```{dropdown} Recall: How to calibrate?
Calibration involves the step-wise adaptation of model input parameters to yield a possibly best stochastic fit of modeled and measured data. In the process of model calibration, only one parameter should be modified at a time by 10 to 20-% deviations from its default value. For instance, if the default is `BETA : 1.3`, the calibration may test for `BETA : 1.2`, then `BETA : 1.1` and so on, ultimately to find out which value for **BETA** brings the model results closest to observations.

Moreover, a sensitivity analysis compares step-wise modifications of multiple parameters (still: one at a time) and theirs effect on model results. For instance, if a 10-% variation of **BETA** yields a 5-% change in global water depth while a 10-% variation of a friction coefficient yields a 20-% change in global water depth, it may be concluded that the model sensitivity with respect to the friction coefficient is higher than with respect to **BETA**. However, such conclusions require careful considerations in multi-parametric, complex models of river ecosystems.
```

### Bedload Calibration
The following list of parameters can be considered for calibrating bedload in Gaia:

* Representative roughness length $k'_{s}$ (cf. Equation {eq}`eq-cf-skin`) with the keyword **RATIO BETWEEN SKIN FRICTION AND MEAN DIAMETER** $f_{k'_{s}}$ (default: $f_{k'_{s}}$=`3.`). Note that this keyword is a multiplier of the characteristic grain size $D_{50}$; thus: $k'_{s}= f_{k'_{s}} \cdot D_{50}$ (goes into Equation {eq}`eq-cf-skin`)
  * To use this calibration parameter, make sure that `SKIN FRICTION CORRECTION : 1`.
  * On dune-form sand riverbeds, start with $f_{k'_{s}}$=`37.` {cite:p}`mendoza2017`.
  * In alternating bar riverbeds, start with $f_{k'_{s}}$=`3.6` {cite:p}`mendoza2017`.
* For models based on the {ref}`Meyer-Peter and Müller <gaia-mpm>` formula (i.e., using a {term}`Shields parameter` for incipient sediment motion), the **SHIELDS PARAMETERS** keyword may be modified:
  * If erosion is overpredicted, increase **SHIELDS PARAMETERS**.
  * If erosion is underestimated, reduce **SHIELDS PARAMETERS**.
* With slope correction enabled and using the {cite:t}`koch1980` correction formulae, adapt the **BETA** keyword from Equation {eq}`eq-qb-corr` (default is `BETA :  1.3`).
  * If erosion in curved channel sections is overpredicted, decrease **BETA**.
  * If erosion in curved channel sections is underpredicted, increase **BETA**.
* To adjust deposition and erosion pattern in curves (riverbends), enable the **SECONDARY CURRENTS** keyword and modify the **SECONDARY CURRENTS ALPHA COEFFICIENT** value (cf. {ref}`Secondary Currents <gaia-secondary>`).

### Suspended Load Calibration

The following list of parameters can be considered for calibrating suspended load transport and deposition-erosion pattern in Gaia:

* {ref}`**CLASSES SETTLING VELOCITIES** <gaia-sl-sed>`:
  - Reduce to enhance transport length and reduce deposition rates
  - Increase to shorten transport trajectories and enhance deposition
* {ref}`**CLASSES CRITICAL SHEAR STRESS FOR MUD DEPOSITION** <gaia-sl-sed>`: Reduce to keep sediment in suspension (or vice versa).
