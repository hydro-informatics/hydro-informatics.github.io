---
title: Pre-Processing for 3D TELEMAC models
tags: [telemac, numerical, modelling, hydraulics, morphodynamics, raster, shapefile, qgis, hydraulics, tin]
keywords: numerics
summary: "Produce a numerical mesh."
sidebar: mydoc_sidebar
permalink: salome-hydro.html
folder: numerics
---

## Under construction. Expected release of this tutorial: Fall 2021.

Thank you for your patience.

{% include requirements.html content="This tutorial refers to *TELEMAC* v7p3 as integral part of *SALOME-HYRO* installed on Debian Linux. For the best learning experience follow the installation guides for [*SALOME-HYDRO*](install-telemac.html#salome-hydro)." %}

This tutorial uses descriptions provided in the [telemac3d_user_v8p1](http://ot-svn-public:telemac1*@svn.opentelemac.org/svn/opentelemac/tags/v8p1r2/documentation/telemac2d/user/telemac3d_user_v8p1.pdf) manual.

## Introduction

Telemac3d solves the Navier-Stokes equations along a three-dimensional (3D) computational grid using a finite element scheme. Telemac3d mounts the tetrahedral 3D mesh from a triangular 2D mesh in a user-defined number of vertical layers. The number of vertical layers to use is defined in the TELEMAC steering (CAS) file. This tutorial walks through the creation of a 2D mesh with SALOME-HYDRO along with boundary and control files. The tutorial also features running a Telemac3d simulation with the files created and plotting results with the *ParaVis* plugin of SALOME-HYDRO (a tweaked version of *ParaView*).

## Input files

A Telemac3d simulation requires similar input files as a Telemac2d simulation and this tutorial uses *MED* files to define the geometry. In particular, the following files will be created:

* Steering file 
    + File format: `cas`
    + Software: SALOME-HYDRO's *HydroSolver* module (alternatively: [Fudaa PrePro](install-telemac.html#fudaa))
* Geometry file 
    + File format: `.MED` 
    + Software: SALOME-HYDRO's *Geometry* and *Mesh* modules
* Boundary conditions
    + File format: `.bcd`
    + Software: SALOME-HYDRO's *HydroSolver* module
* Unsteady flow conditions
    + File format: `.qsl`
    + Prepare with any text editor

Optional files such as a friction data file or a liquid boundary file can also be implemented, but are not featured here. Read more about optional data files and their formats on the [Telemad2d pre-processing page](tm2d-pre.html#optionals).


## Start SALOME-HYDRO {#prepro-salome}

With *SALOME-HYDRO* being installed in a directory called **/home/salome-hydro/appli_V1_1_univ/salome** (adapt according to the installation directory and version of SALOME-HYDRO), launch *SALOME-HYDRO* (give it a moment to start up):

```
/home/salome-hydro/appli_V1_1_univ/salome
```

If no file menus show up because `export QT_STYLE_OVERRIDE=gtk2` is not added to `~/.profile`, close SALOME-HYDRO and restart it with (read more on the [installation page](install-telemac.html#mod-profile)):

```
export QT_STYLE_OVERRIDE=gtk2
/home/salome-hydro/appli_V1_1_univ/salome
```
{% include note.html content="If `QT_STYLE_OVERRIDE=gtk2` is not set, the *HydroSolver* module will not work correctly and throw a `Could not create file tree` error." %}

## HYDRO module

### Create Contours (Polyline)

After starting SALOME-HYDRO, activate the *HYDRO* module, then find the *Object Browser* on the right side of the window and the **POLYLINE** folder symbol. Right-click on the *POLYLINE* folder, select **Create polyline** and a popup window will open. In the popup window:

* For **Name** enter: `Contour`
* Click on the *Insert new section* button:
IMG
    + For **Name** enter: `Section1`
    + For **Type** select **Polyline**
    + Ensure that the **Closed** box is checked
    + Press **Add**
* Click on the *Addition mode* button to draw a polygon
IMG
* Draw a polygon in the viewport, similar as shown below (qualitative match is sufficient for now)
IMG
* Press **Apply and close**

In the viewport, click the polyline, then right-click on it and select **Modification mode** in the context menu. In the popup window, modify the points so that a 500-m lon and 100-m wide rectangle occurs as shown below (the section *Index* numbers will change, so pay attention to not creating crossing lines).

IMG

{% include tip.html content="Save the project by clicking on the **File** (top menu) > **Save As...**. In the popup menu, select the simulation target folder and define a name such as *flume3d*. Press **Save** to save the project in **hdf** format and regularly press the save button (disk symbol) in the next steps to avoid loosing work. Thus, the project can be saved, closed and re-opened any time." %}

### Create a Natural Object

From the *HYDRO* top menu, select **Create immersible zone** to define a wetted area for the later created mesh. In the popup window, make the following settings:

* **Name:** `contour_zone`
* **Polyline:** Select the previously created rectangle.
* **Bathymetry:** Leave empty.

### Create a Calculation Case

One or more calculation cases can be created to define elements for the later simulation. Here, define one calculation case, by clicking on the **HYDRO** top-menu > **Create calculation case**. A popup window opens and guides through setting up the calculation case.

1. Step: Define the framework:
    * **Name**: `steady`
    * **Limits**: `Contour`
    * **Mode**: Select **Manual**.
    * Highlight `contour_zone` in the *Objects* frame and press **Include >>** to add it to the list of *Included objects*.
    * Press **Next >** (button at the bottom)
 
 IMG
 
 2. Step: **Include >>** again `contour_zone`and press **Next >**.
 
 IMG
 
 3. Step: Omit the definition of a *Strickler table* and press **Finish**.
    * Note that this step maybe useful to define zones with different roughness attributes.
 
{% include tip.html content="Save the project by clicking on the disk symbol." %}

## Build the Geometry 

Activate the **Geometry** module, right-click on *HYDRO_steady_1*, and select **Show**.

IMG

Create a new study in *SALOME* and save the study (e.g., *simple_3d*). In *SALOME*, go to the **Geometry** module and create a rectangular 3D block.



### Generate a Mesh from a Geometry

To work with the geometry in a numerical model, the geometry needs to be defined as a mesh. The *Mesh* module in *SALOME* enables the creation of a mesh with just a view clicks.

1. Activate the **Mesh** module in *SALOME* (there might be an error message that can probably be ignored)
1. Go to the **Mesh** menu (do not confuse with the *Mesh* module), and select **Create Mesh**
1. In the **Create Mesh** popup window, set the following:
    * Set **Name** to `Mesh_1`, **Geometry** to `Compound_1`, and **Mesh type** to `Tetrahedal`
    * Leave the *Create all Groups on Geometry* box checked.
    * In the **3D** tab, click on the **Assign a set of automatic hypotheses** button (on the bottom) and select **3D: Tetrahedralization** -  this will call the **Hypothesis Construction**
    * In the **Hypothesis Construction** popup window, set `Length=12` and click **OK**
    * Click on **Apply and Close** (**Create mesh** popup window)
1. In the **Object Browser**, extend (un-collapse) the new `Mesh`, right-click on `Mesh_1`, and click on **Compute**

After the successful computation of the mesh, *SALOME* informs about the mesh properties in a popup window (illustrated below). Do not forget to also **save the study** regularly.
    
{% include image.html file="salome-mesh-simple.png" alt="smeshs" caption="The setup and computation of the tetrahedral mesh in SALOME." %}

{% include image.html file="salome-mesh-only.png" alt="smeshonly" caption="The calculated mesh rendered with the Mesh module in SALOME." %}


Right-click on the mesh and click on **Show** to visualize the mesh in the viewport.


## Verify Mesh

### Orientation of faces and volumes
Go to **Modification** (top menu) > **Orientation** 

In the *Object Browser*, highlight *tetrahedral_mesh* and in the pop-up window, check the **Apply to all** box. Click the **Apply and close** button. The mesh box should have changed from darker blue to a lighter tone of blue (if the inverse is the case, repeat the application of the orientation tool).

### Identify and reconcile over-constraint elements

In the *Object Browser*, highlight *tetrahedral_mesh* and then go to **Controls** (top menu) > **Volume Controls** > **Over-constraint volumes**. The *tetrahedral_mesh* in the *VTK scene:1* (viewport) will turn red and at the bottom of the viewport, the note *Over-constrained-volumes: 2* will appear.




## Export MED File

Exporting the mesh to a MED file requires the definition of mesh groups. To do so, highlight *tetrahedral_mesh* in the object browser and right-click on it. Select **Create Groups from Geometry** from the mesh context menu. In the popup window, select all groups and sub shapes of the *Extrusion_Reg_1* geometry and all groups of **mesh elements** and **mesh nodes**. For selecting multiple geometries, hold down the `CTRL` (`Strg`) and `Shift` keys on the keyboard and select the geometry/mesh groups. The tool will automatically add all nodes concerned. Press **Apply and close** to finalize the creation of groups.

Verify the created groups by right-clicking on the top of the project tree in the *Object Browser* and selecting *Show only* with the option *Auto Color*. If the groups seems correct (see below figure), export them with **File** (top menu) > **Export** > **MED**

In the **Export mesh** popup window, define:
* *File name* `tetrahedral_mesh` (or whatever you prefer)
* *Files of type* `MED 3.2 files` (if not using *SALOME-HYDRO*, make sure that the type is coherent with the [installed version of MED](install-telemac.html#med-hdf))
* Choose a convenient directory (*Quick path*) for saving the *MED* file
* Leave all other default settings.

Click on **Save** to save the *MED* file.


## HydroSolver 

### Generate Boundary Conditions

### Create Simulation Case (CAS)

### Run Simulation (Compute)

If the new PYTEL case is not showing up in the *Object Browser*, save the project (e.g., *tetrahedral_3d.hdf*), close and restart SALOME-HYDRO. Re-open the project *hdf* file and re-activate the HydroSolver module. 

* In the *Object Browser*, click on *tetrahedral_steering* (highlights in blue).
* With the steering file highlighted, find the *Edit Pytel case for execution* button in the menu bar and click on it. 
* Enable the PYTEL radio button
* In the *Object Browser*, right-click on HydroSolver and click *Refresh*. A *EXE* sign next to *tetrahedral steering* should show up*.
* Right-click on the new *EXE tetrahedral steering* item in the *Object Browser*, then click on *Compute*


## ParaVis

### Load Result (MED file)


