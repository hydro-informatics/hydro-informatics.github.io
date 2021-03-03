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

After starting SALOME-HYDRO, activate the *HYDRO* module, then find the *Object Browser* on the right side of the window and the **POLYLINE** folder symbol. 

{% include image.html file="salome/sah-startup.png" max-width="1000" alt="telemac3d salome hydro start" %}

Right-click on the *POLYLINE* folder, select **Create polyline** and a popup window will open. In the popup window:

* For **Name** enter: `Contour`
* Click on the *Insert new section* button: {% include image.html file="salome/sah-hydro-create-polyline.png" alt="telemac salome hydro polyline" %}

    + For **Name** enter: `Section1`
    + For **Type** select **Polyline**
    + Ensure that the **Closed** box is checked
    + Press **Add** 

{% include image.html file="salome/sah-create-polyline.png" alt="telemac salome create polyline" %}

* Click on the *Addition mode* button to draw a polygon
{% include image.html file="salome/sah-polyline-addition.png" alt="telemac salome hydro polygon addition" %} 
* Draw a polygon in the viewport following the direction as shown below (qualitative match is sufficient for now)
{% include image.html file="salome/sah-polyline-draw.png" alt="telemac salome hydro polygon qualitative" %}
{% include image.html file="salome/sah-polyline-draw-dir.png" alt="telemac salome hydro polygon qualitative" %} 
* Press **Apply and close**

In the viewport, click the polyline, then right-click on it and select **Modification mode** in the context menu.

{% include image.html file="salome/sah-polyline-edit.png" max-width="332" alt="telemac salome hydro edit polygon" %} 
{% include image.html file="salome/sah-polyline-edit-popup.png" alt="telemac salome hydro edit polygon modification" %} 

In the popup window, modify the points so that a 500-m long and 100-m wide rectangle occurs as shown below (the section *Index* numbers will change, so pay attention to not create crossing lines).

{% include image.html file="salome/sah-polyline-edit-coords.png" alt="telemac salome hydro polygon table coordinates modification" %} 
{% include image.html file="salome/sah-polyline-edited.png" max-width="420" alt="telemac salome hydro edit polygon" %}

{% include tip.html content="Save the project by clicking on the **File** (top menu) > **Save As...**. In the popup menu, select the simulation target folder and define a name such as *flume3d*. Press **Save** to save the project in **hdf** format and regularly press the save button (disk symbol) in the next steps to avoid loosing work. Thus, the project can be saved, closed and re-opened any time." %}

{% include image.html file="salome/save-study-as.png" max-width="372" alt="telemac salome hydro save study as hdf" %} {% include image.html file="salome/save-study-props.png" max-width="637" alt="telemac salome hydro save study hdf" %} 


### Create a Natural Object

From the *HYDRO* top menu, select **Create immersible zone** to define a wetted area for the later created mesh.
{% include image.html file="salome/sah-nat-immersible-zone.png" max-width="334" alt="telemac salome hydro create immersible zone" %} 
 
In the popup window, make the following settings:

* **Name:** `contour_zone`
* **Polyline:** Select the previously created rectangle.
* **Bathymetry:** Leave empty.

{% include image.html file="salome/sah-nat-wetted-zone.png" max-width="545" alt="telemac salome hydro create wetted area zone" %} 

### Create a Calculation Case

One or more calculation cases can be created to define elements for the later simulation. Here, define one calculation case, by clicking on the **HYDRO** top-menu > **Create calculation case**. A popup window opens and guides through setting up the calculation case.

1. Step: Define the framework:
    * **Name**: `steady`
    * **Limits**: `Contour`
    * **Mode**: Select **Manual**.
    * Highlight `contour_zone` in the *Objects* frame and press **Include >>** to add it to the list of *Included objects*.
    * Press **Next >** (button at the bottom)
 
{% include image.html file="white.png" alt="telemac salome hydro contour create" %} 
 
 2. Step: **Include >>** again `contour_zone`and press **Next >**.
 
{% include image.html file="white.png" alt="telemac salome hydro contour zone" %} 
 
 3. Step: Omit the definition of a *Strickler table* and press **Finish**.
    * Note that this step maybe useful to define zones with different roughness attributes.
 
{% include tip.html content="Save the project by clicking on the disk symbol." %}

## Build the Geometry 

This section guides through the creation of a rectangular geometry surface representing a flume and its boundaries defined with edges (lines). To get ready, activate the **Geometry** module, right-click on *HYDRO_steady_1*, and select **Show**.

{% include image.html file="white.png" alt="telemac salome geometry activate" %} 

### Build basic shape (2d surface) {#geo2d}

Right-click on *HYDRO_steady_1* and select **Create groups** from the context menu. Make the following settings in the popup window:

* **Shape Type** (radio buttons in the upper part): select *Surface*
* **Name**: `FLUME`
* **Main Shape**: select *HYDRO_steady_1*
* Click on **Show all sub-shapes** > **Select All** and make sure that `1` shows up in the white frame.
* Select `1` in the white frame and click **Add** > **Apply**.

