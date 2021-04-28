# Calibration and Valdiation


##	Principles

A numerical model may provide good data, which are not usable meaning, unless a model is calibrated and validated. There are three possibilities to do so.

1. Numerical calibration assess the stability of the simulation itself. The parameters affected are for example the [CFL (Courant-Friedrichs-Lewy) condition](https://en.wikipedia.org/wiki/Courant%E2%80%93Friedrichs%E2%80%93Lewy_condition) or other hydraulic parameters. A numerical calibration can be time consuming and requires expert knowledge to judge the validity of parameters.
1. Hydraulic calibration (and validation), which compares modeled water surface levels, flow velocities or bed shear stress with observation data.
1. Morphological calibration and validation compares simulated with observed terrain change rates (not applicable here because it was not applied in the model).

```{admonition} The Difference between Calibration and Validation
**Calibration** is the iterative adaptation of a simulation to reality using measurement (observation) data with the goal of minimizing error between modeled and observed results. **Validation** only assess the goodness (or error) of the model without adapting the model itself.
```

## What next?

Once the model is calibrated, it can be used to simulate flood hydrographs to assess the stability of river engineering features and the river landscape or inundation area. Moreover, the [habitat quality of rivers for target fish species](https://pubs.er.usgs.gov/publication/70121265) can be assessed as a function of water depth, flow velocity, and grain size (and other parameters). There is even special software to perform these tasks, such as [CASiMiR](http://www.casimir-software.de/ENG/index_eng.html) (commercial) or [River Architect](https://riverarchitect.github.io).
