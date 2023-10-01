# Principles

```{admonition} Theory chapter under development
:class: tip

We are working on a more exhaustive theory section on numerical modeling of rivers and reservoirs. Until then, please use our {ref}`glossary` for detailed explanations of technical terms that might be unclear.
```

Numerical models in water resources engineering approximate the motion of fluids through iterative solutions of the {term}`Navier-Stokes equations` and their statistical approximation with the {term}`Reynolds-averaged Navier-Stokes <RANS>` equations. The role of numerical models is becoming more and more important where models can be distinguished regarding their simplification hypotheses (e.g., for dimensions or fluid characteristics). Purely hydrodynamic models simulate the motion of water and have high accuracy for simulating flow phenomena, but major challenges remain for morphodynamic modeling. While one-dimensional (**1d** cross-section-averaged) modeling is slowly abandoned for its incapacity to account for complex flow phenomena in natural rivers, two-dimensional (**2d**) and three-dimensional (**3d**) models are becoming more and more popular. Still, there are challenges in model choices and understanding numerical models. In this context, {cite:t}`mosselman_five_2016` highlight five widespread and common problems in the creation and interpretation of numerical models. These five mistakes are:

1. Preparation: One-dimensional (1d), two-dimensional (2d), and three-dimensional (3d) models require similar input data (flow series, stage-discharge relation, roughness, digital elevation model, grain sizes). What varies are the computation (3d > 2d > 1d) and the calibration (1d > 2d > 3d) efforts.
2. Grid setup: The model boundaries need to be at an adequate distance to the area of interest. An inflow boundary should only be along the permanently wetted riverbed and the most upstream 1-2% of the modeled channel bed should have a non-erosive constraint assigned to the cells. Otherwise, the model may be unstable because of locally very high velocity and erosion rates close to the inflow boundary.
3. Model setup: Read and understand how turbulence closures are implemented in the model to set the model parameters used for the turbulence closure realistically and yield a stable model.
4. Model validation/post-processing: Wrong confidence in poorly validated numerical models: Every model requires validation data, which involves exhausting and labor-intensive fieldwork.
5. Model interpretation: The direction of sediment transport and water flow vectors mostly differ.

This chapter introduces open-access and open-source software with extensive tutorials on pre-processing (geo) spatially explicit data, setting up model control files, running models, and post-processing. Tutorials are available in this eBook for the following software:

* **BASEMENT (open-access)**<br>The {ref}`chpt-basement` tutorial introduces 2d hydrodynamic modelling with the ETH Zurich's (Switzerland) numerical model *BASEMENT* 3.x, which was primarily developed with benchmark tests on **mountain rivers/streams**.
* **TELEMAC (open source)**<br>Open TELEMAC-MASCARET is a powerful software suite for a large variety of **rivers, lakes, and even ocean deltas**.
  * Get an overview of files and model options in the {ref}`TELEMAC introduction <chpt-telemac>` section.
  * The {ref}`chpt-telemac2d` tutorial introduces 2d hydrodynamic modelling with standard *SLF* (selafin) geometry files.
  * The {ref}`chpt-telemac3d-med` tutorial introduces 3d hydrodynamic modeling based on the highly efficient *MED* file library.

**OpenFOAM** represents another powerful modeling tool, which **is recommended for modeling flow-structure interactions**, and this eBook provides a basic introduction by {{ scolari }} in the {ref}`OpenFOAM section <chpt-openfoam>`. In addition, the OpenFOAM developer's [3-week tutorial](https://wiki.openfoam.com/index.php?title=%223_weeks%22_series) is a good start into OpenFOAM modeling for PhD students or engineers. On {ref}`Debian Linux / Ubuntu / Mint <linux-install>`, preferably install OpenFOAM from the [Ubuntu repository](https://develop.openfoam.com/Development/openfoam/-/wikis/precompiled/debian#ubuntu).

(calibration)=
## Calibration and Validation

A numerical model may provide good data, which is not meaningful unless a model is calibrated and validated. There are three possibilities to do so.

1. Numerical calibration assesses the stability of the simulation itself. The parameters affected are for example the {term}`CFL` (Courant-Friedrichs-Lewy) condition or other hydraulic parameters. A numerical calibration can be time-consuming and requires expert knowledge to judge the validity of parameters.
1. Hydraulic calibration (and validation), which compares modeled water surface levels, flow velocities, or bed shear stress with observation data.
1. Morphological calibration and validation compare simulated with observed terrain change rates (not applicable here because it was not applied in the model).

```{admonition} The Difference between Calibration and Validation
**Calibration** is the iterative adaptation of a simulation to reality using measurement (observation) data with the goal of minimizing the error between modeled and observed results. **Validation** only assess the goodness (or error) of the model without adapting the model itself.
```

This eBook provides hints for model calibration (parameters) in the TELEMAC sections on {ref}`hydrodynamics <tm2d-calibration>` and {ref}`morphodynamics <gaia-calibration>`.

## What to do with Numerical Model Results?

Once the model is calibrated, it can be used to simulate flood hydrographs to assess the stability of river engineering features and the river landscape or inundation area. Moreover, the [habitat quality of rivers for target fish species](https://pubs.er.usgs.gov/publication/70121265) can be assessed, for example, as a function of water depth, flow velocity, and grain size (and other parameters). There is even special software to perform these tasks, such as [CASiMiR](http://www.casimir-software.de/ENG/index_eng.html) (commercial) or [River Architect](https://riverarchitect.github.io).
