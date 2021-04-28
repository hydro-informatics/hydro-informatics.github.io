# Pre-Processing with QGIS

## Pre-processing with *QGIS*

To start any analysis of rivers and fluvial landscapes, a digital elevation model (**DEM**) is required. Nowadays, DEMs mostly are a result of light imaging, detection, and ranging ([LiDAR](https://en.wikipedia.org/wiki/Lidar) and bathymetric surveys. LiDAR employs lights sources and provides terrain assessments up to 2-m deep water. Deeper water requires additional bathymetric surveys with [echo sounding](https://en.wikipedia.org/wiki/Echo_sounding) methods.
Merging LiDAR and bathymetric data produces point clouds that may be stored in many different file types. The first step in river modelling consist in the conversion of such point clouds into usable DEMs and computational meshes. This page guides through the conversion of a point cloud into a computational mesh with *QGIS* and the *BASEmesh* plugin. The descriptions refer to the developer's documentation files ([go to the ETH Zurich's *BASEMENT* documentation](https://basement.ethz.ch/download/documentation/docu3.html)).

(start-qgis)=
## Get ready with *QGIS*

```{admonition} Windows
Download and install the latest version of the open-access GIS software [*QGIS*](https://www.qgis.org).
```

```{admonition} Linux
(1) Make sure to [**install QGIS v3.16 via *Flatpak***](https://flathub.org/apps/details/org.qgis.qgis) or the *Linux* *Software Manager* (open *Software Manager*, search for *QGIS* and install the *QGIS Flatpak*). If *Software Manager* cannot find *QGIS*, make sure that *Flatpak* is added as repository (find the good repository for your Unix-based operating system (OS) [here](https://flatpak.org/setup/)).<br><br>
(2) The ***QGIS Flatpak* installation will** most likely **not include *scipy***. In order to **fix** this issue, **open  *Terminal*** (standard application on Unix-based OS) and type:
<br><br>**`flatpak run --command=pip3 org.qgis.qgis install scipy --user`**<br><br>
This solution has been tested on ***Linux Ubuntu* and *Linux Mint*. It potentially also works with *Red Hat*, *openSUSE*, *Mac OS*, *Arch*, *Fedora*, *Android*, *Debian*, *Kubuntu*** and [many more](https://flatpak.org/setup/). Read more about the *QGIS Flatpak* installation on the [*QGIS web site*](https://qgis.org/en/site/forusers/alldownloads.html#flatpak).
```

Start *QGIS*, create a new project and save it (`Project` > `Save as...`). Then, set the project coordinate reference system (CRS) by clicking on `Project` > `Properties` > `CRS` tab and select `GERMANY_ZONE_3 (ESRI:31493)`. Install *BASEMENT*’s *BASEmesh* Plugin (instructions from the *BASEMENT* System Manual):

1. Load the *QGIS* plugin manager: `Plugins` menu > `Manage and Install Plugins` (see details in {numref}`Fig. %s <qgis-plugins>`
1. Go to the Settings tab; now the *QGIS* plugin repository connections should be visible at the bottom of the `Plugin Manager` (`Plugin Repositories` listbox in {numref}`Fig. %s <qgis-plugins>`).
1. Scroll to the bottom, click on Add..., and enter a name for the new repository (e.g., *BASEmesh* repository)
1. Enter the repository address: [http://people.ee.ethz.ch/~basement/qgis_plugins/qgis_plugins.xml](http://people.ee.ethz.ch/~basement/qgis_plugins/qgis_plugins.xml)
1. Click `OK`. The new repository should now be visible in the `Plugin Repositories` listbox. If the connection is `OK`, click on the Close button on the bottom of the window.
1. Verify that the *BASEmesh* plugin is now available in the *QGIS*' `Plugins` menu (see {numref}`Fig. %s <qgis-pluggedin>`).

```{figure} ../img/qgis-plugins.png
:alt: qgis basement plugins
:name: qgis-plugins

Installation of the BASEmesh plugin.
```

```{figure} ../img/qgis-pluggedin.png
:alt: qgis basement plugins
:name: qgis-pluggedin


The BASEmesh plugin is available in QGIS' Plugins menu after successful installation.
```

(epd)=
## Elevation point data
Terrain survey data are mostly delivered in the shape of an x-y-z point dataset. LiDAR produces massive point clouds, which quickly overcharge even powerful computers. Therefore, LiDAR data may need to be break down to smaller zones of less than approximately 106 points and special LiDAR point processing software (e.g., http://lastools.org/) may be helpful in this task. The range of possible data products and shape from terrain survey is board and this tutorial exemplary uses a set of x-y-z points stored within a text file. Load the points from the provided xyz-points.txt file as follows:

1. [Download](https://github.com/hydro-informatics/materials-bm/blob/master/points_raw/points.txt) the point file from the repository (if necessary, copy the file contents locally into a text editor and save the file as `points.txt` in a local project directory)
1. [Download](https://github.com/hydro-informatics/materials-bm/raw/master/breaklines.zip) the zipped breaklines shapefile into the project folder and unpack `breaklines.shp`.
1. In *QGIS*, click on the `Layer` menu > `Add Layer` > `Add Delimited Text Layer...` (see {numref}`Fig. %s <qgis-add-lyr>`)
1. In the `Add Delimited Text Layer` (`Data Source Manager | Delimited Text`) wizard (see details in Figure 4):
    * Choose [*points.txt*](https://github.com/hydro-informatics/materials-bm/blob/master/points_raw/points.txt) in the `File name` field (alternatively use [*points.csv*](https://github.com/hydro-informatics/materials-bm/blob/master/points_raw/points.csv)
    * Name the new layer (e.g., points)
    * In the `File Format` canvas, select `Custom Delimiters` and activate the `Space` checkbox
    * In the `Record and Field Options` canvas, activate the `First record has field names` checkbox
    * In the `Geometry Definition` canvas, define the `Point Coordinates` as `X Field` = `X`, `Y Field` = `Y` and `Z Field` = `Z`; set the `Geometry CRS` to the `Project CRS`.
    * Click the `Add` button on the bottom of the wizard window. The points should now be plotted in the main *QGIS* window.


```{figure} ../img/qgis-add-lyr.png
:alt: basement qhis add layer
:name: qgis-add-lyr

Open the Add Delimited Text Layer import wizard.
```

```{figure} ../img/qgis-import-pts.png
:alt: basement qgis import points
:name: qgis-import-pts

Load the xyz-points.txt file with QGIS' Add Delimited Text Layer (Data Source Manager | Delimited Text) wizard.
```

Next, export the new point layer as shapefile: In *QGIS*' `Layer`S window, right-click on XYZ-POINTS, then `Export` > `Save Features As...` . In the Format field, select `ESRI Shapefile`. Define a FILE NAME (by clicking on the … button and defining for example *C:\QGIS-projects\xyz-points.shp*), ensure that the ADD SAVED FILE TO MAP checkbox is activated (on the bottom of the `Save Vector Layer As...` window) and click `OK`. Remove the `points` text layer from the `Layers` window (only the shape file should be visible here now).
Finally, rename the three fields (`FIELD_1`, `FIELD_2`, `FIELD_3`) to `X`, `Y`, and `Z`, respectively. The fields can be renamed with a double-click on the `xyz-points` layer (opens `Layer Properties`), then left-click on the `Fields` ribbon, activate the editing mode (click on the pen symbol) and edit the `Name` fields.

(boundary)=
## Model Boundary

The model boundary defines the calculation extent and needs to be define within a polygon shapefile that encloses all points in the above produced point shapefile. *QGIS* provides a Convex Hull tool that enables the automated creation of the outer boundary. This tool is used as follows:

- In *QGIS*' `Processing` menu, select `Toolbox` (see {numref}`Fig. %s <qgis-tbx-fig>`) The `Toolbox` sub-window opens now.
- In the toolbox, click on `Vector Geometry` > `Concave Hull (Alpha Shapes)`, which opens the `Concave Hull (Alpha Shapes)` wizard (see {numref}`Fig. %s <qgis-chull>`).
- In the `Concave Hull (Alpha Shapes)` wizard, select the `xyz-points` layer as `Input Layer`, set the `Threhold` to 0.300 (keep default), define an output `Concave Hull` shapefile (e.g., `boundary.shp`) by clicking on the `...` button, and click on `Run`.

```{figure} ../img/qgis-tbx.png
:alt: qgis basement toolbox
:name: qgis-tbx-fig

Open QGIS' Toolbox from the main menu.
```

```{figure} ../img/qgis-chull.png
:alt: basement qgis convex hull boundary polygon
:name: qgis-chull

The Concave Hull (Alpha Shapes) wizard.
```


- Right-click on *QGIS*' `Settings` menu, and activate the `Snapping` toolbar checkbox. In the now shown snapping toolbar, activate snapping with a click on the horseshoe icon.
- Adapt the boundary.shp polygon to a tighter fit of the shapefile nodes by clicking on the `Toggle editing` (pen) symbol and activating the `Vertex Tool` in the toolbar.

```{figure} ../img/qgis-mod-feat.png
:alt: basement qgis modify feature vertex
:name: qgis-mod-feat

Toggle editing and enable the Vertex Tool.
```

- Modify the boundary edges (as shown in {numref}`Fig. %s <qgis-mod-boundary>`): click on the centre cross (creates a new point) and dragging it to the next outest boundary point of the DEM points. Note:
    * The boundary polygon must not be a perfect fit, but it must include all xyz-points with many details in vicinity of the river inflow and outflow regions (dense point cloud in the left part of the point file).
    * The more precise the boundary the better will be the quality mesh and the faster and more stable will be the simulation.
    * Regularly save edits by clicking on SAVE `Layer` (floppy disk symbol next to the editing pen symbol)


```{figure} ../img/qgis-mod-boundary.png
:alt: basement qgis modify boundary polygon
:name: qgis-mod-boundary

Modify the boundary polygon with a click on the centre cross (creates a new point) and dragging it to the next outest boundary point of the DEM points.
```


```{figure} ../img/qgis-fin-boundary.png
:alt: basement qgis boundary polygon
:name: qgis-fin-boundary

The final boundary (hull of the point cloud).
```

(breaklines)=
## Breaklines
Breaklines indicate, for instance, channel banks and the riverbed, and need to coincide with DEM points (shapefile from [above section](#epd)). Breaklines a stored in a line (vector) shapefile, which is here already provided (`breaklines.shp`). Integrate the breaklines file into the *QGIS* project as follows with a click on *QGIS*' `Layer` menu > `Add Vector Layer...` and select the provided `breaklines.shp` file (if not yet done, [download](https://github.com/hydro-informatics/materials-bm/raw/master/breaklines.zip) and unpack the shapefile).
Note: The default layer style `Single Symbol`. For better representation, double-click on the breaklines layer, got to the `Symbology` ribbon and select `Categroized` (or `Graduated`) instead of `Single Symbol` (at the very top of the `Layer Properties` window). In the `Value` field, select `type`, then click the `classify` button on the bottom of the `Layer Properties` window. The listbox will now show the values bank, bed, hole, and all other values. Change color pattern and/or click `OK` on the bottom-right of the `Layer Properties` window.

(tin-dem)=
## TIN Elevation Model

This section explains the creation of a triangulated irregular network (TIN) with the *QGIS* plugin *BASEmesh* (make sure that all steps in the [above section](#start-qgis) were successful).

1. To start, click on *QGIS*' `Plugins` menu > *BASEmesh* > `Elevation Meshing` to open the mesh wizard. Use the following settings (see also {numref}`Fig. %s <qgis-exp-tin>`:
1. `Model boundary` = `boundary` layer ([see above section](#boundary)
1. `elevation points` = `xyz-points` ([see above section](#epd)
1. Enable the `breaklines` checkbox and select the `breaklines` layer ([see above section](#breaklines)
1. In the `Shapefile output`canvas, click on the BROWSE button and save the new file as, for example, base_tin.shp.
1. Click on `Generate Elevation Mesh` and `Close` the wizard after successful execution.

As a result, two new layers will now show up in the Layers window:
1.	`base_tin_elevation_nodes.shp`, and
1.	`base_tin_elevation_elements.shp`.

```{figure} ../img/qgis-exp-tin.png
:alt: basemesh qgis elevation mesh tin
:name: qgis-exp-tin

Setup BASEmesh's Elevation Meshing wizard.
```

(regions)=
## Region Markers for Quality Meshing

Region markers are placed within regions defined by breaklines and assign for instance material identifiers (MATIDs) and maximum mesh areas to ensure high mesh quality (e.g., the mesh area should be small in the active channel bed and can be wider on floodplains). To create a new region marker file:

- Click on *QGIS*' `Layers` menu > `Create Layer` > `New Shapefile Layer...` (see {numref}`Fig. %s <qgis-new-lyr>`)

```{figure} ../img/qgis-new-lyr.png
:alt: qgis new layer basemesh
:name: qgis-new-lyr

Create a new point shapefile for region definitions from QGIS' Layer menu.
```

- In the newly opened `New Shapefile Layer` window, make the following definitions (see also {numref}`Fig. %s <qgis-reg-lyr>`).
    * Define the File name as region-points.shp (or similar)
    * Ensure the Geometry type is Point and the CRS corresponds to the above definitions ([see above section](#start-qgis))
    * Add four `New Field`s (in addition to the default `Integer` type `ID` field):
                	+ `max_area` = `Decimal number` (`length` = 10, `precision` = 3)
                	+ `MATID` = `Whole number` (`length` = 3)
                	+ `type` = `Text data` (`length` = 20)
- Click `OK` to create the new point shapefile.

```{figure} ../img/qgis-reg-lyr.png
:alt: basement mesh qgis region layer points
:name: qgis-reg-lyr

Definitions and fields to be added to the new regions point shapefile.
```

After the successful creation, right-click on the new REGION-`points` layer and select TOGGLE EDITING. Then go to *QGIS*' EDIT menu and select ADD POINT FEATURE. Create 9 points to define all areas delineated by the `breaklines` layer. These points should include the following region types:

| Type     | riverbed | lower_bank | upper_bank | floodplain | street |
|----------|----------|------------|------------|------------|--------|
| `MATID`  | 1        | 2          | 3          | 4          | 5      |
| max_area | 25.0     | 50.0       | 100.0      | 400.0      | 100    |


{numref}`Figure %s <qgis-reg-pts>` shows an example for defining points within the areas delineated by the breaklines.

```{figure} ../img/qgis-reg-pts.png
:alt: basemesh region points
:name: qgis-reg-pts

Example for distributing region points in the project boundaries (remark: the max_area value may differ and is expert assessment-driven). After the placement of all region points, Save Layer Edits (floppy disk symbol) and Toggle Editing (pencil symbol – turn off).
```

(qualm)=
## Quality meshing

A quality mesh accounts for the definitions made within the regions shapefile ([see above section](#regions), but it does not include elevation data. Thus, after generating a quality mesh, elevation information needs to be added from the TIN ([see above section](#tin-dem)). This section first explains the [generation of a quality mesh](qualm-gen) and then the [insertion of elevation data](#qualm-interp)).

(qualm-gen)=
### Quality mesh generation
In *QGIS*' `Plugins` menu, click on *BASEmesh* > QUALITY MESHING to open the Quality meshing wizard. Make the following settings in the window (see also {numref}`Fig. %s <qgis-qualm>`):

1. `Model boundary` = `boundary` ([see above section](#boundary)
1. `breaklines` = `breaklines` ([see above section](#breaklines)
1. `Regions` = `regions-points` ([see above section](#regions) and activate all checkboxes
1. In the `Shapefile output` canvas, click on the `browse` button to define the output mesh as (for example) `base_qualitymesh.shp`

```{figure} ../img/qgis-qualm.png
:alt: basement qgis quality mesh tin
:name: qgis-qualm

BASEmesh's Quality Meshing wizard.
```

Quality meshing may take time. After successful mesh generation the files `base_qualitymesh_qualityNodes.shp` and `base_qualitymesh_qualityElements.shp` are generated. Finally, click `Close`.

### Elevation data interpolation on a quality mesh<a name="qualm-interp"></a>
*BASEmesh*’s `Interpolation` wizard projects elevation data onto the quality mesh by interpolation from a TIN. Make sure to check (show) the `base_qualitymesh_qualityNodes` and `base_qualitymesh_qualityElements` from the last step, and `base_tin_elevation_nodes.shp` and [`base_tin_elevation_elements.shp`](#tin-dem). Then, open *BASEmesh*’s `Interpolation` wizard (*QGIS* `Plugins` menu > *BASEmesh* > `Interpolation`) and (see also {numref}`Fig. %s <qgis-qualm-interp>`):

1. In the `Quality Mesh` canvas, select `base_qualitymesh_qualityNodes`
1. In the `Elevation Data` canvas, activate the `Elevation Mesh` checkbox and select `base_tin_elevation_nodes.shp` and [`base_tin_elevation_elements.shp`](#tin-dem)
1. In the `Shapefile output` canvas, define the output file as finalmesh.shp.
1. Click `Interpolate elevations` (may take a while)
After successful execution, the new layer finalmesh_Interpolated_nodes_elevMesh.shp will be created. Click Close to close the Interpolation wizard.

```{figure} ../img/qgis-qualm-interp.png
:alt: qgis quality mesh interpolation basement
:name: qgis-qualm-interp

BASEmesh's Interpolation wizard and setup.
```

(qualm-verify)=
### Verify quality mesh elevation

After the elevation interpolation, verify that elevations were correctly assigned. To identify potential outliers double-click on the new `finalmesh_interpolated_Nodes_elevMesh` and go to the `Symbology` ribbon. Select `Graduated` at the very top of the window (instead of `Single Symbol`), set the `Value` to Z, METHOD to COLOR, choose a color ramp, and click on the `classify` bottom (lower part of the window). Click on `Apply` and `OK` to close the `Symbology` window.
{numref}`Fig. %s <qgis-verify-qualm>` shows an example of interpolated mesh, with some irregularities (red points). The irregularities are caused by local imprecision of breaklines (line end points do not coincide with the [`xyz-points.shp`](#epd)). Also some points of the [boundary](#boundary) do not correspond the `xyz-points.shp`. If such irregularities occur, zoom at the red points (irregularities) and ensure that the breakline and boundary nodes all exactly coincide with those stored in `xyz-points.shp`. When all nodes are corrected, repeat all steps from the [TIN generation](#tin-dem) onward.

```{figure} ../img/qgis-verify-qualm.png
:alt: basemesh verify quality mesh
:name: qgis-verify-qualm

Verify elevation interpolation using graduated color ramps. In this example, the red colored points indicated irregularities in the mesh.
```

(2dm)=
##	Export to 2dm

To run *BASEMENT*, the mesh needs to be exported in 2dm format. *BASEmesh*’s `Export Mesh` wizard (*QGIS* `Plugins` menu > *BASEmesh* > `Export Mesh`) does the job with the following settings (see also {numref}`Fig. %s <qgis-exp-mesh>`): Export of the mesh to 2dm format with *BASEmesh*'s `Export Mesh` wizard.):

1. Select the checkbox 2D MESH `Export`
1. Mesh elements = `base_qualitymesh_quality_elementy.shp` ([see above](#qualm-interp) with `Material ID field` = `MATID`
1. Mesh nodes = `finalmesh_interpolated_nodes_elevmesh.shp` ([see above](#qualm) with `Elevation field` =`Z`
1. In the `Mesh output` canvas, click on the `Browse` button and select an export mesh directory and name (e.g., `finalmesh.2dm`).
1. Click on `Export Mesh` (may take a while) and `Close` the wizard afterwards.

```{figure} ../img/qgis-exp-mesh.png
:alt: basement qgis export mesh 2dm
:name: qgis-exp-mesh

Export of the mesh to 2dm format with BASEmesh's Export Mesh wizard.
```

In order to work with *BASEMENT* v3.x, the .2dm file requires a couple of adaptations. Open the produced finalmesh.2dm in a text editor software (right-click and, for example, edit with [*Notepad++*](hy_get-started/others.html#npp) and:

- At the top, insert the following line at line N°2: `NUM_MATERIALS_PER_ELEM 1`

```{figure} ../img/mod-2dm.png
:alt: modify materials basemesh basement 2dm error fix
:name: mod-2dm

Modification of the upper part of the .2dm file.
```

- At the bottom of the file, add the node string definitions for the inflow and outflow boundary. Enter the following 2 new lines (where *nd<sub>i</sub>* and *nd<sub>j</sub>* represent the *Inflow* and *Outflow* nodes, respectively, of [finalmesh_interpolatedNodes_elevMesh.shp](#qualm-interp):
    * *NS[SPACE][SPACE]nd<sub>1</sub>[SPACE]nd<sub>2</sub>[SPACE]nd<sub>i</sub>[SPACE]nd<sub>n</sub>[SPACE]Inflow*
    * *NS[SPACE][SPACE]nd<sub>1</sub>[SPACE]nd<sub>2</sub>[SPACE]nd<sub>j</sub>[SPACE]nd<sub>m</sub>[SPACE]Outflow*

```{tip}
To **identify** the **node IDs** open *QGIS* use ***BASEmesh*’s Stringdef** wizard (from *BASEMENT* v2.8 user manual - read more below).
```

    <a name="stringdef"></a>
    * *Stringdef* identifies points that have a non-empty `stringdef`-field (i.e., all nodes that are located exactly on that line) and writes them into a text file (*BASEMENT*-like `stringdef` block). The content of the `stringdef`-field represents the `stringdef` name.
    * In order to identify the node ids on the inflow and outflow boundary lines, select the final mesh nodes in the *Mesh Nodes* dialogue, select the provided [breaklines shapefile](https://github.com/hydro-informatics/materials-bm/raw/master/breaklines.zip) in the *Breaklines* dialogue and select *stringdef* from the dropdown menu.
    * In the *Textfile OUTPUT* dialogue, select an output text file (e.g., `C:/temp/stringdef-breaklines.txt`) and click on ***Find node IDs***

```{figure} ../img/qgis-stringdef.png
:alt: basement stringdef tool
:name: bm-str-def-tool

BASEmesh's Stringdef tool.
```

    * The *Stringdef* tool now has generated  `stringdef`s in upstream-looking right direction (note: to create new boundaries, the lines need to be drawn from the left riverbank to the right riverbank).
    * Open the resulting text file (`C:/temp/stringdef-breaklines.txt` in the above example) and copy the node list to the bottom of *finalmesh.2dm* with the above-shown format (i.e., start with *NS*, followed by two SPACEs, then the node IDs *nd<sub>i/j </sub>* separated by on SPACE, then *Inflow* and *Outflow*, respectively). *Note: The node IDs my vary from those shown in the figure(s).*

```{figure} ../img/qgis-stringdef-out.png
:alt: basement stringdef
:name: bm-str-def

The output of BASEmesh's Stringdef tool: Node IDs of the Inflow and Outflow boundaries.
```

- Finally, the bottom of the finalmesh.2dm (text editor) should look like this in the text editor (node `ID`s may vary from those in the screenshot):

```{figure} ../img/mod-2dm-bottom.png
:alt: basement 2dm modify bottom nodes error fix
:name: mod-2dm-bottom

Modification of the bottom part of the .2dm file.
```

Congratulations, you finished meshing!
