(qgis-tutorial)=
# QGIS Tutorial

````{admonition} Requirements
This tutorial is designed for **beginners** and has embedded videos featuring the text descriptions in every section. Before diving into this tutorial make sure to install {ref}`QGIS <qgis-install>`.


```{admonition} Expand to watch the video for installing QGIS
:class: dropdown, tip
Find for explanation in the {ref}`qgis-install` section in this eBook.

<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/_0_NOKi-RxY" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe> <p>Sebastian Schwindt <a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>

```

```{admonition} If you read: *Videos not showing up (Firefox Can’t Open This Page)*...
:class: attention, dropdown
If videos are not displaying, this might be caused by strict privacy settings. To resolve the issue, either open the video links by clicking on the **Open Site in New Window** button or by changing browser privacy settings (e.g., in [Mozilla Firefox](https://support.mozilla.org/en-US/questions/1108783)).
```
````

(qgis-project)=
## First Project

Once you installed QGIS, launch the program and walk through the following steps to make fundamental settings:

- Open *QGIS*
- Create a new project (**New Empty Project**)
- Verify **Project Properties**:
  * In the top menu go to **Project** > **Properties**
  * Set the Coordinate Reference System **CRS** to **EPSG:4326**:
    * WGS84 (Coordinate Reference System) Bounds: -180.0000, -90.0000, 180.0000, 90.0000
    * Projected Bounds: -180.0000, -90.0000, 180.0000, 90.0000
    * Scope: Horizontal component of a 3d system. Used by the GPS satellite navigation system and for NATO military geodetic surveying.
    * Last Revised: Aug. 27, 2007
    * Area: World
  * Learn more at http://epsg.io
    * Retrieve point coordinates in any CRS format
    * Convert between different CRSs (e.g., convert 48.745, 9.103 from EPSG 3857 to EPSG 4326)
- **Save** the project as **qgis-project.qgz** in a new **qgis-exercise** folder

```{admonition} Project setup (video)
<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/7_3QqbFonLg" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>
```

```{hint}
All files created in this tutorial can be downloaded from the {{ qgis_tutorial_repo }}.
```

(qgis-tbx-install)=
## Panels, Toolbars, and Plugins

Follow the below illustrated instructions to enable the *QGIS* *Toolbox*.

```{figure} ../img/qgis-tbx.png
:alt: enable QGIS toolbox
:name: qgis-tbx

Open QGIS' Toolbox window from the main menu.
```

The conversion between geospatial data types and numerical (computational) grids can be facilitated with plugins. To install any plugin in *QGIS*, go to the `Plugins` menu > `Manage and Install Plugins...` > `All` tab > `Search...` for a relevant plugin and install it.

In the context of river analysis, the following plugins are recommended and used at multiple places on this website:

```{admonition} QGIS plugins for hydro-informatics
:name: qgis-plugins
* The *Crayfish* plugin for post-processing of numerical model output.
* The *BASEmesh2* plugin provides routines for creating computational meshes for numerical simulations with {ref}`chpt-basement`.
* The *PostTelemac* plugin enables geospatial visualization and conversions of numerical model results produced with {ref}`chpt-telemac`.
```

BASEmesh is only one (very well working) mesh generator for QGIS and {numref}`Tab. %s <tab-mesh-plugins>` lists of other plugins for generating computational meshes for numerical models along with target file formats and models

