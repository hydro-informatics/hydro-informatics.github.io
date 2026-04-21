(chpt-telemac3d)=
# Telemac3d

*Telemac3d* solves the Navier-Stokes equations along a three-dimensional (3d) computational grid using a finite element scheme. *Telemac3d* mounts the tetrahedral 3d mesh from a triangular 2d mesh in a user-defined number of vertical layers. The number of vertical layers to use is defined in the TELEMAC steering (CAS) file. This tutorial walks through the creation of a 2d mesh with SALOME-HYDRO along with boundary and control files. The tutorial also features running a *Telemac3d* simulation with the files created and plotting results with the *ParaVis* plugin of *SALOME-9.8.0* (a tweaked version of *ParaView* that is able to read *MED* files).

A *Telemac3d* simulation requires similar input files as a Telemac2d simulation and this tutorial uses *MED* files to define the geometry. In particular, the following files will be created:

* Steering file
  + File format: `*.cas`
  + Software: SALOME-HYDRO's *HydroSolver* module (alternatively: {ref}`Fudaa PrePro <fudaa>`) or any text editor)
* Geometry file
  + File format: `*.med` or `*.slf`
  + Software: SALOME-HYDRO's *Geometry* and *Mesh* modules
* Boundary conditions
  + File format: `.*bnd`
  + Software: SALOME-HYDRO's *HydroSolver* module
* Unsteady flow conditions
  + File format: `*.qsl`
  + Prepare with any text editor

Optional files such as a friction data file or a liquid boundary file can also be implemented, but are not featured here. Read more about input data files and their formats in the {ref}`TELEMAC introduction <chpt-telemac>`.

This chapter provides two tutorials for 3d modeling with TELEMAC featuring two mesh file formats that are implemented in TELEMAC:

1. A 3d steady hydrodynamic simulation with a standard SLF geometry file  is set up an run in the {ref}`Telemac3d (Standard) <chpt-telemac3d-slf>` tutorial.
1. A 3d steady hydrodynamic simulation based on the MED file library is set up an run with the SALOME software (*Linux* only; stale software - Salome Hydro is currently not maintained) in the {ref}`Telemac3d with Salome-Hydro and MED <chpt-telemac3d-med>` tutorial.
