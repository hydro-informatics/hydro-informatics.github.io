(qgis-tutorial)=
# QGIS tutorial

```{tip}
This tutorial involves embedded videos featuring the text descriptions in every section.
```

To get ready, watch the following video and/or make sure to install {ref}`qgis-install` (detailed instructions).

<iframe width="720" height="405" src="https://youtu.be/_0_NOKi-RxY" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt <a href="https://www.youtube.com/channel/UCGOMSGRrW5eLHiMn5Dfp7WQ">@ Hydro-Morphodynamics channel on YouTube</a>.</p>



## First Project

Once you installed QGIS, launch the program and walk through the following steps to make fundamental settings:

- Open GIS
- Create a new project (New Empty Project) with EPSG:4326, which is:
- Verify Project Properties:
  * Go to Project > Properties
  * CRS: EPSG:4326:
    * WGS84 (Coordinate Reference System) Bounds: -180.0000, -90.0000, 180.0000, 90.0000
    * Projected Bounds: -180.0000, -90.0000, 180.0000, 90.0000
    * Scope: Horizontal component of 3D system. Used by the GPS satellite navigation system and for NATO military geodetic surveying.
    * Last Revised: Aug. 27, 2007
    * Area: World
  * Learn more at http://epsg.io
    * Example: Convert 48.745, 9.103 from EPSG 3857 to EPSG 4326
- Save the project as qgis-project.qgz in a new qgis-exercise folder

<iframe width="720" height="405" src="https://youtu.be/7_3QqbFonLg" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/channel/UCGOMSGRrW5eLHiMn5Dfp7WQ">@ Hydro-Morphodynamics channel on YouTube</a>.</p>


(qgis-tbx-install)=
## Panes, Toolbars, and Plugins

Follow the below illustrated instructions to enable the *QGIS* *Toolbox*.

```{figure} ../img/qgis-tbx.png
:alt: enable QGIS toolbox
:name: qgis-tbx

Open QGIS' Toolbox window from the main menu.
```

The conversion between geospatial data types and numerical (computational) grids can be facilitated with plugins. To install any plugin in *QGIS*, go to the `Plugins` menu > `Manage and Install Plugins...` > `All` tab > `Search...` for a relevant plugin and install it.

In the context of river analysis, the following plugins are recommended and used at multiple places on this website:

* The *Crayfish* plugin, which is available in the *QGIS* toolbox after the installation.

(basemap)=
## Basemaps for QGIS (Google or Open Street Maps Worldmap Tiles)

```{note}
A fast internet connection is required for adding online base maps.
```

To add a base map (e.g., satellite data, streets, or administrative boundaries), go to the ***Browser***, right-click on ***XYZ Tiles***, select ***New Connection...***, add a name and a URL of an online base map. Once the new connection is added, it can be added to a *QGIS* project by drag and drop just like any other geodata layer. The below figure illustrates the procedure of adding a new connection and its XYZ tiles as a layer to the project. To overlay multiple basemaps (or any other layre), ***right-click on a layer***, then ***Layer Properties*** > ***Transparency*** > modify the ***Opacity*** (e.g., to 50%).

```{figure} ../img/qgis-basemap.png
:alt: basemap

Add a base map to QGIS: (1) locate the Browser (2) right-click on XYZ-Tiles and select New Connection... (3) enter a Name and a URL (see below table) for the new connection, click OK (4) drag and drop the new tile (here: Google Satellite) into the Layers tab.
```

<iframe width="720" height="405" src="https://youtu.be/GJsiEdMzCeQ" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/channel/UCGOMSGRrW5eLHiMn5Dfp7WQ">@ Hydro-Morphodynamics channel on YouTube</a>.</p>


The following URL can be used for retrieving online XYZ tiles (more URLs can be found in the internet).

| Provider (Layer Name) | URL                                                                                              |
|-----------------------|--------------------------------------------------------------------------------------------------|
| ESRI World Imagery    | `https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}`  |
| ESRI Street           | `https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}` |
| ESRI Topo             | `https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}`   |
| Google Satellite      | `https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}`                                               |
| Google Street         | `https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}`                                               |
| OpenStreetMap (OSM)   | `http://tile.openstreetmap.org/{z}/{x}/{y}.png`                                                    |
| OSM Black and White   | `http://tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png`                                               |

```{tip}
Most base maps are provided in the `EPSG:3857 -WGS84 / Pseudo Mercator` coordinate system (CRS). To use custom geodata products, make sure that all other layers have the same coordinate system. Read more about coordinate systems projections on the {ref}`geospatial-data` and {ref}`shapefile projection <prj-shp>` sections.
```

## Create a Shapefile

This section guides through the creation of point, line, polygon shapefiles (vector data).

### Create a Point Shapefile

Start with loading a satellite and a street basemap (see above) in the layers pane. Zoom on Central Europe, and roughly locate Stuttgart in Southwest Germany. Find the heavily impaired Neckar River and move in upstream direction, pass the cities of Esslingen and Plochingen until you get to the confluence of the Neckar and the Fils rivers. From there, follow the Fils River in upstream direction for a couple of 100 meters and locate the PEGELHAUS (i.e., a gauging station at the Fils River). To facilitate finding the gauging station in the future, we will now create a point shapefile.


<iframe width="720" height="405" src="https://youtu.be/k2LqPM6wicA" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/channel/UCGOMSGRrW5eLHiMn5Dfp7WQ">@ Hydro-Morphodynamics channel on YouTube</a>.</p>