```{list-table} A list of QGIS mesh generator plugins.
:header-rows: 1
:name: tab-mesh-plugins

* - Mesh Plugin Name and Link
  - Model Compatibility
  - Output Mesh File Format
  - Mesh Characteristics
* - [GMSH](http://geuz.org/gmsh) ([Wiki](https://github.com/ccorail/qgis-gmsh/wiki))
  - [Open CASCADE Technology](https://www.opencascade.com/open-cascade-technology/) / {ref}`OpenFOAM <openfoam-install>`
  - `*.geo`, `*.stl`, `*.msh`
  - 3d finite elements ([Netgen](http://ngsolve.org/) and [Mmg3d](https://www.mmgtools.org/)), compatibility with {ref}`salome-install`
* - [QGribDownloader](https://plugins.qgis.org/plugins/gribdownloader/)
  - [OpenGribs / XyGrib](https://opengribs.org/)
  - `*.GRIB`
  - Purpose: Meteorological/atmospheric modelling
* - [TUFLOW](https://plugins.qgis.org/plugins/tuflow/)
  - [TUFLOW](https://tuflow.com/) (proprietary)
  - `*.2dm` (among others), conversion to `.slf` possible with Crayfish
  - TUFLOW automatically generates meshes (finite volumes / finite differences)
* - [MeshTools](https://github.com/jdugge/MeshTools)
  - {ref}`chpt-basement`, Hydro FT/AS (proprietary), indirectly: {ref}`chpt-telemac`
  - `*.2dm` (conversion to `.slf` possible with Crayfish)
  - Tweaks into multiple mesh algorithms (among others: {cite:t}`shewchuk1996`)
* - DEMto3D
  - Raster to STL (style) files for Blender
  - `*.geo`, `*.stl`, `*.msh`
  - Create digital twins in Blender
```

(basemap)=
## Basemaps for QGIS (Google or Open Street Maps Worldmap Tiles)

```{note}
A fast internet connection is required for adding online basemaps.
```

To add a base map (e.g., satellite data, streets, or administrative boundaries), go to the **Browser**, right-click on **XYZ Tiles**, select **New Connection...**, add a name, and a URL of an online base map. Once the new connection is added, it can be added to a *QGIS* project by drag and drop just like any other geodata layer. The below figure illustrates the procedure of adding a new connection and its XYZ tiles as a layer to the project. To overlay multiple basemaps (or any other layer), **right-click on a layer**, then **Layer Properties** > **Transparency** > modify the **Opacity** (e.g., to 50%).

```{figure} ../img/qgis-basemap.png
:alt: basemap

Add a base map to QGIS: (1) locate the Browser (2) right-click on XYZ-Tiles and select New Connection... (3) enter a Name and a URL (see below table) for the new connection, click OK (4) drag and drop the new tile (here: Google Satellite) into the Layers Panel.
```

```{admonition} Expand to watch the video tutorial on basemaps
:class: tip, dropdown

<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/GJsiEdMzCeQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>
```

The following URL can be used for retrieving online XYZ tiles (more URLs can be found on the internet).

````{div} full-width
```{list-table} Providers of XYZ basemap tiles
:header-rows: 1
:name: basemap-providers

* - Provider (Layer Name)
  - URL
* - ESRI World Imagery
  - ```https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}```
* - ESRI Street
  - `https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}`
* - ESRI Topo
  - `https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}`
* - Google Satellite
  - `https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}`
* - Google Street
  - `https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}`
* - OpenStreetMap (OSM)
  - `http://tile.openstreetmap.org/{z}/{x}/{y}.png`
* - OSM Black and White
  - `http://tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png`
```
````

```{admonition} Coordinate reference systems of basemaps
:class: tip

