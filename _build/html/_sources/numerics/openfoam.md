# OpenFOAM


## Under construction. Expected release of this tutorial: Winter 2021/22.

Thank you for your patience.

```{admonition} Requirements
Install [*OpenFOAM*](../get-started/install-openfoam) and [*SALOME-HYDRO*](../get-started/telemac.html#salome-hydro) or just [*SALOME*](../get-started/install-openfoam.html#salome) on *Debian* or an *Ubuntu* (deriative) *Linux* platform.
```

This tutorial features the construction of a simple three-dimensional (3d) flume in *SALOME* and a hydrodynamic simulation with *OpenFOAM*.


## Input files

The *OpenFOAM* simulation will require the following files:

* Control file
    + File format: `.cas`
    + Software: SALOME-HYDRO's *HydroSolver* module (alternatively: [Fudaa PrePro](../get-started/telemac.html#fudaa)
* Mesh file
    + File format: `.msh`
    + Software: SALOME-HYDRO's *Geometry* and *Mesh* modules
* Boundary conditions
    + File format: `.bcd`
    + Software: SALOME-HYDRO's *HydroSolver* module
* Unsteady flow conditions
    + File format: `.qsl`
    + Prepare with any text editor

Optional files such as a friction data file or a liquid boundary file can also be implemented, but are not featured here. Read more about optional data files and their formats on the [Telemad2d pre-processing page](tm2d-pre.html#optionals).


## Start SALOME or SALOME-HYDRO {#prepro-salome}

Launch either *SALOME-HYDRO*:

```
cd /INSTALL/DIR/OF/SALOME-HYDRO/
./salome
```

or *SALOME*:

```
cd /INSTALL/DIR/OF/SALOME/
source env_launch.sh
./salome
```

## Setup a Base Case

The fundamental settings for running a simulation with *OpenFOAM* resemble. Fir this reason, it makes sense to use one of the tutorials for base case. Here, we use the **CASE** from *OpenFOAM-8/tutorials/*:


The base case contains the following folders and files:

* `0/`
* `constant/`
* `system/`
* `xx.msh` - the mesh (geometry) file with boundary conditions


## Set Initial Values


## Create Geometry, Mesh and Boundaries
With *SALOME-HYDRO* being installed in a directory called **/home/salome-hydro/appli_V1_1_univ/salome** (adapt according to the installation directory and version of SALOME-HYDRO),

If no file menus show up because `export QT_STYLE_OVERRIDE=gtk2` is not added to `~/.profile`, close SALOME-HYDRO and restart it with (read more on the [installation page](../get-started/telemac.html#mod-profile):

```
export QT_STYLE_OVERRIDE=gtk2
/home/salome-hydro/appli_V1_1_univ/salome
```
```{note}
If `QT_STYLE_OVERRIDE=gtk2` is not set, the *HydroSolver* module will not work correctly and throw a `Could not create file tree` error.
```



### Run Simulation (Compute)

Use *icoFoam* Solver with properties:

* incompressible (continuity conservation)
* transient (partial time derivative in momentum conservation)
* laminar (no turbulence solver)
* for Newtonian fluids only (one constant viscosity parameter in the diffusion term of the momentum equations)
* single phase (fluid only)
* isothermal (no energy equation for temperature gradient simulation applies)
* pressure corresponds to pressure divided by density (*PISO-loop*)





## ParaVis

Activate the **ParaVis** module from the top menu.

### Load Result (MED file)