* Go to **Layer** > **Create Layer** > **New Shapefile Layer**
  * Define a filename (e.g., **gauges.shp** - may not be longer than 13 characters), for instance, in a folder called *qgis-exercise*.
  * Geometry type = MultiPoint
  * Additional dimensions: Z(+M Values)
  * Add New Fields:
          1. StnName=TextData
          2. StnID = Whole Number
* Edit / Draw point
  * Enable editing (yellow pen)
  * Add Point Feature
  * StnName = PlochingenFils
  * StnID = 00025
  * URL: https://www.hvz.baden-wuerttemberg.de/pegel.html?id=00025
  * Click on the Pegelhaus to draw a Point
  * Save Edits & Stop Editing
* Change Symbology:
  * Double-click on gauges layer > Symbology
  * Highlight Simple Marker and change to + sign, change fill color, size
  * Highlight Marker and Change Opacity
  * Click Apply and OK
* Show Attribute Table


### Create a Line Shapefile

Create a Line Shapefile “CenterLine.shp” to draw a Centerline of the Fils +- 200 around the Pegelhaus gauge (with one Field=RiverName), along the OpenStreetMap layer similar to the above-created point shapefile.

<iframe width="720" height="405" src="https://youtu.be/yNuiIlPsguQ" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/channel/UCGOMSGRrW5eLHiMn5Dfp7WQ">@ Hydro-Morphodynamics channel on YouTube</a>.</p>

### Create a Polygon Shapefile

Create a Polygon Shapefile “FlowAreas.shp” to draw two Polygons of the of the Fils Floodplain with two Fields = AreaType (Text) and ManningN (Decimal Number).

<iframe width="720" height="405" src="https://youtu.be/zTrowT0ULfo" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/channel/UCGOMSGRrW5eLHiMn5Dfp7WQ">@ Hydro-Morphodynamics channel on YouTube</a>.</p>


* To Draw a Polygon: Click in the map (right-click finalizes Polygon)
* Polygon1: AreaType=“MainChannel”, ManningN = 0.028
* Snapping toolbar: Enable Snapping + Avoid Polygon Overlapping
* Polygon2: AreaType=“FloodPlainRB” , ManningN = 0.05
* Show how to delete a feature using the attribute Table
* Save edits & deactivate Editing
* Modify Symbology to Categorized as a Function of AreaType Field > Keep Random Colors > Click on Classify > Apply and if you like it > OK


## Rasterize (Polygon to Raster)

Convert the above-created Pyolgon “FlowAreas.shp” to a roughness Raster.

<iframe width="720" height="405" src="https://youtu.be/IRLwYSUnjcE" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/channel/UCGOMSGRrW5eLHiMn5Dfp7WQ">@ Hydro-Morphodynamics channel on YouTube</a>.</p>


* Click on View > Panels >Processing Toolbox
* In Toolbox > search Rasterize > select Rasterize (vector to raster)
* In Rasterize Window:
  * Input layer = FlowAreas
  * Field to use for a burn-in value = ManningN
  * Output raster size units = Pixels
  * Width/Horizontal resolution = 100 (the smaller, the coarser the Raster!)
  * Height/Vertical resolution = 100 (the smaller, the coarser the Raster!)
  * … [scroll down] …
  * Output extent: click on … button > Calculate from Layer > FlowAreas
  * Rasterized (FILE NAME) > click on … Button > Save to File > roughness.tif
  * Click Run
* Change Symbology to Singleband pseudocolor, Interpolation=Discrete, Colorramp=Magma, Mode=Equal Interval > Apply & OK


## QGIS Raste Calculator (Map Algebra)

Launch the QGIS Raster Calculator from Raster > Raster Calculator.

<iframe width="720" height="405" src="https://youtu.be/DOkV03uij9k" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/channel/UCGOMSGRrW5eLHiMn5Dfp7WQ">@ Hydro-Morphodynamics channel on YouTube</a>.</p>


* In Raster Calculator Expression field type 1, then click on / Button (Operators Box), then select roughness@1 from the Raster Bands Box – Result: 1 / “roughness@1” (EXPLAIN BANDS!)
* Output layer = qgis-exercise/roughness-stickler.tif /preferably use GeoTIFF)
* Click OK to run Raster Calculator
* Optional: Change symbology


## Create Layout and PDF / JPG (or other) Maps

Start with creating a new print layout by clicking on the **Project** drop-down menu, then select **New Print Layout**.

<iframe width="720" height="405" src="https://youtu.be/hmTByzVPVF0" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/channel/UCGOMSGRrW5eLHiMn5Dfp7WQ">@ Hydro-Morphodynamics channel on YouTube</a>.</p>


* Layout title Res100 (for resolution)
* In Res100 Layout:
  * Go to Add Item > Add Map
  * Draw a rectangle that will contain the map
  * Add Item > Add Scale Bar
  * Add Item > Add Legend
  * In Items Panel, highlight <Legend> and find the Item Properties tab below
  * In the Item Properties tab, find Legend Items > disable Auto update > remove OpenStreetMap and Google Satellite
  * Toggle through other Items in the Add Item menu bar (e.g., Arrow) and the Items panel (e.g., <Scalebar> to change units)
* Save the project (Layout > Save Project)
* Export Image: Layout > Export as Image
* Export PDF: Layout > Export as PDF
* Optional export SVG (Vector graph): Layout > Export as SVG