Most basemaps are provided in the `EPSG:3857 -WGS84 / Pseudo Mercator` coordinate system (CRS). To use custom geodata products, make sure that all other layers have the same coordinate system. Read more about coordinate systems and projections in the {ref}`geospatial-data` and {ref}`shapefile projection <prj-shp>` sections.
```

## Create a Shapefile

This section guides through the creation of a point, a line, and a polygon {ref}`shp` (vector data). To read more about such vector data and other spatially explicit data types, read the section on {ref}`geospatial-data`.

(create-point-shp)=
### Create a Point Shapefile

Start with loading satellite imagery and a street basemap (see above) in the layers pane. Zoom on central Europe and roughly locate Stuttgart in Southwest Germany. Find the heavily impaired Neckar River in the North of Stuttgart and move in the upstream direction (i.e., Eastern direction), pass the cities of Esslingen and Plochingen until you get to the confluence of the Neckar and the Fils rivers. From there, follow the Fils River in the upstream direction for a couple of hundred meters and locate the PEGELHAUS (i.e., a gauging station at the Fils River - [click to visit](https://www.hvz.baden-wuerttemberg.de/pegel.html?id=00025)). To facilitate finding the gauging station in the future, we will now create a point shapefile as explained in the following video and the analogous instructions below the video.

```{admonition} Create point shapefile video
<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/k2LqPM6wicA" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>
```

* In the QGIS top menu go to **Layer** > **Create Layer** > **New Shapefile Layer**
  * Define a filename (e.g., **gauges.shp** - may not be longer than 13 characters), for instance, in a folder called *qgis-exercise*.
  * Geometry type: `MultiPoint`
  * Additional dimensions: `Z(+M Values)`
  * Add two new fields:
    * `StnName` (*Text data*)
    * `StnID`  (*Whole number*)
* Edit/draw points
  * **Toggle Editing** (i.e., enable by clicking on the yellow pen <img src="../img/qgis/yellow-pen.png">) > **Add Point Feature** <img src="../img/qgis/sym-add-point.png">
  * Click on the PEGELHAUS to draw a point and set
    * `StnName`: `PlochingenFils`
    * `StnID`: `00025`
  * Add more points if you like.
  * Finalize the edits by clicking on **Save Layer Edits** <img src="../img/qgis/sym-save-edits.png"> > **Stop (Toggle) Editing** by clicking on the yellow pen <img src="../img/qgis/yellow-pen.png"> symbol.
* Improve the visualization by changing the symbology:
  * **Double-click on** the gauges **layer** > **Symbology**
  * Highlight **Simple Marker**, change to **+** symbol, and change fill color and size.
  * Highlight **Marker** and change the **Opacity**
  * Click **Apply** and **OK**
* Verify the point settings in the **Attribute Table** (right-click on the *gauges* layer and select **Attribute Table**).

(create-line-shp)=
### Create a Line Shapefile

Create a **Line Shapefile** called **CenterLine.shp** to draw a centerline of the Fils $\pm$ 200 m around the PEGELHAUS gauge, similar to the above-created point shapefile. Add one *text* field and call it `RiverName`. Then draw a line along the Fils River starting 200 m upstream and ending 200 m downstream of the PEGELHAUS by following the river on the **OpenStreetMap** layer. See more in the following video.

```{admonition} Create Line shapefile video
<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/yNuiIlPsguQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>
```

(create-polygon-shp)=
### Create a Polygon Shapefile

To delineate different zones of roughness (e.g., as needed for a two-dimensional numerical model), create a **Polygon Shapefile** called **FlowAreas.shp**. The file will contain polygons zoning the considered section of the Fils into the floodplain and main channel bed. Name the first field `AreaType` (type: *Text*) and the second field `ManningN` (type: *Decimal Number*). See more in the following video and the instructions below the video.

```{admonition} Create Polygon video
<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/zTrowT0ULfo" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>
```

To draw the polygons:

* Enable snapping to avoid gaps between the floodplain and main channel polygons
  * Activate the **snapping toolbar**: **View** > **Toolbars** > **Snapping Toolbar**
  * Enable snapping from **Snapping toolbar** > **Enable Snapping** and **Avoid Polygon Overlapping**
* Start drawing by clicking on the map (right-click finalizes Polygon)
* Draw one polygon of the main channel and after finalizing set:
  * `AreaType`: `MainChannel`
  * `ManningN`: `0.028`
* Draw two more polygons of the right-bank (RB) and left-bank (LB) floodplains, and set:
  * `AreaType`: `FloodPlainRB` and `FloodPlainLB`
  * `ManningN`: `0.05` (both)
* If you made a drawing error, use either the *Attribute Table* to select and delete entire polygons, or use the vertex tool <img src="../img/qgis/sym-vertex-tool.png"> from the menu bar.
* After drawing all polygons, **Save edits** and **Toggle Editing** (deactivate).
* To improve the visualization, modify the **Symbology** to **Categorized** as a function of the `AreaType` field: Keep **Random Colors** > Click on **Classify** > **Apply** and if you like the visualization, click **OK**.


## Conversion: Rasterize (Polygon to Raster)

Many numerical models required that roughness is provided in {ref}`raster` format. To this end, this section features the conversion of the above-created polygon shapefile (*FlowAreas.shp*) to a roughness {ref}`raster`. The following video and the instructions below the video describe how the conversion works.

```{admonition} Rasterization video
<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/IRLwYSUnjcE" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>
```

To convert a geospatial vector dataset, use the *Rasterize* tool:

* In the QGIS menu bar make sure to enable the *Processing Toolbox* panel (**View** > **Panels** > **Processing Toolbox**)
* In the **Processing Toolbox** > search (tap) **Rasterize** > select **Rasterize (vector to raster)**

```{hint}
If the *Crayfish* plugin is installed, an additional *Rasterize* tool will show up, which we will not use in this tutorial (i.e., make sure to select *Rasterize (vector to raster)* ).
```

* In the **Rasterize (Vector to Raster)** window set:
  * **Input layer**: `FlowAreas`
  * **Field to use for a burn-in value**: `ManningN`
  * **Output raster size units**: `Pixels`
  * **Width/Horizontal resolution**: `100` (the smaller, the coarser the raster)
  * **Height/Vertical resolution**: `100` (the smaller, the coarser the raster)
  * ... scroll down ...
  * **Output extent**: click on the **…** button > **Calculate from Layer** > `FlowAreas`
  * **Rasterized** (FILE NAME) > click on the **…** button > **Save to File...** > `roughness.tif`
  * Click **Run**
* Set the **Symbology** to **Singleband pseudocolor** with **Interpolation**: `Discrete`, **Colorramp**: `Magma`, **Mode**: `Equal Interval` > **Apply**. If the visualization is satisfactory, click **OK**.

```{admonition} File conversion with Python
:class: tip
The conversion between geospatial data types can be facilitated by using Python. Read the section on {ref}`py-conversion` to learn more.
```

## Polygonize

The inverse operation of *Rasterize* is called **Raster to Vector**, which is documented at [https://docs.qgis.org](https://docs.qgis.org/testing/en/docs/training_manual/complete_analysis/raster_to_vector.html). The creation of a Polygon from a raster is described in a video [coming soon].

```{admonition} Polygonize (Video coming soon)

