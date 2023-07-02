(chpt-basement)=
# BASEMENT

```{admonition} Old BASEMENT versions, BASEMD, and BASEHPC
:class: important

BASEMENT version 2 (v2) was developed with complex structures and a broad range of capacities, yet little focus was drawn on computing time. BASEMENT version 3 (v3) considerably simplified the modeling process for users and came with highly efficient computing options, including massive parallelization on GPUs. However, the simplified v3 lacks many relevant modules, such as multi-layer riverbeds for calculating topographic change as a function of multi-grain size bedload transport formulae. Now, BASEMENT version 4 (v4) provides both the manifold capacities of v2 in the form of BASEMD setups, and the computing efficiency of v3 in the form of BASEHPC setups. This tutorial explains the setup of a BASEHPC model.

```

This chapter guides through the setup of a two-dimensional (2d) numerical simulation with the freely available software BASEMENT developed at the ETH Zurich (Switzerland). Visit their [website](https://basement.ethz.ch/) to download the program and read the detailed documentation. This tutorial features:

* Setting up a 2d hydrodynamic, steady model
* Running a steady hydrodynamic 2d numerical simulation
* Post-processing of simulation results: Visualize, understand and analyze model outputs.

```{admonition} Requirements
:class: attention
Completing this tutorial requires:

* The installation of {ref}`qgis-install`.
* The {term}`SMS 2dm` file resulting from the {ref}`qgis-prepro-bm` tutorial.
* The installation of [BASEMENT v3.1.1](https://basement.ethz.ch/) or newer.
* Optional: [ParaView](https://www.paraview.org/).
```

```{admonition} Platform compatibility
:class: tip
All software applications featured in this tutorial are **compatible with *Linux* and *Windows*** platforms. Note that BASEMENT is **not** available **for *macOS***.
```
