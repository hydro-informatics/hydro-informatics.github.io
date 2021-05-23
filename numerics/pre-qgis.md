(qgis-prepro)=
# Pre-processing with QGIS

```{admonition} Requirements
:class: attention
Before diving into this tutorial make sure to...

1. Follow the installation instructions for {ref}`qgis-install` in this eBook;
2. Read and understand (or watch) this eBook's {ref}`qgis-tutorial`.
```

(get-dem)=
## Digital Elevation Models (DEMs)
To start any analysis of rivers and fluvial landscapes, a digital elevation model (**DEM**) is required. Nowadays, DEMs often stem from light imaging, detection, and ranging ([LiDAR](https://en.wikipedia.org/wiki/Lidar) combined with bathymetric surveys. Older approaches rely on manual surveying (e.g. with a total station) of cross sections between which the terrain is interpolated. The newer LiDAR employs lights sources and provides terrain assessments up to 2-m deep water. Bathymetric [echo sounding](https://en.wikipedia.org/wiki/Echo_sounding) is necessary to map the ground of deeper waters. Thus, merged LiDAR and echo-sounding datasets produces seamless point clouds of river ecosystems, which may be stored in many different file types.

The first step in modelling a river consist in the conversion of a DEM into a computational mesh. This section guides through the conversion of a DEM into a computational mesh with *QGIS* and the *BASEmesh* plugin. The descriptions refer to the developer's documentation files ([go to the ETH Zurich's *BASEMENT* documentation](https://basement.ethz.ch/download/documentation/docu3.html)). At the end of this tutorial, we will have generated a computational grid in {term}`SMS 2dm` format that is compatible with the {ref}`chpt-basement` and {ref}`chpt-telemac2d` numerical models presented in the next chapters of this eBook.


This tutorial uses an application-ready DEM in GeoTIFF {ref}`raster` format. The DEM raster will provide height (Z) information for the computational grids created in the next sections. Therefore, download the example DEM GeoTIFF [here](https://github.com/hydro-informatics/materials-bm/raw/main/rasters/inn-dem.tif) and add it as a new raster layer in *QGIS* (similar to adding {ref}`basemap`).

```{admonition} From LiDAR point clouds to a Raster DEM
:class: tip
Terrain survey data are mostly delivered in the shape of an x-y-z point dataset. LiDAR produces massive point clouds, which quickly overcharge even powerful computers. Therefore, LiDAR data may need to be break down to smaller zones of less than approximately 106 points and special LiDAR point processing software (e.g., http://lastools.org/) may be helpful in this task. The range of possible data products and shape from terrain survey is board and this tutorial exemplary uses a set of x-y-z points stored within a text file.
```


```{admonition} OpenFOAM modelers...
For three-dimensional (3d) modeling with OpenFOAM, the creation of a 2dm file is not necessary. OpenFOAM users can export the terrain in QGIS directly as an `stl` file, as described at the bottom of this section (jump to the {ref}`dem2stl` paragraph).
```

(start-qgis)=
## Install the BASEmesh Plugin

Install *BASEMENT*’s *BASEmesh* Plugin (instructions from the *BASEMENT* System Manual):

* Load the *QGIS* plugin manager: **Plugins** menu > **Manage and Install Plugins**.
* Go to the **Settings** tab.
* Scroll to the bottom (**Plugin Repositories** listbox in {numref}`Fig. %s <qgis-plugins>`), click on **Add...**.
* In the popup window enter:
  * a name for the new repository (e.g., `BASEmesh Repository`);
  * the repository address: [https://people.ee.ethz.ch/~basement/qgis_plugins/qgis_plugins.xml](https://people.ee.ethz.ch/~basement/qgis_plugins/qgis_plugins.xml).
* Click **OK**. The new repository should now be visible in the **Plugin Repositories** listbox. If the connection is **OK**, click on the Close button on the bottom of the window.
* Verify that the *BASEmesh* plugin is now available in the *QGIS*' **Plugins** menu (see {numref}`Fig. %s <qgis-pluggedin>`).

```{figure} ../img/qgis/bm-plugin.png
:alt: qgis basement plugins
:name: qgis-plugins

Add the BASEMENT repository to QGIS' Plugins Manager.
```

```{figure} ../img/qgis/bm-pluggedin.png
:alt: qgis basement plugins
:name: qgis-pluggedin

The BASEmesh plugin is available in QGIS' Plugins menu after the successful installation.
```

(setup-crs)=
## Coordinate Reference System

As featured in the {ref}`qgis-tutorial`, a coordinate reference system (CRS) should be set for the project. This example uses data of a river in Bavaria (Germany zone 4), which requires the following CRS:

* In the QGIS top menu go to **Project** > **Properties**.
* Activate the **CRS** tab.
* Enter `Germany_Zone_4` and select the CRS shown in {numref}`Fig. %s <qgis-crs>`.
* Click **Apply** and **OK**.

```{figure} ../img/qgis/inn-crs.png
:alt: qgis set coordinate reference system crs germany zone_4 Inn river
:name: qgis-crs

Define Germany_Zone_4 as project CRS.
```

```{admonition} Save the project...
:class: tip
Save the QGIS project (**Project** > **Save As...**), for example, under the name **prepro-tutorial.qgz**.
```

(epd)=
## Data


1. [Download](https://github.com/hydro-informatics/materials-bm/blob/main/points_raw/points.txt) the point file for this tutorial (if necessary, copy the file contents locally into a text editor and save the file as **points.txt** in a local project directory)
1. [Download](https://github.com/hydro-informatics/materials-bm/raw/main/breaklines.zip) the zipped breaklines shapefile into the project folder and unpack **breaklines.shp**.



(boundary)=
## Model Boundary

The model boundary defines the calculation extent and needs to be define within a polygon shapefile that encloses all points in the above produced point shapefile. *QGIS* provides a Convex Hull tool that enables the automated creation of the outer boundary. This tool is used as follows:



- Right-click on *QGIS*' **Settings** menu, and activate the **Snapping** toolbar checkbox. In the now shown snapping toolbar, activate snapping with a click on the horseshoe icon.
- Adapt the boundary.shp polygon to a tighter fit of the shapefile nodes by clicking on the **Toggle editing** (pen) symbol and activating the **Vertex Tool** in the toolbar.

```{figure} ../img/qgis-mod-feat.png
:alt: basement qgis modify feature vertex
:name: qgis-mod-feat

Toggle editing and enable the Vertex Tool.
```

- Modify the boundary edges (as shown in {numref}`Fig. %s <qgis-mod-boundary>`): click on the center cross (creates a new point) and dragging it to the next outest boundary point of the DEM points. Note:
    * The boundary polygon must not be a perfect fit, but it must include all xyz-points with many details in vicinity of the river inflow and outflow regions (dense point cloud in the left part of the point file).
    * The more precise the boundary the better will be the quality mesh and the faster and more stable will be the simulation.
    * Regularly save edits by clicking on SAVE **Layer** (floppy disk symbol next to the editing pen symbol)


```{figure} ../img/qgis-mod-boundary.png
:alt: basement qgis modify boundary polygon
:name: qgis-mod-boundary

Modify the boundary polygon with a click on the center cross (creates a new point) and dragging it to the next outest boundary point of the DEM points.
```


```{figure} ../img/qgis-fin-boundary.png
:alt: basement qgis boundary polygon
:name: qgis-fin-boundary

The final boundary (hull of the point cloud).
```

(breaklines)=
## Breaklines
Breaklines indicate, for instance, channel banks and the riverbed, and need to coincide with DEM points (shapefile from [above section](#epd)). Breaklines a stored in a line (vector) shapefile, which is here already provided (**breaklines.shp**). Integrate the breaklines file into the *QGIS* project as follows with a click on *QGIS*' **Layer** menu > **Add Vector Layer...** and select the provided **breaklines.shp** file (if not yet done, [download](https://github.com/hydro-informatics/materials-bm/raw/main/breaklines.zip) and unpack the shapefile).
Note: The default layer style **Single Symbol**. For better representation, double-click on the breaklines layer, got to the **Symbology** ribbon and select **Categorized** (or **Graduated**) instead of **Single Symbol** (at the very top of the **Layer Properties** window). In the **Value** field, select **type**, then click the **classify** button on the bottom of the **Layer Properties** window. The listbox will now show the values bank, bed, hole, and all other values. Change color pattern and/or click **OK** on the bottom-right of the **Layer Properties** window.



(regions)=
## Region Markers for Quality Meshing

Region markers are placed within regions defined by breaklines and assign for instance material identifiers (MATIDs) and maximum mesh areas to ensure high mesh quality (e.g., the mesh area should be small in the active channel bed and can be wider on floodplains). To create a new region marker file:

- Click on *QGIS*' **Layers** menu > **Create Layer** > **New Shapefile Layer...** (see {numref}`Fig. %s <qgis-new-lyr>`)

```{figure} ../img/qgis/create-shp-layer.png
:alt: qgis new layer basemesh
:name: qgis-new-lyr

Create a new point shapefile for region definitions from QGIS' Layer menu.
```

- In the newly opened **New Shapefile Layer** window, make the following definitions (see also {numref}`Fig. %s <qgis-reg-lyr>`).
    * Define the **File name** as **region-points.shp** (or similar)
    * Ensure the **Geometry type** is **Point**
    * The **CRS** corresponds to Germany Zone 4 ({ref}`see project CRS <setup-crs>`)
    * Add three **New Field**s (in addition to the default **Integer** type **ID** field):
      * **max_area** = **Decimal number** (**length** = 10, **precision** = 3)
      * **MATID** = **Whole number** (**length** = 3)
      * **type** = **Text data** (**length** = 20)
- Click **OK** to create the new point shapefile.

```{figure} ../img/qgis/bm-region-pts-create.png
:alt: basement mesh qgis region layer points
:name: qgis-reg-lyr

Definitions and fields to be added to the new regions point shapefile.
```

After the successful creation, right-click on the new REGION-**points** layer and select TOGGLE EDITING. Then go to *QGIS*' EDIT menu and select ADD POINT FEATURE. Create 9 points to define all areas delineated by the **breaklines** layer. These points should include the following region types:

| Type     | riverbed | block_ramp | gravel_bank | floodplain | sand_deposit |
|----------|----------|------------|-------------|------------|--------------|
| `MATID`  | 1        | 2          | 3           | 4          | 5            |
| max_area | 25.0     | 20.0       | 25.0        | 80.0       | 20.0         |


{numref}`Figure %s <qgis-reg-pts>` shows an example for defining points within the areas delineated by the breaklines.

```{figure} ../img/qgis/bm-region-pts-map.png
:alt: basemesh region points
:name: qgis-reg-pts

Example for distributing region points in the project boundaries (remark: the max_area value may differ and is expert assessment-driven). After the placement of all region points, Save Layer Edits (floppy disk symbol) and Toggle Editing (pencil symbol – turn off).
```

(qualm)=
## Quality meshing

A quality mesh accounts for the definitions made within the regions shapefile ([see above section on {ref}`regions`), but it does not include elevation data. Thus, after generating a quality mesh, elevation information needs to be added. This section first explains the {ref}`qualm-gen` and then the {ref}`qualm-interp`.

(qualm-gen)=
### Quality mesh generation
In *QGIS*' **Plugins** menu, click on **BASEmesh 2** > **QUALITY MESHING** to open the Quality meshing wizard. Make the following settings in the window (see also {numref}`Fig. %s <qgis-qualm>`):

1. **Model boundary** = **boundary** ([see above section](#boundary)
1. **breaklines** = **breaklines** ([see above section](#breaklines)
1. **Regions** = **regions-points** ([see above section](#regions) and activate all checkboxes
1. In the **Shapefile output** canvas, click on the **browse** button to define the output mesh as (for example) **base_qualitymesh.shp**

```{figure} ../img/qgis/bm-quality-meshing-success.png
:alt: basement qgis quality mesh tin
:name: qgis-qualm

BASEmesh's Quality Meshing wizard.
```

Quality meshing may take time. After successful mesh generation the file **prepro-tutorial_quality-mesh.2dm** will have been generated.

(qualm-interp)=
### Bottom Elevation Interpolation on a Quality Mesh

*BASEmesh*’s **Interpolation** wizard projects elevation data onto the quality mesh by interpolation from another mesh or a DEM raster. Here, we use the provided [DEM GeoTIFF](https://github.com/hydro-informatics/materials-bm/raw/main/rasters/inn-dem.tif). To run the interpolation, open *BASEmesh*’s **Interpolation** wizard (*QGIS* **Plugins** menu > **BASEmesh 2** > **Interpolation**) and (see also {numref}`Fig. %s <qgis-qualm-interp>`):

1. In the **Mesh layer to interpolate** canvas, select **prepro-tutorial_quality-mesh**.
1. In the **Basic** tab find the **Elevation source** canvas and activate the **Activation via DEM (Raster)** radio button.
1. Select the above imported **inn...** GeoTIFF as **Raster layer**.
1. In the **Output** canvas click on the **Browse** button to define an output mesh name an directory (for example, `/Basement/prepro-tutorial/prepro-tutorial_quality-mesh-interp.2dm`)
1. Click **Run** to create the height-interpolated mesh.

```{figure} ../img/qgis/bm-mesh-interpolation.png
:alt: qgis quality mesh interpolation basement
:name: qgis-qualm-interp

BASEmesh's Z-value (height) interpolation wizard and setup to assign a bottom elevation to the quality mesh.
```

After the elevation interpolation, verify that elevations were correctly assigned. To modify the layer visualization (symbology) double-click on the new **prepro-tutorial_quality-mesh-interp** and go to the **Symbology** ribbon. Select **Graduated** at the very top of the window, set the **Value** to Z, METHOD to COLOR, choose a color ramp, and click on the **classify** bottom (lower part of the window). Click on **Apply** and **OK** to close the **Symbology** window. {numref}`Fig. %s <qgis-verify-qualm>` shows an example visualization of the height-interpolated mesh.

```{figure} ../img/qgis/bm-mesh-interp-success.png
:alt: basemesh verify interpolated quality mesh
:name: qgis-verify-qualm

Verify elevation interpolation using graduated color ramps.
```



(stringdef)=
## String Definitions

In order to identify the node ids on the inflow and outflow boundary lines, select the final mesh nodes in the *Mesh Nodes* dialogue, select the provided [breaklines shapefile](https://github.com/hydro-informatics/materials-bm/raw/main/breaklines.zip) in the *Breaklines* dialogue and select *stringdef* from the dropdown menu.




## Usage with Numerical Models

The 2dm mesh file produced in this tutorial can be directly used with {ref}`chpt-basement`, where only the definition of properties of the geometric (e.g., roughness coefficients) and liquid (e.g., discharges) are required as explained later.

For the usage with {ref}`chpt-telemac2d`, the 2dm file requires a conversion to the serafin/selafin (`slf`) file format that is explained in the {ref}`slf-qgis` section.

(dem2stl)=
## Export DEM as STL

The `stl` (standard tessellation language) file format is native to CAD software and particularly used for the representation of three-dimensional (3d) structures in the form of unstructured triangulated surfaces. `stl` files can be read by pre-processing software for OpenFOAM and this section explains how to convert a GeoTIFF DEM into an `stl` file.

The export requires the **DEMto3D** plugin, which can be installed in *QGIS* as follows:

* Load the *QGIS* plugin manager: **Plugins** menu > **Manage and Install Plugins**.
* Make sure the **All** tab is active and enter `DEMto3D`.
* Click on **Install Plugin**.
* Close the Plugin Manager after the successful installation.

Following the instructions in the above section on {ref}`get-dem`, download the example DEM GeoTIFF [here](https://github.com/hydro-informatics/materials-bm/raw/main/rasters/inn-dem.tif) and add it as a new raster layer in *QGIS* (similar to adding {ref}`basemap`). Then export the DEM to `stl` by opening the DEM 3D printing window from **Rasters** > **DEMto3D** > **DEM 3D printing**. In the popup window (see also {numref}`Fig. %s <qgis-dem3d>`):

* Select the `inn...` DEM as **Layer to print**
* For **Print extent** find the **Select layer extent** symbol and select the `inn...` DEM layer.
* In the **Model size** frame set (approximately - must not be exactly the same):
  * **Spacing** to 2.83 (mm)
  * **Width** to 2621.78 (mm)
  * **Length** to 2000 (mm)
* In the **Model height** frame set the **Height** to 367 (m).
* Click on **Export to STL** > **Yes** > define directory and name.

```{admonition} No visible raster loaded
:class: warning
This error message indicates that the DEM GeoTIFF is not correctly loaded or not activated in the Layers Panel. Re-read or watch the tutorial on {ref}`qgis-tbx-install`.
```

```{figure} ../img/qgis/dem3d-printing.png
:alt: basement export stl demto3d printing dem raster
:name: qgis-dem3d

Setup the DEM 3D printing properties.
```


The export starts and will take approximately 1-2 minutes. The resulting **STL** file can be opened with CAD software such as {ref}`salome-install` modules or {ref}`freecad-install`. The result looks similar to {numref}`Fig. %s <qgis-stl-exported>` (depending on the **Height (m)** value used).


```{figure} ../img/qgis/stl-exported.png
:alt: basement export stl
:name: qgis-stl-exported

The resulting stl file of the DEM.
```