Coming soon.

```


```{admonition} Raster to (line/point) Vector

Other options for creating vector datasets from rasters are the [Contour](https://docs.qgis.org/3.28/en/docs/training_manual/processing/interp_contour.html) tool (**Raster** menu > **Extraction** > **Contour**) or the [Raster pixels to points](https://docs.qgis.org/3.28/en/docs/user_manual/processing_algs/qgis/vectorcreation.html#raster-pixels-to-points) algorithm (**Processing** toolbox > enter `raster pixels to points`).

```

## Working with Rasters

### QGIS Raster Calculator (Map Algebra)

Some models preferably (default use) Manning's *n*, others use the Strickler roughness coefficient $k_{st}$, which is the inverse of Manning's *n* (i.e., $k_{st} = 1/n$ - read more about roughness coefficients in the {ref}`ex-1d-hydraulics` exercise). Thus, transforming a Strickler roughness raster into a Manning roughness raster requires performing an algebraic raster (pixel-by-pixel) operation. The next video and the instructions below the video feature the usage of the QGIS **Raster Calculator** to perform such algebraic operations.

<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/DOkV03uij9k" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>

Start with opening **Raster Calculator** from QGIS menu bar (**Raster** > **Raster Calculator...**). Then, convert the above-created *roughness.tif* raster of Manning's *n* values to a Strickler roughness raster:

* Define an **Output layer** (e.g., *qgis-exercise/roughness-stickler.tif*) and keep the **Output format** of **{term}`GeoTIFF`**.
* Optionally select a layer extent corresponding to the above-created *roughness.tif* raster.
* In the **Raster Calculator Expression** frame type **1**, then click on the **/** button (**Operators** frame), then select **roughness@1** from the **Raster Bands** frame.
* The **Raster Calculator Expression** frame should now contain: `1 / "roughness@1"`, where the `@` sign refers to band number `1`.
* Click **OK** to run *Raster Calculator*.
* After successful calculation, optionally modify the symbology of the new layer (*roughness-stickler*).

```{admonition} Batch-process geodata
:class: tip
To implement a tailored raster calculator for batch-processing of raster files with Python read the {ref}`py-raster-calculator` section in the {ref}`ex-geco` exercise.
```

(make-xyz)=
### Raster to XYZ

Scientific data formats, such as {term}`HDF`, work best with raw geospatial datasets like `*.xyz` files. A `.*xyz` file contains s only X, Y, and Z coordinates of points (i.e., point clouds) with or without a simple header. For instance, this eBook uses `*.xyz` data for the elevation interpolation of a computational mesh for the scientific numerical modeling software {ref}`chpt-telemac`. To generate a `*.xyz` from a {term}`GeoTIFF` raster use the following workflow:

* In the **Layers** panel make sure to have raster layer imported for conversion and **identify its No-Data** value (**Layer Properties** > **Information** > **Bands** section > **No-Data** field show by default `-9999` in QGIS).
* In QGIS top menu go to **Raster** > **Conversion** > **Translate (Convert Format)...**
* In the **Translate (Convert Format)** window, make the following settings:
  * **Input layer** =  the raster (e.g., a {term}`DEM`) to convert
  * **Advanced Parameters** frame > **Output data type** > select **Float32** (corresponds to single precision in numerical models)
  * **Converted** > **...** button (at the end of the line) > **Save to File...** > define a **File name** such as `dem-points` and select `XYZ files (*.xyz)` in the **Save as type** field.
  * **Save** and **Run** the translation (conversion).

The resulting `*.xyz` file contains also points with **No-Data** to fill void spaces in the rectangular image of the {term}`GeoTIFF` (which QGIS did recognize as no-data pixels). The no-data points may make the `*.xyz` file unnecessarily heavy, in particular, when it is a {term}`DEM` of a near-census natural river. To eliminate the unnecessary no data points, open the `*.xyz` file in spreadsheet software, such as {ref}`Calc in LibreOffice <lo>` and use the *Sort* tool (in **Calc** highlight all points go to **Data** > **Sort...**) to sort by `Z` values (largest to smallest) and then delete all rows that have the above-identified **No-Data** value (`-9999`) as `Z` value. Save the `*.xyz` file and close the spreadsheet software.

```{admonition} Shapefile to XYZ
:class: tip, dropdown
**Shapefiles** do not have to be converted to {term}`GeoTIFF` to create an `*.xyz` file. To create a `*.xyz` file from a **shapefile**:

* Right click on the shapefile in the **Layer** panel > **Export** > **Save Feature As...**.
* Select **Comma Separated Value ({term}`CSV`)** in the **Format** field.
* Define a **File name** on clicking on the **...** button.
* In the **Layer Options** frame, select **AS_XYZ** in the **GEOMETRY** field and keep all other defaults.
* Click **OK** to convert to {term}`CSV`.
* Open the {term}`CSV` file in a {ref}`text editor <npp>` and use its *find and replace* function (usually `CTRL`+`F` or `CTRL`+`H`) to replace all COMMA `,` by a space symbol ` `. Note that this action requires that the comma has not been used as decimal separator.
* Save the {term}`CSV` file as `*.xyz` file.
```

To finalize the `*.xyz` file, open it in a {ref}`text editor <npp>` and add a header. For instance, use the following header to work with {ref}`Blue Kenue <bluekenue>`:

```
:FileType xyz  ASCII  EnSim 1.0
:EndHeader
```

Save the changes. The `*.xyz` file is now slim and ready to use, for instance, for the {ref}`TELEMAC pre-processing <get-dem-xyz>`.

## Create Layout and PDF / JPG (or other) Maps

Georeferenced images in {term}`GeoTIFF` or other raster formats, possibly with super-positioned shapefiles on top, are handy and flexible for use with geospatial software, such as QGIS, but not appropriate for presentations or reports. For presentation purposes, geospatial imagery or maps should preferably be exported to common formats, such as the **P**ortable **D**ocument **F**ormat (PDF) or **JPEG/JPG**. To create commonly formatted maps with QGIS, first, a new (print) layout needs to be created, which can then be exported to a common map format (e.g., along with a legend, a scale bar, and a North arrow). The following video and the descriptions below the video guide through the map creation process with QGIS.


<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/hmTByzVPVF0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>

Start with creating a new print layout by clicking on the **Project** drop-down menu, then select **New Print Layout**. In the new print layout prepare the map and export the map as follows:

* Set a **Layout title** (e.g., *exercise-layout*).
* In the new (*exercise-layout*) Layout:
  * Go to **Add Item** > **Add Map**.
  * Draw a rectangle that will contain the map.
  * **Add Item** > **Add Scale Bar**
  * To control scales and units shown in the scale bar:
    * In **Items** panel, highlight `<Scalebar>` and find the **Item Properties** tab below.
    * In the **Item Properties** tab modify units to your convenience.
  * **Add Item** > **Add Legend**
  * To control elements of the legend:
    * In **Items** panel, highlight `<Legend>` and find the **Item Properties** tab below.
    * In the **Item Properties** tab, find **Legend Items** > disable **Auto update** > **remove** *OpenStreetMap* and *Google Satellite*.
  * Toggle through other **Items** in the **Add Item** menu bar (e.g., **Arrow** for Northing).
* **Save** the layout project (from top menu **Layout** > **Save Project**)
* Export the map to common formats:
  * For JPG or PNG: **Layout** > **Export as Image**
  * For PDF: **Layout** > **Export as PDF**
  * Optional, for SVG-vector graphs: **Layout** > **Export as SVG**

QGIS has many other capacities, but this fundamental tutorial should have provided you with the necessary knowledge to leverage the power of QGIS for many applications.

(pygis)=
## PyQGIS: QGIS and Python

The QGIS graphical user interface (GUI) provides a Python command line (**Plugins** > **Python Console**), which enables to automate almost any mouse click in the GUI. This Python command line is referred to as **PyQGIS** and the [QGIS developer docs](https://docs.qgis.org/latest/en/docs/pyqgis_developer_cookbook/intro.html) provide instructions on how to import and run standalone Python scripts outside of the QGIS GUI. Here is the basic Python template to run a PyQGIS script:


```python
from qgis.core import *

# define qgis installation location
QgsApplication.setPrefixPath("/path/to/qgis/installation", True)


# instantiate a QgsApplication, where the second argument (False) disables the GUI
qgs = QgsApplication([], False)


# load providers
qgs.initQgis()

# HERE GOES YOUR CUSTOM CODE

# exit the QGIS application to remove the provider and layer registries from memory
qgs.exitQgis()
```

However, when opening your system's terminal or Anaconda Prompt to run a PyQGIS code, you may get stuck on the first line of code already: `from qgis.core import *` yields `ImportError: No module named qgis.core`. According to the [QGIS developer docs](https://docs.qgis.org/latest/en/docs/pyqgis_developer_cookbook/intro.html), this error happens because your system's Python does not know where the PyQGIS environment lives. To make your terminal recognize PyQGIS, take the following action according to your system:

`````{tab-set}
````{tab-item} Linux

Open Terminal and install `python-qgis`:

```
sudo apt install python-qgis
```

After the successful installation, try if you can now import `qgis.core`:

```
USER@computer:~$ python
Python 3.8.10 (default, Nov 14 2022, 12:59:47) 
[GCC 9.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from qgis.core import *
>>> exit()
```

If `from qgis.core import *` did not throw any error, you are all set and can stop reading. **Otherwise**, find and open your `.bashrc` file (Debian/Ubuntu/Mint: `/home/USERNAME/.bashrc`). Note that files starting with a `.` name are hidden on Linux and become visible by toggling with simultaneously pressing the `CTRL`+`H` keys.

At the bottom of `.bashrc` add the following

```
export PYTHONPATH=/<qgispath>/share/qgis/python
```

The `<qgispath>` expression should be replaced by the location where the PyQGIS environment lives. To find out where that is, tap (in Terminal):

```
dpkg-query -L python-qgis
```

This points to where PyQGIS lives, which, on Ubuntu/Mint typically is: `/usr/lib/python3/dist-packages/`

Thus, in this case add to `.bashrc`:

```
export PYTHONPATH=/usr/lib/python3/dist-packages/
```

Afterward, log out and re-login to your system (i.e., reload `.bashrc`). The command `from qgis.core import *` should now work in Python.
````

````{tab-item} Windows

Make sure your system knows the where PyGIS lives by adding the following line to the Environment Variables (Windows 10: **My Computer** > **Properties** > **Advanced System Settings** > **Environment Variables**). Replace `<qgispath>` with the path where QGIS lives on your system.

* Variable name = `PYTHONPATH`
* Variable value = `C:\<qgispath>\python`

Or use the Windows prompt:

```
set PYTHONPATH=C:\<qgispath>\python
```

````
`````


