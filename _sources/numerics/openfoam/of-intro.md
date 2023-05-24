
<div style="text-align: center"><img src="https://www.openfoam.com/themes/bs4esi/img/openfoam-logo.png"></div>

This chapter is developed by {{ scolari }}.

# OpenFOAM

OpenFOAM is a free, open source CFD software developed primarily by OpenCFD Ltd since 2004. OpenFOAM (Open Field Operation and Manipulation, www.openfoam.com) is a C++ toolbox that can be used to develop Finite Volume (FV) Method based solvers for general continuum mechanics problems, mostly for fluid flow and heat transfer.

OpenFOAM has a wide range of functions, such as:

* The ability to simulate anything related to the CFD area, such as: turbulent flows in automotive aerodynamics, through to fires and fire suppression in buildings, involving combustion, chemical reactions, heat transfer, liquid sprinklers and films.
  
* It includes tools for dealing with complex geometries (e.g., a fish pass) and for data processing and visualization. 
  
* It performs parallel calculations allowing to take full advantage of today's multicore processors and multiprocessor computers.
  
## Basic directory structure

The basic directory structure for an OpenFOAM case that contains the minimum set of files required to run an application is shown in {numref}`Fig. %s <of-case-structure>`:
 
```{figure} ../../img/openfoam/case-structure.png
:alt: case structure openfoam folder directories
:name: of-case-structure

OpenFOAM case directory structure.
```
 

## Constant directory

The constant directory contains all values that remain constant during the calculation. These are files that specify the physical properties (e.g., transport properties and turbulence models). The subdirectory *polyMesh* contains all information concerning the mesh.

```{figure} ../../img/openfoam/constant.png
:alt: case structure openfoam files constant
:name: of-constant-dir

Example of the constant directory contents.
```


## System directory

In this directory, it is possible to modify the parameters associated with the solution procedure. It contains at least the following files: 

* *controlDict* including parameters like the start/end time, time step and data output are set; 
* *fvSchemes* where the discretization schemes can be selected;
* *fvSolution* in which the parameters and solver choice are set for the run. 

```{figure} ../../img/openfoam/system.png
:alt: case structure openfoam files parameters
:name: of-system-dir

Example of the system directory contents.
```


## Time directories

These directories contain the data files for every field of the simulation.

```{figure} ../../img/openfoam/time-dir.png
:alt: case structure openfoam files parameters time
:name: of-time-dir

Example of the zero time step directory contents.
```


## Documentation & further reading

The list below provides further sources where more information regarding OpenFOAM
can be found, including tutorials and lecture notes.

* General information about running OpenFOAM, compilation, solvers, models, mesh generation, and post-processing in the {{ of_usr }} and {{ of_dev }}
* [OpenFOAM Wiki](https://openfoamwiki.net/)
* The CFD Online OpenFOAM Forum at: [https://www.cfd-online.com/Forums/openfoam/](https://www.cfd-online.com/Forums/openfoam/)
* More tutorials, videos and the book "Mathematics, Numerics, Derivations and OpenFOAM" can be found at: [https://holzmann-cfd.com/](https://holzmann-cfd.com/)  
* Video tutorials with detailed step-by-step instructions can be found at: [youtube.com/OpenFOAMJozsefnagy](https://www.youtube.com/@OpenFOAMJozsefNagy/)
* Lecture notes of a PhD course CFD with openSource Software, available at: [tfd.chalmers.se](http://www.tfd.chalmers.se/~hani/kurser/OS_CFD/#YEAR_2022)
  

