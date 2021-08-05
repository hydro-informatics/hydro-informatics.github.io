(gaia-sl)=
# Suspended Load

{term}`Suspended load` refers to fine particles ($\lesssim$ 0.5 mm) that are transported in the water column. The TELEMAC software suite uses the hydrodynamic Telemac2d/3d models to simulate {term}`Suspended load` by solving the {term}`Advection`-{term}`Diffusion` equations for tracers.

and additionally requires closures for sediment erosion and deposition fluxes.

`SUSPENSION FOR ALL SANDS : YES or NO`

## Numerical options and parameters
Define which numerical schemes, solvers to use in your calculation. Consider the following important keywords:

`TIDAL FLATS : YES or NO`

`OPTION FOR THE TREATMENT OF TIDAL FLATS`

`SCHEME FOR ADVECTION OF SUSPENDED SEDIMENTS`

`FINITE VOLUMES : YES or NO`

`ADVECTION-DIFFUSION SCHEME WITH SETTLING VELOCITY`

`SOLVER FOR DIFFUSION OF SUSPENSION`

## Example Applications

Examples for the implementation of suspended load come along with the TELEMAC installation (e.g., in `telemac/v8p2/examples/gaia`). The following examples in the `gaia` folder are feature (pure) suspended load implementations:

* 2d model of combined cohesive and non-cohesive suspended transport: **hippodrome-t2d/**
* 2d model of cohesive mud: **mud_conservation-t2d/**
* 3d model of combined cohesive and non-cohesive suspended transport: **hippodrome-t2d/**
* 3d model of non-cohesive suspended transport with skin friction correction: **lyn-t3d/**
* 3d model of cohesive suspended transport as tracer in Telemac3d: **rouse-t3d/**
* 3d model of a tidal flume with cohesive sediment: **tidal_flats-t3d/**
* Coupling with waves: **sandpit-t2d/**
