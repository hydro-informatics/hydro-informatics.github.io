---
title: Pre-Processing for 3D TELEMAC models
tags: [telemac, numerical, modelling, hydraulics, morphodynamics, raster, shapefile, qgis, hydraulics, tin]
keywords: numerics
summary: "Produce a numerical mesh."
sidebar: mydoc_sidebar
permalink: tm3d-pre.html
folder: numerics
---

## Under construction. Expected release of this tutorial: Spring 2021.

Thank you for your patience.

{% include requirements.html content="This tutorial refers to *TELEMAC* v8p1 (parallel with *Open MPI*) installed on Debian Linux. For the best learning experience follow the installation guides for [Debian Linux on a Virtual Machine (VM)](#vm.html) and [*TELEMAC*](install-telemac.html)." %}

This tutorial uses descriptions provided in the [telemac3d_user_v8p1](http://ot-svn-public:telemac1*@svn.opentelemac.org/svn/opentelemac/tags/v8p1r2/documentation/telemac2d/user/telemac3d_user_v8p1.pdf) manual.

## Input files

A TELEMAC 3D simulation requires similar input files as described in detail on the 2D page.

* Steering file 
    + File format: `cas`
    + Prepare either with [Fudaa PrePro](https://fudaa-project.atlassian.net/wiki/spaces/PREPRO/pages/253165587/How+to+launch+Fudaa-Prepro) or [*BlueKenue<sup>TM</sup>*](install-telemac.html#bluekenue).
* Geometry file
    + File format: `.slf` (selafin)
    + Prepare either with
* Boundary conditions
    + File format: `.cli`
    + Prepare either with

Optional files such as a friction data file or a liquid boundary file can also be implemented. Read more about optional data files and their formats on the [2D pre-processing page](tm2d-pre.html#optionals).


### The TELEMAC 3D steering file (CAS)

The steering file is the main simulation file with information about mandatory files (e.g., the *selafin* geometry or the *cli* boundary), optional files, and simulation parameters. The steering file can be created or edited either with a basic text editor or an advanced software such as [*Fudaa-PrePro*](install-telemac.html#fudaa), or [*BlueKenue*](install-telemac.html#bluekenue).

A 3D simulation needs to make less simplifications (i.e., hypotheses about the environment) than a 2D or 1D model. TELEMAC developers recommend using the following variables for optimum results with *telemac3d*.

```
/ 3D_steering.cas
/
/ accelerate simulations without tidal flat effects in the advection term
SCHEME OPTION FOR ADVECTION OF VELOCITIES = 2
SCHEME OPTION FOR ADVECTION OF K-EPSILON = 2
SCHEME OPTION FOR ADVECTION OF TRACERS = 2
/
/ Use Nikuradse roughness law (all others are not 3D compatible) with reasonable friction coefficient
LAW OF BOTTOM FRICTION = 5
FRICTION COEFFICIENT FOR THE BOTTOM = 3 · d90  / calculate this value for your case study - in the presence of ripple or dune bedforms use van Rijn recommendations
LAW OF FRICTION ON LATERAL BOUNDARIES = 0  / for symmetry calculations
LAW OF FRICTION ON LATERAL BOUNDARIES = 5  / for natural banks
FRICTION COEFFICIENT FOR LATERAL SOLID BOUNDARIES = 
/
/ Preferably use k-epsilon model or alternatively Spalart-Allmaras (=5)
/
VERTICAL TURBULENCE MODEL = 3
/
/ Reduce wiggle free surface instabilities by reducing the FREE SURFACE GRADIENT SOMPATBILITY
/
/ FREE SURFACE GRADIENT COMPATIBILITY = 0.9  / uncomment this line if there are instabilities
/
/ Enable MED geometry format to use SALOME Meshes
/
GEOMETRY FILE FORMAT = MED 
```


## Build a geometry with SALOME

A 3D mesh for TELEMAC should be possibly built with tetrahedral elements. This tutorial guides through the creation of a simple block geometry and building a tetrahedral mesh for the block.

### Start SALOME
Make sure to have *SALOME* installed ([see instructions](install-telemac.html#salome)) and launch *SALOME* (on *Debian*):

```
cd SALOME-9.5.0-DB10-SRC
./sat environ SALOME-9.5.0
./salome
```

{% include tip.html content="If you are working on a **Debian Linux VM**, **use `./mesa_salome` instead of `./salome`**. Otherwise, the *Mesh* module will fail to show render the mesh graphically (*SIGSEGV 'segmentation violation' detected* because of `error: GLSL 1.50 is not supported [...]`)." %}

### Build 3D Geometry Block

Create a new study in *SALOME* and save the study (e.g., *simple_3d*). In *SALOME*, go to the **Geometry** module and create a rectangular 3D block.

1. Make a 2D sketch of the block extents:
    * Go to **New Entity** > **Basic** > **2D Sketch**
    * Use *Global Coordinate System*  and select the third element type (rectangle &#9645;)
    * Set `Name=Sketch_1`, `X1=0` and `Y1=0`, and `X2=300` and `Y2=75`
    * Click on **Apply and Close**
1. Build a (sur)face from the 2D sketch:
    * Go to **New Entity** > **Build** > **Face**
    * Select the first option (*Face creation from wires and/or edges*)
    * Use `Name=Face_1` and select `Sketch_1` for **Objects** (click on the button next to **Objects** and select `Sketch_1` from the **Object Browser** - multiple objects can be select from the **Object Browser** by holding the `CTRL` key)
    * Click on **Apply and Close**
1. Extrude the (sur)face to build a 3D block:
    * Go to **New Entity** > **Generation** > **Extrusion**
    * Select the first option (*Base Shapes + Vector*)
    * Define `Base=Face_1`, `Vector=OZ`, and `Height: 70` 
    * *Note: To select objects, click on the button next to **Base**/**Vector** and select objects from the **Object Browser** - multiple objects can be select from the **Object Browser** by holding the `CTRL` key.*
    * Click on **Apply and Close**

Save the *SALOME* study (`CTRL` + `S` keys). As a result, the 3D block should look as illustrated below. 

{% include image.html file="salome-block.png" alt="sblock" caption="The 3D block geometry built in SALOME with the New Entity menu, the Geometry module and the three created items (Sketch_1, Face_1, and Extrusion_1) highlighted." %}

### Generate a Mesh from a Geometry

To work with the geometry in a numerical model, the geometry needs to be defined as a mesh. The *Mesh* module in *SALOME* enables the creation of a mesh with just a view clicks.

1. Activate the **Mesh** module in *SALOME* (there might be an error message that can probably be ignored)
1. Go to the **Mesh** menu (do not confuse with the *Mesh* module), and select **Create Mesh**
1. In the **Create Mesh** popup window, set the following:
    * `Name=Mesh_1`, `Geometry=Extrusion_1`, and `Mesh type=Tetrahedal`
    * Leave the *Create all Groups on Geometry* box checked.
    * In the **3D** tab, select `Agorithm=NETGEN 1D-2D-3D`, click on the **Assign a set of automatic hypotheses** button and select **3D: Tetrahedralization** -  this will call the **Hypothesis Construction**
    * In the **Hypothesis Construction** popup window, set `Length=15` and click **OK**
    * Click on **Apply and Close** (**Create mesh** popup window)
1. In the **Object Browser**, extend (un-collapse) the new `Mesh`, right-click on `Mesh_1`, and click on **Compute**

After the successful computation of the mesh, *SALOME* informs about the mesh properties in a popup window (illustrated below). Do not forget to also **save the study** regularly.
    
{% include image.html file="salome-mesh-simple.png" alt="smeshs" caption="The setup and computation of the tetrahedral mesh in SALOME." %}

{% include image.html file="salome-mesh-only.png" alt="smeshonly" caption="The calculated mesh rendered with the Mesh module in SALOME." %}

### Export MED Geometry File

To export the just created mesh, go to **File** > **Export** > **MED**

In the **Export mesh** popup window, define:
* *File name* `simple3Dblock` (or whatever you prefer)
* *Files of type* `MED 3.2 files` (make sure that this is coherent with the [installed version of MED](install-telemac.html#med-hdf))
* Choose a convenient directory (*Quick path*) for saving the *med* file
* Leave all other default settings.

Click on **Save** to save the *med* file.

***

Next: [> Start the simulation >](tm-run.html)
