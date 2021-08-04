
(gaia-run)=
# Run Gaia
The simulation is started identically to a hydrodynamic simulation by calling the telemac2d.py script.
Please note that `*_tel.cas` is the hydrodynamic and not the GAIA steering file.

`cd /go/to/dir`

`telemac2d.py *_tel.cas`

However, in the steering file of the hydrodynamic model
the required keywords (see Coupling GAIA and TELEMAC) for the coupling must be present.


```{admonition} Get inspired by the TELEMAC examples
The installation of TELEMAC comes with examples for Gaia applied to Telemac2d and Telemac3d models, which can be found in:

`/telemac/v8p2/examples/gaia/`

Because Gaia is the successor of SISYPHE, also the SISYPHE examples are useful, in particular with regards to multi-grain size modeling:

`/telemac/v8p2/examples/sisyphe/`

```


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
