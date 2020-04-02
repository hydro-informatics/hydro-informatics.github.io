---
title: Pre-Processing with *QGIS*
keywords: numerics
summary: "Produce a numerical mesh with *QGIS*."
sidebar: mydoc_sidebar
permalink: bm-pre.html
folder: numerics
---

## Pre-processing with *QGIS*

To start any analysis of rivers and fluvial landscapes, a digital elevation model (**DEM**) is required. Nowadays, DEMs mostly are a compiste result of light imaging, detection, and ranging ([LiDAR](https://en.wikipedia.org/wiki/Lidar)) and bathymetric surveys. LiDAR employs lights sources and provides terrain assessments up to 2-m deep waters. Deeper waters require additional bathymetric surveys with [echo sounding](https://en.wikipedia.org/wiki/Echo_sounding) methods.
Merging LiDAR and bathymetric data produces point clouds that may be stored in many different file types. The first step in river modelling consist in the conversion of such point clouds into usable DEMs and computational meshes. This page guides through the conversion of a point cloud into a computational mesh with *QGIS* and the *BASEmesh* plugin. The descriptions refer to the developer's documentation files ([go to the ETH Zurich's *BASEMENT* documentation](https://*BASEMENT*.ethz.ch/download/documentation/docu3.html)).


## Get ready with *QGIS*<a name="start-qgis"></a>
Download and install the latest version of the open-access GIS software [*QGIS*](https://www.*QGIS*.org). Start *QGIS*, create a new project and save it (PROJECT > SAVE AS…). Then, set the project coordinate reference system (CRS) by clicking on `Project` > `Properties` > `CRS` tab and select `GERMANY_ZONE_3 (ESRI:31493)`. Install *BASEMENT*’s *BASEmesh* Plugin (instructions from the *BASEMENT* System Manual):
1. Load the *QGIS* plugin manager: `Plugins` menu > `Manage and Install Plugins` (see details in [figure](#qgis-plugins))
1. Go to the Settings tab; now the *QGIS*-plugin repository connections should be visible at the bottom of the `Plugin Manager` (`Plugin Repositories` listbox in below [figure](#qgis-plugins)).
1. Scroll to the bottom, click on Add..., and enter a name for the new repository (e.g., *BASEmesh* repository)
1. Enter the repository address: [http://people.ee.ethz.ch/~BASEMENT/QGIS_plugins/QGIS_plugins.xml]([http://people.ee.ethz.ch/~BASEMENT/QGIS_plugins/QGIS_plugins.xml])
1. Click `OK`. The new repository should now be visible in the `Plugin Repositories` listbox. If the connection is `OK`, click on the Close button on the bottom of the window.
1. Verify that the *BASEmesh* plugin is now available in the *QGIS*' Plugin menu (see [figure](#qgis-pluggedin)).

<a name="qgis-plugins"></a>
{% include image.html file="qgis-plugins.png" alt="bm-1" caption="Installation of the BASEmesh plugin." %}
<a name="qgis-pluggedin"></a>
{% include image.html file="qgis-pluggedin.png" alt="bm-2" caption="The BASEmesh plugin is available in QGIS' Plugins menu after successful installation." %} 


## Elevation point data<a name="epd"></a>
Terrain survey data are mostly delivered in the shape of an x-y-z point dataset. LiDAR produces massive point clouds, which quickly overcharge even powerful computers. Therefore, lidar data may need to be break down to smaller zones of less than approximately 106 points and special lidar point-treatment software (e.g., http://lastools.org/) may be helpful in this task. The range of possible data products and shape from terrain survey is board and this tutorial ex-emplary uses a set of x-y-z points stored within a text file. Load the points from the provided xyz-points.txt file as follows:

1. In *QGIS*, click on the `Layer` menu > `Add Layer` > `Add Delimited Text Layer...` (see [figure](#qgis-add-lyr))
1. In the `Add Delimited Text Layer` wizard (see details in Figure 4):
    * Choose *points.txt* in the `File name` field
    * Name the new layer (e.g., points)
    * In the `File Format` canvas, select `Custom Delimiters` and activate the `Space` checkbox
    * In the `Record` and Field Options canvas`, deactivate the `First record has field names` checkbox
    * In the `Geometry Definition` canvas, define the `Point Coordinates` as `X Field` = `FIELD_1`, `Y Field` = `FIELD_2` and `Z Field` = `FIELD_3`; set the `Geometry CRS` to the `Project CRS`.
    * Click the ADD button on the bottom of the wizard window. The points should now be plotted in the main *QGIS* window.
	
<a name="qgis-add-lyr"></a>
{% include image.html file="qgis-add-lyr.png" alt="bm-3" caption="Open the `Add Delimited Text Layer` import wizard." %} 

<a name="qgis-export-pts"></a>
{% include image.html file="qgis-export-pts.png" alt="bm-4" caption="Load the xyz-points.txt file with QGIS' Add Delimited Text Layer wizard." %}

Next, export the new point layer as shapefile: In *QGIS*' `Layer`S window, right-click on XYZ-POINTS, then `Export` > `Save Features As...` . In the Format field, select `ESRI Shapefile`. Define a FILE NAME (by clicking on the … button and defining for example *C:\QGIS-projects\xyz-points.shp*), ensure that the ADD SAVED FILE TO MAP checkbox is activated (on the bottom of the `Save Vector Layer As...` window) and click `OK`. Remove the `points` text layer from the `Layers` window (only the shape file should be visible here now).
Finally, rename the three fields (`FIELD_1`, `FIELD_2`, `FIELD_3`) to `X`, `Y`, and `Z`, respectively. The fields can be renamed with a double-click on the `xyz-points` layer (opens `Layer Properties`), then left-click on the `Fields` ribbon, activate the editing mode (click on the pen symbol) and edit the `Name` fields.

## Model Boundary<a name="boundary"></a>
The model boundary defines the calculation extent and needs to be define within a polygon shapefile that encloses all points in the above produced point shapefile. *QGIS* provides a Convex Hull tool that enables the automated creation of the outer boundary. This tool is used as follows:

- In *QGIS*' `Processing` menu, select `Toolbox` (see [figure](#qgis-tbx)). The `Toolbox` sub-window opens now.
- In the toolbox, click on `Vector Geometry` > `Concave Hull (Alpha Shapes)`, which opens the `Concave Hull (Alpha Shapes)` wizard (see [figure](#qgis-chull)).
- In the `Concave Hull (Alpha Shapes)` wizard, select the `xyz-points` layer as `Input Layer`, set the `Threhold` to 0.300 (keep default), define an output `Concave Hull` shapefile (e.g., `boundary.shp`) by clicking on the `...` button, and click on `Run`.

<a name="qgis-tbx"></a>
{% include image.html file="qgis-tbx.png" alt="bm-5" caption="Open QGIS' Toolbox from the main menu." %} 

<a name="qgis-chull"></a>
{% include image.html file="qgis-chull.png" alt="bm-6" caption="The Concave Hull (Alpha Shapes) wizard." %}


- Right-click on *QGIS*' `Settings` menu, and activate the `Snapping` toolbar checkbox. In the now shown snapping toolbar, activate snapping with a click on the horseshoe icon.
- Adapt the boundary.shp polygon to a tighter fit of the shapefile nodes by clicking on the `Toggle editing` (pen) symbol and activating the `Vertex Tool` in the toolbar.

<a name="qgis-mod-feat"></a>
{% include image.html file="qgis-mod-feat.png" alt="bm-6a" caption="Toggle editing and enable the Vertex Tool." %} 
 
- Modify the boundary edges (as shown in [figure](#qgis-mod-boundary)): click on the centre cross (creates a new point) and dragging it to the next outest boundary point of the DEM points. Note: 
    * The boundary polygon must not be a perfect fit, but it must include all xyz-points with many details in vicinity of the river inflow and outflow regions (dense point cloud in the left part of the point file). 
    * The more precise the boundary the better will be the quality mesh and the faster and more stable will be the simulation.
    * Regularly save edits by clicking on SAVE `Layer` (floppy disk symbol next to the editing pen symbol)

<a name="qgis-mod-boundary"></a>
{% include image.html file="qgis-mod-boundary.png" alt="bm-7" caption="Modify the boundary polygon with a click on the centre cross (creates a new point) and dragging it to the next outest boundary point of the DEM points." %} 

<a name="qgis-fin-boundary"></a>
{% include image.html file="qgis-fin-boundary.png" alt="bm-8" caption="The final boundary (hull of the point cloud)." %}


## Breaklines<a name="breaklines"></a>
Breaklines indicate, for instance, channel banks and the riverbed, and need to coincide with DEM points (shapefile from [above section](#epd)). Breaklines a stored in a line (vector) shapefile, which is here already provided (`breaklines.shp`). Integrate the breaklines file into the *QGIS* project as follows with a click on *QGIS*' `Layer` menu > `Add Vector Layer...` and select the provided `breaklines.shp` file.
Note: The default layer style `Single Symbol`. For better representation, double-click on the breaklines layer, got to the `Symbology` ribbon and select `Categroized` (or `Graduated`) instead of `Single Symbol` (at the very top of the `Layer Properties` window). In the `Value` field, select `type`, then click the `classify` button on the bottom of the `Layer Properties` window. The listbox will now show the values bank, bed, hole, and all other values. Change color pattern and/or click `OK` on the bottom-right of the `Layer Properties` window.

## TIN Elevation Model<a name="tin"></a>
This section explains the creation of a triangulated irregular network (TIN) with the *QGIS* plugin *BASEmesh* (make sure that all steps in the [above section](#start-qgis) were successful).

1. To start, click on *QGIS*' `Plugins` menu > *BASEmesh* > `Elevation Meshing` to open the mesh wizard. Use the following settings (see also [figure](#qgis-exp-tin)):
1. `Model boundary` = `boundary` layer ([see above section](#boundary))
1. `elevation points` = `xyz-points` ([see above section](#epd))
1. Enable the `breaklines` checkbox and select the `breaklines` layer ([see above section](#breaklines))
1. In the `Shapefile output`canvas, click on the BROWSE button and save the new file as, for example, base_tin.shp.
1. Click on `Generate Elevation Mesh` and `Close` the wizard after successful execution.

As a result, two new layers will now show up in the Layers window:
1.	`base_tin_elevation_nodes.shp`, and
1.	`base_tin_elevation_elements.shp`.

<a name="qgis-exp-tin"></a>
{% include image.html file="qgis-exp-tin.png" alt="bm-9" caption="Setup BASEmesh's Elevation Meshing wizard." %}


## Region Markers for Quality Meshing<a name="regions"></a>

Region markers are placed within regions defined by breaklines and assign for instance mate-rial identifiers (MATIDs) and maximum mesh areas to ensure high mesh quality (e.g., the mesh area should be small in the active channel bed and can be wider on floodplains). To create a new region marker file:

- Click on *QGIS*' `Layers` menu > `Create Layer` > `New Shapefile Layer...` (see [figure](#qgis-new-lyr))
<a name="qgis-new-lyr"></a>
{% include image.html file="qgis-new-lyr.png" alt="bm-10" caption="Create a new point shapefile for region definitions from QGIS' Layer menu." %}

- In the newly opened `New Shapefile Layer` window, make the following definitions (see also [figure](#qgis-reg-lyr)).
    * Define the File name as region-points.shp (or similar)
    * Ensure the Geometry type is Point and the CRS corresponds to the above definitions ([see above section](#start-qgis)).
    * Add four `New Field`s (in addition to the default `Integer` type `ID` field):
                	+ `max_area` = `Decimal number` (`length` = 10, `precision` = 3)
                	+ `MATID` = `Whole number` (`length` = 3)
                	+ `type` = `Text data` (`length` = 20)
- Click `OK` to create the new point shapefile.

<a name="qgis-reg-lyr"></a>
{% include image.html file="qgis-reg-lyr.png" alt="bm-11" caption="Definitions and fields to be added to the new regions point shapefile." %}

After the successful creation, right-click on the new REGION-`points` layer and select TOGGLE EDITING. Then go to *QGIS*' EDIT menu and select ADD POINT FEATURE. Create 9 points to de-fine all areas delineated by the `breaklines` layer. These points should include the following region types:

| Type     | riverbed | lower_bank | upper_bank | floodplain | street |
|----------|----------|------------|------------|------------|--------|
| `MATID`    | 1        | 2          | 3          | 4          | 5      |
| max_area | 25.0     | 50.0       | 100.0      | 400.0      | 100    |


The below [figure](#qgis-reg-pts) shows an example for defining points within the areas delineated by the breaklines. 

<a name="qgis-reg-pts"></a>
{% include image.html file="qgis-reg-pts.png" alt="bm-12" caption="Example for distributing region points in the project boundaries (remark: the max_area value may differ and is expert assessment-driven). After the placement of all region points, Save Layer Edits (floppy disk symbol) and Toggle Editing (pencil symbol – turn off)." %}  

## Quality meshing<a name="qualm"></a>
A quality mesh accounts for the definitions made within the regions shapefile ([see above section](#regions)), but it does not include elevation data. Thus, after generating a quality mesh, elevation infor-mation needs to be added from the TIN ([see above section](#tin)). This section first explains the [generation of a quality mesh](qualm-gen) and then the [insertion of elevation data](#qualm-interp)).

###	Quality mesh generation<a name="qualm-gen"></a>
In *QGIS*' `Plugins` menu, click on *BASEmesh* > QUALITY MESHING to open the Quality mesh-ing wizard. Make the following settings in the window (see also [figure](#qgis-qualm)):

1. `Model boundary` = `boundary` ([see above section](#boundary))
1. `breaklines` = `breaklines` ([see above section](#breaklines))
1. `Regions` = `regions-points` ([see above section](#regions)) and activate all checkboxes
1. In the `Shapefile output` canvas, click on the `browse` button to define the output mesh as (for example) `base_qualitymesh.shp`

<a name="qgis-qualm"></a>
{% include image.html file="qgis-qualm.png" alt="bm-13" caption="BASEmesh's Quality Meshing wizard." %} 

Quality meshing may take time. After successful mesh generation the files `base_qualitymesh_qualityNodes.shp` and `base_qualitymesh_qualityElements.shp` are generated. Finally, click `Close`.

###	Elevation data interpolation on a quality mesh<a name="qualm-interp"></a>
*BASEmesh*’s `Interpolation` wizard projects elevation data onto the quality mesh by interpo-lation from a TIN. Make sure to check (show) the `base_qualitymesh_qualityNodes` and `base_qualitymesh_qualityElements` from the last step, and `base_tin_elevation_nodes.shp` and [`base_tin_elevation_elements.shp`](#tin). Then, open *BASEmesh*’s `Interpolation` wizard (*QGIS* `Plugins` menu > *BASEmesh* > `Interpolation`) and (see also [figure](#qgis-qualm-interp)):
1. In the `Quality Mesh` canvas, select `base_qualitymesh_qualityNodes`
1. In the `Elevation Data` canvas, activate the `Elevation Mesh` checkbox and select `base_tin_elevation_nodes.shp` and [`base_tin_elevation_elements.shp`](#tin)
1. In the `Shapefile output` canvas, define the output file as finalmesh.shp.
1. Click `Interpolate elevations` (may take a while)
After successful execution, the new layer finalmesh_Interpolated_nodes_elevMesh.shp will be created. Click Close to close the Interpolation wizard.

<a name="qgis-qualm-interp"></a>
{% include image.html file="qgis-qualm-interp.png" alt="bm-14" caption="BASEmesh's Interpolation wizard and setup." %} 


###	Verify quality mesh elevation <a name="qualm-verify"></a>
After the elevation interpolation, verify that elevations were correctly assigned. To identify potential outliers double-click on the new `finalmesh_interpolated_Nodes_elevMesh` and go to the `Symbology` ribbon. Select `Graduated` at the very top of the window (instead of `Single Symbol`), set the `Value` to Z, METHOD to COLOR, choose a color ramp, and click on the `classify` bottom (lower part of the window). Click on `Apply` and `OK` to close the `Symbology` window. 
The below [figure](#qgis-verify-qualm) shows an example of interpolated mesh, with some irregularities (red points). The irregularities are caused by local imprecision of breaklines (line end points do not coincide with the [`xyz-points.shp`](#epd)). Also some points of the [boundary](#boundary) do not correspond the `xyz-points.shp`. If such irregularities occur, zoom at the red points (irregularities) and ensure that the breakline and boundary nodes all exactly coincide with those stored in `xyz-points.shp`. When all nodes are corrected, repeat all steps from the [TIN generation](#tin) onward.

<a name="qgis-verify-qualm"></a>
{% include image.html file="qgis-verify-qualm.png" alt="bm-15" caption="Verify elevation interpolation using graduated color ramps. In this example, the red-colored points indicated irregularities in the mesh." %} 


##	Export to 2dm<a name="2dm"></a>
To run *BASEMENT*, the mesh needs to be exported in 2dm format. *BASEmesh*’s `Export Mesh` wizard (*QGIS* `Plugins` menu > *BASEmesh* > `Export Mesh`) does the job with the following settings (see also below [figure](#qgis-exp-mesh): Export of the mesh to 2dm format with *BASEmesh*'s `Export Mesh` wizard.):
1. Select the checkbox 2D MESH `Export`
1. Mesh elements = `base_qualitymesh_quality_elementy.shp` ([see above](#qualm-interp)) with `Material ID field` = `MATID`
1. Mesh nodes = `finalmesh_interpolated_nodes_elevmesh.shp` ([see above](#qualm)) with `Elevation field` =`Z`
1. In the `Mesh output` canvas, click on the `Browse` button and select an export mesh directory and name (e.g., `finalmesh.2dm`).
1. Click on `Export Mesh` (may take a while) and `Close` the wizard afterwards.

<a name="qgis-exp-mesh"></a>
{% include image.html file="qgis-exp-mesh.png" alt="bm-16" caption="Export of the mesh to 2dm format with BASEmesh's Export Mesh wizard." %} 

In order to work with *BASEMENT* v3.x, the .2dm file requires a couple of adaptations. Open the produced finalmesh.2dm in a text editor software (right-click and, for example, edit with Notepad++) and:

- At the top, insert the following line at line N°2: </br> `NUM_MATERIALS_PER_ELEM 1`

<a name="mod-2dm"></a>
{% include image.html file="mod-2dm.png" alt="bm-x2" caption="Modification of the upper part of the .2dm file." %} 
 
- At the bottom of the file, add the node string definitions for the inflow and outflow boundary. Enter the following 2 new lines:
    * *NS[SPACE][SPACE]nd<sub>1</sub>[SPACE]nd<sub>2</sub>[SPACE]nd<sub>i</sub>[SPACE]nd<sub>n</sub>[SPACE]Inflow*
    * *NS[SPACE][SPACE]nd<sub>1</sub>[SPACE]nd<sub>2</sub>[SPACE]nd<sub>j</sub>[SPACE]nd<sub>m</sub>[SPACE]Outflow*
- Replace ndi and ndj with the inflow and outflow nodes of [FINALMESH_NTERPOLATED_NODES_ELEVMESH.SHP](#qualm-interp). To identify these nodes open *QGIS* and
- Use *BASEmesh*’s STRINGDEF wizard (from *BASEMENT* v2.8 user manual):
    * For each line feature with a non-empty STRINGDEF-field, all nodes that are lo-cated exactly on that line, are listed in a text file (*BASEMENT*-like STRINGDEF block). The content of the STRINGDEF-field represents the STRINGDEF name.
    * The `Stringdef` line features are favorably included in the breaklines layer (shapefile) of the quality mesh. To distinguish between regular breaklines and `Stringdef` lines, the `Stringdef`-field can be used (empty or non-empty).
    * The upstream direction of the generated `Stringdef`s is right. Therefore the line feature has to be drawn from the left riverbank to the right riverbank
- Finally, the bottom of the finalmesh.2dm (text editor) should look like this in the text editor (node `ID`s may vary from those in the screenshot):
 
 <a name="mod-2dm-bottom"></a>
{% include image.html file="mod-2dm-bottom.png" alt="bm-x3" caption="Modification of the bottom part of the .2dm file." %} 


Congratulations, you finished meshing!


