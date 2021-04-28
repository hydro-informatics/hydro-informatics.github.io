# Pre-Processing for TELEMAC models

## Under construction. Expected release of this tutorial: Fall 2021.

Thank you for your patience.

```{admonition} Requirements
The case featured in this tutorial was established with: <br><br>**- [*BlueKenue* v3.12](../get-started/install-telemac.html#sbluekenue)** (on *Windows*)<br>**- [*QGIS v3.16*](../get-started/geo.html#qgis)** (tested on *Windows* and **Debian 10 Linux*),<br>**- [*Fudaa PrePro v1.4*](../get-started/install-telemac.html#fudaa)** (tested on *Windows* and **Debian 10 Linux*), and <br>**- [*TELEMAC* v8p2r0](../get-started/install-telemac.html#modular-install)** (stand-alone installation on *Debian 10 Linux*).
```

This tutorial uses descriptions provided in the [telemac2d](http://ot-svn-public:telemac1*@svn.opentelemac.org/svn/opentelemac/tags/v8p1r1/documentation/telemac2d/user/telemac2d_user_v8p1.pdf) user manual.

## Input files

### Overview

For any TELEMAC 2D simulation, the following files are mandatory:

* Steering file
    + File format: `cas`
    + Prepare either with [Fudaa PrePro](https://fudaa-project.atlassian.net/wiki/spaces/PREPRO/pages/253165587/How+to+launch+Fudaa-Prepro) or [*BlueKenue<sup>TM</sup>*](../get-started/install-telemac.html#bluekenue).
* Geometry file
    + File format: `.slf` ([selafin](https://gdal.org/drivers/vector/selafin.html)
    + Prepare either with
* Boundary conditions
    + File format: `.cli`
    + Prepare either with

The basic setup of the files is explained below.

## Build geometry and computational mesh

## Geometry File Option 1: BlueKenue

### File description and reference to CAS
The geometry file in [*slf* (*selafin*)](https://gdal.org/drivers/vector/selafin.html) format contains binary data about the mesh with its nodes. The name format of the geometry file can be modified in the steering file with:

```
/steering.cas
GEOMETRY FILE            : 't2d_channel.slf'
GEOMETRY FILE FORMAT     : SLF  / or MED with SALOME verify usage
```

### Load points to create a geometry file (BK)


To load any point *shapefile* start *BK* and:

* *File* > *Import* > *ArcView Shape File* > Navigate to the directory where the point *shapefile* lives > Select the *All Files (\*.\*)* option (in lieu of *Telemac Selafin File (\*.slf)*) > Select the file (e.g., *xyz.shp*)
* ALTERNATIVELY: Open any other point data file with *File* > *Open* > Navigate to DIR > look for *.xyz* or *.dat* files

```{figure} ../img/bk-import-pts.png
:alt: bkimportpts

Importing a point shapefile in BK.
```

* Right-click on **points (X)** and open the **Properties**
* In the **Properties** window got to the **Data** tab > select **Z(float)** and **Apply**; then go to the **ColourScale** tab > **Reset** button > **Apply** > **OK**. Now, **points (X)** should have turned into **points (Z)**
* Drag **points (X)** from **Data Items** to **Views | 2D View (1)**
* ALTERNATIVELY: Use a three-dimensional (3D) view of the points: Go to the **Window** menu > **New 3D View** > drag **points (X)** from **Data Items** to **Views | 3D View (1)**

```{figure} ../img/bk-imported-3dpts.png
:alt: bk3dpts
:name: bk3dpts

The imported points a point shapefile in BK.
```

### Generate a Mesh

TM solves the (depth-averaged) Navier Stokes equations along a computational grid based on either a finite element or a finite volume scheme. BK provides mesh generators for creating regular or unstructured computational grids (meshes). This example features the **T3 Channel Mesher** to generate a triangular mesh. Switch to a **2D View** of the above points and walk down the following workflow.

1. Define the computational domain with a **New Closed Line**
    * Find the *New Closed Line* button approximately below the *Help* menu
    * Draw a polygon around the region of interest by clicking on the most outside points of the point cloud
    * When finished drawing, press the `Esc` key and enter `ClosedLine_domain` in the *Name* field > click OK and OK (in the popup window)

```{figure} ../img/bk-domain-closedline.png
:alt: BlueKenue domain
```

1. Draw **New Open Line** objects to delineate the main (river) channel, levees, and right-left extents.
    * Find the *New Open Line* button next to the *New Closed Line* button




## Geometry File Option 2: QGIS & BASEMESH

Follow the instructions in the [QGIS data pre-processing](../numerics/pre-qgis) section for creating a .2dm file.

Then...


(prepro-fudaa)=
## Model setup with Fudaa Prepro

*Fudaa PrePro* facilitates the definition of boundaries, initial conditions, and setting up a steering file. To start *Fudaa*, open *Terminal* (*Linux*) or *Command Prompt* (*Windows*) and:

* `cd` to the installation directory of *Fudaa*
* start the GUI:
    + *Linux*: tap `sh supervisor.sh`
    + *Windows*: tap `supervisor.bat`


## Boundary Conditions

The boundary file in *cli* format contains information about inflow and outflow nodes (coordinates and IDs). The *cli* file can be opened and modified with any text editor, which is not recommended to avoid inconsistencies. Preferably use [*Fudaa-PrePro*](../get-started/install-telemac.html#fudaa) or [*BlueKenue*](../get-started/install-telemac.html#bluekenue) for generating and/or modifying *cli* files.

In addition, users can define a liquid boundary conditions file (*qsl*) to define time-dependent boundary conditions (e.g., discharge, water depth, flow velocity or tracers).

### Stage-discharge (or WSE-Q) Relationship

Define a stage-discharge file (*ASCII* format) to use a stage (water surface elevation *WSE*) - discharge relationship for boundary conditions. Such files typically apply to the downstream boundary of a model at control sections (e.g., a free overflow weir). To use a stage-discharge file, define the following keyword in the steering file:

```
/steering.cas
STAGE-DISCHARGE CURVES FILE : YES
```


### Define steady flow boundaries {#prepro-steady}

Qconst

### Define unsteady flow boundaries {#prepro-unsteady}

The name format of the boundary conditions file can be modified in the steering file with:

```
/steering.cas
BOUNDARY CONDITIONS FILE : 'bc_channel.cli'
LIQUID BOUNDARIES FILE   : 'bc_unsteady.qsl'
```

Example for a liquid boundary conditions file:
```
# bc_unsteady.qsl
# Time-dependent inflow (discharge Q(2) and outflow (depth SL(1)
T           Q(1)     SL(2)
s           m3/s     m
0.            0.     5.0
500.        100.     5.0
5000.       150.     5.0
```

### Activate morphodynamics (sediment transport with Gaia) {#prepro-gaia}

Qs



## Run Telemac2d

### Load environment and files

Load the TELEMAC *Python* variables:

```
cd ~/telemac/v8p1/configs
source pysource.openmpi.sh
config.py
```



### Start a 2D hydrodynamic simulation (steady) {#steadyrun}

To start a simulation, `cd` to the directory where the simulation files live (see previous page) and launch the steering file (*cas*) with *telemac2d.py*:

```
cd /go/to/dir
telemac2d.py run_2dhydrodynamic.cas
```


## Post-processing with QGIS

### Install the PostTelemac plugin

Open QGIS' *Plugin Manager*, go to the *All* tab and type *posttelemac* in the search field. Click on the *Install* button to install the *PostTelemac* plugin.

```{figure} ../img/qgis-plugin-manager.png
```

```{figure} ../img/qgis-plugin-install-posttm.png
```

After the successful installation, click the *Close* button. The *PostTelemac* symbol should now be visible in the QGIS menu bar.

### Open the PostTelemac plugin

Find the *PostTelemac* icon in the menu bar to open the plugin. By default, the plugin window will most likely open up in the bottom-right corner of the QGIS window. For better handling, click the *detach* symbol and enlarge the detached plugin window.

```{figure} ../img/posttm-display.png

The detached window of the PostTelemac plugin with the Display tab opened to render simulation variables such as VELOCITY U/V, VITESSE (principal absolute U-V velocity) or DEPTH.
```

```{figure} ../img/posttm-tools.png

The detached window of the PostTelemac plugin with the Tools tab opened (e.g., to create shapefiles or GeoTIFF rasters).
```