{% include image.html file="white.png" alt="telemac salome geometry group faces" %} 

The popup window should still be opened and wait for the definition of the four boundaries (edges) of the rectangle.


### Build edges (surface boundaries)

If you accidentally closed the *Create Group* window through clicking on *Apply and Close* in lieu of *Apply*, reopen the popup window as described in the previous step.

The four boundary edges of the surface will represent an upstream (inflow), a downstream (outflow), a left wall, and a right wall of the flume. To create the four boundary edges repeat the following steps for every edge:

* **Shape Type** (radio buttons in the upper part): select *Edge* (line symbol)
* **Name**: `upstream` (then `downstream`, `leftwall`, and `rightwall`)
* **Main Shape**: select *HYDRO_steady_1*
* Click on **Show all sub-shapes** > **Select All** and all edge numbers will show up in the white frame.
* In the white frame make sure to select the good edge corresponding to the name and the following figure. **Add** the correct edge and **Remove** all others.

{% include image.html file="tm-rectangular-flume.png" alt="telemac salome rectangular flume" %} 

* Click **Apply** to create the edge boundary and proceed with the next. After the last (fourth) edge, click **Apply and Close**.

Ultimately, the *Geometry* block in the *Object Browser* should look as follows.

{% include image.html file="white.png" alt="telemac salome geometry" %} 

## Generate a Mesh

To work with the geometry in a numerical model, the geometry needs to be defined as a triangular computational mesh that Telemac3d will extrapolate to a tetrahedral mesh. The *Mesh* module in *SALOME-HYDRO* enables the creation of a mesh with just a view clicks. The mesh is generated first for the surface (2d), then for every boundary edge (1d), and eventually computed and verified. To get ready, activate the **Mesh** module from the top menu.

### Two-dimensional (2d) mesh of the surface 

Go to the **Mesh** top menu (do not confuse with the *Mesh* module), and select **Create Mesh**. In the **Create mesh** popup window, set the following:

* **Name**: `Mesh_steady_1`
* **Geometry**: `HYDRO_steady_1`
* Leave the **Mesh type** as *Any*
* In the **2D** tab:
    * Choose *Netgen 1D-2D* for **Algorithm**
    * Find the cogwheel symbol behind the **Hypothesis** field and click on it to construct hypotheses for **Netgen 2D Parameters**.
    * In the **Hypothesis Construction** popup window:
        + Define **Name** as `NETGEN 2D Parameters 10_30`
        + Set **Max. Size** to `30`
        + Set **Min. Size** to `10`
        + Set **Fineness** to *Very Fine*, 
        + Leave all other field's default values and click **OK**.
* Back in the **Create mesh** window, set the just created *NETGEN 2D Parameters 10_30* as **Hypothesis**.
* Click on **Apply and Close** (**Create mesh** popup window)

{% include image.html file="white.png" alt="telemac salome create mesh 2d hypothesis" %}

### One-dimensional (1d) meshes of boundary edges

The 1d meshes of the boundary edges will represent sub-meshes of the 2d mesh. To create the sub-meshes, highlight the previously created *Mesh_steady_1* in the *Object Browser* (click on it), then go to the **Mesh** top menu and select **Create Sub-Mesh**. In the **Create sub-mesh** popup window, start with creating the upstream boundary edge's mesh:

* **Name**: `Upstream`
* **Mesh**: `Mesh_steady_1`
* Leave the **Mesh type** as *Any*
* In the **1D** tab:
    * Choose *Wire Descretisation* for **Algorithm**
    * Find the cogwheel symbol behind the **Hypothesis** field and click on it to construct hypotheses for **Number of Segments**.
    * In the **Hypothesis Construction** popup window:
        + Define **Name** as `Segments10`
        + Set **Number of Segments** to `10`
        + Set **Type of distribution** to *Equidistant distribution*.
* Back in the **Create Mesh** window, set the just created *Segments10* as **Hypothesis**.
* Click on **Apply** in the **Create sub-mesh** popup window, which will remain open for the definition of the three other boundary edge's meshes.

**Repeat** the above steps for creating sub-meshes for the downstream, left wall, and right wall edges, but with different construction hypotheses.

* For the downstream sub-mesh use **Name** *Downstream* and construct the following hypothesis:
    + Type: **Number of Segments**
    + Define **Name** as `Segments05`
    + Set **Number of Segments** to `5`
    + Set **Type of distribution** to *Equidistant distribution*.
* For the left wall sub-mesh use **Name** *LeftWall* and construct the following hypothesis:
    + Type: **Arithmetic Progression 1D**
    + Define **Name** as `Arithmetic1d10_30`
    + Set **Start length** to `10`
    + Set **End length** to `30`.
* For the right wall sub-mesh use **Name** *RightWall* and construct the following hypothesis:
    + Type: **Arithmetic Progression 1D**
    + Define **Name** as `Arithmetic1d15_10`
    + Set **Start length** to `15`
    + Set **End length** to `10`.

To this end, the *Object Browser* should include the 5 hypotheses and the non-computed meshes (warning triangles).

