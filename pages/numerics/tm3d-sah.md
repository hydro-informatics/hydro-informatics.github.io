---
title: 3d modelling with TELEMAC
tags: [telemac, numerical, modelling, hydraulics, morphodynamics, hydraulics]
keywords: numerics
sidebar: mydoc_sidebar
permalink: telemac3d.html
folder: numerics
---

This tutorial describes setting up and running a simple three-dimensional (3d) model of a flume based on the *MED* file library provided by [salome-platform.org](https://www.salome-platform.org/). The explanations build on the [telemac3d user manual (v8p1)](http://ot-svn-public:telemac1*@svn.opentelemac.org/svn/opentelemac/tags/v8p1r2/documentation/telemac2d/user/telemac3d_user_v8p1.pdf) and more documentation can be found on [opentelemac.org/doku](http://wiki.opentelemac.org/doku.php?id=documentation_v8p2r0).

{% include requirements.html content="The case featured in this tutorial was established with **[*SALOME-HYDRO* v2_2](install-telemac.html#salome-hydro), [*SALOME 9.6.0*](install-openfoam.html#salome) (yes, both), and a stand-alone installation of [*TELEMAC* v8p2r0](install-telemac.html#modular-install) on *Debian Linux* (*buster*)**." %}

To explore example cases of *Telemac3d*, check out the installation folder of *Salome-Hydro*: **/SALOME-HYDRO/Salome-V2_2-s9/tools/Telemac-v8p2r0/examples/**.

## Introduction

Telemac3d solves the Navier-Stokes equations along a three-dimensional (3D) computational grid using a finite element scheme. Telemac3d mounts the tetrahedral 3D mesh from a triangular 2D mesh in a user-defined number of vertical layers. The number of vertical layers to use is defined in the TELEMAC steering (CAS) file. This tutorial walks through the creation of a 2D mesh with SALOME-HYDRO along with boundary and control files. The tutorial also features running a Telemac3d simulation with the files created and plotting results with the *ParaVis* plugin of *SALOME-9.6.0* (a tweaked version of *ParaView*).

## Input files

A Telemac3d simulation requires similar input files as a Telemac2d simulation and this tutorial uses *MED* files to define the geometry. In particular, the following files will be created:

* Steering file 
    + File format: `cas`
    + Software: SALOME-HYDRO's *HydroSolver* module (alternatively: [Fudaa PrePro](install-telemac.html#fudaa) or any text editor)
* Geometry file 
    + File format: `med` or `slf`
    + Software: SALOME-HYDRO's *Geometry* and *Mesh* modules
* Boundary conditions
    + File format: `.bnd`
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

{% include image.html file="salome/sah-startup.png" alt="telemac3d salome hydro start" %}

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

{% include image.html file="salome/sah-polyline-edited.png" alt="telemac salome hydro edit polygon" %}

{% include tip.html content="Save the project by clicking on the **File** (top menu) > **Save As...**. In the popup menu, select the simulation target folder and define a name such as *flume3d*. Press **Save** to save the project in **hdf** format and regularly press the save button (disk symbol) in the next steps to avoid loosing work. Thus, the project can be saved, closed and re-opened any time." %}

{% include image.html file="salome/save-study-as.png" alt="telemac salome hydro save study as hdf" %} {% include image.html file="salome/save-study-props.png" max-width="637" alt="telemac salome hydro save study hdf" %} 


### Create a Natural Object

From the *HYDRO* top menu, select **Create immersible zone** to define a wetted area for the later created mesh.
{% include image.html file="salome/sah-nat-immersible-zone.png" alt="telemac salome hydro create immersible zone" %} 
 
In the popup window, make the following settings:

* **Name:** `wetted_contour`
* **Polyline:** Select the previously created `Contour` rectangle (double-click in the field).
* **Bathymetry:** Leave empty.

{% include image.html file="salome/sah-nat-wetted-zone.png" alt="telemac salome hydro create wetted area zone" %} 

* Press **Apply and close**.

{% include tip.html content="A **bathymetry** file **assigns bottom elevations** to the geometry and can either be directly added in the HYDRO module or later with the [*STBTEL* software](http://ot-svn-public:telemac1*@svn.opentelemac.org/svn/opentelemac/tags/v8p1r1/documentation/stbtel/user/stbtel_user_v8p1.pdf) that comes along with *TELEMAC*. Not providing a bathymetry file like in this tutorial will set the bottom level to zero." %} 

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

{% include image.html file="salome/sah-exported-calc-case-geometry.png" alt="telemac salome hydro calculation case exported geometry" %} 

<!--
### Build basic shape (2d surface) {#geo2d}

* **Shape Type** (radio buttons in the upper part): select **Surface** (the rectangle)
* **Name**: `FLUME`
* **Main Shape**: select **HYDRO_Hydrodynamic_1**
* Click on **Show all sub-shapes** > **Select All** and make sure that `1` shows up in the white frame.
* Select `1` in the white frame and click **Add** > **Apply**.

{% include image.html file="salome/geo-create-group.png" alt="telemac salome geometry group faces" %} 

The popup window should still be opened and wait for the definition of the four boundaries (edges) of the rectangle.
-->

{% include note.html content="Earlier versions of *SALOME-HYDRO* will also require to create a surface group, which already exists in this case with `Hydrodynamic_Reg_1`." %} 

Right-click on *HYDRO_Hydrodynamic_1* and select **Create Group** from the context menu. 
The four boundary edges of the surface will represent an upstream (inflow), a downstream (outflow), a left wall, and a right wall of the flume. To create the four boundary edges repeat the following steps for every edge:

* **Shape Type** (radio buttons in the upper part): select *Edge* (line symbol)
* **Name**: `upstream` (then `downstream`, `leftwall`, and `rightwall`)
* **Main Shape**: select `HYDRO_Hydrodynamic_1`
* Click on **Show all sub-shapes** > **Select line in the viewport**. In the white frame of the *Create Group* window, make sure to select the good edge only. **Add** the correct edge and **Remove** all others.
 
{% include image.html file="salome/geo-create-group-upstream.png" max-width="1000" alt="telemac salome geometry group faces" caption="Define the upstream edge of the surface." %}

* For defining the other edges (`downstream`, `leftwall`, and `rightwall`), use the indications in the following figure.
 
{% include image.html file="tm-rectangular-flume.png" alt="telemac salome rectangular flume" %} 

* Click **Apply** to create the edge boundary and proceed with the next. After the last (fourth) edge, click **Apply and Close**.

Ultimately, the *Geometry* block in the *Object Browser* should look as follows.

{% include image.html file="salome/geo-created-groups-ob.png" alt="telemac salome geometry group object browser" %}

## Generate a Mesh

To work with the geometry in a numerical model, the geometry needs to be defined as a triangular computational mesh that Telemac3d will extrapolate to a tetrahedral mesh. The *Mesh* module in *SALOME-HYDRO* enables the creation of a mesh with just a view clicks. The mesh is generated first for the surface (2d), then for every boundary edge (1d), and eventually computed and verified. To get ready, activate the **Mesh** module from the top menu.

### Two-dimensional (2d) mesh of the surface 

**Highlight *HYDRO_Hydrodynamic_1***  in the *Object Browser*. Then, go to the **Mesh** top menu (do not confuse with the *Mesh* module), and select **Create Mesh**.

{% include image.html file="salome/mes-01-create-mesh.png" alt="telemac salome mesh create" %} 

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

{% include image.html file="salome/mes-02-create-mesh-netgen2d-hypo.png" max-width="444" alt="telemac salome mesh create netgen 2d hypothesis" %}  {% include image.html file="salome/mes-03-create-mesh-netgen2d.png" alt="telemac salome mesh create netgen 1d-2d" %} 


### One-dimensional (1d) meshes of boundary edges

The 1d meshes of the boundary edges will represent sub-meshes of the 2d mesh. To create the sub-meshes, **highlight** the previously created **Mesh_Hn_1** in the *Object Browser* (click on it), then go to the **Mesh** top menu and select **Create Sub-Mesh**.

{% include image.html file="salome/mes-04-create-submesh-menu.png" max-width="582" alt="telemac salome mesh create" %} 

In the **Create sub-mesh** popup window, start with creating the upstream boundary edge's mesh:

* **Name**: `upstream`
* **Mesh**: `Mesh_Hn_1`
* Leave the **Mesh type** as *Any*
* In the **1D** tab:
    * Choose `Wire Discretisation` for **Algorithm**
    * Find the cogwheel symbol behind the **Hypothesis** field and click on it to construct hypotheses for **Number of Segments**.
    * In the **Hypothesis Construction** popup window:
        + Define **Name** as `Segments_10`
        + Set **Number of Segments** to `10`
        + Set **Type of distribution** to `Equidistant distribution`.
* Back in the **Create Mesh** window, set the just created *Segments10* as **Hypothesis**.
* Click on **Apply** in the **Create sub-mesh** popup window, which will remain open for the definition of the three other boundary edge's meshes.

{% include image.html file="salome/mes-05-create-submesh-hypo.png" alt="telemac salome submesh create number of segments hypothesis" %}  {% include image.html file="salome/mes-06-create-submesh-seg10us.png" alt="telemac salome submesh create wire discretisation" %} 

**Repeat** the above steps for creating sub-meshes for the downstream, left wall, and right wall edges, but with different construction hypotheses.

* For the downstream sub-mesh use **Name** `downstream` and construct the following hypothesis:
    + Type: **Number of Segments**
    + Define **Name** as `Segments_05`
    + Set **Number of Segments** to `5`
    + Set **Type of distribution** to  `Equidistant distribution`.
* For the left wall sub-mesh use **Name** `leftwall` and construct the following hypothesis:
    + Type: **Arithmetic Progression 1D**
    + Define **Name** as `Arithmetic1d10_30`
    + Set **Start length** to `10`
    + Set **End length** to `30`.

{% include image.html file="salome/mes-09-create-submesh-hypoarith1030.png" alt="telemac salome submesh create arithmetic progression hypothesis" %}  {% include image.html file="salome/mes-10-create-submesh-arith1030lw.png" alt="telemac salome submesh create wire discretisation arithmetic" %} 

* For the right wall sub-mesh use **Name** `rightwall` and construct the following hypothesis:
    + Type: **Arithmetic Progression 1D**
    + Define **Name** as `Arithmetic1d15_10`
    + Set **Start length** to `15`
    + Set **End length** to `10`.

To this end, the *Object Browser* should include the 5 hypotheses and the non-computed meshes (warning triangles in the below figure indicating the *Compute* menu).

{% include tip.html content="Save the project by clicking on the disk symbol." %}

{% include note.html content="If an info or warning windows pops up and asks for defining the order to apply, that means the geometry groups contain too many elements. In this case go back to the [geometry creation](#geo2d) and make sure that always only one element is added per group. For more complex models, the order of mesh hypotheses may not be an error, but in this simple case it must not appear being an issue." %}

### Compute Mesh

In the **Object Browser**, extend (un-collapse) the new *Mesh* block, **right-click** on **Mesh_Hn_1**, and select **Compute**.

{% include image.html file="salome/mes-13-start-compute.png" alt="telemac salome compute mesh menu" %}

This will automatically also compute all sub-meshes. After the successful computation of the mesh, *SALOME-HYDRO* informs about the mesh properties in a popup window.
    
{% include image.html file="salome/mes-14-end-compute.png" alt="smesh compute netgen 2d 3d" %}

In the view port (*VTK scene* tab), find the **-OZ** button to switch to plane view. If the mesh is not visible even though the computation was successful, right-click on the mesh in the *Object Browser* and click on **Show**.

{% include image.html file="salome/mes-15-gotoOZ.png" alt="smesh show only" %}

### Verify Mesh

***Orientation of faces and volumes***

This step will ensure that the mesh is correctly oriented for the simulation with *Telemac3d*. In the *Object Browser*, highlight *Mesh_Hn_1* and then go to the **Modification** top menu > **Orientation**. In the pop-up window, check the **Apply to all** box. Click the **Apply and close** button. The mesh should have changed from darker blue to a lighter tone of blue (if the inverse is the case, repeat the application of the orientation tool).

{% include image.html file="salome/mes-16-mod-orient.png" alt="mesh modification orientation" %}

***Identify and reconcile over-constraint elements***

In the *Object Browser*, **highlight *Mesh_Hn_1***. Then go to the **Controls** top menu > **Face Controls** > **Over-constraint faces**. Over-constrained triangles in the *Mesh_Hn_1* will turn red in the viewport (*VTK scene:1*) and at the bottom of the viewport, the note *Over-constrained faces: 3* will appear.

{% include image.html file="salome/mes-17-mod-over-const.png" alt="mesh over constrained constraint faces" %}

To reconcile the edge cause the triangle's over-constrain, go to the **Modification** top menu > **Diagonal inversion**, and select the internal edge of the concerned triangles.

{% include image.html file="salome/mes-18-mod-over-const-edge-select.png" alt="mesh over-constrained diagonal inversion internal edges triangle" %}

Over-constrained triangles might be hidden in by the axes arrows in the corner. Thus, pay attention to sufficiently zoom into the corner unless the *Over-constrained faces* notification in the viewport shows **0**.

{% include image.html file="salome/mes-19-mod-over-const-edge-hidden.png" alt="mesh over-constrained diagonal inversion hidden edges faces" %}

{% include tip.html content="Save the project by clicking on the disk symbol." %}

## Export MED File {#med-export}

Exporting the mesh to a MED file requires the definition of mesh groups. To do so, highlight *Mesh_Hn_1* in the object browser and right-click on it. Select **Create Groups from Geometry** from the mesh context menu.

{% include image.html file="salome/mes-20-create-group-menu.png" alt="mesh export create groups context menu" %}

In the popup window, select all groups and sub shapes of the *FLUME* geometry and all groups of **mesh elements** and **mesh nodes**. For selecting multiple geometries, hold down the `CTRL` (`Strg`) and `Shift` keys on the keyboard and select the geometry/mesh groups. The tool will automatically add all nodes selected. Press **Apply and close** to finalize the creation of groups.

{% include image.html file="salome/mes-21-create-group.png" alt="mesh export create groups select" %}

Verify the created groups by right-clicking on the top of the project tree in the *Object Browser* and selecting *Show only* with the option *Auto Color*.

{% include image.html file="salome/mes-21-final-groups.png" alt="mesh export create groups final control" %}

{% include warning.html content="Make sure that every group element is unique within every group. If an element appears twice in one group, the next step (export mesh) will through a warning message about double-defined group elements, which will lead to an error later." %}

 If the groups seems correct (see above figure), export them with **File** (top menu) > **Export** > **MED**.

{% include image.html file="salome/mes-22-export-med-menu.png" alt="mesh export med context menu" %}

In the **Export mesh** popup window, define:

* **File name** `Mesh_Hn_1` (or whatever you prefer)
* **Files of type** `MED 4.1 files` <br>*Note: The installation of *TELEMAC* described in the [installation section](install-telemac.html#med-hdf) requires to use **`MED 3.2 files`**.*
* Choose a convenient directory (*Quick path*) for saving the *MED* file
* Leave all other default settings.
* Click on **Save** to save the *MED* file.

{% include image.html file="salome/mes-23-export-med.png" alt="telemac salome save med file" %}

{% include tip.html content="Save the project by clicking on the disk symbol." %}

## Generate Boundary Conditions 

### Basic Setup with the HydroSolver Module

Activate the **HydroSolver** module from the top menu and click on the *Edit boundary conditions file* button to create a new boundary condition file.

{% include image.html file="salome/hs01-edit-bc.png" alt="telemac salome hydrosolver create edit boundary conditions menu" %}

In the opening popup window, select the just exported **MED** file containing the mesh and leave the *Boundary conditions file* field in the *Input files* frame free. In the **Output files** frame, click on **...** and define a boundary conditions file (e.g., `flume3d_bc.bnd`).

{% include important.html content="Make sure that all model (*MED*, *BND*, and others such as the later defined *CAS*) files are all located in the same folder." %}

Make the following definitions in the **Boundary conditions** frame (table): 

* Group **Hydrodynamic_wetted_contour_Outer**: Set **Preset** to **Custom** and all values to `0`
* Group **downstream**: Set **Preset** to **Prescribed H / free T**
* Group **leftwall**: Set **Preset** to **Closed boundaries/walls**
* Group **rightwall**: Set **Preset** to **Closed boundaries/walls**
* Group **upstream**: Set **Preset** to **Prescribed Q / free T**

{% include image.html file="salome/hs02-create-bc.png" alt="telemac salome hydrosolver create edit boundary conditions" %}

Then click on **Apply and Close**. 

### Modify the Boundary File {#bnd-mod}

The boundary file created with the *HydroSolver* involves a couple of issues that need to be resolved to enable *TELEMAC* assigning the correct boundary conditions. For this purpose, open the  boundary condition file in a text editor (e.g., on *Xfce* desktop use right-click > *mousepad*) and make the following adaptations.

* Only 4 edge boundaries are needed:
    + Set the single number in the first line to `4`
    + Remove the entire line (2) describing  Group **Hydrodynamic_wetted_contour_Outer**
* To enable the coherent use of flow rates for liquid boundaries, make sur that:
    + Line 2 defines `LIHBOR` with `5` (prescribed depth), `LIUBOR` and `LIVBOR` with `4` (free velocity), and `LITBOR` with `4` (free tracer) for the **downstream** boundary edge.
    + Line 3 defines `LIHBOR` with `4` (free depth), `LIUBOR` and `LIVBOR` with `5` (prescribed flow rate), and `LITBOR` with `4` (free tracer) for the **upstream** boundary edge. Note that the line needs to be copied from the bottom to the top when using the *bnd* file created with the *HydroSolver* module.
* Assign wall friction (i.e., zero velocities) to the left and right wall edges:
    + In Line 4, set `LIUBOR` and `LIVBOR` to `0` (zero *U* and *V* velocities, respectively) for the **leftwall** boundary edge.
    + In Line 5, set `LIUBOR` and `LIVBOR` to `0` (zero *U* and *V* velocities, respectively) for the **rightwall** boundary edge.  

The boundary file should now resemble the block below (can also be downloaded [here](https://raw.githubusercontent.com/Ecohydraulics/telemac-helpers/master/model-templates/flume3d_bc.bnd)). Save and close the *bnd* file.

```
4
5 4 4 4 downstream
4 5 5 4 upstream
2 0 0 2 leftwall
2 0 0 2 rightwall

```


{% include note.html content="*SLF* geometry files require more complex (node-wise) definitions of boundaries, which need to be setup with [*BlueKenue<sup>TM</sup>*](install-telemac.html#bluekenue) and [*Fudaa-PrePro*](install-telemac.html#fudaa)." %}

## Create Simulation Case (CAS)

The *CAS* (`.cas`) file is the control (or *steering*) file for any *TELEMAC* simulation and links all model parameters. This section guides through setting up a simple *CAS* file for *Telemac3d* simulations either manually based on a template or with the *HydroSolver module* in *SALOME-HYDRO*. Because of program instabilities and incoherent linking of file names (directories) in *SALOME-HYDRO*, it is recommended working with the manual CAS file setup (or with Fudaa PrePro).

{% include tip.html content="Copy a sample case from the *TELEMAC* folder (*/telemac/v8p2/examples/telemac3d/*) and edit it for convenience." %}
{% include windows.html content="The *CAS* file can also be edited/created with [Fudaa PrePro](install-telemac.html#fudaa) - or any text editor software -  for use with *Salome-Hydro* on a *Linux* system later." %}

### Overview: Manual CAS File Setup (Recommended)

The following CAS template uses the following input files:

* The boundary condition file named `flume3d_bc.bnd` (see [boundary file section](#bnd-mod))
* The geometry *MED* file `Mesh_Hn_1.med` (see [med file export section](#med-export))

The CAS file defines a steady, hydrodynamic model with an inflow rate of 50 m<sup>3</sup>/s (prescribed upstream flow rate boundary) and an outflow depth of 2 m (prescribed downstream elevation). The simulation uses 5 vertical layers that constitute a numerical grid of prisms. 3d outputs of *U* (*x*-direction), *V* (*y*-direction), and *W* (*z*-direction) velocities, as well as the elevation *Z*, are written to a file named `r3d_canal-t3d.med`. 2d outputs of depth-averaged *U* velocity (*x*-direction), depth-averaged *V* velocity (*y*-direction), and water depth *h* are written to a file named `r2d3d_canal-t3d.med`.

The below code block shows the steering file `t3d_flume.cas` and details for every parameter are provided after the code block. The `\` escape character comments out lines (i.e., *TELEMAC* will ignore anything in a line the `\` character). The `:` character separates `VARIABLE NAME` and `VALUE`s. Alternatively to the `:`, also a `=` sign may be used. 

{% include tip.html content="To facilitate setting up the steering (CAS) file for this tutorial, [download the template](https://raw.githubusercontent.com/Ecohydraulics/telemac-helpers/master/model-templates/t3d_template.cas) (right-click on the link > *Save Link As...* > navigate to the local tutorial folder), which contains more descriptions and options for simulation parameters." %}

```yaml
/ t3d_flume.cas
/------------------------------------------------------------------/
/			COMPUTATION ENVIRONMENT
/------------------------------------------------------------------/
TITLE : 'TELEMAC 3D FLUME'
MASS-BALANCE : YES
/
BOUNDARY CONDITIONS FILE : flume3d_bc.bnd
GEOMETRY FILE            : Mesh_Hn_1.med
GEOMETRY FILE FORMAT 	 : 'MED'
3D RESULT FILE           : r3d_canal-t3d.med
3D RESULT FILE FORMAT    : 'MED'
2D RESULT FILE           : r2d3d_canal-t3d.med
2D RESULT FILE FORMAT    : 'MED'
/
VARIABLES FOR 2D GRAPHIC PRINTOUTS : U,V,H
VARIABLES FOR 3D GRAPHIC PRINTOUTS : Z,U,V,W
/
/------------------------------------------------------------------/
/			GENERAL PARAMETERS
/------------------------------------------------------------------/
TIME STEP : 1.
NUMBER OF TIME STEPS : 5000
GRAPHIC PRINTOUT PERIOD : 100
LISTING PRINTOUT PERIOD : 100
/
/------------------------------------------------------------------/
/			VERTICAL
/------------------------------------------------------------------/
/ vertical cell height defined by initial condition x no. of levels
/ default and minimum is 2, upward vertical direction
NUMBER OF HORIZONTAL LEVELS : 5 
/
/------------------------------------------------------------------/
/			NUMERICAL PARAMETERS
/------------------------------------------------------------------/
/
/ CONVECTION-DIFFUSION
/------------------------------------------------------------------
SCHEME FOR ADVECTION OF VELOCITIES : 5
SCHEME FOR ADVECTION OF K-EPSILON : 5
SCHEME FOR ADVECTION OF TRACERS : 5
/ scheme options - use 2 for disabling tidal flats and increase speed
SCHEME OPTION FOR ADVECTION OF VELOCITIES : 4
SCHEME OPTION FOR ADVECTION OF K-EPSILON : 4
SCHEME OPTION FOR ADVECTION OF TRACERS : 4
/
SUPG OPTION : 2;2;2;2  / classic supg for U and V  see docs sec 6.2.2
/
/ PROPAGATION HEIGHT AND STABILITY
/ ------------------------------------------------------------------
IMPLICITATION FOR DEPTH : 0.55 / should be between 0.55 and 0.6
IMPLICITATION FOR VELOCITIES : 0.55 / should be between 0.55 and 0.6
IMPLICITATION FOR DIFFUSION : 1.
FREE SURFACE GRADIENT COMPATIBILITY : 0.1  / default 1.
/
/------------------------------------------------------------------/
/			HYDRODYNAMICS
/------------------------------------------------------------------/  
/
/ HYDRODYNAMIC SOLVER
/------------------------------------------------------------------
NON-HYDROSTATIC VERSION : YES / use default solver number 7 (GMRES)
MAXIMUM NUMBER OF ITERATIONS FOR DIFFUSION OF VELOCITIES : 100 / default is 60
/
/ BOUNDARY CONDITIONS
/------------------------------------------------------------------
/ Use Nikuradse roughness law - all others are not 3D compatible
LAW OF BOTTOM FRICTION : 5
LAW OF FRICTION ON LATERAL BOUNDARIES : 5  / for natural banks - 0 for symmetry
FRICTION COEFFICIENT FOR THE BOTTOM : 0.1 / 3 times d90 according to van Rijn
/
/ Liquid boundaries 
PRESCRIBED FLOWRATES  : 0.;50.
PRESCRIBED ELEVATIONS : 2.;0.
/
/ INITIAL CONDITIONS
/ ------------------------------------------------------------------
INITIAL CONDITIONS : 'CONSTANT ELEVATION'
INITIAL ELEVATION : 50 / corresponds to depth here - not son in boundary file
INITIAL GUESS FOR DEPTH : 1 / INTEGER for speeding up calculations
/
/ Type of velocity profile can be 0-user defined) 1-constant (default), 2-Log
VELOCITY PROFILE : 1 / horizontal profile
VELOCITY VERTICAL PROFILES : 2;2  
/
/------------------------------------------------------------------/
/			TURBULENCE
/------------------------------------------------------------------/
/ in 3d use 3-k-epsilon model, alternatively 5-Spalart-Allmaras or 4-Smagorinsky for highly non-linear flow 
HORIZONTAL TURBULENCE MODEL : 3
VERTICAL TURBULENCE MODEL : 3
MIXING LENGTH MODEL : 3
/
&ETA
```

### Computation Environment

The computation environment defines a **Title** (e.g., `TELEMAC 3D FLUME`). The most important parameters involve the **input** files:

* `GEOMETRY FILE`: `Mesh_Hn_1.med` - alternatively, select a *serafin* (SLF) geometry file
* `Geometry file format`: `MED` - omit this parameter when use a *SLF* geometry file
* `Boundary conditions file`: `flume3d_bc.bnd` - with a *SLF* file, use a *CLI* boundary file

In the **output** can be defined with the following keywords:

* `3D RESULT FILE`: `r3d_canal.med` - can be either a *MED* file or a *SLF* file
* `2D RESULT FILE`: `r2d3d_canal.med` - can be either a *MED* file or a *SLF* file
* `3D RESULT FILE FORMAT`: `'MED'` - can be omitted when using *SLF* output files
* `2D RESULT FILE FORMAT`: `'MED'` - can be omitted when using *SLF* output files
* `VARIABLES FOR 3D GRAPHIC PRINTOUTS`:  `Z,U,V,W` - many more options can be found in section 3.12 of the [Telemac 3d docs](http://ot-svn-public:telemac1*@svn.opentelemac.org/svn/opentelemac/tags/v8p1r1/documentation/telemac3d/user/telemac3d_user_v8p1.pdf) 
* `VARIABLES FOR 2D GRAPHIC PRINTOUTS`:  `U,V,H` - many more options can be found in section 3.13 of the [Telemac 3d docs](http://ot-svn-public:telemac1*@svn.opentelemac.org/svn/opentelemac/tags/v8p1r1/documentation/telemac3d/user/telemac3d_user_v8p1.pdf) 

In addition, the `MASS-BALANCE : YES` setting will printout the mass fluxes and error in the computation region, which is an important parameter for verifying the plausibility of the model.

### General Parameters

The *General parameters* specify *time* and *location* settings for the simulation:

* **Location** can be used for geo-referencing of outputs (not to set in this tutorial).
* **Time**:
    + `TIME STEP`: `1.0` defines the time step as a multiple of graphic / listing printout period.*Use small enough and sufficient time steps to achieve/increase computational stability and increase for computational efficiency.* 
    + `NUMBER OF TIME STEPS` : `5000` defines the overall simulation length. <br>*Limit the number of time steps to a minimum (e.g., until equilibrium conditions are reached in a steady simulation).*
    + `GRAPHIC PRINTOUT PERIOD` : `100` time step at which graphic variables are written (in this example `5000` / (`100` · `1.0`) = 50 graphic printouts will be produced, i.e., every `100` · `1.0` = 100 seconds)
    + `LISTING PRINTOUT PERIOD` : `100` time step multiplier at which listing variables are printed (in this example, listings are printed every `100` · `1` = 100 seconds)

Modify the time parameters to examine the effect in the simulation later.
 
{% include important.html content="Graphic printouts, just like all other data printouts, are time consuming and will slow down the simulation." %}


### Vertical (3d) Parameters

*Telemac3d* will add *Horizontal levels* (i.e., layers) that correspond to copies of the 2d-mesh to build a 3d-mesh of prisms (default) or tetrahedrons. These parameters can be defined with:

* `NUMBER OF HORIZONTAL LEVELS` : `5` where the default and minimum is `2` and the horizontal levels point in upward vertical direction. The thickness of vertical layers results from the water depth, which can be user-defined through the `INITIAL ELEVATION` parameter (see [initial conditions](#inc)).
* `MESH TRANSFORMATION` : `1` is the kind of level for the distribution (default is `1`, a homogenous sigma distribution). For unsteady simulations, set this value to `2` (or `0` - calcot) and implement a `ZSTAR` array in a user fortran file (`USER_MESH_TRANSFORM` subroutine).
* `ELEMENT` : `'PRISM'` (default) and prisms can optionally split into tetrahedrons by settings this parameter to `'TETRAHEDRON'` (can potentially crash the simulation).

{% include tip.html content="For unsteady simulations (time-variable inflow/outflow rates), pre-define the thickness of vertical layers with the `ZSTAR` parameter in a user fortran file (subroutine) as described in section 4.1 of the [Telemac 3d docs](http://ot-svn-public:telemac1*@svn.opentelemac.org/svn/opentelemac/tags/v8p1r1/documentation/telemac3d/user/telemac3d_user_v8p1.pdf)." %}

To get started with writing subroutines (it is no magic neither), have a look at the **bottom_bc** example (`~/telemac/v8p2/examples/telemac3d/bottom_bc/`). In particular, examine the user fortran file `/user_fortran-source/user_mesh_transf.f` and its call in the steering file `t3d_bottom_source.cas` through the definition of the `FORTRAN FILE` keyword and setting of `MESH TRANSFORMATION = 2`.

### Numerical Parameters

This section defines internal numerical parameters for the *Advection* and *Diffusion* solvers, which are also sometimes listed in the section of [hydrodynamic parameters](#hydrodynamics) in *TELEMAC* documentations. 

In *Telemac3d*, it is recommended to use the so-called distributive predictor-corrector (PSI) scheme ([read more](https://henry.baw.de/bitstream/handle/20.500.11970/104314/13_Hervouet_2015.pdf?sequence=1&isAllowed=y) at the BAW's hydraulic engineering repository) with local implication for tidal flats (for velocity, tracers, and k-epsilon):

* Set the PSI scheme:
    + `SCHEME FOR ADVECTION OF VELOCITIES`: `5`
    + `SCHEME FOR ADVECTION OF K-EPSILON`: `5`
    + `SCHEME FOR ADVECTION OF TRACERS`: `5`
* Enable predictor-corrector with local implication:
    + `SCHEME OPTION FOR ADVECTION OF VELOCITIES`: `4`
    + `SCHEME OPTION FOR ADVECTION OF K-EPSILON`: `4`
    + `SCHEME OPTION FOR ADVECTION OF TRACERS`: `4`

These values (`5` for the scheme and `4` for the scheme option) are default values since *TELEMAC v8p1*, but it still makes sense to define these parameters for enabling backward compatibility of the steering file. If the occurrence of tidal flats can be excluded (note that already a little backwater upstream of a barrier can represent a tidal flat), the `SCHEME OPTIONS` can generally set to `2` for speeding up the simulation.

Similar as for advection, the above keywords can be used to define diffusion steps (replace `ADVECTION` with `DIFFUSION` in the keywords), where a value of `0` can be used to override the default value of `1` and disable diffusion.

{% include callout.html content="**Recall**: **Advection** represents the motion of particles along the bulk flow. **Diffusion** is the result of random motion of particles, driven by differences in concentration (e.g., dissipation of highly concentrated particles towards regions of low concentration). **Convection** encompassed both time-dependent phenomena." %} 

The `SUPG OPTION` (Streamline Upwind Petrov Galerkin) keyword is a list of four integers that define if upwinding applies and what type of upwinding applies. The integers may take the following values:

* `0` disables upwinding,
* `1` enables upwinding with a classical SUPG scheme (recommended when the [Courant number](https://en.wikipedia.org/wiki/Courant-Friedrichs-Lewy_condition) is unknown), and
* `2` enables upwinding with a modified SUPG scheme, where upwinding corresponds to the Courant number.

The default is `SUPG OPTION : 1;0;1;1`, where the first list element refers to flow velocity (default `1`), the second to water depth (default `0`), the third to tracers (default `1`), and the last to the k-epsilon model (default `1`). Read more in section 6.2.2 of the [Telemac 3d docs](http://ot-svn-public:telemac1*@svn.opentelemac.org/svn/opentelemac/tags/v8p1r1/documentation/telemac3d/user/telemac3d_user_v8p1.pdf).

An additional option for speeding up is to enable mass lumping for diffusion, depth, and/or weak characteristics. Mass lumping results in faster convergence, but it introduces artificial dispersion in the results, which is why enabling mass lumping is discouraged by the *TELEMAC* developers. The provided [*t3d_template.cas*](https://raw.githubusercontent.com/Ecohydraulics/telemac-helpers/master/model-templates/t3d_template.cas) includes the keywords for mass lumping, though they are disabled.

**Implication parameters** (`IMPLICITATION FOR DEPTH` and `IMPLICITATION FOR VELOCITIES`) should be set between 0.55 and 0.60 (default is 0.55 since *TELEMAC v8p1*) and can be considered as a degree of implicitation. `IMPLICITATION FOR DIFFUSION` is set to `1.0` by default. Read more in section 6.4 of the [Telemac 3d docs](http://ot-svn-public:telemac1*@svn.opentelemac.org/svn/opentelemac/tags/v8p1r1/documentation/telemac3d/user/telemac3d_user_v8p1.pdf).

The parameter `FREE SURFACE GRADIENT` can be used for increasing the stability of a model. Its default value is `1.0`, but it can be reduced to `0.1` to achieve stability.

### Hydrodynamic Parameters <a name="hydrodynamics"></a>

In river analyses, the non-hydrostatic version of *TELEMAC* should be used through the following keyword: `NON-HYDROSTATIC VERSION : YES``.

Depending on the type of analysis, the solver-related parameters of `SOLVER`, `SOLVER OPTIONS`, `MAXIMUM NUMBER OF ITERATION`, `ACCURACY`, and `PRECONDITIONING` may be modified. The provided [*t3d_template.cas*](https://raw.githubusercontent.com/Ecohydraulics/telemac-helpers/master/model-templates/t3d_template.cas) includes solver keywords and comments for modifications, but the default options already provide a coherent a stable setup. Read more about solver parameters in section 6.5 of the [Telemac 3d docs](http://ot-svn-public:telemac1*@svn.opentelemac.org/svn/opentelemac/tags/v8p1r1/documentation/telemac3d/user/telemac3d_user_v8p1.pdf).


Parameters for **Boundary Conditions** enable the definition of roughness laws and properties of liquid boundaries.

With respect to roughness, *TELEMAC* developers recommend using the [*Nikuradse*](https://en.wikipedia.org/wiki/Johann_Nikuradse) roughness law in 3d (number `5`), because all others are not meaningful or not integrally implemented in the 3d version. To apply the *Nikuradse* roughness law to the bottom and the boundaries use:

* `LAW OF BOTTOM FRICTION`: `5`
* `LAW OF FRICTION ON LATERAL BOUNDARIES`: `5`, which can well be applied to model natural banks, or alternatively set to `0` (no slip) for symmetry.<br>*Note that the [boundary conditions file](#bnd-mod) sets the `LIUBOR` and `LIVBOR` for the `leftwall` and `rightwall` boundary edges to zero, to enable friction.
* `FRICTION COEFFICIENT FOR THE BOTTOM`: `0.1` corresponds to 3 times a hypothetical *d90* (grain diameter of which 90% of the surface grain mixture are finer) according to [van Rijn](https://www.leovanrijn-sediment.com/).
* `FRICTION COEFFICIENT FOR LATERAL SOLID BOUNDARIES`: `0.1` corresponds to 3 times a hypothetical *d90*, similar as for the bottom.

The liquid boundary definitions for `PRESCRIBED FLOWRATES` and `PRESCRIBED ELEVATIONS` correspond to the definitions of the **downstream** boundary edge in line 2 and the **upstream** boundary edge in line 3 (see [boundary definitions section](#bnd-mod)). From the boundary file, *TELEMAC* will understand the **downstream** boundary as edge number **1** (first list element) and the **upstream** boundary as edge number **2** (second list element). Hence:

* The list parameter `PRESCRIBED FLOWRATES : 0.;50.` assigns a flow rate of zero to the **downstream** boundary and a flow rate of 50 m<sup>3</sup>/s to the **upstream** boundary.
* The list parameter `PRESCRIBED ELEVATIONS : 2.;0.` assigns an elevation (i.e., water depth) of two m to the **downstream** boundary and a water depth of 0.0 m to the **upstream** boundary. 

The `0.` value for the flow rate does physically not make sense at the downstream boundary, but because they do not make sense, and because the boundary file (`flume3d_bc.bnd`) only defines (*prescribes*) water depth, *TELEMAC* will ignore the zero-flow rate at the downstream boundary.

Similarly, the `0.` value for the water does physically not make sense at the upstream boundary, but because they do not make sense, and because the boundary file (`flume3d_bc.bnd`) only defines (*prescribes*) a flow rate (by setting `LIUBOR` and `LIVBOR` to `5`), *TELEMAC* will ignore the zero-water depth at the upstream boundary.

Instead of a list in the steering *CAS* file, the liquid boundary conditions can also be defined with a liquid boundary condition file in *ASCII* text format. For this purpose, a `LIQUID BOUNDARIES FILE` or a `STAGE-DISCHARGE CURVES FILE` (sections 4.3.8 and 4.3.10 in the [Telemac 3d docs](http://ot-svn-public:telemac1*@svn.opentelemac.org/svn/opentelemac/tags/v8p1r1/documentation/telemac3d/user/telemac3d_user_v8p1.pdf), respectively can be defined. The [*t3d_template.cas*](https://raw.githubusercontent.com/Ecohydraulics/telemac-helpers/master/model-templates/t3d_template.cas) file includes these keywords in the *COMPUTATION ENVIRONMENT* section, even though they are disabled. A liquid boundary file (*QSL*) may look like this:

```
# t3d_canal.qsl
# time-dependent inflow upstream-discharge Q(2) and outflow downstream-depth SL(1)
T           Q(2)     SL(1)
s           m3/s     m
0.            0.     5.0
500.        100.     5.0
5000.       150.     5.0
```

{% include tip.html content="The `ELEVATION` parameter in the *CAS* file denotes water depth, while the `ELEVATION` keyword in an external liquid boundary file (e.g. stage-discharge curve) refers to absolute (geodetic) elevation (`Z` plus `H`)." %} 

<a name="inc"></a>
The **initial conditions** describe the condition at the beginning of the simulation. This tutorial uses a constant elevation (corresponding to a constant water depth) of `2.`, and enables using an initial guess for the water depth to speed up the simulation:

* `INITIAL CONDITIONS`: `'CONSTANT ELEVATION'` can alternatively be set to `'CONSTANT DEPTH'` 
* `INITIAL ELEVATION`: `2.` corresponds to depth here, but would be different in an external liquid boundary file (see above).
* `INITIAL DEPTH`: ` 2.` is not used in this tutorial.
* `INITIAL GUESS FOR DEPTH`: `1` must be an **integer** value and speeds up the calculation (convergence).

Read more about the initial conditions in section 4.2 of the [Telemac 3d docs](http://ot-svn-public:telemac1*@svn.opentelemac.org/svn/opentelemac/tags/v8p1r1/documentation/telemac3d/user/telemac3d_user_v8p1.pdf).






* `Velocity profile`: `[Velocity = square root elevation' , 'Velocity = square root elevation']` (IDs: `[4;4]`)
* `Options for liquid boundaries`: `['classical'; 'classical']` (expand the table).

### Turbulence


* `MIXING LENGTH MODEL` : `3` sets the model for computing vertical diffusivity to *Nezu and *Nakagawa*. The default is `1`, which is preferable for strong tidal influences. Read more in section 5.2.2 of the [Telemac 3d docs](http://ot-svn-public:telemac1*@svn.opentelemac.org/svn/opentelemac/tags/v8p1r1/documentation/telemac3d/user/telemac3d_user_v8p1.pdf).

### *HydroSolver* CAS File Setup (Unstable)

Go to the **Hydro** top menu > **Edit cas file (English)** and a popup window along with a new frame will open.

{% include image.html file="salome/hs04-create-cas-menu.png" max-width="478" alt="telemac create edit cas file menu" %}

The popup window will ask for the version of *TELEMAC* (i.e., the solver) to use. Select **telemac3d** and clock **Ok**.

{% include image.html file="salome/hs05-cas-choose-solver.png" alt="telemac create edit cas file choose solver version" %}

In the new frame (*Eficas Telemac* viewport), go to **File** > **New** for creating a new *CAS* (case or *French* *cas*).

{% include image.html file="salome/hs06-create-cas-new.png" alt="telemac create new cas file" %}

A new *unnamed file1* case is created and opens up in the *Computation environment* frame. To make sure that no information will be lost, save the new case *CAS* file (e.g., as `flume3d-steady.cas`).

{% include image.html file="salome/hs08-cas-save-as.png" alt="telemac new cas file save as" %}
{% include image.html file="salome/hs09-cas-save-popup.png" alt="telemac new cas file save" %}




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


[tm3d-doc]: http://ot-svn-public:telemac1*@svn.opentelemac.org/svn/opentelemac/tags/v8p1r1/documentation/telemac3d/user/telemac3d_user_v8p1.pdf
