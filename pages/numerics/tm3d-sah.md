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

{% include requirements.html content="This tutorial was established with **[*SALOME-HYRO* v2_2](install-telemac.html#salome-hydro) and a stand-alone installation of [*TELEMAC* v8p2r0](install-telemac.html#modular-install) on *Debian Linux* (*buster*)**." %}

This tutorial uses descriptions provided in the [telemac3d_user_v8p1](http://ot-svn-public:telemac1*@svn.opentelemac.org/svn/opentelemac/tags/v8p1r2/documentation/telemac2d/user/telemac3d_user_v8p1.pdf) manual. More documentation can be found on [opentelemac.org/doku](http://wiki.opentelemac.org/doku.php?id=documentation_v8p2r0).

To explore example cases of *Telemac3d*, check out the installation folder of *Salome-Hydro*: **/SALOME-HYDRO/Salome-V2_2-s9/tools/Telemac-v8p2r0/examples/**.

## Introduction

Telemac3d solves the Navier-Stokes equations along a three-dimensional (3D) computational grid using a finite element scheme. Telemac3d mounts the tetrahedral 3D mesh from a triangular 2D mesh in a user-defined number of vertical layers. The number of vertical layers to use is defined in the TELEMAC steering (CAS) file. This tutorial walks through the creation of a 2D mesh with SALOME-HYDRO along with boundary and control files. The tutorial also features running a Telemac3d simulation with the files created and plotting results with the *ParaVis* plugin of SALOME-HYDRO (a tweaked version of *ParaView*).

## Input files

A Telemac3d simulation requires similar input files as a Telemac2d simulation and this tutorial uses *MED* files to define the geometry. In particular, the following files will be created:

* Steering file 
    + File format: `cas`
    + Software: SALOME-HYDRO's *HydroSolver* module (alternatively: [Fudaa PrePro](install-telemac.html#fudaa) or any text editor)
* Geometry file 
    + File format: `med` or `slf`
    + Software: SALOME-HYDRO's *Geometry* and *Mesh* modules
* Boundary conditions
    + File format: `.bcd`
    + Software: SALOME-HYDRO's *HydroSolver* module
* Unsteady flow conditions
    + File format: `.qsl`
    + Prepare with any text editor

Optional files such as a friction data file or a liquid boundary file can also be implemented, but are not featured here. Read more about optional data files and their formats on the [Telemad2d pre-processing page](tm2d-pre.html#optionals).


## Start SALOME-HYDRO {#prepro-salome}

With *SALOME-HYDRO* being installed in a directory called **/home/salome-hydro/appli_V2_2/** (adapt according to the installation directory and version of SALOME-HYDRO), launch *SALOME-HYDRO* (give it a moment to start up):

```
/home/salome-hydro/appli_V2_2/salome
```

{% include tip.html content="Read more about the installation, requirements, and launching (starting) *SALOME-HYDRO* on the [installation page](install-telemac.html#salome-hydro)." %}

## HYDRO module

### Create Contours (Polyline)

After starting SALOME-HYDRO, activate the *HYDRO* module, then find the *Object Browser* on the right side of the window and the **POLYLINE** folder symbol. 

{% include image.html file="salome/sah-startup.png" max-width="1000" alt="telemac3d salome hydro start" %}

Right-click on the *POLYLINE* folder, select **Create polyline** and a popup window will open. In the popup window:

* For **Name** enter: `Contour`
* Click on the *Insert new section* button: {% include image.html file="salome/sah-hydro-create-polyline.png" alt="telemac salome hydro polyline" %}

    + For **Name** enter: `Section_1`
    + For **Type** select **Polyline**
    + Ensure that the **Closed** box is checked
    + Press **Add** 

{% include image.html file="salome/sah-create-polyline.png" alt="telemac salome create polyline" %}

* Click on the *Addition mode* button to draw a polygon: Start with the first point in the upper left corner and move in clock-wise direction to draw the other three points.
{% include image.html file="salome/sah-polyline-addition.png" alt="telemac salome hydro polygon addition" %} 
* The polygon should show up in the viewport as shown below (qualitative match is sufficient for now)
{% include image.html file="salome/sah-polyline-draw.png" alt="telemac salome hydro polygon qualitative" %}
{% include image.html file="salome/sah-polyline-draw-dir.png" alt="telemac salome hydro polygon qualitative" %} 
* Press **Apply and close**

In the viewport, click the polyline, then right-click on it and select **Modification mode** in the context menu.

{% include image.html file="salome/sah-polyline-edit.png" max-width="332" alt="telemac salome hydro edit polygon" %} 

{% include image.html file="salome/sah-polyline-edit-popup.png" alt="telemac salome hydro edit polygon modification" %} 

To get the data table (*Section* / *Index*) visible in the lower part of the popup window, highlight the four edges of the polygon in the viewport with the mouse. 

In the popup window, modify the points so that a 500-m long and 100-m wide rectangle occurs as shown below (the section *Index* numbers will change, so pay attention to not create crossing lines).

{% include image.html file="salome/sah-polyline-edit-coords.png" alt="telemac salome hydro polygon table coordinates modification" %} 
{% include image.html file="salome/sah-polyline-edited.png" alt="telemac salome hydro edit polygon" %}

{% include tip.html content="Save the project by clicking on the **File** (top menu) > **Save As...**. In the popup menu, select the simulation target folder and define a name such as *flume3d*. Press **Save** to save the project in **hdf** format and regularly press the save button (disk symbol) in the next steps to avoid loosing work. Thus, the project can be saved, closed and re-opened any time." %}

{% include image.html file="salome/save-study-as.png" max-width="372" alt="telemac salome hydro save study as hdf" %} {% include image.html file="salome/save-study-props.png" max-width="637" alt="telemac salome hydro save study hdf" %} 


### Create a Natural Object

From the *HYDRO* top menu, select **Create immersible zone** to define a wetted area for the later created mesh.
{% include image.html file="salome/sah-nat-immersible-zone.png" max-width="334" alt="telemac salome hydro create immersible zone" %} 
 
In the popup window, make the following settings:

* **Name:** `wetted_contour`
* **Polyline:** Select the previously created rectangle.
* **Bathymetry:** Leave empty.

{% include image.html file="salome/sah-nat-wetted-zone.png" max-width="545" alt="telemac salome hydro create wetted area zone" %} 

* Press **Apply and close**.

{% include tip.html content="A **bathymetry** file **assigns bottom elevations** to the geometry. Not providing a bathymetry file like in this tutorial will set the bottom level to zero." %} 

### Create a Calculation Case

One or more calculation cases can be created to define elements for the later simulation. Here, define one calculation case, by clicking on the **HYDRO** top-menu > **Create calculation case**. A popup window opens and guides through setting up the calculation case.

**Step 1:** Define the framework:
    * **Name**: `Hydrodynamic`
    * **Limits**: `Contour`
    * **Mode**: Select **Manual**.
    * Highlight `wetted_contour` and `Contour` in the *Objects* frame and press **Include >>** to add it to the list of *Included objects*.
    * Press **Next >** (button at the bottom)
 
{% include image.html file="salome/sah-create-calc-case-popup.png" alt="telemac salome hydro contour create" %} 
 
**Step 2:** **Include >>**  `wetted_contour_Outer`and press **Next >**.
 
{% include image.html file="salome/sah-create-calc-case-groups.png" alt="telemac salome hydro contour zone" %} 

**Step 3:** Leave the boundary polygons window as-is and just click **Next >**

{% include image.html file="salome/sah-create-calc-case-bc.png" alt="telemac salome hydro contour boundary" %} 
 
**Step 4:** Omit the definition of a *Strickler table* and press **Next >**.
    * Note that this step maybe useful to define zones with different roughness attributes.

{% include image.html file="salome/sah-create-calc-case-strickler.png" alt="telemac salome hydro contour strickler" %} 

**Step 5:** Finalize the calculation case creation by clicking on the **Finish** button.

{% include image.html file="salome/sah-create-calc-case-finish.png" alt="telemac salome hydro calculation case" %} 

Export the calculation case by right-clicking on the **Hydrodynamic** calculation case in the *Object Browser*, then **Export calculation case**. As a result, a *Geometry* entry becomes visible in the *Object Browser*.

{% include image.html file="salome/sah-export-calc-case-menu.png" alt="telemac salome hydro calculation case export menu" %} 
 
{% include tip.html content="Save the project by clicking on the disk symbol." %}

## Build the Geometry 

This section guides through the creation of a rectangular geometry surface representing a flume and its boundaries defined with edges (lines). To get ready, activate the **Geometry** module, right-click on *HYDRO_Hydrodynamic_1*, and select **Show Only**.

{% include image.html file="salome/sah-exported-calc-case-geometry.png" max-width="415" alt="telemac salome hydro calculation case exported geometry" %} 

### Build basic shape (2d surface) {#geo2d}

Right-click on *HYDRO_Hydrodynamic_1* and select **Create Group** from the context menu. Make the following settings in the popup window:

* **Shape Type** (radio buttons in the upper part): select **Surface** (the rectangle)
* **Name**: `FLUME`
* **Main Shape**: select **HYDRO_Hydrodynamic_1**
* Click on **Show all sub-shapes** > **Select All** and make sure that `1` shows up in the white frame.
* Select `1` in the white frame and click **Add** > **Apply**.

{% include image.html file="salome/geo-create-group.png" max-width="572" alt="telemac salome geometry group faces" %} 

The popup window should still be opened and wait for the definition of the four boundaries (edges) of the rectangle.


### Build edges (surface boundaries)

If you accidentally closed the *Create Group* window through clicking on *Apply and Close* in lieu of *Apply*, reopen the popup window as described in the previous step.

The four boundary edges of the surface will represent an upstream (inflow), a downstream (outflow), a left wall, and a right wall of the flume. To create the four boundary edges repeat the following steps for every edge:

* **Shape Type** (radio buttons in the upper part): select *Edge* (line symbol)
* **Name**: `upstream` (then `downstream`, `leftwall`, and `rightwall`)
* **Main Shape**: select *HYDRO_Hydrodynamic_1*
* Click on **Show all sub-shapes** > **Select line in the viewport**. In the white frame of the *Create Group* window, make sure to select the good edge only. **Add** the correct edge and **Remove** all others.
 
{% include image.html file="salome/geo-create-group-upstream.png" max-width="1000" alt="telemac salome geometry group faces" caption="Define the upstream edge of the surface." %}

* For defining the other edges (`downstream`, `leftwall`, and `rightwall`), use the indications in the following figure.
 
{% include image.html file="tm-rectangular-flume.png" alt="telemac salome rectangular flume" %} 

* Click **Apply** to create the edge boundary and proceed with the next. After the last (fourth) edge, click **Apply and Close**.

Ultimately, the *Geometry* block in the *Object Browser* should look as follows.

{% include image.html file="salome/geo-created-groups-ob.png" max-width="390" alt="telemac salome geometry group object browser" %}

## Generate a Mesh

To work with the geometry in a numerical model, the geometry needs to be defined as a triangular computational mesh that Telemac3d will extrapolate to a tetrahedral mesh. The *Mesh* module in *SALOME-HYDRO* enables the creation of a mesh with just a view clicks. The mesh is generated first for the surface (2d), then for every boundary edge (1d), and eventually computed and verified. To get ready, activate the **Mesh** module from the top menu.

### Two-dimensional (2d) mesh of the surface 

**Highlight *HYDRO_Hydrodynamic_1***  in the *Object Browser*. Then, go to the **Mesh** top menu (do not confuse with the *Mesh* module), and select **Create Mesh**.

{% include image.html file="salome/mes-01-create-mesh.png" max-width="581" alt="telemac salome mesh create" %} 

In the **Create mesh** popup window, set the following:

* **Name**: `Mesh_Hn_1`
* **Geometry**: `HYDRO_Hydrodynamic_1`
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

{% include image.html file="salome/mes-02-create-mesh-netgen2d-hypo.png" max-width="444" alt="telemac salome mesh create netgen 2d hypothesis" %}  {% include image.html file="salome/mes-03-create-mesh-netgen2d.png" max-width="579" alt="telemac salome mesh create netgen 1d-2d" %} 


### One-dimensional (1d) meshes of boundary edges

The 1d meshes of the boundary edges will represent sub-meshes of the 2d mesh. To create the sub-meshes, highlight the previously created *Mesh_Hn_1* in the *Object Browser* (click on it), then go to the **Mesh** top menu and select **Create Sub-Mesh**.

{% include image.html file="salome/mes-04-create-submesh-menu.png" max-width="582" alt="telemac salome mesh create" %} 

In the **Create sub-mesh** popup window, start with creating the upstream boundary edge's mesh:

* **Name**: `Upstream`
* **Mesh**: `Mesh_Hn_1`
* Leave the **Mesh type** as *Any*
* In the **1D** tab:
    * Choose *Wire Discretisation* for **Algorithm**
    * Find the cogwheel symbol behind the **Hypothesis** field and click on it to construct hypotheses for **Number of Segments**.
    * In the **Hypothesis Construction** popup window:
        + Define **Name** as `Segments10`
        + Set **Number of Segments** to `10`
        + Set **Type of distribution** to *Equidistant distribution*.
* Back in the **Create Mesh** window, set the just created *Segments10* as **Hypothesis**.
* Click on **Apply** in the **Create sub-mesh** popup window, which will remain open for the definition of the three other boundary edge's meshes.

{% include image.html file="salome/mes-05-create-submesh-hypo.png" max-width="508" alt="telemac salome submesh create number of segments hypothesis" %}  {% include image.html file="salome/mes-06-create-submesh-seg10us.png" max-width="579" alt="telemac salome submesh create wire discretisation" %} 

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

{% include image.html file="salome/mes-09-create-submesh-hypoarith1030.png" max-width="575" alt="telemac salome submesh create arithmetic progression hypothesis" %}  {% include image.html file="salome/mes-10-create-submesh-arith1030lw.png" max-width="579" alt="telemac salome submesh create wire discretisation arithmetic" %} 

* For the right wall sub-mesh use **Name** *RightWall* and construct the following hypothesis:
    + Type: **Arithmetic Progression 1D**
    + Define **Name** as `Arithmetic1d15_10`
    + Set **Start length** to `15`
    + Set **End length** to `10`.

To this end, the *Object Browser* should include the 5 hypotheses and the non-computed meshes (warning triangles in the below figure indicating the *Compute* menu).

{% include tip.html content="Save the project by clicking on the disk symbol." %}

{% include note.html content="If an info or warning windows pops up and asks for defining the order to apply, that means the geometry groups contain too many elements. In this case go back to the [geometry creation](#geo2d) and make sure that always only one element is added per group. For more complex models, the order of mesh hypotheses may not be an error, but in this simple case it must not appear being an issue." %}

### Compute Mesh

In the **Object Browser**, extend (un-collapse) the new *Mesh* block, right-click on *Mesh_Hn_1*, and click on **Compute**.

{% include image.html file="salome/mes-13-start-compute.png" max-width="693" alt="telemac salome compute mesh menu" %}

This will automatically also compute all sub-meshes. After the successful computation of the mesh, *SALOME-HYDRO* informs about the mesh properties in a popup window.
    
{% include image.html file="salome/mes-14-end-compute.png" alt="smesh compute netgen 2d 3d" %}

In the view port (*VTK scene* tab), find the **-OZ** button to switch to plane view. If the mesh is not visible even though the computation was successful, right-click on the mesh in the *Object Browser* and click on **Show**.

{% include image.html file="salome/mes-15-gotoOZ.png" alt="smesh show only" %}

### Verify Mesh

***Orientation of faces and volumes***

This step will ensure that the mesh is correctly oriented for the simulation with *Telemac3d*. In the *Object Browser*, highlight *Mesh_Hn_1* and then go to the **Modification** top menu > **Orientation**. In the pop-up window, check the **Apply to all** box. Click the **Apply and close** button. The mesh should have changed from darker blue to a lighter tone of blue (if the inverse is the case, repeat the application of the orientation tool).

{% include image.html file="salome/mes-16-mod-orient.png" max-width="471" alt="mesh modification orientation" %}

***Identify and reconcile over-constraint elements***

In the *Object Browser*, highlight *Mesh_Hn_1*. Then go to the **Controls** top menu > **Face Controls** > **Over-constraint faces**. Over-constrained triangles in the *Mesh_Hn_1* will turn red in the viewport (*VTK scene:1*) and at the bottom of the viewport, the note *Over-constrained faces: 3* will appear.

{% include image.html file="salome/mes-17-mod-over-const.png" alt="mesh over constrained constraint faces" %}

To reconcile the edge cause the triangle's over-constrain, go to the **Modification** top menu > **Diagonal inversion**, and select the internal edge of the concerned triangles.

{% include image.html file="salome/mes-18-mod-over-const-edge-select.png" max-width="663" alt="mesh over-constrained diagonal inversion internal edges triangle" %}

Over-constrained triangles might be hidden in by the axes arrows in the corner. Thus, pay attention to sufficiently zoom into the corner unless the *Over-constrained faces* notification in the viewport shows **0**.

{% include image.html file="salome/mes-19-mod-over-const-edge-hidden.png" max-width="665" alt="mesh over-constrained diagonal inversion hidden edges faces" %}

{% include tip.html content="Save the project by clicking on the disk symbol." %}

## Export MED File

Exporting the mesh to a MED file requires the definition of mesh groups. To do so, highlight *Mesh_Hn_1* in the object browser and right-click on it. Select **Create Groups from Geometry** from the mesh context menu.

{% include image.html file="salome/mes-20-create-group-menu.png" max-width="526" alt="mesh export create groups context menu" %}

In the popup window, select all groups and sub shapes of the *FLUME* geometry and all groups of **mesh elements** and **mesh nodes**. For selecting multiple geometries, hold down the `CTRL` (`Strg`) and `Shift` keys on the keyboard and select the geometry/mesh groups. The tool will automatically add all nodes selected. Press **Apply and close** to finalize the creation of groups.

{% include image.html file="salome/mes-21-create-group.png" alt="mesh export create groups select" %}

Verify the created groups by right-clicking on the top of the project tree in the *Object Browser* and selecting *Show only* with the option *Auto Color*.

{% include image.html file="salome/mes-21-final-groups.png" max-width="303" alt="mesh export create groups final control" %}

{% include warning.html content="Make sure that every group element is unique within every group. If an element appears twice in one group, the next step (export mesh) will through a warning message about double-defined group elements, which will lead to an error later." %}

 If the groups seems correct (see above figure), export them with **File** (top menu) > **Export** > **MED**.

{% include image.html file="salome/mes-22-export-med-menu.png" max-width="660" alt="mesh export med context menu" %}

In the **Export mesh** popup window, define:

* **File name** `Mesh_Hn_1` (or whatever you prefer)
* **Files of type** `MED 4.1 files` (if not using *SALOME-HYDRO*, make sure that the type is coherent with the [installed version of MED](install-telemac.html#med-hdf))
* Choose a convenient directory (*Quick path*) for saving the *MED* file
* Leave all other default settings.
* Click on **Save** to save the *MED* file.

{% include image.html file="salome/mes-23-export-med.png" max-width="675" alt="telemac salome save med file" %}

{% include tip.html content="Save the project by clicking on the disk symbol." %}

## HydroSolver: Generate Boundary Conditions 

Activate the **HydroSolver** module from the top menu and click on the *Edit boundary conditions file* button to create a new boundary condition file.

{% include image.html file="salome/hs01-edit-bc.png" max-width="400" alt="telemac salome hydrosolver create edit boundary conditions menu" %}

In the opening popup window, select the just exported **MED** file containing the mesh and leave the *Boundary conditions file* field in the *Input files* frame free. In the **Output files** frame, click on **...** and define a boundary conditions file (e.g., `flume3d_bc.bcd`).

{% include important.html content="Make sure that all model (*MED*, *BCD*, and others such as the later defined *CAS*) files are all located in the same folder." %}

Make the following definitions in the **Boundary conditions** frame (table): 

* Group **upstream**: Set **Preset** to **Prescribed H / free T**
* Group **downstream**: Set **Preset** to **Prescribed Q / prescribed T**
* Group **leftwall**: Set **Preset** to **Closed boundaries/walls**
* Group **rightwall**: Set **Preset** to **Closed boundaries/walls**

{% include image.html file="salome/hs02-create-bc.png" max-width="789" alt="telemac salome hydrosolver create edit boundary conditions" %}

Then click on **Apply and Close**. Verify if the boundary condition file was correctly created by opening it in a text editor (e.g., on *Xfce* desktop use right-click > *mousepad*). The file should resemble the figure below.

{% include image.html file="salome/hs03-bc-file.png" max-width="487" alt="telemac boundary conditions file bcd" %}

## HydroSolver: Create Simulation Case (CAS)

The *CAS* (`.cas`) file is the control (or *steering*) file for any *TELEMAC* simulation and links all model parameters. The next sections guide through setting up a simple *CAS* file for *Telemac3d* simulations with *Salome-Hydro*. 

{% include tip.html content="Copy a sample case from the *TELEMAC* folder (*/SALOME-HYDRO/Salome-V2_2-s9/tools/Telemac-v8p2r0/examples/*) and edit it for convenience." %}
{% include windows.html content="The *CAS* file can also be edited/created with [Fudaa PrePro](install-telemac.html#fudaa) - or any text editor software -  for use with *Salome-Hydro* on a *Linux* system later." %}

### Create a new Case

Go to the **Hydro** top menu > **Edit cas file (English)** and a popup window along with a new frame will open.

{% include image.html file="salome/hs04-create-cas-menu.png" max-width="478" alt="telemac create edit cas file menu" %}

The popup window will ask for the version of *TELEMAC* (i.e., the solver) to use. Select **telemac3d** and clock **Ok**.

{% include image.html file="salome/hs05-cas-choose-solver.png" max-width="472" alt="telemac create edit cas file choose solver version" %}

In the new frame (*Eficas Telemac* viewport), go to **File** > **New** for creating a new *CAS* (case or *French* *cas*).

{% include image.html file="salome/hs06-create-cas-new.png" max-width="659" alt="telemac create new cas file" %}

A new *unnamed file1* case is created and opens up in the *Computation environment* frame. To make sure that no information will be lost, save the new case *CAS* file (e.g., as `flume3d-steady.cas`).

{% include image.html file="salome/hs08-cas-save-as.png" max-width="458" alt="telemac new cas file save as" %}
{% include image.html file="salome/hs09-cas-save-popup.png" max-width="675" alt="telemac new cas file save" %}

### Parameters: Computation environment

In the **Global** frame, define a **Title** (e.g., `flume3d-tutorial`) and **enable Checking the mesh (True)**.

In the **Input frame**, define the input files:

* **Geometry file**: `Mesh_Hn_1.med`
* **Geometry file format**: **MED**
* **Boundary conditions file**: `flume3d_bc.bcd`

In the **Output frame** make the following definitions:

* **3d result file**: `flume3d_results.med`
* **3d result file format**: **MED**
* In the side menu, fine the **2d result file** definitions; assign a 2d-result file name (e.g., `flume3d_2dresults.med`) and the **MED** file format.
* **Variables for 3d graphic printouts**: Expand the side variable options (`+` sign) and select **velocity along x/y/z axis (m/s)** (i.e., select three velocity variables)  and **elevation z (m)**.
* **Variables for 2d graphic printouts**: Expand the variable options and select **velocity along x/y axis (m/s)** (i.e., select two velocity variables) and **H: water depth (m)**.
* Define a **Graphic printout period** (e.g., `1000`).
* **Number of first time step for graphic printouts**: `50`

{% include tip.html content="Define output variables to your convenience (the values here are indicative)." %}
 
{% include important.html content="Graphic printouts, just like all other data printouts, are time consuming and will slow down the simulation." %}

{% include image.html file="salome/hs07-glob-inpt-outp.png" alt="telemac cas environment input output" caption="The here shown parameters are indicative - follow the text instructions for coherent parameter settings." %}

### Parameters: General

The *General parameters* specify *time* and *location* settings for the simulation:

* **Time**:
    + **Time step**: 50.0
    + **Number of time steps**: 800 

{% include important.html content="Limit the number of time steps to a minimum and use a large enough time step for computational efficiency (short duration). Vice versa, use small enough and sufficient time steps to achieve/increase computational stability." %} 

* Location:
    + Nothing to set in this tutorial.
    + Can be used in other simulations for geo-referencing.

{% include image.html file="salome/hs10-general-pars.png" alt="telemac cas general parameters" caption="The here shown parameters are indicative - follow the text instructions for coherent parameter settings." %}

{% include tip.html content="**Save the project and the CAS files** regularly (two different files)." %}

### Parameters: Vertical (3d)

*Telemac3d* will add *Horizontal levels* (i.e., layers) that correspond to copies of the 2d-mesh to build a tetrahedral 3d-mesh. To this end, modify the **Number of Horizontal levels** to `5` for implementing the third model dimension.

{% include image.html file="salome/hs11-vertical-pars.png" max-width="584" alt="telemac3d cas vertical horizontal levels parameters" %}

Read more about the *Telemac3d* solver and the vertical component in the *Telemac3d* documentation that is available at [opentelemac.org/doku](
http://wiki.opentelemac.org/doku.php?id=documentation_v8p2r0).

### Parameters: Numerical

This section defines internal numerical parameters for the *Advection* and *Diffusion* solvers (do not confuse with other numerical parameters to be defined in the *Hydrodynamic parameters* section). **Enable mass lumping for diffusion** by setting it to `1.0` and leave all other parameters as defined by default.

{% include image.html file="salome/hs12-numerical-pars.png" alt="telemac3d numerical parameters mass-lumping diffusion" %}

### Parameters: Hydrodynamics

Find the **Boundary Conditions** block on the right of the window and add the following elements:


* **Prescribed elevations**: `[0.0; 2.0]` (expand the table to enter values).
* **Prescribed flow rates**: `[50.0; 0.0]` (expanding the table).
* **Velocity profile**: `[Velocity = square root elevation' , 'Velocity = square root elevation']` (IDs: `[4;4]`)
* **Options for liquid boundaries**: `['classical'; 'classical']` (expand the table).



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