{% include image.html file="white.png" alt="telemac salome create mesh 1d hypotheses" %}

{% include tip.html content="Save the project by clicking on the disk symbol." %}

{% include note.html content="If an info or warning windows pops up and asks for defining the order to apply, that means the geometry groups contain too many elements. In this case go back to the [geometry creation](#geo2d) and make sure that always only one element is added per group. For more complex models, the order of mesh hypotheses may not be an error, but in this simple case it must not appear being an issue." %}

### Compute Mesh

In the **Object Browser**, extend (un-collapse) the new *Mesh* block, right-click on *Mesh_steady_1*, and click on **Compute**. This will automatically also compute all sub-meshes. 

After the successful computation of the mesh, *SALOME-HYDRO* informs about the mesh properties in a popup window.
    
{% include image.html file="salome-mesh-simple.png" alt="smesh compute 2d 3d" caption="The setup and computation of the triangular mesh in SALOME-HYDRO." %}

Right-click on the mesh in the *Object Browser* and click on **Show** to visualize the mesh in the viewport.

{% include image.html file="salome-mesh-only.png" alt="smesh show only" caption="The calculated mesh rendered with the Mesh module in SALOME-HYDRO's viewport." %}

### Verify Mesh

***Orientation of faces and volumes***

This step will ensure that the mesh is correctly oriented for the simulation with *Telemac3d*. In the *Object Browser*, highlight *Mesh_steady_1* and then go to the **Modification** top menu > **Orientation**. In the pop-up window, check the **Apply to all** box. Click the **Apply and close** button. The mesh should have changed from darker blue to a lighter tone of blue (if the inverse is the case, repeat the application of the orientation tool).

***Identify and reconcile over-constraint elements***

In the *Object Browser*, highlight *Mesh_steady_1*. Then go to the **Controls** top menu > **Face Controls** > **Over-constraint faces**. Over-constrained triangles in the *Mesh_steady_1* will turn red in the viewport (*VTK scene:1*) and at the bottom of the viewport, the note *Over-constrained-faces: 2* will appear. 

To reconcile the edge cause the triangle's over-constrain, go to the **Modification** top menu > **Diagonal inversion**, and select the internal edge of the concerned triangles.

{% include tip.html content="Save the project by clicking on the disk symbol." %}

## Export MED File

Exporting the mesh to a MED file requires the definition of mesh groups. To do so, highlight *Mesh_steady_1* in the object browser and right-click on it. Select **Create Groups from Geometry** from the mesh context menu. In the popup window, select all groups and sub shapes of the *FLUME* geometry and all groups of **mesh elements** and **mesh nodes**. For selecting multiple geometries, hold down the `CTRL` (`Strg`) and `Shift` keys on the keyboard and select the geometry/mesh groups. The tool will automatically add all nodes selected. Press **Apply and close** to finalize the creation of groups.

{% include image.html file="white.png" alt="telemac salome create geometry mesh groups" %}

Verify the created groups by right-clicking on the top of the project tree in the *Object Browser* and selecting *Show only* with the option *Auto Color*. If the groups seems correct (see below figure), export them with **File** (top menu) > **Export** > **MED**.

{% include image.html file="white.png" alt="telemac salome geometry mesh groups view show" %}

In the **Export mesh** popup window, define:

* **File name** `flume3d` (or whatever you prefer)
* **Files of type** `MED 3.2 files` (if not using *SALOME-HYDRO*, make sure that the type is coherent with the [installed version of MED](install-telemac.html#med-hdf))
* Choose a convenient directory (*Quick path*) for saving the *MED* file
* Leave all other default settings.
* Click on **Save** to save the *MED* file.

{% include image.html file="white.png" alt="telemac salome save med file" %}

{% include tip.html content="Save the project by clicking on the disk symbol." %}

## HydroSolver 

Activate the **HydroSolver** module from the top menu.

### Generate Boundary Conditions

Click on the boundary condition window to create a new boundary condition file.

* upstream
* downstream
* right wall and left wall

{% include image.html file="white.png" alt="telemac salome hydro create boundary conditions" %}

### Create Simulation Case (CAS)

Alternatively, use Fudaa Prepro.

### Run Simulation (Compute)

If the new PYTEL case is not showing up in the *Object Browser*, save the project (e.g., *tetrahedral_3d.hdf*), close and restart SALOME-HYDRO. Re-open the project *hdf* file and re-activate the HydroSolver module. 

* In the *Object Browser*, click on *tetrahedral_steering* (highlights in blue).
* With the steering file highlighted, find the *Edit Pytel case for execution* button in the menu bar and click on it. 
* Enable the PYTEL radio button
* In the *Object Browser*, right-click on HydroSolver and click *Refresh*. A *EXE* sign next to *tetrahedral steering* should show up*.
* Right-click on the new *EXE tetrahedral steering* item in the *Object Browser*, then click on *Compute*

## Alternative Run Option: TELEMAC (direct)

## ParaVis

Activate the **ParaVis** module from the top menu.

### Load Result (MED file)


